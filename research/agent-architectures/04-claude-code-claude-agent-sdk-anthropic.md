# 4. Claude Code / Claude Agent SDK (Anthropic)
- **Underagenter:** hver får sin egen kontekst, sitt eget sett med verktøy og skills, og en grense på antall turer (`maxTurns`). Bare en oppsummering går tilbake til hovedagenten. Kilde: https://code.claude.com/docs/en/agent-sdk/subagents
- **Skills:** SKILL.md-filer på disk. Bare beskrivelsen lastes først, og hele innholdet lastes når skillen trengs («progressive disclosure»). Kilde: https://code.claude.com/docs/en/agent-sdk/skills
- **Hooks:** PreToolUse, PostToolUse, SubagentStart/Stop og PreCompact/PostCompact. De kan blokkere eller endre et verktøykall. Kilde: https://code.claude.com/docs/en/agent-sdk/hooks
- **For oss:** (a) en PreToolUse-hook for computer-use som blokkerer innlogging, betaling og sletting deterministisk i kode, i stedet for å stole på prompten. (b) Underagenter med egen kontekst, slik at 9B-modellen får en ren og kort kontekst per deloppgave.
