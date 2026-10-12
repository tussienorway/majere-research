# 2. OpenClaw
- **Gateway:** én langlivet daemon (WS på 127.0.0.1:18789) som eier WhatsApp, Telegram, Slack, Discord og andre kanaler. Den bruker typede JSON-rammer og idempotensnøkler på handlinger med sideeffekter. Kilde: https://docs.openclaw.ai/architecture
- **Løkka:** kjøringene settes i kø per økt, og eventuelt i en global kø. Hver kjøring gjør dette: inntak, kontekst, modell, verktøy, strømming og lagring. Kanalene velger kømodus (steer/followup/collect/interrupt). Kilde: https://docs.openclaw.ai/concepts/agent-loop
- **Kjøremotorer:** den innebygde motoren kan byttes ut per modell (Codex, Copilot, claude-cli). Kilde: https://docs2.openclaw.ai/concepts/agent-runtimes
- **Kontekst og minne:** filene AGENTS.md, SOUL.md, IDENTITY.md, USER.md og MEMORY.md legges inn i systemprompten. Økter lagres i SQLite med komprimering. Kilde: https://docs.openclaw.ai/concepts/agent
- **Enhetsnoder:** telefoner og Mac kobler seg til som `role: node` og gir tilgang til kamera, skjermopptak osv. etter paring.
- **For oss:** (a) kømodus «steer/interrupt» i Hermes-gatewayen, slik at en ny Telegram-melding midt i en kjøring styrer kjøringen i stedet for å starte en ny parallelt. (b) En egen kjøremotor per modell, med 9B på llama.cpp for council og Gemini for hovedagenten, styrt av konfigurasjonen.
