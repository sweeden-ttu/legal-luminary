#!/bin/bash
LOG_FILE="/tmp/monitor_log.txt"
echo "Starting Daily Monitor..." > "$LOG_FILE"
curl -sL "https://www.bellcountytx.com/publicnotice_detail_T3_R730.php" > /tmp/temp_primary.html
curl -sL "https://www.bellcountytx.com/publicnotice_list.php" > /tmp/temp_list.html
if grep -iE "Election|Candidate|Judge" /tmp/temp_primary.html /tmp/temp_list.html >> "$LOG_FILE"; then
    echo "ALERT: Target keywords found. Triggering Jules review." >> "$LOG_FILE"
    JULES_BIN="/Users/sweeden/.local/bin/jules"
    if [ -x "$JULES_BIN" ]; then
        "$JULES_BIN" remote new --repo sweeden-ttu/legal-luminary --session "Methodology: Subsumption Architecture. Monitor alert triggered." --parallel 2 >> "$LOG_FILE" 2>&1
    fi
else
    echo "No relevant keywords found today." >> "$LOG_FILE"
fi
rm -f /tmp/temp_primary.html /tmp/temp_list.html

