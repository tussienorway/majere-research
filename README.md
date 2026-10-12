# Majere Research

Open research side of **Majere: Multi-Persona Deliberation ("Archetype Council") as an Architecture for Affect-Modulated, Self-Monitoring Language Agents**.

Project site: https://majere.austenaa.no · Contact: thomas@austenaa.no

## Summary
Majere is an agent architecture in which several "archetype" personas deliberate before the agent acts. The council maintains an internal affect state (valence/arousal) and a tunable impulsivity parameter. We test it against baselines that get the same token budget, and we publish every result, including negative ones.

## Research questions (falsifiable)
1. **RQ1 – Affect modulation:** Does a council-updated affect state produce more consistent and context-appropriate behaviour than a prompted single persona?
2. **RQ2 – Impulsivity vs. deliberation:** Does a tunable impulsivity parameter give a measurable speed–quality trade-off curve?
3. **RQ3 – Self-monitoring:** Does the council improve calibration (lower ECE, more precise abstention) and reduce self-contradictions compared with a single model and with self-consistency?
4. **RQ4 – Consciousness indicators:** Which functional indicators from the literature (global-workspace-like broadcast, a self-model, reports of internal state) are present, and do they survive ablations?

**Framing:** RQ4 measures *functional indicators of architectural properties* only. We make **no claim** that the system is conscious or has feelings.

**Falsification:** The core hypothesis is rejected if the council does not beat an equal-token-budget baseline (self-consistency or multi-agent debate).

## Layout
- `docs/research-plan.md`: questions, hypotheses, method
- `docs/evaluation-protocol.md`: baselines, metrics, falsification criteria
- `pilot/`: planned pilot (not yet run)
- `results/`: results will be published here (none yet)

The core agent implementation is private for now. This repository holds the open protocol, the evaluation code and the results.

## Licence
Code: MIT (see `LICENSE`). Documentation and results: CC BY 4.0.

## Cite this
```bibtex
@misc{majere2026,
  title  = {Majere: Multi-Persona Deliberation as an Architecture for Affect-Modulated, Self-Monitoring Language Agents},
  author = {Thomas},
  year   = {2026},
  howpublished = {\url{https://github.com/tussienorway/majere-research}},
  note   = {Research protocol; results pending}
}
```
See also `CITATION.cff`. Project site: https://tussienorway.github.io/majere-site/ (will move to majere.austenaa.no).
