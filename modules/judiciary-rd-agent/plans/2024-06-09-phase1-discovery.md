# Phase 1: Discovery Agent Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the "Discovery Agent" to build the initial relational database of Bell County judicial officials.

**Architecture:** The Alpha Automaton (orchestrator) will spawn a Discovery Agent as a separate process via `spawn_agents.sh`. The agent will use `ollama launch` to process targeted URLs, extract official data, and update the `judiciary_db.json` relational store. Correctness is verified by the `verification_automaton.py`.

**Tech Stack:** Python, Bash, Ollama (Llama3/Llava), JSON.

---

### Task 1: Refine JSON Schema and Initial State

**Files:**
- Modify: `../legal-lumany/modules/judiciary-rd-agent/judiciary_db.json`

- [ ] **Step 1: Define the complete relational structure in `judiciary_db.json`**
    - Ensure fields for `name`, `title`, `office`, `election_date`, `term_end`, `re_election_year`, `type`, `url`, and `headshot_path` are present.

- [ ] **Step 2: Commit initial schema**

### Task 2: Implement Discovery Logic in `spawn_agents.sh`

**Files:**
- Modify: `../legal-lumany/modules/judiciary-rd-agent/spawn_agents.sh`

- [ ] **Step 1: Update `spawn_agents.sh` to handle the 'discovery' agent type**
    - The script should call `ollama launch` with a specific prompt for data extraction from the Bell County government URLs.
    - It must output standardized logs for the `verification_automaton.py`.

- [ ] **Step 2: Verify script output**
    - Run: `./spawn_agents.sh discovery "https://www.bellcountytx.com/about_us/elected_officials/index.php"`
    - Expected: Log file created in `logs/` with valid transitions.

### Task 3: Automated Data Extraction and DB Update

**Files:**
- Create: `../legal-lumany/modules/judiciary-rd-agent/update_db.py`

- [ ] **Step 1: Write `update_db.py` to parse agent output and update `judiciary_db.json`**
    - This script will take the text output from the Discovery Agent and update the JSON database.

- [ ] **Step 2: Integrate update logic into `spawn_agents.sh`**

### Task 4: Formal Verification

**Files:**
- Modify: `../legal-lumany/modules/judiciary-rd-agent/verification_automaton.py`

- [ ] **Step 1: Ensure the automaton covers the 'Discovery' state transitions**
    - Transition: S1 (Launched) -> S2 (Crawl/Extract) -> S5 (Data Verified) -> S6 (Done).

- [ ] **Step 2: Run end-to-end test**
    - Expected: `VERIFICATION SUCCESS` in terminal.
