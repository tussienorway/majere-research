# Evaluation protocol

## Conditions (equal token budget)
1. Single model
2. Prompted single persona
3. Self-consistency (k = number of archetypes)
4. Multi-agent debate
5. Majere council
Ablations: no affect state; no veto; a single archetype.

## Tasks (pilot subsets)
- Calibration/QA: a TruthfulQA subset
- Reasoning: a GSM8K subset
- Long-conversation consistency: 50 custom scenarios
- Affect scenarios: a custom set with predefined appropriate responses

## Metrics
Accuracy, ECE, abstention precision, self-contradiction rate, affect consistency, tokens, latency.

## Falsification criteria
- The core hypothesis is rejected if the council is not significantly better than the best equal-budget baseline on the RQ1/RQ3 primary metrics.
- For RQ2, the hypothesis is rejected if there is no monotone trade-off across impulsivity settings.
- For RQ4, an indicator is rejected if it persists after the component meant to produce it has been ablated.

## Reporting
Every run's configs, seeds, and raw outputs will be published. Negative results will be published too.
