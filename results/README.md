# Results

## 2026-10-12: Baseline on 40 seed tasks (NO-FC v0), no fine-tuning
Run on an RTX 5060 Ti 16 GB with Ollama 0.40.2, Q4_K_M quantisation, temperature 0 and native tool calling.

| Model | Exact match (all) | Bokmål | Nynorsk | Function name | Arguments | No call | Clarify |
|---|---|---|---|---|---|---|---|
| qwen3:8b | **0.825** (33/40) | 0.85 | 0.80 | 0.917 | 0.819 | 1.00 | 1.00 |
| NorMistral-11B-thinking | not scored: no tool support in Ollama | | | | | | |

The error analysis and raw answers are in [majere-nofc/results](https://github.com/tussienorway/majere-nofc/tree/main/results). In short:
- wrong weekday (3)
- "halv ni" read as 09:30 (1)
- wrong phone number in Nynorsk (1)
- unnecessary follow-up questions (2)

These are indicative numbers on a small development set.

NO-FC v1 (120 tasks, 80 dev / 40 held-out test, `data/nofc_v1.jsonl` in [majere-nofc](https://github.com/tussienorway/majere-nofc)) has no scores yet. The table above is the only published NO-FC result.

## Index
- [2026-10-12: Hermes local model eval (4B fine-tune vs 9B, candidates)](2026-10-12-hermes-local-model-eval.md) — Hermes Agent measurements, not NO-FC scores.
- [2026-10: AI agent architectures overview + per-agent deep dives (Norwegian)](../research/ai-agent-architectures-2026-10.md) – [details](../research/agent-architectures/README.md)
- [2026-10-13: Semantisk ruter fase 1 (norsk)](2026-10-13-semantisk-ruter-fase1.md) – [plan](../research/plan-semantisk-ruting.md)
