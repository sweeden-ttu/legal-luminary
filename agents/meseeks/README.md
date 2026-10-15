# Meseeks inbox processor

Turns mail sent to `meseeks@legalluminary.com` into posts on [/meseeks/](https://www.legalluminary.com/meseeks/).
Named, loosely, for the Rick and Morty automatons that exist only to complete a task. Ours have a standing one.

```
mail ──▶ mailbox.py ──▶ agent.yaml / round.yaml ──▶ guardrails.enforce ──▶ _data/meseeks.json ──▶ _pages/meseeks.md
          (IMAP/.eml)    (ADK orchestrator: local     (deterministic;         (committed by the      (Jekyll renders)
                          model → coders → API)        model can't widen)      workflow)
                                                            │
                                                            └─▶ _data/meseeks_review.json ──▶ review.py (human confirm / ack)
```

Formal model: `specs/tla/Meseeks.tla` (TLA+, checked with TLC) and `specs/prolog/meseeks.pl`.

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
python -m meseeks.run --adk --dry-run --eml ../tests/meseeks/fixtures   # ADK agent, no writes
python -m meseeks.run --adk                                             # ADK agent over IMAP
python -m meseeks.run --dry-run --eml ../tests/meseeks/fixtures         # legacy single classifier
adk run meseeks                                                         # interactive (root_agent.yaml)
```

### The ADK agent (agent.yaml → round.yaml)

`agent.yaml` is a `LoopAgent` orchestrator; `round.yaml` is the sub-autonomous `LlmAgent` it
loops over. Per round the model is `meseeks.backends.MODEL`, a chain tried in order until one
answers: a local Ollama / LM Studio / OpenAI-compatible server on `MESEEKS_LLM_HOSTS`
(`127.0.0.1,192.168.0.15`) at ports `1234,15443`; then the headless coders `claude`, `codex`,
`agy`, `agent`, `opencode` (one prompt, one unattended call, own budget each; override with
`MESEEKS_CODERS` JSON); then the Anthropic API if `ANTHROPIC_API_KEY` is set. If all fail the
keyword rules classify the batch.

Clocks: no single call is waited on longer than `MESEEKS_MAX_CALL_SECONDS` (60); a round's
window is 1.3 × the sum of the sub-agent budgets (`MESEEKS_WINDOW_SLACK`), 0.9 × during a
human-in-the-loop drill (`MESEEKS_HITL=1`); the loop stops when every message has a proposal,
when no sub-agent answered, after `MESEEKS_IDLE_SECONDS` (60) without a new proposal, or after
`MESEEKS_MAX_ROUNDS` (3) question + reason + instruction rounds.

Guardrails run in Python before and after the model: hard rejects and out-of-scope mail
(anything not in the Killeen / Bell County / Texas statutory, political or judicial context —
`guardrails.scope_of`) are held before any model sees them; model output is advisory
(`adk_agent._advisory`: unknown categories and unusable confidences fall back to the rules, a
rule-detected question can never be relabeled out of its anonymity) and `guardrails.enforce`
makes every publish decision.

### Prompts

Every prompt is pulled by name from one Evidently project (`prompts.yml`: host
`http://192.168.0.15:8000`, prompt names `meseeks.instruction`, `meseeks.coder_wrapper`,
`meseeks.classifier`), falling back to `prompts/<name>.md` when the host is unreachable.

```bash
python -m meseeks.prompts init   # create the project if needed, seed the prompts, write project_id
python -m meseeks.prompts pull   # which version each prompt resolves to right now
```

### Human in the loop — witness agents

Held messages (other than hard rejects) wait in `_data/meseeks_review.json`. Only a **witness**
may decide them (`_data/meseeks_witnesses.yml`): Scott Weeden (`scotdwg`, `sweeden`) or
Johnathan King (`jcking1278`), as a username or first/last-name combination at `ttu.edu`,
`cloudfrontsgroup.org`, `cloudfronts.group`, `legalluminary.com` or `luminarylegal.com`, acting
from the local or wide-area network, on macOS, Rocky Linux or Kodachi Linux.

