"""OIDC verification + validation for witness agents, against an offline stand-in provider."""
import json
import os
import sys
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "agents"))
os.environ["MESEEKS_RULES_ONLY"] = "1"
os.environ["MESEEKS_PROMPTS_OFFLINE"] = "1"

jwt = pytest.importorskip("jwt")
from cryptography.hazmat.primitives import serialization  # noqa: E402
from cryptography.hazmat.primitives.asymmetric import rsa  # noqa: E402
from jwt.algorithms import RSAAlgorithm  # noqa: E402

from meseeks import oidc, witness  # noqa: E402

ISSUER = "https://www.login.cloudfronts.group:3443"
KEY = rsa.generate_private_key(public_exponent=65537, key_size=2048)
OTHER_KEY = rsa.generate_private_key(public_exponent=65537, key_size=2048)
PEM = KEY.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption())
OTHER_PEM = OTHER_KEY.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption())
JWK = json.loads(RSAAlgorithm.to_jwk(KEY.public_key()))
JWK.update(kid="k1", use="sig", alg="RS256")

DISCOVERY = {"issuer": ISSUER, "jwks_uri": f"{ISSUER}/jwks", "authorization_endpoint": f"{ISSUER}/authorize",
             "token_endpoint": f"{ISSUER}/token", "device_authorization_endpoint": f"{ISSUER}/device"}


@pytest.fixture(autouse=True)
def provider(monkeypatch):
    docs = {f"{ISSUER}/.well-known/openid-configuration": DISCOVERY, f"{ISSUER}/jwks": {"keys": [JWK]}}
    monkeypatch.setattr(oidc, "_get", lambda url, timeout=5: docs[url])
    oidc._cache.clear()
    monkeypatch.setenv("MESEEKS_WITNESS_IP", "192.168.0.42")
    monkeypatch.setenv("MESEEKS_WITNESS_PLATFORM", "macos")
    monkeypatch.delenv("MESEEKS_ID_TOKEN", raising=False)
    monkeypatch.setattr(oidc, "TOKEN_FILE", Path("/nonexistent/token.json"))
    return oidc.Provider.from_config(witness.load())


def token(email="sweeden@legalluminary.com", pem=PEM, kid="k1", exp=None, iss=ISSUER, aud="meseeks", alg="RS256", **extra):
    now = int(time.time())
    claims = {"iss": iss, "aud": aud, "sub": "u-1", "iat": now, "exp": exp if exp is not None else now + 300,
              "email": email, "email_verified": True, "preferred_username": email.split("@")[0], **extra}
    return jwt.encode(claims, pem, algorithm=alg, headers={"kid": kid})


def test_provider_from_config(provider):
    assert provider.issuer == ISSUER and provider.audience == "meseeks" and provider.require_for_review


def test_discovery_checks_issuer(provider, monkeypatch):
    assert oidc.discover(provider)["jwks_uri"].endswith("/jwks")
    bad = dict(DISCOVERY, issuer="https://evil.example")
    monkeypatch.setattr(oidc, "_get", lambda url, timeout=5: bad if "well-known" in url else {"keys": [JWK]})
    oidc._cache.clear()
    with pytest.raises(oidc.OidcError):
        oidc.discover(provider)


def test_verify_accepts_a_good_token_and_rejects_bad_ones(provider):
    claims = oidc.verify(token(), provider)
    assert claims["email"] == "sweeden@legalluminary.com"
    for bad in (
        token(pem=OTHER_PEM),                              # signed by someone else
        token(kid="k2"),                                   # unknown key id
        token(exp=int(time.time()) - 3600),                # expired
        token(iss="https://evil.example"),                 # wrong issuer
        token(aud="other-app"),                            # wrong audience
        token(email_verified=False),                       # provider says the email is unverified
        token(azp="not-meseeks"),                          # issued to another client
    ):
        with pytest.raises(oidc.OidcError):
            oidc.verify(bad, provider)
    with pytest.raises(oidc.OidcError):                    # alg=none is never accepted
        oidc.verify(jwt.encode({"iss": ISSUER, "aud": "meseeks", "sub": "x", "iat": 1, "exp": 2**31}, None, algorithm="none"), provider)


