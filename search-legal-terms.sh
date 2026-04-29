#!/bin/bash
# Set SKIP_AGENTS=1 (default below) so agent_claude.sh only validates prompts without running agent/claude/opencode/cline.
# For a full agent run: SKIP_AGENTS=0 bash search-legal-terms.sh
#
# STRICT_LEAF_DIRS (default 1) — only directories with no child directories are scanned.
#   Set STRICT_LEAF_DIRS=0 to run one recursive grep from SEARCH_DIR (legacy).
# SEARCH_DIR — root under which leaf dirs are discovered (default ~/legal-luminary).
# REPO_ROOT — optional; if set, paths passed to agent_claude.sh are relative to REPO_ROOT (not each leaf).
#
# Example — strict leaves under _candidates with repo-root-relative paths:
#   repo="$HOME/legal-luminary"
#   SKIP_AGENTS=1 REPO_ROOT="$repo" SEARCH_DIR="$repo/_candidates" bash "$repo/search-legal-terms.sh"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AGENT_CLAUDE="${AGENT_CLAUDE:-$SCRIPT_DIR/agent_claude.sh}"

STRICT_LEAF_DIRS="${STRICT_LEAF_DIRS:-1}"
SEARCH_DIR="${SEARCH_DIR:-$HOME/legal-luminary}"
PATH_PREFIX="${REPO_ROOT:-$SEARCH_DIR}"

if [ ! -d "$SEARCH_DIR" ]; then
  echo "Error: Directory $SEARCH_DIR does not exist." >&2
  exit 1
fi
if [[ -n "${REPO_ROOT:-}" && ! -d "$REPO_ROOT" ]]; then
  echo "Error: REPO_ROOT is not a directory: $REPO_ROOT" >&2
  exit 1
fi

SEARCH_TERMS="mayor|justice|judge|council|representative|senator|secretary|governor|comptroller|commissioner|sheriff|clerk|treasurer|constable|attorney|councilman|alderman|trustee"

if [[ ! -f "$AGENT_CLAUDE" ]]; then
  echo "Error: agent script not found: $AGENT_CLAUDE" >&2
  exit 1
fi

# True iff $1 is a directory and contains no child directories (only files / empty / symlinks to files).
is_filesystem_leaf_dir() {
  local d="$1"
  [[ -d "$d" ]] || return 1
  [[ -z "$(find "$d" -mindepth 1 -maxdepth 1 -type d 2>/dev/null)" ]]
}

# Scan one directory tree for matching markdown and invoke agent_claude.sh per hit.
run_grep_pass() {
  local scan_root="$1"
  grep -rwi -l --include="*.md" -E "$SEARCH_TERMS" "$scan_root" 2>/dev/null \
    | while IFS= read -r file; do
        [[ -f "$file" ]] || continue
        echo "Searching $file"
        relative_path="${file#"$PATH_PREFIX"/}"
        relative_path="${relative_path#/}"
        # Site URL path for legalluminary.com (slashes, leading _ stripped from repo paths e.g. _candidates/... -> candidates/...)
        normalized_path="${relative_path%.md}"
        normalized_path="${normalized_path#_}"
        while IFS= read -r term; do
          echo "  term=$term relative_path=$relative_path normalized_path=$normalized_path"
          SKIP_AGENTS="${SKIP_AGENTS:-1}" bash "$AGENT_CLAUDE" "$relative_path" "$normalized_path" "$term"
        done < <(grep -Eio -w "$SEARCH_TERMS" "$file" | sort -fu)
      done
}

if [[ "$STRICT_LEAF_DIRS" == "1" ]]; then
  echo "STRICT_LEAF_DIRS=1: scanning filesystem leaf directories under $SEARCH_DIR" >&2
  find "$SEARCH_DIR" \( -name .git -o -name node_modules \) -prune -o -type d -print 2>/dev/null \
    | while IFS= read -r d; do
        is_filesystem_leaf_dir "$d" || continue
        run_grep_pass "$d"
      done
else
  echo "STRICT_LEAF_DIRS=0: single recursive scan from $SEARCH_DIR" >&2
  run_grep_pass "$SEARCH_DIR"
fi
