# Jules Discovery System

A multi-agent system for searching and ranking Central Texas news and government updates.

## Architecture
Grounded in **Agent-Oriented Programming** and **Trustworthy Agents** literature.

- **Monitor Agent (`monitor.py`)**: Perception layer. Scans RSS feeds and government websites.
- **Analyst Agent (`analyst.py`)**: Interpretation layer. Uses a weighted lexicon to rank articles.
- **Jules Orchestrator (`jules.py`)**: Coordination layer. Manages parallelism and data storage.

## Usage
Run the discovery cycle from the module directory:
```bash
python jules.py
```
Results are saved to `_data/recent_articles.json`.

## Theoretical Grounding
- **Perception-Interpretation Cycle**: Follows the *OntoAgent* architecture.
- **Trustworthy Ranking**: Provides explicit reasoning for each confidence score (Section 8.4).
- **Parallel Execution**: Implements speculative parallelism paradigms.
