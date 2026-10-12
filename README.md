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
| Baseline, no fine-tuning | Only published score: qwen3:8b **0.825** exact match (33/40) on NO-FC v0. v1 baselines not run. NorMistral-11B was not scored on v0 (no native tool support in Ollama). See [results/](results/README.md) |
| QLoRA pilot (RTX 5060 Ti 16 GB) | Scripts ready, not run |
| Fine-tuned results | None yet |
| Next | v1 baselines (qwen3 `--no-think`; NorMistral via `--tool-mode prompt` and the Ollama Modelfile), then the pilot |

## Latest (13 Oct 2026)
- **NO-FC v1** is on [majere-nofc](https://github.com/tussienorway/majere-nofc) main. The evaluator has `--no-think` and `--tool-mode prompt`. An Ollama Modelfile for the NorMistral template is under `ollama/`. No v1 scores yet.
- **Published NO-FC score:** v0 only, qwen3:8b exact match 0.825 (33/40).
- Hermes-agent measurements live in [results/](results/README.md) and [model-cards/](model-cards/). They are not NO-FC scores. A technical note already in this repo: [paper/majere-preprint.md](paper/majere-preprint.md).
- Compute tracker: [COMPUTE.md](COMPUTE.md).

## Layout
- `docs/research-plan.md`: questions, hypotheses, method and compute plan.
- `docs/evaluation-protocol.md`: benchmarks, metrics and the success criterion.
- `results/`: published results, the baseline so far.
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
