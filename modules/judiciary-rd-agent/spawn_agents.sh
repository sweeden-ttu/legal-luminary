#!/bin/bash
AGENT_TYPE=$1
TARGET_URL=$2

if [ -z "$AGENT_TYPE" ] || [ -z "$TARGET_URL" ]; then
  echo "Usage: ./spawn_agents.sh <research|vision> <url>"
  exit 1
fi

mkdir -p logs
LOG_FILE="logs/agent_latest.log"
echo "[Alpha] Spawning $AGENT_TYPE agent for $TARGET_URL..." > "$LOG_FILE"

python3 real_agent.py "$TARGET_URL" >> "$LOG_FILE" 2>&1

python3 verification_automaton.py "$LOG_FILE"

