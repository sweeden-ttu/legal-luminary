#!/bin/bash
# Schedules the daily monitoring task using Jules via Cron

JULES_CMD="/Users/sweeden/.local/bin/jules remote new --repo sweeden-ttu/legal-luminary --session \"Methodology: Subsumption Architecture & Reactive Agents (Agent-Oriented Programming, Chapter 10). Reasoning: This architecture builds a robust, layered scraper. you are the subagent using Subsumption Architecture. Extract Small Claims and Consumer Complaints cases, as well as Foreclosure cases involving McCarthy Holthus. Continuous scan for election-related updates and legal notices on https://www.bellcountytx.com/publicnotice_detail_T3_R730.php\" --parallel 2"

# Write the cron job to a temporary file
CRON_JOB="0 9 * * * $JULES_CMD"

(crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
echo "Successfully scheduled daily Jules session via crontab."
