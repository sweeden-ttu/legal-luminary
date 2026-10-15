"""OpenID Connect for witness agents: discovery, ID-token verification and validation, login.

Provider: the `oidc:` block of _data/meseeks_witnesses.yml (issuer
https://www.login.cloudfronts.group:3443 by default; MESEEKS_OIDC_ISSUER overrides).

  discover()            GET <issuer>/.well-known/openid-configuration (cached, short timeout)
  verify(token)         signature against the provider's JWKS (RS256/ES256), then the claims:
                        iss, aud, exp/nbf/iat with small skew, email_verified when present
  identity_from(token)  the witness Identity the token speaks for (address from the email or
                        preferred_username claim); witness.is_witness still decides
  login()               device-authorization flow when the provider offers it, otherwise the
                        authorization-code flow with PKCE on a loopback redirect; the ID token
                        is kept in ~/.config/meseeks/token.json (0600) for `meseeks.review`

TLS is always verified; MESEEKS_OIDC_CA points at the CA bundle for a private CA.
"""
from __future__ import annotations

import base64
import hashlib
import http.server
import json
import os
import secrets
import ssl
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import webbrowser
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

DEFAULT_ISSUER = "https://www.login.cloudfronts.group:3443"
TIMEOUT = float(os.environ.get("MESEEKS_OIDC_TIMEOUT", "5"))
SKEW = int(os.environ.get("MESEEKS_OIDC_SKEW", "60"))
TOKEN_FILE = Path(os.environ.get("MESEEKS_TOKEN_FILE", str(Path.home() / ".config" / "meseeks" / "token.json")))
UA = "LegalLuminaryMeseeks/1.0 (+https://legalluminary.com/meseeks/)"

_cache: dict[str, tuple[float, Any]] = {}
CACHE_SECONDS = 600


@dataclass
class Provider:
    issuer: str
    client_id: str = "meseeks"
    audience: str = "meseeks"
    scopes: str = "openid email profile"
    email_claim: str = "email"
    username_claim: str = "preferred_username"
    require_for_review: bool = True
    require_for_mail: bool = False
    extra: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_config(cls, cfg: dict | None) -> Provider:
        o = dict((cfg or {}).get("oidc") or {})
        issuer = os.environ.get("MESEEKS_OIDC_ISSUER") or o.pop("issuer", None) or DEFAULT_ISSUER
        known = {k: o.pop(k) for k in list(o) if k in cls.__dataclass_fields__ and k not in ("issuer", "extra")}
        return cls(issuer=issuer.rstrip("/"), extra=o, **known)


class OidcError(Exception):
    pass


# --------------------------------------------------------------------------- transport

def _context() -> ssl.SSLContext:
    return ssl.create_default_context(cafile=os.environ.get("MESEEKS_OIDC_CA") or None)


def _get(url: str, timeout: float = TIMEOUT) -> Any:
    now = time.monotonic()
    hit = _cache.get(url)
    if hit and now - hit[0] < CACHE_SECONDS:
        return hit[1]
    req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout, context=_context()) as r:
        data = json.loads(r.read().decode())
    _cache[url] = (now, data)
    return data


def _post(url: str, form: dict[str, str], timeout: float = TIMEOUT) -> Any:
    req = urllib.request.Request(url, data=urllib.parse.urlencode(form).encode(), method="POST",
                                 headers={"Content-Type": "application/x-www-form-urlencoded", "Accept": "application/json", "User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=_context()) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        try:
            return json.loads(body)
        except json.JSONDecodeError:
            raise OidcError(f"{url}: HTTP {e.code} {body[:200]}") from e


# --------------------------------------------------------------------------- discovery

def discover(provider: Provider) -> dict[str, Any]:
    """The provider's metadata; its `issuer` must equal the configured issuer (RFC 8414 / OIDC Discovery 4.3)."""
    doc = _get(f"{provider.issuer}/.well-known/openid-configuration")
    if doc.get("issuer", "").rstrip("/") != provider.issuer:
        raise OidcError(f"discovery issuer {doc.get('issuer')!r} does not match {provider.issuer!r}")
    for key in ("jwks_uri", "authorization_endpoint", "token_endpoint"):
        if key not in doc:
            raise OidcError(f"discovery document lacks {key}")
    return doc


def jwks(provider: Provider) -> dict[str, Any]:
    return _get(discover(provider)["jwks_uri"])


# --------------------------------------------------------------------------- verification + validation

def verify(token: str, provider: Provider) -> dict[str, Any]:
    """Return the ID token's claims if the signature verifies against the JWKS and the claims validate."""
    try:
        import jwt
        from jwt import PyJWKClient  # noqa: F401  (ensures the crypto extra is installed)
    except ImportError as e:  # pragma: no cover
        raise OidcError("PyJWT with the crypto extra is required: pip install 'PyJWT[crypto]'") from e

    header = jwt.get_unverified_header(token)
    alg = header.get("alg")
    if alg not in ("RS256", "RS384", "RS512", "ES256", "ES384", "ES512", "PS256"):
        raise OidcError(f"unsupported or unsafe alg {alg!r}")
    kid = header.get("kid")
    keys = [k for k in jwks(provider).get("keys", []) if not kid or k.get("kid") == kid]
    if not keys:
        _cache.clear()   # key rotation: refetch once
        keys = [k for k in jwks(provider).get("keys", []) if not kid or k.get("kid") == kid]
    if not keys:
        raise OidcError(f"no JWKS key for kid {kid!r}")
    key = jwt.PyJWK.from_dict(keys[0]).key
    try:
        claims = jwt.decode(
            token, key, algorithms=[alg], audience=provider.audience, issuer=provider.issuer,
            leeway=SKEW, options={"require": ["exp", "iat", "iss", "aud", "sub"]},
        )
    except jwt.PyJWTError as e:
        raise OidcError(f"id token rejected: {e}") from e
    if claims.get("email") and claims.get("email_verified") is False:
        raise OidcError("email claim is not verified by the provider")
    if "azp" in claims and claims["azp"] != provider.client_id:
        raise OidcError(f"azp {claims['azp']!r} is not {provider.client_id!r}")
    return claims


def address_of(claims: dict[str, Any], provider: Provider) -> str | None:
    addr = claims.get(provider.email_claim)
    if addr and "@" in addr:
        return addr.lower()
    user = claims.get(provider.username_claim)
    if user and "@" in user:
        return user.lower()
    return None


def identity_from(token: str, provider: Provider, ip: str | None, platform: str | None):
    """A witness Identity backed by a verified ID token (address comes from the token, not the caller)."""
    from .witness import Identity

    claims = verify(token, provider)
    addr = address_of(claims, provider)
    if not addr:
        raise OidcError("id token carries no email / username address")
    return Identity(addr, ip, platform), claims


# --------------------------------------------------------------------------- login

def _b64url(b: bytes) -> str:
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode()


def save_token(data: dict[str, Any], path: Path = TOKEN_FILE) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2))
    path.chmod(0o600)
    return path


