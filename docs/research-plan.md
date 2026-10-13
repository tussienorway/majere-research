# Research plan

## Questions
1. **RQ1:** How well do open 7–8B models call tools when the user writes in Bokmål or Nynorsk (NO-FC)?
2. **RQ2:** Does QLoRA fine-tuning on Norwegian instruction data plus Norwegian-translated function-calling data improve NO-FC without hurting general Norwegian ability (NorEval/EuroEval) or English tool calling (BFCL)?
3. **RQ3:** Which base is the better starting point under the same budget: a multilingual tool-capable model (Qwen3-8B) or a Norwegian-pretrained model without tool training (NorMistral)?
4. **RQ4:** Does the result survive 4-bit quantisation on a single 16 GB GPU?

## Method
- **Bases:** Qwen3-8B and NorMistral-7B-warm, both Apache-2.0. The 11B thinking variant is also used for comparison. Llama 3.1 is excluded because of its licence and gated access.
- **Data:** NCC (only the openly licensed parts), norwegian-alpaca (CC BY 4.0), glaive-function-calling-v2 (Apache-2.0) and xlam-function-calling-60k (CC BY 4.0). The function-calling data is translated into Bokmål and Nynorsk and validated.
- **Training:** QLoRA (NF4, r=16) on an RTX 5060 Ti 16 GB for the pilot, then scaled runs on grant compute. A 50-step smoke run is done (2026-10-13); the full pilot SFT has not been run yet. See [pilot-runbook.md](pilot-runbook.md).
- **Evaluation set:** NO-FC v0 is 40 seed tasks; the qwen3:8b exact match 0.825 (33/40) on v0 is kept as a historical baseline. NO-FC v1 is 120 tasks (80 dev / 40 held-out test) in [majere-nofc](https://github.com/tussienorway/majere-nofc) `data/nofc_v1.jsonl`. v1 baselines are done (see [results/README.md](../results/README.md)): on the test split qwen3:8b thinking off with native tools scores 0.825 and NorMistral-11B-thinking Q4 with prompt tools scores 0.325. Native tool calling is the default. qwen3 is also run with `--no-think`. NorMistral, which has no native tools in Ollama, is scored with `--tool-mode prompt` and the Modelfile under `ollama/`. Those modes are reported separately.
- **Compute estimate for the scaled phase:** about 275 H100 GPU-hours. Method: FLOPs ≈ 6·N·T, at 35% utilisation, plus a 50% buffer. Measured pilot throughput (2026-10-13): ~327 tok/s for Qwen3-8B QLoRA on an RTX 5060 Ti (9.41 GiB peak); rescaling follows after the full pilot.

## Pre-registered success criterion
NO-FC exact match improves clearly over both untouched bases, and NorEval does not drop more than seed noise. Results are published either way.

## Decisions
- **2026-10-13: Qwen3-8B with thinking off is the base for the pilot.** On NO-FC v1 it leads NorMistral-11B-thinking by a wide margin on tool calling: 0.825 vs 0.325 exact match on the held-out test split (qwen3:8b thinking off, native tools vs NorMistral-11B-thinking Q4, prompt tools; call-name accuracy for NorMistral is 0.11, it barely emits parseable calls). For qwen3, thinking off is both faster and better than thinking on (test 0.825 vs 0.800, dev 0.775 vs 0.688, native tools). Sources: [LOG.md](../LOG.md) (2026-10-13 (later)) and [results/README.md](../results/README.md).
- **NorMistral stays** as a comparison base and a possible later check of Norwegian fluency. Caveat: the baseline above is for NorMistral-11B-thinking, while the pilot script supports `normistral-7b` (`ltg/normistral-7b-warm`); that 7B base has no NO-FC baseline yet, so RQ3 is not settled by this decision.
- How to run the pilot: [pilot-runbook.md](pilot-runbook.md).