Witnesses authenticate with OpenID Connect against `https://www.login.cloudfronts.group:3443`
(`oidc:` in the witness file): `review login` discovers the provider at
`/.well-known/openid-configuration` and signs in (device flow if offered, else authorization
code + PKCE on a loopback port); every review command then verifies the ID token's signature
against the provider's JWKS and validates `iss`, `aud`, `exp`, `email_verified`, and takes the
acting address from the token — never from the caller. `MESEEKS_OIDC_CA` names the private CA.

```bash
python -m meseeks.review login                        # ID token -> ~/.config/meseeks/token.json (0600)
python -m meseeks.review list
python -m meseeks.review confirm <id> <category>   # goes through the same advisory layer and gate
python -m meseeks.review ack <id> [note]
```

A witness can also mail the inbox `confirm <id> <category>` or `ack <id>`; the directive is
verified by sender address, the originating IP in the earliest `Received` header, and platform
(and by a `token: <id token>` line when present or when `require_for_mail` is on), is never
shown to a model, and is applied through the same `review` path.

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

### Witnessed forwards (newspaper clippings, council members' posts)

A witness can forward a notice they have seen — e.g. a Killeen Daily Herald legal notice a
council member clipped and posted on Facebook — from a listed forwarding address
(`forwarders:` in `_data/meseeks_witnesses.yml`: `sweeden.ttu@gmail.com`,
`scott.weeden@gmail.com`, `sweeden@ttu.edu`). The forward is published as
"Witnessed by Scott Weeden" (never the forwarding address), the forwarded-message header is
stripped, image attachments of the clipping are allowed, and the scope and category gates still
apply. It counts as witnessed only when the mail host stamped `Authentication-Results:
mail.legalluminary.com; ... dmarc=pass` (or an aligned `dkim=pass`); a forged `From:` is
treated like any stranger, and Authentication-Results written by the sender are ignored.

### Background monitor

```bash
cd agents
python -m meseeks.monitor                 # one cycle: git pull --ff-only, run --adk, test, commit + push
python -m meseeks.monitor --loop 7200     # every two hours in the foreground
python -m meseeks.monitor --install       # prints the launchd (macOS) or systemd timer (Rocky/Kodachi) unit
```

`MESEEKS_IMAP_FOLDERS=INBOX,Sent` watches incoming and outgoing mail. Nothing is pushed unless
`tests/meseeks` passes on that machine; every cycle is logged to `logs/meseeks/monitor.jsonl`.

## Client intake: lemmas, dilemmas and non-action

`_data/meseeks_cases.yml` holds each case opened from a public notice: only facts from the
notice (court, cause number, dates, amounts), never party names or property addresses.
`python -m meseeks.intake brief <case>` builds the intake brief:

- **Lemmas**: each fact the decision rests on, with its source and days left to its deadline.
- **Dilemma**: the options (answer / retain counsel / do nothing for a citation; reinstate /
  alternatives with counsel or a HUD counselor / do nothing for a HUD sale) and what follows
  from each on the notice's own terms.
- **Non-action**: the countdown and what happens if no one acts.
- Money is compared only with numbers the client or attorney supplies (`--value`, `--payoff`,
  `--other-costs`); nothing is estimated. `--save` stores the brief and the client's answers
  under `MESEEKS_INTAKE_DIR` (default `~/.local/share/meseeks/intake`, 0600), never in the repo.

The brief informs the defendant and their attorney; it does not choose for them and is not
legal advice.

## Where inputs and outputs live

- **Inputs (private):** every message the inbox fetches is kept by `meseeks/store.py` when
  `MESEEKS_MAIL_STORE` is set, in the layout witnesses already use under `~/ll/mail_attachments`:
  `thread_id_<N>/attachedtomessage<K>.<ext>`, `thread_id_<N>/link_id_<K>` and a
  `thread_id_<N>/thread.json` (messages, attachment sha256 / size / original name, links, and
  the posts or intake briefs made from the thread). Identical attachments are stored once;
  archives are never opened. Dirs 0700, files 0600, never in the repo.
- **Outputs (public):** what the guardrails publish goes to `_data/meseeks.json` (notices,
  opportunities, questions, answers); case facts for intake go to `_data/meseeks_cases.yml`;
  each is recorded back in its thread's `thread.json` under `outputs`.
- **Intake answers (private):** `~/.local/share/meseeks/intake`, see above.
