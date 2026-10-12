# 1. Hermes Agent (Nous Research)
- **Løkka:** en vanlig verktøykall-løkke i `run_agent.py` med verktøysett som kan slås av og på per profil. Kilde: https://github.com/NousResearch/hermes-agent
- **Minne:** `MemoryManager` med en innebygd leverandør (MEMORY.md/USER.md) og maks én ekstern (Honcho, Mem0 osv.), for å unngå at verktøyskjemaene sveller. Kilde: `agent/memory_manager.py` og `agent/memory_provider.py` i repoet.
- **Ferdigheter:** `skill_manage` (create/patch/edit/delete). Agenten oppretter en skill etter vanskelige oppgaver med 5 eller flere kall. Med `write_approval` legges skrivingen i `~/.hermes/pending/skills/` til godkjenning. Kilde: https://hermes-agent.nousresearch.com/docs/user-guide/features/skills
- **Selvforbedring:** etter svaret starter en bakgrunnstråd med bare minne- og skill-verktøy og maks 5 iterasjoner. Den startes hver 10. brukertur, eller etter 10 eller flere verktøyiterasjoner. Kilde: commit 45058b4 (#2235).
- **For oss (vurdering):** vi bruker dette allerede. Neste steg er å skru på `write_approval` for skills som computer-use-profilen skriver, og la gjennomgangen kjøre på Gemini, ikke på 9B-modellen.
