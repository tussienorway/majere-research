# Eval plan: which local model should be Hermes's brain (RTX 5060 Ti 16 GB, llama.cpp)
Date: 2026-10-12. [S] = sourced, [E] = estimate or own judgment.

## 1. Sourced principles
- **pass^k for reliability** [S: τ-bench paper, Yao et al. 2024]. pass^k is the probability that *all* k trials succeed, averaged over tasks, with the unbiased estimator C(c,k)/C(n,k). For gpt-4o retail, pass^1 was over 60% but pass^8 was under 25%, so a single run overstates reliability. tau2-bench supports `--num-trials` and `compute_metrics().pass_hat_ks` [S: sierra-research/tau2-bench docs].
- **Grade the end state, not the text** [S: τ-bench]. τ-bench compares the database state against a goal state. For us that means checking the effect: the file exists, the field has the right value, the right tool was called with the right arguments.
- **BFCL** [S: pypi bfcl-eval 2026.3.23]. Categories: simple/multiple/parallel (AST), live, irrelevance, and multi_turn_base/miss_func/miss_param/long_context. `--skip-server-setup` and `LOCAL_SERVER_ENDPOINT/PORT` work against our llama-server. Each multi_turn subset has 200 tasks [S: evalscope BFCL-v4 doc]. evalscope can also run `bfcl_v4` against any OpenAI URL with `--limit`.
- **EuroEval Norwegian** [S: euroeval.com]. Datasets include NoReC, NorNE, ScaLA-nb/nn, NorQuAD, NRK-quiz-QA, idioms-no and nor-common-sense-qa (the leaderboard columns). It runs against a local OpenAI server with `hosted_vllm/<id> --api-base` [S: EuroEval discussion #1309]. Leaderboard scores have ± uncertainty, which makes them usable as an external reference.
- **LLM-as-judge is noisy** [S: arXiv 2606.13685]:
  - Pairwise verdicts flip 13.6% of the time on identical repeats.
  - One judge showed a 72% first-position bias.
  - Agreement between judges was only 76% (κ=0.51).
  - Rewording the prompt changed the majority outcome in 25% of cases.
  - About 11 repeats were needed for a 95% stable majority.
  - Position bias depends on the judge and the task [S: Judging the Judges, IJCNLP 2025].
  - Conclusion: use exact or programmatic scoring wherever possible. Where a judge is needed, use a judge from another model family, swap positions, repeat 3–5 times [E], and spot-check 20 cases by hand.
- **Computer use**. These were not re-checked in this round, so they come from my general knowledge [E]: OSWorld checks the end state with scripts, and ScreenSpot(-Pro) measures click grounding as whether the click lands inside the target's bbox. Both are too heavy or too English-only to run in full here. Copy the method instead.

## 2. Test categories (one shared OpenAI-compatible interface, port 8081, temp 0 plus a temp 0.7 repeat)
| # | Category | Source / tool | Tasks | Repeats | Score | Gate |
|---|---|---|---|---|---|---|
| A | Norwegian Bokmål answers | existing eval.py, 60 tasks | 60 → expand to 100 [E] | 3 | language detection (share in nb) plus similarity | **≥95% nb** (TussieBot rule) |
| B | Hermes tool calls, single-step | eval.py, 60 tasks → 120 with Hermes's real tool schema [E] | 120 | 3 | right tool %, **exact args %** (normalised JSON), irrelevance (should NOT call) | **exact args ≥70%** and not worse than 9B (70%) |
| C | Standard function calling | BFCL subset: simple_python, multiple, parallel, irrelevance, live_simple, live_multiple (`run_bfcl.sh`) | ~1,000 total; `--limit 100` per category to save time [E] | 1 | BFCL AST accuracy | reference only, no gate |
| D | Multi-step agent flow | BFCL multi_turn_base + miss_param (limit 50 each), plus 20 own Hermes flows (vault, files, council) with state check | 120 | 3 | end state ok, pass^1 and pass^3 | pass^3 ≥ 9B |
| E | Computer use | majere-core hermes/computer-use benchmark, 10 tasks → 25 (browser 12, desktop 13) [E] | 25 | 3 | scripted end-state check plus steps and "stopped correctly" | ≥ 9B's 9/10 pass^1; no safety breaches (0 tolerance) |
| F | Grounding (clicks) | 50 own screenshots of Windows and agent-browser with bbox annotations, ScreenSpot method [E] | 50 | 1 | click inside bbox % | reference, relevant when choosing Holo2 |
| G | Council | council_round.py on 15 fixed questions | 15 | 2 | format/protocol followed (programmatic), Norwegian %, plus a blind cross-family judge with position swap | protocol ≥95% |
| H | Long context | `needle.py` at 8K/32K/64K/88K × depth 0.1/0.5/0.9 × 2, plus 10 BFCL multi_turn_long_context | 34 | 2 | exact match | ≥90% up to 88K [E] |
| I | Speed/VRAM | `perf_probe.py` at 2K/32K/80K; nvidia-smi | 3 points | 1 | pp/tg tok/s, VRAM MiB | must fit 96K plus mmproj in ≤15.5 GB; tg ≥ 25 tok/s [E] |
| J | External Norwegian | EuroEval: norquad, nrk-quiz-qa, nor-common-sense-qa, scala-nb, norec, idioms-no (`run_euroeval.sh`) | per dataset | 1 | EuroEval metric ± CI | reference against the leaderboard |

## 3. Statistics (stats.py)
- Every model runs the **same tasks** with paired comparison. stats.py gives Wilson 95% CI, an exact McNemar test on per-task majority, a paired bootstrap CI of the delta, and pass^k.
- With n=120 and p≈0.7, the Wilson CI is about ±8 points [E: computed]. A difference under ~8 points on one category is therefore NOT a real improvement unless McNemar p<0.05.
- **Switch rule** [E, built on TussieBot's rule]. The candidate must pass all of these:
  - nb ≥95%
  - exact args ≥70%
  - bootstrap delta CI lower bound > 0 on B or D or E
  - no category significantly worse (p<0.05)
  - fits 96K in VRAM
  - 0 safety breaches
- Use 3 repeats as the default, with seeds 0/1/2 and temp 0.7 for runs 2–3 [E]. The repeats are for pass^3. Temp 0 alone hides instability.

## 4. Failure analysis (per failed trial, tag automatically or by hand)
wrong tool, missing or incorrect argument, hallucinated tool, called when it should not, format/JSON error, loop/no stop (the Notepad failure), English drift, lost in context, wrong click coordinate. Report the counts per model. They feed the next round of fine-tuning data.

## 5. Run order and time (estimate) [E]
1. I (5 min)
2. A+B×3 (~30 min)
3. H (~40 min at 88K with about 1,800 pp tok/s)
4. D+E×3 (~1.5 h)
5. G (~30 min)
6. C+J reference (~2–3 h, can run overnight)

One model at a time on 8081. 9B on 8080 is the baseline and only needs to be run once with the new tasks.

## 6. Scripts in /workspace/research/hermes-eval/
- `stats.py`: paired statistics (CI, McNemar, bootstrap, pass^k) on JSONL `{task_id, category, pass}`. Tested with dummy data.
- `needle.py`: Norwegian needle test, outputs JSONL for stats.py.
- `perf_probe.py`: pp/tg tok/s from llama-server `timings` plus nvidia-smi VRAM.
- `run_euroeval.sh`: EuroEval Norwegian subset against llama-server. Verify the dataset ids against euroeval.com.
- `run_bfcl.sh`: BFCL subset with `--skip-server-setup`. Requires a matching BFCL handler name, with evalscope as the alternative.
- `repeat_eval.ps1`: runs eval.py N times. **Adjust the arguments to eval.py's real CLI**, which has not been checked.
Not run against any model: research only, no GPU used.
