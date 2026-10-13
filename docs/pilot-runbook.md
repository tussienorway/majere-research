# Pilot runbook: full QLoRA SFT on Qwen3-8B (Windows, RTX 5060 Ti 16 GB)

This runbook covers the **full pilot SFT** of Qwen3-8B, the next step after the 50-step smoke run. It uses only scripts and flags that exist in [majere-nofc](https://github.com/tussienorway/majere-nofc) (`train/build_data.py`, `train/qlora_sft.py`, `nofc/evaluate.py`). Numbers come from [LOG.md](../LOG.md) (entry 2026-10-13 (later)), [majere-nofc PR #7](https://github.com/tussienorway/majere-nofc/pull/7) and the smoke metrics file [`results/v1/pilot_metrics_qwen3-8b_smoke-2026-10-13.json`](https://github.com/tussienorway/majere-nofc/blob/main/results/v1/pilot_metrics_qwen3-8b_smoke-2026-10-13.json). Why Qwen3-8B: see [Decisions](research-plan.md#decisions).

Status: the smoke run is done, the full pilot is not run yet. Nothing below is a result until it has been run and logged.

## 1. Prerequisites
- Windows PC with an RTX 5060 Ti 16 GB (Blackwell).
- An NVIDIA driver that supports CUDA 12.8 or newer. Blackwell needs PyTorch built for CUDA 12.8+ (`torch>=2.7`, see the header of `train/requirements.txt`). The smoke run used torch 2.11.0+cu128.
- Python and git. The evaluator needs Python 3.10+. The exact Python version of the smoke run is not recorded.
- Internet access to Hugging Face for the base model (`Qwen/Qwen3-8B`, Apache-2.0) and the two data sources: `NbAiLab/norwegian-alpaca` (CC BY 4.0) and `glaiveai/glaive-function-calling-v2` (Apache-2.0).
- **Free the GPU first.** Stop every other GPU user: Ollama, ComfyUI, any llama.cpp server. At max_len 2048 the smoke run hit CUDA OOM at step 25 while another llama.cpp server held ~5 GB of VRAM. Check with `nvidia-smi` that nothing else is holding VRAM before you start.

## 2. Setup
Commands as they appear in the majere-nofc README (PowerShell or cmd, from the repo root):

```bash
git clone https://github.com/tussienorway/majere-nofc
cd majere-nofc
pip install torch --index-url https://download.pytorch.org/whl/cu128   # Blackwell needs CUDA 12.8+
pip install -r train/requirements.txt
```

`train/requirements.txt` already contains `triton-windows<3.7` for Windows. It is needed because trl's fused LM head requires Triton. The training script already uses `warmup_steps=5`, because trl 1.15 dropped `warmup_ratio`. Do not change either.

## 3. Build the pilot data
```bash
python train/build_data.py --n-alpaca 4000 --n-glaive 4000 --out pilot_mix.jsonl
```
This is the command in the majere-nofc README (4000 and 4000 are also the script defaults). Notes:
- The mix is plain text in one `<|role|>` format with `<tool_call>{json}</tool_call>` for tool calls.
- The glaive part is English. It is used as-is in the pilot; translating the function-calling data into Bokmål and Nynorsk is a later step.
- The smoke run trained on 800 examples and 249,889 dataset tokens (from its metrics file). The `build_data.py` arguments used for the smoke mix are not recorded, so do not assume the full mix has the same size. Its token count is written to `pilot_metrics.json` as `dataset_tokens`.

## 4. Optional: repeat the smoke run
```bash
python train/qlora_sft.py --base qwen3-8b --data pilot_mix.jsonl --max-steps 50 --max-len 1024
```
Use this to check that the machine reproduces the numbers in section 6 before committing to a long run.

## 5. Run the full pilot
```bash
python train/qlora_sft.py --base qwen3-8b --data pilot_mix.jsonl --max-len 1024
```
- Keep `--max-len 1024`. The script default is 2048, which OOMed in the smoke test (with ~5 GB held by another process). 1024 fits at 9.41 GiB peak.
- Fixed in the script: 4-bit NF4 with double quantisation, LoRA on all projections (`--rank`, default 16), batch size 1 with `--grad-accum` (default 16), gradient checkpointing, paged 8-bit AdamW, learning rate `--lr` (default 2e-4), `--epochs` (default 1.0), `--seed` (default 0).
- Output goes to `runs/qwen3-8b-r16-s0` by default (`runs/<base>-r<rank>-s<seed>`), or to the directory you give with `--out`. It holds the adapter and `pilot_metrics.json`.
- Leave the PC alone during the run: no other GPU work, and make sure Windows does not sleep.

## 6. Expected VRAM and throughput
From the 50-step smoke run (Qwen3-8B, 4-bit, r16, max_len 1024, grad_accum 16, torch 2.11.0+cu128, triton-windows):

| Metric | Smoke run |
|---|---|
| Peak VRAM | 9.41 GiB |
| Step time | 15.3 s (15.28 s in the metrics file) |
| Throughput | ~327 tok/s (327.2 in the metrics file) |
| Tokens per step | ~5.0k (4997.8 in the metrics file) |
| Wall time, 50 steps | 763.8 s |

To estimate the full run: steps per epoch = examples / 16 (batch size 1 × grad_accum 16), and wall time ≈ `dataset_tokens` / 327 s at the smoke throughput. The smoke measurements of ~330 tok/s correspond to ~1.2M tokens/h on this card (LOG.md). Compare the real `pilot_metrics.json` against these numbers: a much higher peak VRAM or a much lower throughput usually means another process is using the GPU.

## 7. Checkpointing and resume
What the script does today:
- `save_strategy="epoch"` with `--epochs` defaulting to 1.0, so Trainer writes a checkpoint only at the end of the epoch. Then `save_model` writes the final adapter to the output directory.
- There is **no intermediate checkpoint** and **no resume flag**. `train/qlora_sft.py` calls `train()` without `resume_from_checkpoint`.
- If the run is interrupted, restart it from the beginning with the same command. Run it when you can leave the PC undisturbed.

Possible follow-up in majere-nofc (not done): add a `--save-steps` option and a `--resume` option to `train/qlora_sft.py` before any run that is much longer than the pilot.

## 8. Evaluate the adapter on the v1 test split
`nofc/evaluate.py` talks to any OpenAI-compatible chat endpoint and scores the 40 held-out test tasks:

```bash
python -m nofc.evaluate --base-url <endpoint>/v1 --model <served-model-name> --tasks data/nofc_v1.jsonl --split test --out results/v1/<name>-<date>.jsonl
```

Add `--tool-mode prompt` (schemas in the system prompt, `<tool_call>` parsed from the reply) or leave the default native mode, and say which you used. The training text uses `<tool_call>{json}</tool_call>`, so prompt mode is the closest match to what the adapter saw; this is a suggestion, not a measured result. Add `--no-think` only if you also report the Qwen3 baseline with it. The baselines to compare against are in [results/README.md](../results/README.md): on the test split, qwen3:8b thinking off scores **0.825** with native tools and 0.800 with prompt tools.

**Known gap:** majere-nofc has no script yet to serve the adapter. Its README says that before NO-FC can be run against a fine-tuned model, the server needs a matching chat template (TODO: a template file plus GGUF export). The training format is not Qwen3's own chat template, so a server that applies the stock Qwen3 template will not reproduce the training format. Until that exists, any evaluation setup is ad hoc: write down exactly how the adapter was served (merge or adapter loading, server, chat template). Do not report the Ollama Q4_K_M baselines and an adapter served another way as a like-for-like comparison without saying so.

Do the evaluation with the other GPU users still stopped, then compare with the same hardware and temperature 0, as the baselines were.

## 9. What to log back
In majere-nofc (as PR #7 did):
- `pilot_metrics.json` from the run directory, copied to `results/v1/` with a name like `pilot_metrics_qwen3-8b_<run>-<date>.json`.
- The NO-FC raw answers (`.jsonl`) and the `.summary.json` from the evaluation, in `results/v1/`.
- The exact command lines, `max_len`, rank, grad_accum, seed, torch and trl versions, and how the adapter was served.

In this repo:
- A new [LOG.md](../LOG.md) entry: what was run, `dataset_tokens`, steps, wall time, peak VRAM, tokens/s, and the NO-FC test-split score next to the baseline. Report the result either way, as the [research plan](research-plan.md) pre-registers.
- Update the Status table and Latest section in [README.md](../README.md), and add a section to [results/README.md](../results/README.md).
- Rescale the scaled-phase GPU-hour estimate in [research-plan.md](research-plan.md) and [COMPUTE.md](../COMPUTE.md) from the measured throughput. LOG.md already notes this as pending until the full pilot is done.
- Update the status line in [pilot/README.md](../pilot/README.md).