def load_token(path: Path = TOKEN_FILE) -> str | None:
    env = os.environ.get("MESEEKS_ID_TOKEN")
    if env:
        return env
    if path.exists():
        try:
            return json.loads(path.read_text()).get("id_token")
        except (OSError, json.JSONDecodeError):
            return None
    return None


def login(provider: Provider, open_browser: bool = True, timeout: float = 300) -> dict[str, Any]:
    """Obtain an ID token: device flow if offered, else authorization code + PKCE on a loopback port."""
    doc = discover(provider)
    if doc.get("device_authorization_endpoint"):
        return _device_flow(provider, doc, timeout)
    return _pkce_flow(provider, doc, open_browser, timeout)


def _device_flow(provider: Provider, doc: dict[str, Any], timeout: float) -> dict[str, Any]:
    start = _post(doc["device_authorization_endpoint"], {"client_id": provider.client_id, "scope": provider.scopes})
    print(f"Visit {start.get('verification_uri_complete') or start['verification_uri']} and enter code {start['user_code']}")  # noqa: T201
    interval, deadline = float(start.get("interval", 5)), time.monotonic() + min(timeout, float(start.get("expires_in", timeout)))
    while time.monotonic() < deadline:
        time.sleep(interval)
        tok = _post(doc["token_endpoint"], {"grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                                            "device_code": start["device_code"], "client_id": provider.client_id})
        if "id_token" in tok:
            verify(tok["id_token"], provider)
            save_token(tok)
            return tok
        err = tok.get("error")
        if err == "slow_down":
            interval += 5
        elif err not in ("authorization_pending", None):
            raise OidcError(f"device flow: {err}: {tok.get('error_description', '')}")
    raise OidcError("device flow timed out")


def _pkce_flow(provider: Provider, doc: dict[str, Any], open_browser: bool, timeout: float) -> dict[str, Any]:
    verifier = _b64url(secrets.token_bytes(32))
    challenge = _b64url(hashlib.sha256(verifier.encode()).digest())
    state, nonce = secrets.token_urlsafe(16), secrets.token_urlsafe(16)
    result: dict[str, str] = {}

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):  # noqa: N802
            q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            result.update({k: v[0] for k, v in q.items()})
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Meseeks: you may close this window.")

        def log_message(self, *a):  # silence
            pass

    srv = http.server.HTTPServer(("127.0.0.1", 0), Handler)
    redirect = f"http://127.0.0.1:{srv.server_port}/callback"
    url = doc["authorization_endpoint"] + "?" + urllib.parse.urlencode({
        "response_type": "code", "client_id": provider.client_id, "redirect_uri": redirect, "scope": provider.scopes,
        "state": state, "nonce": nonce, "code_challenge": challenge, "code_challenge_method": "S256"})
    print(f"Open to sign in: {url}")  # noqa: T201
    if open_browser:
        webbrowser.open(url)
    t = threading.Thread(target=srv.handle_request, daemon=True)
    t.start()
    t.join(timeout)
    srv.server_close()
    if result.get("state") != state or "code" not in result:
        raise OidcError("no authorization code received (state mismatch or timeout)")
    tok = _post(doc["token_endpoint"], {"grant_type": "authorization_code", "code": result["code"], "redirect_uri": redirect,
                                        "client_id": provider.client_id, "code_verifier": verifier})
    if "id_token" not in tok:
        raise OidcError(f"token endpoint returned no id_token: {tok}")
    claims = verify(tok["id_token"], provider)
    if claims.get("nonce") != nonce:
        raise OidcError("nonce mismatch")
    save_token(tok)
    return tok
