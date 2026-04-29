#!/bin/bash

relative_path="${1:-}"
normalized_path="${2:-}"
term="${3:-}"
if [[ -z "${relative_path}" || -z "${normalized_path}" || -z "${term}" ]]; then
  echo "Usage: $(basename "$0") <relative_md_path> <normalized_site_path> <term>" >&2
  echo "  normalized_site_path: URL path under https://legalluminary.com/ (e.g. candidates/texas/nolanville/james_bilberry)" >&2
  exit 2
fi

VERIFY_PREFIX="Verify https://legalluminary.com/${normalized_path} matches the content in ${relative_path} before making any changes. If not, commit push and sync changes, and then you are done.

"

PROMPT_1=$(cat <<EOF
${VERIFY_PREFIX}First, check whether ${relative_path}.official already exists in the workspace (same directory as ${relative_path}).

If ${relative_path}.official exists: stop immediately. Do not create or modify ${relative_path}.tmp, do not scan for "${term}", and do not run any later pipeline steps for this invocation. Report that the official verification record already exists and you are done.

If ${relative_path}.official does not exist: continue with the instructions below.

Scan ${relative_path} for occurrences of the word ${term}.

For each occurrence:
1. Examine how ${term} is used in context.
2. Determine which of the following applies:
   a. A specific individual is named to the title (e.g., "Jose Guerrero is Mayor of Temple, Texas")
   b. The person is a candidate running against the incumbent (not currently holding the title)
   c. The text only discusses the office or position, with no individual named

Only when case (a) applies, you may record a row. Deduplicate aggressively:
- At most one row per distinct (full_name, title, jurisdiction) for the whole file.
- If the same person is named to the same title for the same jurisdiction more than once (same line, nearby sentences, or different phrasing), write exactly one row using the lowest line number where that claim appears, then treat that claim as complete — do not emit duplicate rows for repeated wording about the same office-holding.
- After recording a row for one distinct claim, continue scanning only for new distinct (full_name, title, jurisdiction) triples (e.g., another office-holder or another jurisdiction).

Write each row to ${relative_path}.tmp with exactly four comma-separated values:
   line_number, full_name, title, jurisdiction

Example:
   Line 40: "Jose Guerrero is Mayor of Temple Texas."
   Output: 40, Jose Guerrero, Mayor, Temple Texas

Do not write rows for cases (b) or (c).
EOF
)

