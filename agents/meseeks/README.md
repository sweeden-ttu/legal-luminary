# Meseeks inbox processor

Turns mail sent to `meseeks@legalluminary.com` into posts on [/meseeks/](https://www.legalluminary.com/meseeks/).
Named, loosely, for the Rick and Morty automatons that exist only to complete a task. Ours have a standing one.

```
mail ──▶ mailbox.py ──▶ classifier.py ──▶ guardrails.enforce ──▶ _data/meseeks.json ──▶ _pages/meseeks.md
          (IMAP/.eml)    (rules, or Claude   (deterministic;        (committed by the     (Jekyll renders)
                          if key present)     model can't widen)     workflow)
```

## Categories

| category | published when |
|---|---|
| `opportunity` | job / clerkship / internship / pro bono / RFP |
| `notice` | public notice, agenda, hearing, council or county announcement, newspaper legal notice |
| `standing_order` | court standing / general / administrative order **and** it carries a source link or PDF |
| `question` | member of the public asking about their own situation; identifiers redacted, sender never stored |
| `answer` | sender domain is in `_data/meseeks_firm_domains.yml` **and** subject carries `[Q-<id>]` of a posted question |

Everything else is held: spam, abuse, non-PDF attachments, bodies under 40 chars, low-confidence
classifications, answers from anyone who is not a listed firm. Posts expire after `retention_days` (60).

## Run

```bash
cd agents
python -m meseeks.run --dry-run --eml ../tests/meseeks/fixtures   # no network, no writes
python -m meseeks.run --eml some/dir                               # write from .eml files
python -m meseeks.run                                              # IMAP
```

Env for IMAP: `MESEEKS_IMAP_HOST`, `MESEEKS_IMAP_USER`, `MESEEKS_IMAP_PASSWORD`, optional `MESEEKS_IMAP_FOLDER`.
Optional `ANTHROPIC_API_KEY` enables the Claude classifier (`LL_ADK_MODEL` to pick the model);
`MESEEKS_RULES_ONLY=1` forces the keyword rules.

Audit of every decision goes to `logs/meseeks/YYYY-MM-DD.jsonl`.

## Schedule

`.github/workflows/meseeks-inbox.yml` runs every two hours and is a no-op until the three
`MESEEKS_IMAP_*` repository secrets exist.

## Adding a firm

Append to `_data/meseeks_firm_domains.yml` after the firm agrees its replies are anonymous,
general, public, and end with a referral to private counsel. Subdomains of a listed domain are accepted.

## Tests

```bash
pytest tests/meseeks -q
```
