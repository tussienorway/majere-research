# Results

## 2026-10-12/13: NO-FC v1 baselines, no fine-tuning
120 tasks: 80 dev, 40 held-out test (`data/nofc_v1.jsonl` in [majere-nofc](https://github.com/tussienorway/majere-nofc)). Run on an RTX 5060 Ti 16 GB through Ollama, temperature 0. The test split is the headline number. Exact match is the share of tasks answered completely correctly. The columns call_name, call_arg and clarify are over all 120 tasks.

| Model | Mode | Test exact (40) | Dev exact (80) | All exact (120) | call_name | call_arg | clarify |
|---|---|---|---|---|---|---|---|
| qwen3:8b, thinking off | native tools | **0.825** (33/40) | 0.775 | 0.792 | 0.847 | 0.772 | 0.958 |
| qwen3:8b, thinking off | prompt tools | 0.800 (32/40) | 0.762 | 0.775 | 0.944 | 0.804 | 0.917 |
| qwen3:8b, thinking on | native tools | 0.800 (32/40) | 0.688 | 0.725 | 0.833 | 0.721 | 0.875 |
| NorMistral-11B-thinking Q4 | prompt tools | 0.325 (13/40) | 0.287 | 0.300 | 0.111 | 0.097 | 0.250 |

Notes:
- NorMistral-11B-thinking almost never produces a parseable tool call in prompt mode (call_name 0.11). It only scores on no-call tasks, so it is not a usable tool-calling base without fine-tuning.
- Thinking off is both faster and better for qwen3:8b.
- The v1 test score of 0.825 for qwen3:8b (thinking off, native tools) is a different task set from the v0 score of 0.825 (33/40) below.
- The qwen3:8b native-tools runs (thinking off and on) each report 1 errored request in the 120-task summary file.
- Native and prompt tool modes, and thinking on and off, are separate settings and are reported separately.

Sources in majere-nofc: [results/README.md](https://github.com/tussienorway/majere-nofc/blob/main/results/README.md), the raw answers and summary files in [results/v1/](https://github.com/tussienorway/majere-nofc/tree/main/results/v1), and [PR #7](https://github.com/tussienorway/majere-nofc/pull/7). Also recorded in [LOG.md](../LOG.md) (entry 2026-10-13 (later)).

### QLoRA smoke run (50 steps), 2026-10-13
Qwen3-8B, 4-bit NF4, rank 16, grad_accum 16, max_len 1024, torch 2.11.0+cu128. Not a result for NO-FC, only a throughput and memory measurement.

| Peak VRAM | Step time | Tokens/s | Tokens/step |
|---|---|---|---|
| 9.41 GiB | 15.3 s | ~327 | ~5.0k |

At max_len 2048 the run hit CUDA OOM at step 25 while another llama.cpp server held ~5 GB of VRAM. Metrics file: [pilot_metrics_qwen3-8b_smoke-2026-10-13.json](https://github.com/tussienorway/majere-nofc/blob/main/results/v1/pilot_metrics_qwen3-8b_smoke-2026-10-13.json). How to run the full pilot: [docs/pilot-runbook.md](../docs/pilot-runbook.md).

## 2026-10-12: Baseline on 40 seed tasks (NO-FC v0), no fine-tuning (historical)
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

This v0 result is kept as history. The current baselines are on NO-FC v1, in the section above.

## Index
- [2026-10-12: Hermes local model eval (4B fine-tune vs 9B, candidates)](2026-10-12-hermes-local-model-eval.md) — Hermes Agent measurements, not NO-FC scores.
- [2026-10: AI agent architectures overview + per-agent deep dives (Norwegian)](../research/ai-agent-architectures-2026-10.md) – [details](../research/agent-architectures/README.md)
- [2026-10-13: Semantisk ruter fase 1 (norsk)](2026-10-13-semantisk-ruter-fase1.md) – [plan](../research/plan-semantisk-ruting.md)
