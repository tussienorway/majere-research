# Model card: Qwen3.5-4B + Majere LoRA, round 1 (negative result, not released for use)
- **Base:** Qwen3.5-4B (Apache-2.0). **Method:** 16-bit LoRA, Unsloth, 1 epoch, 883 steps, RTX 5060 Ti 16 GB. Loss 1.27 → ≈1.05.
- **Data:** 6,000 NbAiLab/norwegian-alpaca (CC BY 4.0) + 1,823 NousResearch/hermes-function-calling-v1 (Apache-2.0).
- **Eval:** 90.0% Norwegian (5 Danish/Swedish, 1 English drift), chrF 41.5, 63.3% right tool, 53.3% exact arguments; agent bench 8/8.
- **Verdict:** below the 9B baseline on every switching criterion; kept as a documented negative result. Weights may be published on request for reproducibility.
- **Next:** 9B SFT + distillation with cloud compute, see [COMPUTE.md](../COMPUTE.md) and [paper](../paper/majere-preprint.pdf).
