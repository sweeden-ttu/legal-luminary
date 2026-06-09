#!/bin/bash
CRON_JOB="0 9 * * * /Users/sweeden/legal-luminary/modules/judiciary-rd-agent/daily_monitor.sh"
(crontab -l 2>/dev/null | grep -v "daily_monitor"; echo "$CRON_JOB") | crontab -
echo "Successfully scheduled daily monitor via crontab."

