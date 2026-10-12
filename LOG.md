# Research log

## 2026-10-13 (later)
- **NO-FC v1 baselines** (Ollama, RTX 5060 Ti; test = 40 held-out / dev = 80, exact match): qwen3:8b thinking off native tools **0.825** test / 0.775 dev; thinking off prompt tools 0.800 / 0.762; thinking on native 0.800 / 0.688; NorMistral-11B-thinking Q4 prompt tools **0.325** / 0.287 (call-name acc 0.11, it barely emits parseable calls). Thinking off is both faster and better for qwen3.
- **QLoRA smoke run** (Qwen3-8B, 4-bit, r16, max_len 1024, 50 steps, torch 2.11+cu128): peak 9.41 GiB, 15.3 s/step, ~327 tok/s. At max_len 2048 it hit OOM at step 25 with another llama.cpp server holding ~5 GB. Needed fixes: trl 1.15 dropped `warmup_ratio` (now `warmup_steps=5`), and trl's fused LM head needs Triton, so `triton-windows` is added on Windows. Details: [majere-nofc PR #7](https://github.com/tussienorway/majere-nofc/pull/7).
- **Compute:** measured ~1.2M tokens/h on 16 GB; 100M tokens ≈ 85 h per seed. The scaled-phase GPU-hour estimate is to be rescaled from this after the full pilot.
- **Next:** full pilot SFT on qwen3-8b (base choice leans Qwen3 given NorMistral's tool-call baseline), then evaluation on the v1 test split.

## 2026-10-13
- **NO-FC v1** is on [majere-nofc](https://github.com/tussienorway/majere-nofc) main: 120 tasks (80 dev / 40 held-out test) in `data/nofc_v1.jsonl`. The evaluator has `--tool-mode prompt` and `--no-think`. QLoRA pilot scripts were updated for transformers 5 (`dtype`). An Ollama Modelfile under `ollama/` fixes the NorMistral chat template. No v1 baseline scores yet.
- **Docs:** README, results index, evaluation protocol, research plan and the compute tracker in this repo are synced to v1. The only published NO-FC score remains the v0 qwen3:8b baseline, 0.825 exact match (33/40).
- **Next:** v1 baselines — qwen3 with `--no-think`, and NorMistral via `--tool-mode prompt` plus the Modelfile — then the QLoRA pilot (scripts ready, not run).

## 2026-10-12
- **Change of direction:** the project now targets Norwegian (Bokmål/Nynorsk) plus reliable tool calling on a single 16 GB GPU. The Archetype Council track is paused and moved to `docs/archive/`.
- **Base models and data:** checked existence and licences. Qwen3-8B, NorMistral-7B/11B-warm (ltg) and Mistral-7B v0.3 are Apache-2.0; Llama 3.1 has its own licence and is gated. Data: NCC (licences vary per sub-corpus), norwegian-alpaca (CC BY 4.0), glaive-fc-v2 (Apache-2.0), xlam-fc-60k (CC BY 4.0, gated). Benchmarks: NorEval (MIT), EuroEval (MIT), BFCL (Apache-2.0).
- **Site:** rebuilt and published at https://majere.thomasaustenaa.no (GitHub Pages, HTTPS enforced). The compute ask is about 275 H100 GPU-hours (estimate, method stated).
- **majere-nofc** created (Apache-2.0): NO-FC v0 with 40 hand-written tasks (20 nb, 20 nn; 24 call, 8 no-call, 8 clarify), an evaluator for OpenAI-compatible endpoints, unit tests and QLoRA pilot scripts.
- **First baseline** on an RTX 5060 Ti 16 GB via Ollama: qwen3:8b scores 0.825 exact match (nb 0.85, nn 0.80). The errors are mainly relative weekdays and Norwegian time expressions. NorMistral-11B-thinking (GGUF) has no tool support in Ollama, so it wasn't scored.
- **Next:** prompt-based tool mode for NorMistral, qwen3 with thinking off, more date and time tasks, then the QLoRA pilot.