PROMPT_2=$(cat <<EOF
${VERIFY_PREFIX}Read ${relative_path}.tmp. If multiple rows are identical (same name, title, jurisdiction), collapse them to a single row (keep the lowest line number) before further steps. For each distinct row (line, name, title, jurisdiction), verify that the named individual is officially listed under that title in the corresponding jurisdiction's directory.

Official jurisdiction directories:
- Bell County:    https://www.bellcountytx.com/about_us/elected_officials/index.php
- Texas State:    https://wrm.capitol.texas.gov/map?address=&city=&zip=&county=14&cityCode=&cdp=&matchmode=county
- Belton:         https://www.beltontexas.gov/how_do_i/contact/index.php
- Temple:         https://www.templetx.gov/departments/staff_directory.php
- Nolanville:     https://www.nolanvilletx.gov/page/Council
- Bartlett:       https://www.bartlett-tx.us/citycouncil
- Killeen:        https://www.killeentexas.gov/Directory.aspx?did=7

Example:
   Row: "John Doe, City Council, Killeen Texas"
   Action: Confirm John Doe appears under City Council at the Killeen directory.

After you locate the matching roster entry, go one step deeper on that same official site: open the person's **biography** or **profile** (linked name, staff detail page, council member subpage, PDF linked from the directory, or equivalent). Read whatever term dates, prior offices, board appointments, or role descriptions that page provides.

Then compare that official biography to ${relative_path} (especially the profile_summary and office_timeline front matter blocks). **Update ${relative_path}** by merging in any **new, non-contradictory** facts that appear only on the official biography and are not already stated. Rules:
- Prefer editing the profile_summary and office_timeline fields; keep valid YAML (preserve two-space indentation for multiline block scalars after the pipe).
- Add nothing that does not appear on the official directory or its directly linked official bio pages from this visit path; do not invent dates or titles.
- If the official bio contradicts the markdown, prefer the official source and correct the markdown (or append a CORRECTION row if the issue is a false title claim per the rules below).
- If there is nothing new to add, note that briefly and leave ${relative_path} unchanged.

If a person is NOT listed under the stated title in the stated jurisdiction's official directory, append a note to ${relative_path}.tmp:
   CORRECTION: \${name} is not officially listed as \${title} of \${jurisdiction}

When verification is finished for every distinct row (and any CORRECTION lines have been written for rows that failed verification), move the working file to the official record: rename ${relative_path}.tmp to ${relative_path}.official (e.g. \`mv ${relative_path}.tmp ${relative_path}.official\`). If ${relative_path}.tmp does not exist, skip the rename.
EOF
)

PROMPT_3=$(cat <<EOF
${VERIFY_PREFIX}Read ${relative_path}.official (if that file is missing, read ${relative_path}.tmp and rename it to ${relative_path}.official after you finish processing). Process each CORRECTION note.

For each line of the form:
   CORRECTION: \${name} is not officially listed as \${title} of \${jurisdiction}

1. Locate the corresponding claim in ${relative_path} (the original assertion that \${name} holds \${title} of \${jurisdiction}).
2. Edit ${relative_path} to fix the mistake. Acceptable fixes:
   a. Remove the false title claim while preserving the surrounding context.
   b. Replace \${name} with the correct office-holder if known from the official directory.
   c. Reword to clarify \${name} is a candidate, former official, or otherwise not the current \${title} — whichever the source context supports.
   Whenever you use an official directory or linked biography page as the source of truth, also merge any new factual lines from that biography into profile_summary and office_timeline (same rules as the verification step: official text only, valid YAML).
3. After the fix is applied to ${relative_path}, remove that CORRECTION line from ${relative_path}.official (or from ${relative_path}.tmp if the official file is not present yet, then ensure the result ends up in ${relative_path}.official).

In parallel, launch a background agent that crawls the following election sources to identify named candidates running for office in each remaining \${jurisdiction} referenced in ${relative_path}:
- Bartlett:    https://www.bartlett-tx.us/secretary/page/city-elections
- Nolanville:  https://www.nolanvilletx.gov/page/Elections
- Killeen:     https://killeentexas.gov/650/Elections
- Belton:      https://www.beltontexas.gov/government/city_clerk/election/index.php

For each jurisdiction, the agent should record:
   candidate_name, office_sought, jurisdiction, source_url

Append these results to ${relative_path}.candidates so they can be cross-referenced against ${relative_path} (e.g., to distinguish current office-holders from candidates).
EOF
)

PROMPT_4=$(cat <<EOF
${VERIFY_PREFIX}1. Crawl the website https://legalluminary.com
2. Compare information and phone numbers with official sources at bellcounty website or municipal city websites
3. Crawl all elections pages underneath the official city website to find:
  - Who is running for office
  - When the election is
You shall invoke an background cline command to do this for each website placing the CITYURL in the export variable:

Elections pages:
- Bartlett:    https://www.bartlett-tx.us/secretary/page/city-elections
- Nolanville:  https://www.nolanvilletx.gov/page/Elections
- Killeen:     https://killeentexas.gov/650/Elections
- Belton:      https://www.beltontexas.gov/government/city_clerk/election/index.php

  3a. After exporting CITYURL and CITYNAME, run cline with: --yolo --oneshot --no-interactive --moode act. Use --prompt to check the elections page, record candidates for that city only, write output under ${relative_path}.elections, then report city completion. Quote arguments as needed in the shell.

4. Create a long term memory store (SQL database, CSV spreadsheet, or directory with dossiers)
5. Lookup all candidates discovered on Facebook using the chrome-devtools-mcp server
6. Document everything in writing at ~/legal-luminary (where the live site files are stored)

This is a complex multi-step task that requires planning. Let me first gather some information about what exists in the current environment and what the user is expecting.

Let me start by:

1. Checking if ~/legal-luminary directory exists
2. Understanding the scope better by asking some clarifying questions

EOF
)

if [[ "${SKIP_AGENTS:-0}" == "1" ]]; then
  printf "SKIP_AGENTS: relative_path=%s normalized_path=%s term=%s PROMPT_CHARS=%s/%s/%s/%s\n" \
    "${relative_path}" "${normalized_path}" "${term}" \
    "${#PROMPT_1}" "${#PROMPT_2}" "${#PROMPT_3}" "${#PROMPT_4}"
  exit 0
fi

agent -f -p --yolo "${PROMPT_1}"

claude -p --dangerously-skip-permissions "${PROMPT_2}" &
wait $!

opencode run --dangerously-skip-permissions "${PROMPT_3}"

cline --yolo --oneshot --no-interactive --moode "act" "${PROMPT_4}" &
