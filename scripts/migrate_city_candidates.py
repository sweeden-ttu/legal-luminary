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


def front_matter(payload: dict[str, Any]) -> str:
    lines: list[str] = [
        "---",
        "layout: candidate-profile",
        f'title: "{payload["title"]}"',
        f'state: "{payload["state"]}"',
        f'city: "{payload["city"]}"',
        f'candidate_slug: "{payload["candidate_slug"]}"',
        f'source_slug: "{payload["source_slug"]}"',
        f'office: "{payload["office"]}"',
        f'permalink: "{payload["permalink"]}"',
        f'headshot: "{payload["headshot"]}"',
        f'thumbnail: "{payload["thumbnail"]}"',
        "---",
        "",
    ]
    return "\n".join(lines)


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def migrate_candidate(candidate_dir: Path) -> dict[str, Any] | None:
    poll_result_path = candidate_dir / "poll_result.json"
    source_md_path = candidate_dir / "deep-research.md"
    if not poll_result_path.exists() or not source_md_path.exists():
        return None

    poll_data = json.loads(poll_result_path.read_text(encoding="utf-8"))
    source_markdown = source_md_path.read_text(encoding="utf-8")

    candidate_name = poll_data.get("candidate_name", candidate_dir.name).strip()
    source_slug = poll_data.get("candidate_slug", candidate_dir.name).strip()
    city = slugify(poll_data.get("city_context", "killeen"))

    candidate_slug = parse_candidate_slug(candidate_name, source_slug)
    office = extract_office(source_markdown)

    target_dir = TARGET_COLLECTION_ROOT / city
    ensure_dir(target_dir)
    target_page_path = target_dir / f"{candidate_slug}.md"
    permalink = f"/candidates/{STATE}/{city}/{candidate_slug}/"

    candidate_payload = {
        "title": candidate_name,
        "state": STATE,
        "city": city,
        "candidate_slug": candidate_slug,
        "source_slug": source_slug,
        "office": office,
        "permalink": permalink,
        "headshot": f"/assets/imgs/candidates/{STATE}/{city}/{candidate_slug}/headshot.png",
        "thumbnail": f"/assets/imgs/candidates/{STATE}/{city}/{candidate_slug}/thumbnail.png",
    }
    content = front_matter(candidate_payload) + source_markdown.rstrip() + "\n"
    target_page_path.write_text(content, encoding="utf-8")

    return {
        "name": candidate_name,
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
