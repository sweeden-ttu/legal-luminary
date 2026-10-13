# Legal Luminary ADK agents

Google ADK workflows that run on Claude (`google.adk.models.anthropic_llm.AnthropicLlm`,
first-party Anthropic API) to crawl legalluminary.com, audit cited sources, and
research facts from official Killeen and Bell County sources.

| Workflow | What Claude does | What plain Python does |
|---|---|---|
| `official_source_research` (`root_agent`) | Reads pages and PDFs, proposes findings with verbatim quotes | Fetches allowlisted hosts only; re-fetches every source and drops findings whose quote is not on the page |
| `source_audit` | Writes a prioritized fix list | Extracts every cited URL and classifies it (ok, redirected, blocked, unverified, dead) |
| `crawl` (CLI only) | — | Maps every public page from the sitemap and internal links |

## Setup

```bash
pip install -r requirements_adk.txt
export ANTHROPIC_API_KEY=...        # or any credential the Anthropic SDK can discover
```

Optional: `LL_ADK_MODEL` (default `claude-opus-5-5`), `LL_ADK_EFFORT` (default `high`).

## Run

From the `agents/` directory:

```bash
python -m legal_luminary_adk.cli crawl --out ../site-map.json
python -m legal_luminary_adk.cli audit-sources _pages/texas-ag-race-26 --fail-on dead
python -m legal_luminary_adk.cli research "What charter amendments are on Killeen's Nov. 3, 2026 ballot?"
adk web .                            # interactive dev UI
```

`crawl` and `audit-sources` (without `--llm`) make no model calls.

## Tests

```bash
pytest tests/adk -m "not integration"          # unit: no network, no model
pytest tests/adk -m "integration and not llm"  # live web, no model
pytest tests/adk -m llm                        # billed Claude run; skips without a credential
```

CI: `.github/workflows/tests.yml`.
