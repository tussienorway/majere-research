---
title: "Majere: Measuring and Improving Norwegian Tool-Calling in Small Local LLMs on a Single 16 GB GPU"
author: "Thomas Austenaa — independent researcher, Grimstad, Norway (mail@thomasaustenaa.no)"
date: "Technical preprint v0.1, 13 October 2026"
---

**Abstract.** Small open-weight language models (4–14B parameters) can now run on a single consumer GPU, but two capabilities that matter for local agents remain weak and poorly measured for Norwegian: (i) answering consistently in Norwegian Bokmål without drifting into Danish, Swedish or English, and (ii) emitting tool calls with the correct function *and* exactly correct arguments. We describe Majere, an open research project that studies these capabilities inside a local agent stack (Hermes Agent on llama.cpp, RTX 5060 Ti 16 GB), including an optional council-of-personas layer with an explicit PAD/OCC affect state. We release a 120-item evaluation set and harness, report a baseline (Qwen3.5-9B: 98.3% Norwegian responses, 81.7% correct tool, 70.0% exact arguments) and an honest negative result (a LoRA-finetuned Qwen3.5-4B reached only 90.0% / 63.3% / 53.3%). We then lay out a concrete compute plan (≈400 A100-hours) for supervised fine-tuning and distillation of a 9B model, released as GGUF quantisations that fit 16 GB GPUs.

# 1. Problem

Local agents need a "brain" model that (a) speaks the user's language and (b) drives tools reliably. For Norwegian, public benchmarks (NorEval, EuroEval) measure general language ability but not tool use; tool-calling benchmarks (BFCL and similar) are English-only. In practice we observe two failure modes in small models: *language drift* (answers partly or wholly in Danish/Swedish/English) and *argument errors* (right function, wrong or missing argument values). Both silently break agent workflows. Our goal is to measure these on consumer hardware and to find training recipes that improve them without growing the model beyond what a 16 GB GPU can run.

**Research questions.** RQ1: How far can prompting and constrained decoding alone take a 9B model? RQ2: Does SFT on mixed Norwegian instruction data and tool-call data improve exact-argument accuracy without hurting Norwegian? RQ3: Does distillation from a larger teacher transfer agentic (multi-step, computer-use) behaviour to a 9B student? RQ4: Does an explicit affect/council layer change user-facing quality or tool reliability?

# 2. System architecture

**Runtime.** Hermes Agent (tool-using agent framework) talks to an OpenAI-compatible llama.cpp server. Target hardware: one NVIDIA RTX 5060 Ti, 16 GB VRAM. The 9B baseline at Q4/Q5 quantisation with a 96K context uses 11.5 GB VRAM, prefill ≈1,840–2,015 tok/s and decode 35–46 tok/s.

**Council layer (optional).** A user message can be routed to six persona agents (Healer, Gambler, Smith, Rival, Steward, Gleeman), each with a narrow role (wellbeing, risk, craft/implementation, critique, planning/resources, communication). A synthesiser merges their short opinions into one reply. A public, deliberately tiny in-browser demo is at `huggingface.co/spaces/tussienorway/majere-demo`.

**Affect model.** A PAD state (pleasure/valence, arousal, dominance/control, each in [-1, 1]) is updated each turn from OCC-style appraisals of the conversation (goal-congruence, praise/blame, likelihood). The state conditions persona weighting and tone. It is an engineering hypothesis, not a claim about machine emotion; RQ4 tests whether it has any measurable effect.

# 3. Evaluation protocol

**Data (released as `tussienorway/majere-eval-no-tools`).**

* *A — Norwegian (60 items):* instructions from NbAiLab/norwegian-alpaca (CC BY 4.0) with reference answers; the system prompt requires Bokmål.
* *B — Tool calling (60 items):* multi-turn conversations with tool schemas from NousResearch/hermes-function-calling-v1 (Apache-2.0); gold tool calls as references.

**Metrics.** A: share of answers classified as Norwegian by a lexical language identifier (Norwegian vs. English vs. Danish/Swedish function words), plus chrF against the reference. B: *right tool* (predicted sequence of function names equals gold) and *exact arguments* (names and parsed JSON arguments identical). Failures are tagged `no_call`, `format_json_error`, `wrong_tool`, `wrong_tool_count`, `wrong_or_missing_arg`, `english_drift`, `danish_swedish_drift`.

**Settings.** Temperature 0, fixed seed, thinking mode disabled, native tool calls via the server's chat template. Planned extensions: 3 trials per item with pass^k, paired comparison with Wilson intervals, McNemar and bootstrap; BFCL subset; NorEval/EuroEval; multi-step and computer-use tasks; needle-in-a-haystack at 8K–88K tokens. With 120 items the 95% interval is roughly ±8 points, so small differences are not claimed.

**Switching criterion.** A candidate replaces the baseline only if it has ≥95% Norwegian, ≥70% exact arguments, and is not worse on the agent benchmark.

