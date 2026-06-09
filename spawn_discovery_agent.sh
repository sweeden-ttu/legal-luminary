#!/bin/bash
echo "Setting up environment for Discovery Agent..."
pip install requests beautifulsoup4 pdfplumber docling > /dev/null 2>&1

echo "Reading AGENTS.md for operational context grounding..."
if [ -f "agents/AGENTS.md" ]; then
    export AGENTS_CONTEXT=$(cat agents/AGENTS.md)
else
    export AGENTS_CONTEXT="Context missing"
fi

echo "Spawning Discovery Agent (Phase 1)..."
python3 discovery_agent.py
