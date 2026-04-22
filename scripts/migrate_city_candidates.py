#!/usr/bin/env python3
"""Migrate municipal candidate research docs into city-organized Jekyll pages."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

SOURCE_ROOT = Path(
    "/Users/sweeden/projects/CS5374_Software_VV/election_2026/municipal/candidates"
)
SITE_ROOT = Path("/Users/sweeden/legal-luminary")
TARGET_COLLECTION_ROOT = SITE_ROOT / "_candidates" / "texas"
OUTPUT_DATA = SITE_ROOT / "_data" / "candidates_city_index.json"

STATE = "texas"


def slugify(value: str) -> str:
    lowered = re.sub(r"[^a-z0-9]+", "_", value.lower())
    return lowered.strip("_")


def extract_office(markdown_text: str) -> str:
    match = re.search(
        r"^##\s+Office Sought\s*$\n+(.+?)\n",
        markdown_text,
        flags=re.MULTILINE,
    )
    if not match:
        return "Municipal Candidate"
    return match.group(1).strip()


def parse_candidate_slug(candidate_name: str, source_slug: str) -> str:
    tokens = [slugify(token) for token in candidate_name.split() if token.strip()]
    tokens = [token for token in tokens if token]
    if len(tokens) >= 2:
        first = tokens[-1]
        last = tokens[0]
        return slugify(f"{first}_{last}")
    return slugify(source_slug)


_SUFFIXES = {"sr", "jr", "ii", "iii", "iv", "v"}


def _title_token(token: str) -> str:
    t = token.replace("-", " ").strip()
    if len(t) == 1:
        return t.upper()
    return t[:1].upper() + t[1:].lower() if t else t


def display_name_from_source_slug(source_slug: str) -> str:
    """
    source_slug matches dossier folder: lastname_firstname[_more][_suffix].
    Produces 'First ... Last' (and optional suffix) for UI — avoids relying on
    poll_result candidate_name word order, which can be inconsistent.
    """
    raw = source_slug.strip().lower()
    parts = [p for p in raw.split("_") if p]
    if len(parts) <= 1:
        return _title_token(parts[0]) if parts else source_slug.strip()
    body = parts[:]
    suffix: str | None = None
    if len(body) >= 2 and body[-1] in _SUFFIXES:
        suffix = body[-1]
        body = body[:-1]
    last_token = body[0]
    given_tokens = body[1:]
    given = " ".join(_title_token(g) for g in given_tokens)
    last = _title_token(last_token)
    if suffix:
        suf = suffix.upper() if suffix in ("ii", "iii", "iv", "v") else suffix.title()
        return f"{given} {last} {suf}".strip()
    return f"{given} {last}".strip()


def extract_profile_summary(markdown_text: str) -> str:
    """First narrative block after a known summary heading; avoids shipping full dossier in page body."""
    text = markdown_text.lstrip("\ufeff")
    patterns = [
        r"^#\s+Candidate Profile Summary\s*\n+(.*?)(?=\n# |\Z)",
        r"^#\s+Executive Summary\s*\n+(.*?)(?=\n# |\Z)",
        r"^#\s+Candidate Overview\s*\n+(.*?)(?=\n# |\Z)",
    ]
    for pat in patterns:
        m = re.search(pat, text, flags=re.DOTALL | re.MULTILINE)
        if m:
            block = m.group(1).strip()
            if block:
                return block
    m = re.search(r"^#\s+[^\n]+\n+(.*?)(?=\n# |\Z)", text, flags=re.DOTALL | re.MULTILINE)
    if m:
        return m.group(1).strip()
    return ""


def yaml_profile_summary_block(summary: str) -> str:
    if not summary.strip():
        return 'profile_summary: ""\n'
    lines = summary.rstrip().splitlines()
    indented = "\n".join("  " + line for line in lines)
    return f"profile_summary: |\n{indented}\n"


def front_matter(payload: dict[str, Any]) -> str:
    title_json = json.dumps(payload["title"])
    office_json = json.dumps(payload["office"])
    lines: list[str] = [
        "---",
        "layout: candidate-profile",
        f"title: {title_json}",
        f'state: "{payload["state"]}"',
        f'city: "{payload["city"]}"',
        f'candidate_slug: "{payload["candidate_slug"]}"',
        f'source_slug: "{payload["source_slug"]}"',
        f"office: {office_json}",
        f'permalink: "{payload["permalink"]}"',
        f'headshot: "{payload["headshot"]}"',
        f'thumbnail: "{payload["thumbnail"]}"',
        yaml_profile_summary_block(payload.get("profile_summary") or "").rstrip("\n"),
        "---",
        "",
    ]
    return "\n".join(lines) + "\n"


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def migrate_candidate(candidate_dir: Path) -> dict[str, Any] | None:
    poll_result_path = candidate_dir / "poll_result.json"
    source_md_path = candidate_dir / "deep-research.md"
    if not poll_result_path.exists() or not source_md_path.exists():
        return None

    poll_data = json.loads(poll_result_path.read_text(encoding="utf-8"))
    source_markdown = source_md_path.read_text(encoding="utf-8")

    source_slug = poll_data.get("candidate_slug", candidate_dir.name).strip()
    candidate_name_poll = poll_data.get("candidate_name", candidate_dir.name).strip()
    display_name = display_name_from_source_slug(source_slug)
    city = slugify(poll_data.get("city_context", "killeen"))

    candidate_slug = parse_candidate_slug(candidate_name_poll, source_slug)
    office = extract_office(source_markdown)
    profile_summary = extract_profile_summary(source_markdown)

    target_dir = TARGET_COLLECTION_ROOT / city
    ensure_dir(target_dir)
    target_page_path = target_dir / f"{candidate_slug}.md"
    permalink = f"/candidates/{STATE}/{city}/{candidate_slug}/"

    candidate_payload = {
        "title": display_name,
        "state": STATE,
        "city": city,
        "candidate_slug": candidate_slug,
        "source_slug": source_slug,
        "office": office,
        "permalink": permalink,
        "headshot": f"/assets/imgs/candidates/{STATE}/{city}/{candidate_slug}/headshot.png",
        "thumbnail": f"/assets/imgs/candidates/{STATE}/{city}/{candidate_slug}/thumbnail.png",
        "profile_summary": profile_summary,
    }
    # Body intentionally empty: executive summary lives in front matter only.
    content = front_matter(candidate_payload)
    target_page_path.write_text(content, encoding="utf-8")

    return {
        "name": display_name,
        "state": STATE,
        "city": city,
        "candidate_slug": candidate_slug,
        "source_slug": source_slug,
        "office": office,
        "profile_url": permalink,
        "headshot": candidate_payload["headshot"],
        "thumbnail": candidate_payload["thumbnail"],
    }


def build_index(records: list[dict[str, Any]]) -> dict[str, Any]:
    sorted_records = sorted(records, key=lambda row: (row["city"], row["name"]))
    cities: dict[str, dict[str, Any]] = {}
    for record in sorted_records:
        city = record["city"]
        city_bucket = cities.setdefault(city, {"city": city, "candidates": []})
        city_bucket["candidates"].append(record)

    return {
        "state": STATE,
        "cities": list(cities.values()),
        "candidates": sorted_records,
        "count": len(sorted_records),
    }


def main() -> None:
    ensure_dir(TARGET_COLLECTION_ROOT)
    records: list[dict[str, Any]] = []
    for candidate_dir in sorted(SOURCE_ROOT.iterdir()):
        if not candidate_dir.is_dir():
            continue
        migrated = migrate_candidate(candidate_dir)
        if migrated:
            records.append(migrated)

    OUTPUT_DATA.write_text(json.dumps(build_index(records), indent=2), encoding="utf-8")
    print(f"Migrated {len(records)} candidates")
    print(f"Wrote index: {OUTPUT_DATA}")


if __name__ == "__main__":
    main()
