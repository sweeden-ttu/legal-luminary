#!/usr/bin/env python3
"""
Enrich judicial officer profile front matters with data from:
  - _data/candidates.yml  (social URLs, notes, campaign info)
  - _data/judges.yml      (court contact, election info)
  - judiciary.sqlite       (appointment dates, term end)

Usage: python enrich_profiles.py
"""

import os
import re
import sqlite3
import yaml
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent  # legal-luminary/
DATA_DIR = BASE_DIR / "_data"
PROFILES_DIR = BASE_DIR / "collections" / "_candidates" / "courts"

# ── Load candidates.yml ──────────────────────────────────────
with open(DATA_DIR / "candidates.yml") as f:
    candidates_root = yaml.safe_load(f)

candidates_list = [c for c in candidates_root.get("candidates", [])
                   if c.get("group_function") == "Judicial"]

candidates_by_name = {}
for c in candidates_list:
    name = c.get("name", "").strip()
    if name:
        candidates_by_name[name] = c

# ── Load judges.yml ──────────────────────────────────────────
with open(DATA_DIR / "judges.yml") as f:
    judges_list = yaml.safe_load(f) or []

judges_by_name = {}
for j in judges_list:
    name = j.get("judge_name", "").strip()
    if name:
        judges_by_name[name] = j

# ── Load judiciary.sqlite ────────────────────────────────────
DB_PATH = BASE_DIR / "modules" / "judiciary-rd-agent" / "judiciary.sqlite"
db_data = {}
if DB_PATH.exists():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    for row in conn.execute("SELECT * FROM officials"):
        db_data[row["name"].strip()] = dict(row)
    conn.close()

# ── Name matching helpers ────────────────────────────────────
def normalize(name):
    return re.sub(r"[^a-z0-9]", "", name.lower())

def find_match(name, lookup):
    exact = lookup.get(name)
    if exact:
        return exact
    nname = normalize(name)
    for k, v in lookup.items():
        if normalize(k) == nname:
            return v
    return None

def find_db_match(name):
    exact = db_data.get(name)
    if exact:
        return exact
    nname = normalize(name)
    for k, v in db_data.items():
        if normalize(k) == nname:
            return v
    return None

# ── Profile file collection ──────────────────────────────────
profile_files = list(PROFILES_DIR.rglob("*.md"))
profile_files = [p for p in profile_files if p.name != "courts-directory.md"]
print(f"Found {len(profile_files)} profile files")

# ── Enrichment loop ──────────────────────────────────────────
updated_count = 0

for fpath in sorted(profile_files):
    with open(fpath) as f:
        content = f.read()

    # Split front matter from body
    parts = content.split("---", 2)
    if len(parts) < 3:
        print(f"  SKIP {fpath.name}: no valid front matter")
        continue

    front_matter = yaml.safe_load(parts[1])
    body = parts[2]

    if not isinstance(front_matter, dict):
        print(f"  SKIP {fpath.name}: front matter not a dict")
        continue

    title = front_matter.get("title", "")
    if not title:
        print(f"  SKIP {fpath.name}: no title")
        continue

    # ── Match from candidates.yml ────────────────────────────
    c = find_match(title, candidates_by_name)

    # ── Match from judges.yml ────────────────────────────────
    j = find_match(title, judges_by_name)

    # ── Match from sqlite ────────────────────────────────────
    d = find_db_match(title)

    # ── Track changes ────────────────────────────────────────
    changes = []

    # Social URLs
    if c:
        for field, key in [
            ("facebook_url", "facebook_url"),
            ("linkedin_url", "linkedin_url"),
            ("instagram_url", "instagram_url"),
            ("campaign_website", "campaign_website"),
        ]:
            val = c.get(key)
            if val and val not in (None, "", "null"):
                old = front_matter.get(field)
                front_matter[field] = val
                if old != val:
                    changes.append(f"  {field}: {old} -> {val}")

    # Court contact info from judges.yml
    if j:
        contact = {}
        for field in ["court_name", "court_type", "court_coordinator",
                       "coordinator_email", "court_reporter", "phone",
                       "fax", "address", "mailing_address"]:
            val = j.get(field)
            if val and val not in (None, ""):
                contact[field] = val

        if contact:
            # Remove null keys
            contact = {k: v for k, v in contact.items() if v}
            old_contact = front_matter.get("court_contact")
            front_matter["court_contact"] = contact
            if old_contact != contact:
                changes.append(f"  court_contact: updated")

        # Election info
        election_info = j.get("election_info")
        if election_info:
            old_ei = front_matter.get("election_info")
            front_matter["election_info"] = election_info
            if old_ei != election_info:
                changes.append(f"  election_info: updated")

    # Enrich notes with data we have
    notes_parts = []
    existing_notes = front_matter.get("notes", "")
    if existing_notes and existing_notes not in ("", "null"):
        notes_parts.append(existing_notes.strip().rstrip("."))

    if d:
        extra = []
        if d.get("elected_date"):
            extra.append(f"Elected {d['elected_date']}")
        if d.get("term_end"):
            extra.append(f"Term expires {d['term_end']}")
        if extra:
            extra_str = ". ".join(extra)
            if extra_str not in existing_notes:
                notes_parts.append(extra_str)

    if notes_parts:
        new_notes = ". ".join(notes_parts)
        if len(notes_parts) > 1:
            new_notes += "."
        front_matter["notes"] = new_notes

    # Write back
    if changes:
        print(f"\n{title} ({fpath.relative_to(BASE_DIR)}):")
        for c in changes:
            print(c)

    new_yaml = yaml.dump(front_matter, allow_unicode=True,
                          default_flow_style=False, sort_keys=False,
                          width=120, indent=2)
    new_content = f"---\n{new_yaml}---{body}"

    with open(fpath, "w") as f:
        f.write(new_content)

    updated_count += 1

print(f"\nDone. Processed {updated_count} profiles.")
