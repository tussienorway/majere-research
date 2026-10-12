# 5. OpenAI Codex CLI / Agents SDK
- **Codex CLI:** sandkasse på OS-nivå (Seatbelt på macOS, Landlock/seccomp på Linux) og godkjenningsmoduser (read-only, auto, full-access). Instruksjonene står i AGENTS.md. Kilde: https://github.com/openai/codex
- **Agents SDK:** Agent, Handoff, Guardrail (inn/ut, kjører parallelt) og innebygd tracing. Kilde: https://openai.github.io/openai-agents-python/
- **For oss:** guardrails som kjører parallelt med en billig modell og kan avbryte. For eksempel kan 9B sjekke om Gemini-planen inneholder risikable handlinger. Godkjenningsnivåer per profil.
