# Majere Research

[![Preprint](https://img.shields.io/badge/preprint-PDF-b31b1b)](paper/majere-preprint.pdf) [![HF dataset](https://img.shields.io/badge/%F0%9F%A4%97%20dataset-majere--eval--no--tools-yellow)](https://huggingface.co/datasets/tussienorway/majere-eval-no-tools) [![HF Space](https://img.shields.io/badge/%F0%9F%A4%97%20Space-majere--demo-blue)](https://huggingface.co/spaces/tussienorway/majere-demo) [![License: MIT](https://img.shields.io/badge/code-MIT-green)](LICENSE) [![Docs: CC BY 4.0](https://img.shields.io/badge/docs-CC%20BY%204.0-lightgrey)](https://creativecommons.org/licenses/by/4.0/) [![Cite](https://img.shields.io/badge/cite-CITATION.cff-orange)](CITATION.cff)

The open research side of **Majere**: fine-tuning a 7–8B open model for **Norwegian (Bokmål and Nynorsk)** and **reliable function/tool calling**, quantised so it runs locally on a single 16 GB GPU.

- Project site: https://majere.thomasaustenaa.no
- Contact: mail@thomasaustenaa.no
- Benchmark and code: https://github.com/tussienorway/majere-nofc (NO-FC, the evaluator, the QLoRA pilot)
- Research log: [LOG.md](LOG.md)

## Status (13 Oct 2026)
| Item | Status |
|---|---|
| Plan, data and benchmark selection | Done ([docs/research-plan.md](docs/research-plan.md)) |
| NO-FC v0: 40 seed tasks (nb/nn) and evaluator | Done ([majere-nofc](https://github.com/tussienorway/majere-nofc)) |
| NO-FC v1: 120 tasks (80 dev / 40 held-out test) | Done ([majere-nofc](https://github.com/tussienorway/majere-nofc), `data/nofc_v1.jsonl`) |
| Baseline v0, no fine-tuning (historical) | qwen3:8b **0.825** exact match (33/40) on NO-FC v0. NorMistral-11B was not scored on v0 (no native tool support in Ollama). See [results/](results/README.md) |
| Baselines v1, no fine-tuning | Done, exact match on test (40) / dev (80): qwen3:8b thinking off, native tools **0.825** / 0.775; thinking off, prompt tools 0.800 / 0.762; thinking on, native tools 0.800 / 0.688; NorMistral-11B-thinking Q4, prompt tools **0.325** / 0.287 (call-name acc 0.11). See [results/](results/README.md#2026-10-1213-no-fc-v1-baselines-no-fine-tuning) |
| Base-model decision | Qwen3-8B, thinking off, for the pilot. See [Decisions](docs/research-plan.md#decisions) |
| QLoRA smoke run (RTX 5060 Ti 16 GB) | Done: Qwen3-8B, 4-bit, r16, max_len 1024, 50 steps. Peak 9.41 GiB, 15.3 s/step, ~327 tok/s. Source: [majere-nofc PR #7](https://github.com/tussienorway/majere-nofc/pull/7) |
| Full pilot SFT | Not run yet. Runbook: [docs/pilot-runbook.md](docs/pilot-runbook.md) |
| Fine-tuned results | None yet |
| Next | Full pilot SFT on Qwen3-8B, then evaluation on the v1 test split |

## Latest (13 Oct 2026)
- **NO-FC v1 baselines are in** (Ollama, RTX 5060 Ti, exact match on the 40-task test split / 80-task dev split). qwen3:8b with thinking off and native tools scores **0.825** / 0.775. NorMistral-11B-thinking Q4 with prompt tools scores **0.325** / 0.287 and barely emits parseable calls (call-name acc 0.11). Full table in [results/](results/README.md). Thinking off is both faster and better for qwen3. Note that the v1 test score of 0.825 is a different task set from the v0 score of 0.825 (33/40).
- **QLoRA smoke run done** (50 steps, peak 9.41 GiB at max_len 1024). The full pilot SFT is not run yet. Next: full pilot SFT on Qwen3-8B, then eval on the v1 test split. See [docs/pilot-runbook.md](docs/pilot-runbook.md).
- **Base-model decision:** Qwen3-8B with thinking off is the pilot base. See [docs/research-plan.md](docs/research-plan.md#decisions).
- **NO-FC v1** is on [majere-nofc](https://github.com/tussienorway/majere-nofc) main. The evaluator has `--no-think` and `--tool-mode prompt`. An Ollama Modelfile for the NorMistral template is under `ollama/`.
- Hermes-agent measurements live in [results/](results/README.md) and [model-cards/](model-cards/). They are not NO-FC scores. A technical note already in this repo: [paper/majere-preprint.md](paper/majere-preprint.md).
- Compute tracker: [COMPUTE.md](COMPUTE.md).

## Layout
- `docs/research-plan.md`: questions, hypotheses, method and compute plan.
- `docs/evaluation-protocol.md`: benchmarks, metrics and the success criterion.
- `docs/pilot-runbook.md`: how to run the full pilot SFT on a Windows PC with an RTX 5060 Ti 16 GB.
- `results/`: published results (v1 baselines, v0 baseline kept as historical).
- `LOG.md`: dated research log.
- `docs/archive/`: the earlier Archetype Council track (paused, kept for transparency).

## Licence
Code: MIT (see `LICENSE`). Documentation and results: CC BY 4.0. Benchmark code in majere-nofc: Apache-2.0.

## Cite this
```bibtex
@misc{majere2026,
  title  = {Majere: Norwegian (Bokm{\aa}l/Nynorsk) Language Models with Reliable Tool Calling on a Single 16 GB GPU},
  author = {Austenaa, Thomas},
  year   = {2026},
  howpublished = {\url{https://github.com/tussienorway/majere-research}},
  note   = {Research protocol and baseline results}
}
```