def test_identity_comes_from_the_token_not_the_caller(provider, monkeypatch):
    monkeypatch.setenv("MESEEKS_ID_TOKEN", token("jcking1278@cloudfronts.group"))
    ident = witness.local_identity("sweeden@legalluminary.com")   # caller claims to be Scott
    assert ident.address == "jcking1278@cloudfronts.group" and ident.verified and ident.claims[1] == ISSUER
    assert witness.is_witness(ident)[0]


def test_review_requires_an_authenticated_witness(provider, monkeypatch):
    ok, why = witness.is_witness(witness.Identity("sweeden@legalluminary.com", "192.168.0.42", "macos"))
    assert not ok and "not authenticated" in why
    ok, _ = witness.is_witness(witness.Identity("sweeden@legalluminary.com", "192.168.0.42", "macos", verified=True))
    assert ok
    ok, why = witness.is_witness(witness.Identity("someone@gmail.com", "192.168.0.42", "macos", verified=True))
    assert not ok and "not a witness identity" in why                  # a valid token for a stranger is still a stranger
    ok, why = witness.is_witness(witness.Identity("sweeden@legalluminary.com", "8.8.8.8", "macos", verified=True))
    assert not ok and "outside" in why                                  # authentication does not waive the network check
    assert witness.is_witness(witness.Identity("sweeden@legalluminary.com", "192.168.0.42", "macos"), channel="mail")[0]  # mail: origin check only


def test_mailed_directive_with_token(provider, tmp_path, monkeypatch):
    from meseeks import adk_agent, mailbox
    monkeypatch.setenv("MESEEKS_REVIEW", str(tmp_path / "review.json"))
    monkeypatch.setenv("MESEEKS_DATA", str(tmp_path / "meseeks.json"))
    monkeypatch.setattr("meseeks.review.LOG", tmp_path / "logs")
    monkeypatch.setattr("meseeks.review.load_firm_domains", lambda: set())
    held = {"id": "hq", "message_id": "<hq@x>", "sender_domain": "gmail.com", "subject": "Killeen council notice?",
            "body": "Public notice: the Killeen city council meets Tuesday; comment period open.", "received": "2026-10-15T00:00:00Z", "attachments": [],
            "has_source_link": False, "links": [], "in_reply_to": None, "proposed": "notice", "reason": "low confidence", "classifier": "model", "status": "pending"}
    (tmp_path / "review.json").write_text(json.dumps({"inbox": "x", "items": [held]}))
    eml = (f"Received: from mac.lan (mac.lan [192.168.0.42]) by mail.legalluminary.com with ESMTPSA; Thu, 15 Oct 2026 10:00:00 -0500\r\n"
           f"From: Someone <someone@gmail.com>\r\nTo: meseeks@legalluminary.com\r\nSubject: confirm hq notice\r\n"
           f"Date: Thu, 15 Oct 2026 10:00:00 -0500\r\nMessage-ID: <t1@x>\r\n\r\nconfirm hq notice\r\ntoken: {token()}\r\n").encode()
    msg = mailbox.parse_eml(eml)
    entry = adk_agent.apply_directive(msg, witness.directive(msg.subject, msg.body), {})
    assert entry["publish"] and entry["category"] == "notice" and "Scott Weeden" in entry["reason"]   # token identity, not the From header
    bad = mailbox.parse_eml(eml.replace(token().encode(), token(pem=OTHER_PEM).encode()))
    entry = adk_agent.apply_directive(bad, witness.directive(bad.subject, bad.body), {})
    assert not entry["publish"] and "rejected" in entry["reason"]
