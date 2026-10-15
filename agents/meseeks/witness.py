"""Witness agents: who may act as the human in the loop (see _data/meseeks_witnesses.yml).

A witness identity is (address, origin IP, platform). The address must be a known person's
username or a first/last-name combination at an allowed domain; the IP must lie inside the
local or wide-area network; the platform must be one the witness agents run on (macOS, Rocky
Linux, Kodachi Linux). review.confirm/ack refuse anyone else, and so does the inbox when a
witness directive arrives by mail.
"""
from __future__ import annotations

import ipaddress
import os
import platform as _platform
import re
import socket
from dataclasses import dataclass
from email.utils import parseaddr
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "_data" / "meseeks_witnesses.yml"

_DIRECTIVE_RE = re.compile(r"^\s*(confirm|ack|acknowledge)\s+(\S+)(?:[ \t]+([a-z_]+))?", re.I | re.M)


@dataclass(frozen=True)
class Identity:
    address: str
    ip: str | None
    platform: str | None


def load(path: Path | None = None) -> dict:
    p = path or Path(os.environ.get("MESEEKS_WITNESSES", str(CONFIG)))
    doc = yaml.safe_load(p.read_text()) if p.exists() else {}
    doc = doc or {}
    doc.setdefault("people", [])
    doc.setdefault("domains", [])
    doc.setdefault("networks", [])
    doc.setdefault("platforms", [])
    return doc


def local_parts(person: dict) -> set[str]:
    f, l = person.get("first", "").lower(), person.get("last", "").lower()
    parts = {u.lower() for u in person.get("usernames", [])}
    if f and l:
        parts |= {f"{f}.{l}", f"{l}.{f}", f"{f}{l}", f"{l}{f}", f"{f}_{l}", f"{f[0]}{l}", f"{f}.{l[0]}", f"{f}-{l}"}
    return parts


def person_for(address: str, cfg: dict | None = None) -> dict | None:
    cfg = cfg or load()
    _, addr = parseaddr(address)
    addr = (addr or address).strip().lower()
    if "@" not in addr:
        return None
    local, domain = addr.rsplit("@", 1)
    if domain not in {d.lower() for d in cfg["domains"]}:
        return None
    local = re.sub(r"\+.*$", "", local)
    for person in cfg["people"]:
        if local in local_parts(person):
            return person
    return None


def ip_allowed(ip: str | None, cfg: dict | None = None) -> bool:
    cfg = cfg or load()
    if not ip:
        return False
    try:
        a = ipaddress.ip_address(ip)
    except ValueError:
        return False
    return any(a in ipaddress.ip_network(n, strict=False) for n in cfg["networks"])


def platform_allowed(name: str | None, cfg: dict | None = None) -> bool:
    cfg = cfg or load()
    return bool(name) and name.lower() in {p.lower() for p in cfg["platforms"]}


def bare_address(address: str) -> str:
    _, addr = parseaddr(address)
    return (addr or address).strip().lower()


def is_witness(identity: Identity, cfg: dict | None = None) -> tuple[bool, str]:
    cfg = cfg or load()
    person = person_for(identity.address, cfg)
    if not person:
        return False, "address is not a witness identity"
    if not ip_allowed(identity.ip, cfg):
        return False, f"origin {identity.ip or 'unknown'} is outside the local / wide-area network"
    if not platform_allowed(identity.platform, cfg):
        return False, f"platform {identity.platform or 'unknown'} is not a witness platform"
    return True, person.get("name", identity.address)


# --------------------------------------------------------------------------- this machine

def this_platform() -> str:
    sysname = _platform.system().lower()
    if sysname == "darwin":
        return "macos"
    if sysname == "linux":
        try:
            rel = Path("/etc/os-release").read_text().lower()
        except OSError:
            rel = ""
        for key in ("kodachi", "rocky"):
            if key in rel:
                return key
        return "linux"
    return sysname


def this_ip() -> str | None:
    if os.environ.get("MESEEKS_WITNESS_IP"):
        return os.environ["MESEEKS_WITNESS_IP"]
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("192.168.0.15", 9))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except OSError:
        return None


def local_identity(address: str | None = None) -> Identity:
    return Identity(address or os.environ.get("MESEEKS_WITNESS", ""), this_ip(), os.environ.get("MESEEKS_WITNESS_PLATFORM") or this_platform())


# --------------------------------------------------------------------------- directives by mail

def directive(subject: str, body: str) -> tuple[str, str, str | None] | None:
    """`confirm <id> <category>` or `ack <id>` in the subject or first lines of a mail."""
    for text in (subject, body[:400]):
        m = _DIRECTIVE_RE.search(text)
        if m:
            verb = "ack" if m.group(1).lower().startswith("ack") else "confirm"
            return verb, m.group(2).strip("[]<>"), (m.group(3) or "").lower() or None
    return None
