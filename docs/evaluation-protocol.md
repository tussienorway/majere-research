# Evaluation protocol
- **NO-FC** (majere-nofc): exact_match, call_name_acc, call_arg_acc, no_call_acc and clarify_acc, reported for all tasks, Bokmål and Nynorsk.
  - Fixed reference time for all tasks.
  - temperature 0.
  - OpenAI-compatible endpoint with native tool calling.
  - Models without native tool support get a separate prompt-based mode, reported separately.
- **NorEval** and **EuroEval:** general Norwegian ability.
- **BFCL:** English tool calling, to check that nothing regresses.
- **Reporting:** every run publishes model, quantisation, hardware, date, raw answers and summary. 40 tasks (v0) is a development set. Final claims require NO-FC v1 (≥500 tasks, human-checked test split) and several seeds.
