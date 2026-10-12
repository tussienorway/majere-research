# Research log

## 2026-10-12
- **Change of direction:** the project now targets Norwegian (Bokmål/Nynorsk) plus reliable tool calling on a single 16 GB GPU. The Archetype Council track is paused and moved to `docs/archive/`.
- **Base models and data:** checked existence and licences. Qwen3-8B, NorMistral-7B/11B-warm (ltg) and Mistral-7B v0.3 are Apache-2.0; Llama 3.1 has its own licence and is gated. Data: NCC (licences vary per sub-corpus), norwegian-alpaca (CC BY 4.0), glaive-fc-v2 (Apache-2.0), xlam-fc-60k (CC BY 4.0, gated). Benchmarks: NorEval (MIT), EuroEval (MIT), BFCL (Apache-2.0).
- **Site:** rebuilt and published at https://majere.thomasaustenaa.no (GitHub Pages, HTTPS enforced). The compute ask is about 275 H100 GPU-hours (estimate, method stated).
- **majere-nofc** created (Apache-2.0): NO-FC v0 with 40 hand-written tasks (20 nb, 20 nn; 24 call, 8 no-call, 8 clarify), an evaluator for OpenAI-compatible endpoints, unit tests and QLoRA pilot scripts.
- **First baseline** on an RTX 5060 Ti 16 GB via Ollama: qwen3:8b scores 0.825 exact match (nb 0.85, nn 0.80). The errors are mainly relative weekdays and Norwegian time expressions. NorMistral-11B-thinking (GGUF) has no tool support in Ollama, so it wasn't scored.
- **Next:** prompt-based tool mode for NorMistral, qwen3 with thinking off, more date and time tasks, then the QLoRA pilot.
