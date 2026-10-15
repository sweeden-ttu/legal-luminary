# Meseeks formal specs

| file | what |
|---|---|
| `Meseeks.tla` | TLA+ spec of the Meseeks orchestration: oracle sub-agents, per-call budgets, derived window (130% of Σ budgets, 90% in a human-in-the-loop drill), idle expiry, bounded question + reason + instruction rounds, human confirm/ack, the guardrails as `Enforce`, and the property `ModelDependencyFreeRecursivelyEnumeratedLanguageWhichHasDetermined`. |
| `MC_Meseeks.tla` / `.cfg` | TLC model: 3 messages (question → firm answer → spam), 7 sub-agents, drill mode. |
| `../prolog/meseeks.pl` | First-order twin in SWI-Prolog: the same laws (ratified by majority vote of the agents), an exhaustive check over every oracle output and every timing, and a timeline of test-games with naive-Bayes belief networks and a Nash-equilibrium check. |

```bash
# TLC (needs Java; tla2tools.jar from https://github.com/tlaplus/tlaplus/releases)
cd specs/tla && java -cp /path/to/tla2tools.jar tlc2.TLC -workers auto MC_Meseeks

# Prolog universe (needs swipl)
swipl -g run_all -t halt specs/prolog/meseeks.pl
```

TLC's first pass on the human-in-the-loop model found that a confirmation could relabel a
citizen's question out of its anonymity; `HumanConfirm` (and `agents/meseeks/review.py`) now
pass confirmations through the same advisory layer as model proposals.
