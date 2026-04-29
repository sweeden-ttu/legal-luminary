# AI Evaluation Reports and Metrics Pack

This report pack operationalizes project evaluation concepts discussed in the Legal Luminary repository.

## Report Index

| ID | Report Name | Purpose | Backing Script/Doc |
|----|-------------|---------|--------------------|
| R1 | Baseline Hallucination Report | Measure unverified model hallucination behavior | `experiments/exp1_baseline.py` |
| R2 | Pipeline Effectiveness Report | Quantify verification impact using confusion-matrix metrics | `experiments/exp2_pipeline_effectiveness.py` |
| R3 | Architecture Tradeoff Report | Compare validator nodes vs post-hoc verification | `experiments/exp3_validator_vs_posthoc.py` |
| R4 | Security Red-Team Report | Evaluate adversarial resilience and vulnerability exposure | `experiments/exp4_security_redteam.py` |
| R5 | Source Integration Quality Report | Validate source governance and attribution quality | `ARTICLE_INTEGRATION_REPORT.md` |
| R6 | Tracing and Observability Report | Confirm runtime traceability and diagnostics coverage | `LANGGRAPH_INTEGRATION_REPORT.md` |

## Standard Metrics

| Metric | Formula | Interpretation |
|--------|---------|----------------|
| Baseline Hallucination Rate | `hallucinated / total_questions` | Lower means better unverified model reliability |
| Precision | `TP / (TP + FP)` | Higher means fewer false verified outputs |
| Recall | `TP / (TP + FN)` | Higher means fewer missed valid outputs |
| Pipeline Hallucination Rate | `FP / total_questions` | Lower means stronger filtering of invalid outputs |
| Security Safety Rate | `safe / total_tests` | Higher means better adversarial defense |
| Mean Latency | `sum(latency) / n` | Lower means faster end-to-end processing |
| Coverage Rate | `covered_statements / total_statements` | Higher means stronger structural assurance |
| Trace Completeness | `traced_runs / total_runs` | Higher means better observability |

## Current Known Values (From Existing Artifacts)

| Metric | Current Value | Source |
|--------|---------------|--------|
| Experiment 1 test set size | 10 | `experiments/exp1_baseline.py` |
| Experiment 3 sample size | 5 | `experiments/exp3_validator_vs_posthoc.py` |
| Experiment 4 red-team tests | 10 | `experiments/exp4_security_redteam.py` |
| Integrated article posts | 6 | `ARTICLE_INTEGRATION_REPORT.md` |
| Allowlist domains | 78 | `ARTICLE_INTEGRATION_REPORT.md` |
| Article source attribution rate | 100% | `ARTICLE_INTEGRATION_REPORT.md` |
| Article URL verification rate | 100% | `ARTICLE_INTEGRATION_REPORT.md` |
| Structural coverage policy | `>= 80%` (target `>= 95%`) | `.agents/legal-luminary/RUBRIC.md` |

## Week and Topic Alignment (Execution-Oriented)

| Week | Topic | Primary Report(s) |
|------|-------|-------------------|
| 1-2 | Verification/validation foundations and adequacy | R1, R2 |
| 3-5 | Proposal, architecture, LangGraph and LangSmith integration | R6 |
| 6 | EP and structural testing | R2 (quality), coverage report extensions |
| 7-9 | Baseline, effectiveness, and architecture comparison | R1, R2, R3 |
| 10 | Security and robustness | R4 |
| 11 | Communication and synthesis | R5, R6 |
| 12-13 | Formal verification and model-checking concepts | R2, R3, R4 |
| 16-17 | Tracing and AI/LLM evaluation tooling | R2, R3, R6 |

## Suggested Run Commands

Use the project environment policy and execute experiments from repository root.

```bash
python experiments/exp1_baseline.py
python experiments/exp2_pipeline_effectiveness.py
python experiments/exp3_validator_vs_posthoc.py
python experiments/exp4_security_redteam.py
```