# 4. Baseline and negative result

| Model (GGUF, llama.cpp) | Norwegian | chrF | Right tool | Exact args | Agent bench |
|---|---|---|---|---|---|
| Qwen3.5-9B (baseline) | **98.3%** | 37.4 | **81.7%** | **70.0%** | 15/16 (2 runs) |
| Qwen3.5-4B + LoRA (ours) | 90.0% | **41.5** | 63.3% | 53.3% | 8/8 |

**Finetuning setup (4B).** 16-bit LoRA with Unsloth, one epoch, 883 steps, on 6,000 Norwegian-Alpaca examples and 1,823 hermes-function-calling examples, on the 16 GB GPU. Training loss fell from 1.27 to ≈1.05.

**Interpretation.** The 4B model's chrF improved (closer to the style of the references) but it drifted into Danish/Swedish in 5/60 answers and English in 1/60, and lost 17 points on exact arguments compared with the 9B. Small-model capacity, a single epoch and a data mix dominated by general instructions are plausible causes. We report it as a negative result: *consumer-GPU LoRA of a 4B model does not reach the 9B baseline*, which motivates training at 9B scale, which our 16 GB GPU can do only with heavy compromises (QLoRA, short sequences, a 3–6 h iteration per run and no room for ablations or seeds).

**Error analysis of the baseline.** The baseline fails 18/60 items on exact arguments: 11 already pick the wrong tool (or wrong number of calls) and 7 pick the right tool with wrong or missing argument values. A per-tag breakdown is published with the raw outputs. Grammar-constrained decoding (RQ1) can remove formatting errors but not wrong tool choice or wrong values, which is why better training data (RQ2/RQ3) is needed.

# 5. Compute plan

Local work (prompting, constrained decoding, evaluation, GGUF conversion, small pilots) continues on the 16 GB GPU. Cloud compute is requested for training at 9B scale with proper seeds and ablations.

| Milestone | Work | A100-80GB hours |
|---|---|---|
| M1 (weeks 1–3) | SFT of Qwen3.5-9B (bf16 LoRA r=64 and full-parameter comparison) on ≈12K Norwegian instruction + tool-call dialogues already built; 3 data mixes × 2 seeds | 90 |
| M2 (weeks 3–5) | Agentic/computer-use SFT: multi-step tool trajectories and browser/desktop action traces, Norwegian and English | 70 |
| M3 (weeks 4–7) | Distillation: generate ≈30K Norwegian tool-use trajectories with an open 27–32B teacher (vLLM), filter by execution, train 9B student; 3 runs | 110 |
| M4 (weeks 6–8) | Ablations: data mix, LoRA vs. full FT, affect/council layer on/off, 4B vs. 9B vs. 14B scaling point | 70 |
| M5 (weeks 8–9) | Evaluation at scale (3 trials, BFCL, NorEval/EuroEval), GGUF quantisation (Q4_K_M, Q5_K_M, Q6_K, IQ4_XS) and quantisation-aware comparison | 30 |
| Buffer | Failed runs, re-runs | 30 |
| **Total** | | **≈400** |

On TPU v4/v5e the same plan maps to ≈30–60 days of a v4-8 slice with JAX/MaxText or PyTorch/XLA. Success criterion for the 9B student: ≥95% Norwegian, ≥80% exact arguments on the released set (baseline 70%), no regression on BFCL, and fits a 16 GB GPU at Q4_K_M with ≥32K context.

# 6. Open outputs

All code (MIT), documentation and results (CC BY 4.0), the evaluation set (CC BY 4.0, mixing CC BY 4.0 and Apache-2.0 sources with attribution), adapters, merged weights and GGUF files (under the base model's licence, Apache-2.0 for Qwen3.5) will be published on GitHub (`tussienorway/majere-research`) and Hugging Face (`tussienorway`), with training configs, logs and raw evaluation outputs so every number can be reproduced on a consumer GPU.

# 7. Limitations

The evaluation set is small (120 items) and the language identifier is lexical; a human-checked NO-FC v1 with ≥500 items is planned. Results are single-run so far. The author works independently, without institutional affiliation; all results are self-reported and reproducible from the released code.

# References

NbAiLab. *norwegian-alpaca* (CC BY 4.0). huggingface.co/datasets/NbAiLab/norwegian-alpaca.
NousResearch. *hermes-function-calling-v1* (Apache-2.0). huggingface.co/datasets/NousResearch/hermes-function-calling-v1.
Qwen Team. *Qwen3.5 model family*, 2026.
Patil et al. *Berkeley Function Calling Leaderboard (BFCL)*.
Mehrabian, A. *Pleasure-arousal-dominance: a general framework for describing temperament*, 1996.
Ortony, A., Clore, G., Collins, A. *The Cognitive Structure of Emotions* (OCC), 1988.
Popović, M. *chrF: character n-gram F-score for automatic MT evaluation*, WMT 2015.
