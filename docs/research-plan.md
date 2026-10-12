# Research plan

## Questions
1. **RQ1:** How well do open 7–8B models call tools when the user writes in Bokmål or Nynorsk (NO-FC)?
2. **RQ2:** Does QLoRA fine-tuning on Norwegian instruction data plus Norwegian-translated function-calling data improve NO-FC without hurting general Norwegian ability (NorEval/EuroEval) or English tool calling (BFCL)?
3. **RQ3:** Which base is the better starting point under the same budget: a multilingual tool-capable model (Qwen3-8B) or a Norwegian-pretrained model without tool training (NorMistral)?
4. **RQ4:** Does the result survive 4-bit quantisation on a single 16 GB GPU?

## Method
- **Bases:** Qwen3-8B and NorMistral-7B-warm, both Apache-2.0. The 11B thinking variant is also used for comparison. Llama 3.1 is excluded because of its licence and gated access.
- **Data:** NCC (only the openly licensed parts), norwegian-alpaca (CC BY 4.0), glaive-function-calling-v2 (Apache-2.0) and xlam-function-calling-60k (CC BY 4.0). The function-calling data is translated into Bokmål and Nynorsk and validated.
- **Training:** QLoRA (NF4, r=16) on an RTX 5060 Ti 16 GB for the pilot, then scaled runs on grant compute.
- **Compute estimate for the scaled phase:** about 275 H100 GPU-hours. Method: FLOPs ≈ 6·N·T, at 35% utilisation, plus a 50% buffer. This will be replaced with throughput measured in the pilot.

## Pre-registered success criterion
NO-FC exact match improves clearly over both untouched bases, and NorEval does not drop more than seed noise. Results are published either way.
