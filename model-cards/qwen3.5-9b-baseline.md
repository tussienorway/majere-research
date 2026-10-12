# Model card: Qwen3.5-9B as Majere baseline (no fine-tuning)
- **Base:** Qwen3.5-9B (Apache-2.0), GGUF via llama.cpp. Not modified by us.
- **Use in Majere:** local "brain" for Hermes Agent on one RTX 5060 Ti 16 GB.
- **Eval (temp 0, thinking off, [majere-eval-no-tools](https://huggingface.co/datasets/tussienorway/majere-eval-no-tools)):** 98.3% Norwegian, chrF 37.4, 81.7% right tool, 70.0% exact arguments; agent benchmark 15/16 over 2 runs.
- **Speed (96K ctx):** prefill ≈1,840–2,015 tok/s, decode 35–46 tok/s, 11.5 GB VRAM.
- **Limitations:** single-run numbers, 120-item set (±8 pt CI). 11/60 wrong tool, 7/60 wrong argument values.
