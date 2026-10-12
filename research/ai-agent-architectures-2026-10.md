# AI-agentarkitekturer – oversikt og hva Hermes kan lære (oktober 2026)

Skrevet 12.10.2026 for Hermes Agent-oppsettet vårt: lokal Qwen3.5-9B i llama.cpp på RTX 5060 Ti 16 GB, Gemini som hovedmodell, multi-mind-rådet og `computer-use`-profilen med agent-browser og cua. Koden ligger i `tussienorway/majere-core`.

Faktaene har kilde. Det som er mitt eget estimat eller min vurdering, er merket **(estimat)** eller **(vurdering)**. Kildene ble sjekket 12.10.2026, men noen produkter endrer seg raskt.

## 1. Liste

| # | Navn | Type | Laget av | Lisens | Det unike |
|---|------|------|----------|--------|-----------|
| 1 | Hermes Agent | Personlig agent som forbedrer seg selv (CLI, gateway, meldingsapper) | Nous Research | MIT, åpen | Lager og retter sine egne «skills» (prosedyreminne), og en bakgrunnsgjennomgang kjører etter hver økt |
| 2 | OpenClaw | Personlig agentplattform som kjører lokalt (gateway-daemon) | OpenClaw-prosjektet | Åpen (MIT) | Én gateway som eier alle meldingskanaler, økter, cron og enhetsnoder. Personlighet og minne ligger i filer i arbeidsområdet (SOUL.md, MEMORY.md) |
| 3 | Vellum | Plattform der du bygger agenter ved å chatte, uten kode | Vellum AI | Lukket plattform med åpen SDK | Beskriv målet, så bygger Vellum agenten som en arbeidsflytgraf, med evalueringer, avspilling av kjøringer og kode du kan eksportere |
| 4 | Claude Code / Claude Agent SDK | Kodeagent og agent-SDK | Anthropic | Proprietær (SDK-en kan brukes fritt) | Underagenter med egen kontekst, SKILL.md-ferdigheter, hooks (PreToolUse/PreCompact) og automatisk komprimering |
| 5 | OpenAI Codex (CLI) / Agents SDK | Kodeagent og agent-SDK | OpenAI | Codex CLI: Apache-2.0. Agents SDK: MIT | Sandkasse på OS-nivå med godkjenningsmoduser. SDK-en har handoffs, guardrails og tracing |
| 6 | ChatGPT Agent (Operator) | Skyagent med egen virtuell nettleser og datamaskin | OpenAI | Proprietær | En modell (CUA) som er trent på skjermbilde → mus/tastatur, og som spør brukeren ved innlogging og kjøp |
| 7 | Manus | Generell autonom skyagent | Manus AI | Proprietær | Hver oppgave får sin egen sky-VM. Bruker filsystemet som minne (todo.md) og legger stor vekt på KV-cache-vennlig kontekst |
| 8 | OpenHands | Åpen agent for programvareutvikling og SDK | All Hands AI / fellesskapet | MIT | Hendelseslogg der alt lagres (event sourcing), en «condenser» som komprimerer historikken, CodeAct og en sikkerhetsanalysator |
| 9 | Goose | Lokal agent for utviklere (CLI og desktop) | Block | Apache-2.0 | Nesten alle verktøy kommer som MCP-«extensions», og «recipes» kan deles |
| 10 | LangGraph | Rammeverk for agenter som tilstandsgrafer | LangChain | MIT | Eksplisitt tilstandsmaskin med sjekkpunkter, menneskelig godkjenning underveis og «time travel» |
| 11 | CrewAI | Rammeverk for flere agenter med roller | CrewAI Inc. | MIT | Agenter med rolle, mål og bakgrunnshistorie som jobber i en «crew», pluss deterministiske «Flows» |
| 12 | AutoGen / AG2 / Microsoft Agent Framework | Rammeverk for samtaler mellom flere agenter | Microsoft og AG2-fellesskapet | MIT | Agenter som snakker sammen i gruppechat med en «speaker selector». Videreført i Microsoft Agent Framework |
| 13 | Letta (MemGPT) | Plattform for agenter med tilstand og minne | Letta | Apache-2.0 | Minneblokker som agenten redigerer selv, pluss «sleep-time»-agenter som rydder minnet i bakgrunnen |
| 14 | smolagents | Minimalt agentbibliotek | Hugging Face | Apache-2.0 | CodeAgent: modellen skriver Python i stedet for JSON-verktøykall |
| 15 | Agent Zero | Personlig, generell agent i Docker | Agent Zero-fellesskapet | MIT | Svært lite hardkodet. Agenten bruker terminalen som verktøy og lager underordnede agenter selv |
| 16 | Open Interpreter | Lokal kodekjørende assistent | Open Interpreter | AGPL-3.0 | Kjører kode lokalt (Python/shell/JS) i en REPL-løkke, og har en OS-modus for skjermstyring |
| 17 | Desktop Commander MCP | MCP-server for terminal og filer | wonderwhy-er (Eduard Ruzga) | MIT | Interaktive prosesser som kjører lenge, utdata delt i sider, kirurgisk «edit_block» og revisjonslogg |
| 18 | browser-use | Bibliotek for nettleseragenter | Browser Use | MIT | Rå CDP. DOM, tilgjengelighetstre og layout slås sammen til en indeksert liste over elementer som kan klikkes |
| 19 | UI-TARS Desktop / Agent TARS | GUI-agent for desktop og nettleser | ByteDance | Apache-2.0 | Bruker en egen GUI-modell (UI-TARS) som gir koordinater rett fra skjermbildet |
| 20 | Cline / Roo Code | Kodeagenter i VS Code | Cline / Roo-fellesskapet | Apache-2.0 | Plan- og Act-modus, godkjenning per handling og sjekkpunkter (git-snapshot) per steg |
| 21 | Aider | Kodeagent for parprogrammering i terminalen | Paul Gauthier | Apache-2.0 | «Repo map» bygget med tree-sitter og PageRank, redigering i diff-format og automatisk git-commit |
| 22 | n8n (AI Agent-node) | Arbeidsflytautomatisering med agentnoder | n8n GmbH | Fair-code («Sustainable Use License») | En agent er én node i en deterministisk arbeidsflyt med over 400 integrasjoner |

## 2. Hvordan hver enkelt gjør det, og hva vi kan kopiere

### 1. Hermes Agent (Nous Research)
- **Løkka:** en vanlig verktøykall-løkke i `run_agent.py` med verktøysett som kan slås av og på per profil. Kilde: https://github.com/NousResearch/hermes-agent
- **Minne:** `MemoryManager` med en innebygd leverandør (MEMORY.md/USER.md) og maks én ekstern (Honcho, Mem0 osv.), for å unngå at verktøyskjemaene sveller. Kilde: `agent/memory_manager.py` og `agent/memory_provider.py` i repoet.
- **Ferdigheter:** `skill_manage` (create/patch/edit/delete). Agenten oppretter en skill etter vanskelige oppgaver med 5 eller flere kall. Med `write_approval` legges skrivingen i `~/.hermes/pending/skills/` til godkjenning. Kilde: https://hermes-agent.nousresearch.com/docs/user-guide/features/skills
- **Selvforbedring:** etter svaret starter en bakgrunnstråd med bare minne- og skill-verktøy og maks 5 iterasjoner. Den startes hver 10. brukertur, eller etter 10 eller flere verktøyiterasjoner. Kilde: commit 45058b4 (#2235).
- **For oss (vurdering):** vi bruker dette allerede. Neste steg er å skru på `write_approval` for skills som computer-use-profilen skriver, og la gjennomgangen kjøre på Gemini, ikke på 9B-modellen.

### 2. OpenClaw
- **Gateway:** én langlivet daemon (WS på 127.0.0.1:18789) som eier WhatsApp, Telegram, Slack, Discord og andre kanaler. Den bruker typede JSON-rammer og idempotensnøkler på handlinger med sideeffekter. Kilde: https://docs.openclaw.ai/architecture
- **Løkka:** kjøringene settes i kø per økt, og eventuelt i en global kø. Hver kjøring gjør dette: inntak, kontekst, modell, verktøy, strømming og lagring. Kanalene velger kømodus (steer/followup/collect/interrupt). Kilde: https://docs.openclaw.ai/concepts/agent-loop
- **Kjøremotorer:** den innebygde motoren kan byttes ut per modell (Codex, Copilot, claude-cli). Kilde: https://docs2.openclaw.ai/concepts/agent-runtimes
- **Kontekst og minne:** filene AGENTS.md, SOUL.md, IDENTITY.md, USER.md og MEMORY.md legges inn i systemprompten. Økter lagres i SQLite med komprimering. Kilde: https://docs.openclaw.ai/concepts/agent
- **Enhetsnoder:** telefoner og Mac kobler seg til som `role: node` og gir tilgang til kamera, skjermopptak osv. etter paring.
- **For oss:** (a) kømodus «steer/interrupt» i Hermes-gatewayen, slik at en ny Telegram-melding midt i en kjøring styrer kjøringen i stedet for å starte en ny parallelt. (b) En egen kjøremotor per modell, med 9B på llama.cpp for council og Gemini for hovedagenten, styrt av konfigurasjonen.

### 3. Vellum
- **Slik fungerer det:** du chatter med en «Agent Builder» som stiller oppfølgingsspørsmål, bekrefter en plan og genererer en arbeidsflyt med noder og integrasjoner. Arbeidsflyten kan eksporteres som kode via deres åpne SDK. Kilde: https://www.vellum.ai/blog/introducing-vellum-for-agents
- **Kvalitet:** kjøringstabeller, en replay-scrubber for å bla gjennom agentløkker steg for steg, et «Actuals»-API for fasit og online-evalueringer på hver kjøring. Kilde: https://docs.vellum.ai/product/deployments/observability.mdx
- **Mocking:** den bygger med falske data for integrasjoner, slik at testing ikke skriver til ekte systemer. Kilde: changelog januar 2026.
- **For oss:** en replay-visning av Hermes-økter (JSON-logg til HTML-tidslinje) og mock-modus for verktøy under eval. Begge passer godt sammen med eval-planen vår.

### 4. Claude Code / Claude Agent SDK (Anthropic)
- **Underagenter:** hver får sin egen kontekst, sitt eget sett med verktøy og skills, og en grense på antall turer (`maxTurns`). Bare en oppsummering går tilbake til hovedagenten. Kilde: https://code.claude.com/docs/en/agent-sdk/subagents
- **Skills:** SKILL.md-filer på disk. Bare beskrivelsen lastes først, og hele innholdet lastes når skillen trengs («progressive disclosure»). Kilde: https://code.claude.com/docs/en/agent-sdk/skills
- **Hooks:** PreToolUse, PostToolUse, SubagentStart/Stop og PreCompact/PostCompact. De kan blokkere eller endre et verktøykall. Kilde: https://code.claude.com/docs/en/agent-sdk/hooks
- **For oss:** (a) en PreToolUse-hook for computer-use som blokkerer innlogging, betaling og sletting deterministisk i kode, i stedet for å stole på prompten. (b) Underagenter med egen kontekst, slik at 9B-modellen får en ren og kort kontekst per deloppgave.

### 5. OpenAI Codex CLI / Agents SDK
- **Codex CLI:** sandkasse på OS-nivå (Seatbelt på macOS, Landlock/seccomp på Linux) og godkjenningsmoduser (read-only, auto, full-access). Instruksjonene står i AGENTS.md. Kilde: https://github.com/openai/codex
- **Agents SDK:** Agent, Handoff, Guardrail (inn/ut, kjører parallelt) og innebygd tracing. Kilde: https://openai.github.io/openai-agents-python/
- **For oss:** guardrails som kjører parallelt med en billig modell og kan avbryte. For eksempel kan 9B sjekke om Gemini-planen inneholder risikable handlinger. Godkjenningsnivåer per profil.

### 6. ChatGPT Agent (Operator/CUA)
- **Slik fungerer det:** CUA-modellen er trent med forsterkningslæring på skjermbilde → handling (klikk på x,y, skriving, scrolling) i en virtuell maskin. Den kombineres med en tekstnettleser og terminal. Ved innlogging, CAPTCHA og kjøp gir den kontrollen tilbake til brukeren («takeover»). Kilder: https://openai.com/index/computer-using-agent/ og https://openai.com/index/introducing-chatgpt-agent/
- **For oss:** en eksplisitt «takeover»-tilstand i computer-use-profilen, der agenten pauser og sender en Telegram-melding med skjermbilde. Vi bør også velge mellom DOM-verktøy og pikselklikk etter hvilken oppgave det er (vurdering). Hele den lukkede CUA-modellen kan vi ikke kopiere.

### 7. Manus
- **Kontekstteknikk (fra deres egen blogg):** stabile prefiks i prompten for å få treff i KV-cachen. Verktøy maskeres med logits i stedet for å fjernes fra konteksten. Filsystemet brukes som ekstern hukommelse. En `todo.md` skrives om hele tiden for å holde målet «sist i konteksten». Feil beholdes i konteksten slik at modellen lærer av dem. Kilde: https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus
- **Kjøremiljø:** en sky-VM per oppgave.
- **For oss:** svært relevant for llama.cpp. Med stabile systemprompter og verktøylister kan llama-server gjenbruke prompt-cachen (`cache_prompt`). Det gir raskere steg for 9B (estimat: betydelig). Todo-fil-mønsteret passer for lange computer-use-oppgaver. Det kan også fikse Notisblokk-feilen der agenten ikke stoppet.

### 8. OpenHands
- **Arkitektur:** en hendelseslogg der alt lagres og ingenting overskrives (event sourcing), og en agent uten tilstand som leser en «View». ActionEvent og Observation er typede hendelser. Kilde: https://arxiv.org/html/2511.03690v2
- **Condenser:** beholder de første N og siste M hendelsene og oppsummerer midten. Oppsummeringen lagres som en egen hendelse, slik at hele loggen bevares. Ifølge artikkelen opptil 2× lavere kostnad uten tap av ytelse. Kilde: https://docs.openhands.dev/sdk/arch/condenser.md
- **Sikkerhet:** en SecurityAnalyzer vurderer risikoen ved hver handling, og handlingen venter på bekreftelse (WAITING_FOR_CONFIRMATION). Kilde: https://docs.openhands.dev/sdk/arch/agent
- **For oss:** en head+tail-condenser for 9B-kontekst. Selv om vi har 96K, faller kvaliteten på lange kontekster (vurdering). Handlinger merket med risiko, med en pausetilstand.

### 9. Goose (Block)
- **Arkitektur:** en Rust-kjerne der alle verktøy er MCP-extensions. «Recipes» er YAML-filer med prompt, extensions og parametere som kan deles og kjøres i CI. Kilde: https://github.com/block/goose og https://block.github.io/goose/
- **For oss:** «recipes» for faste rutiner (som den daglige multi-mind-runden) som versjonerte YAML-filer i majere-core.

### 10. LangGraph
- **Arkitektur:** en StateGraph med noder og kanter. En checkpointer lagrer tilstanden etter hvert steg, og `interrupt()` brukes for menneskelig godkjenning og for å gjenoppta fra et hvilket som helst sjekkpunkt. Kilde: https://langchain-ai.github.io/langgraph/
- **For oss:** sjekkpunkter etter hvert steg i council_round.py. Da kan en runde fortsette etter at PC-en har vært offline, som har skjedd flere ganger.

### 11. CrewAI
- **Arkitektur:** Agent (rolle, mål, bakgrunnshistorie), Task og Crew (sekvensiell eller hierarkisk med en manager). «Flows» gir en hendelsesdrevet, deterministisk ramme rundt agentene. Kilde: https://docs.crewai.com/
- **For oss:** rådsprofilene ligner allerede. Vi kan legge til en hierarkisk «manager»-modus, der Gemini fordeler oppgaver og 9B-stemmene utfører.

### 12. AutoGen / AG2 / Microsoft Agent Framework
- **Arkitektur:** asynkron meldingsutveksling mellom agenter. GroupChat med en speaker selector, som kan være en LLM eller regelbasert. Microsoft har slått AutoGen og Semantic Kernel sammen til Microsoft Agent Framework, mens AG2 er en videreføring drevet av fellesskapet. Kilder: https://github.com/microsoft/autogen, https://github.com/microsoft/agent-framework og https://github.com/ag2ai/ag2
- **For oss:** speaker selection i rådet. I stedet for at alle stemmene alltid snakker, velges den neste som er mest relevant. Det sparer VRAM-tid på én GPU.

### 13. Letta (MemGPT)
- **Arkitektur:** «core memory»-blokker (persona, human osv.) i konteksten, som agenten redigerer selv med verktøy. Arkiv- og recall-minne ligger utenfor konteksten. Sleep-time-agenter konsoliderer minnet i bakgrunnen (for eksempel `sleeptime_agent_frequency=5`). I 2026 går Letta over til subagenter på klientsiden og git-basert «MemFS». Kilder: https://www.letta.com/blog/sleep-time-compute/ og https://docs.letta.com/configuration/memory/
- **For oss:** git-versjonert minne. Hermes sine MEMORY- og skills-mapper kan ligge i et privat git-repo med en commit per endring, slik at alt kan spores og rulles tilbake. Sleep-time kan kjøre om natten på 9B når GPU-en er ledig.

### 14. smolagents (Hugging Face)
- **Arkitektur:** CodeAgent, der modellen skriver Python-kodeblokker som kaller verktøyene som funksjoner. Kjøringen skjer i en begrenset lokal tolk eller i en sandkasse (E2B/Docker). Ifølge CodeAct-artikkelen gir det færre steg og høyere suksess enn JSON-kall. Kilder: https://github.com/huggingface/smolagents og https://arxiv.org/abs/2402.01030
- **For oss:** test et «code mode»-verktøy for 9B, der flere handlinger skrives i ett Python-skript. Det kan løse problemet med feil argumenter, fordi Python-syntaks er godt trent (vurdering, må måles i evalen).

### 15. Agent Zero
- **Arkitektur:** svært lite er hardkodet. Promptene ligger i mapper og kan overstyres. Agenten bruker terminal og kode som hovedverktøy og kan opprette underordnede agenter («subordinates») i et hierarki. Den kjører i Docker. Kilde: https://github.com/agent0ai/agent-zero
- **For oss:** prompter som filer per profil, noe Hermes langt på vei har allerede. Ingen ny stor idé.

### 16. Open Interpreter
- **Arkitektur:** en LLM-løkke som skriver kode, kjører den lokalt med brukerens godkjenning og leser resultatet. OS-modus bruker skjermbilder og mus. Kilde: https://github.com/openinterpreter/open-interpreter
- **For oss:** godkjenning per kodeblokk. Vi har allerede tilsvarende.

### 17. Desktop Commander MCP
- **Arkitektur:** en MCP-server med 26 verktøy, blant annet `start_process`, `interact_with_process` og `read_process_output` (med sider). Den har `edit_block` med diff-tilbakemelding på tegnnivå, revisjonslogg for alle kall (rotasjon ved 10 MB), blokkliste for kommandoer og valgfri Docker-isolasjon. Kilde: https://github.com/wonderwhy-er/DesktopCommanderMCP
- **For oss:** dette er «remote desktop commander» som brukeren nevnte. Den kan kobles rett inn i Hermes som MCP-server, fordi den er gratis og MIT-lisensiert. Alternativt kan vi kopiere mønsteret med utdata delt i sider og interaktive prosesser.

### 18. browser-use
- **Arkitektur:** styrer Chrome via rå CDP, fordi de har gått bort fra Playwright. DomService henter DOM, tilgjengelighetstre, snapshot og layout parallelt. Den bygger noder med synlighet, rekkefølge for tegning og registrerte JS-lyttere, og gir modellen en nummerert liste over elementer som kan brukes. Den kan også bruke skjermbilder. Kilder: https://github.com/browser-use/browser-use og https://browser-use.com/posts/playwright-to-cdp
- **For oss:** agent-browser bruker allerede referanser fra tilgjengelighetstreet. Vi kan legge til filtrering etter synlighet og rekkefølge for tegning, slik at 9B-modellen får en kortere liste.

### 19. UI-TARS Desktop / Agent TARS (ByteDance)
- **Arkitektur:** UI-TARS-modellen tar inn et skjermbilde og gir ut en tanke og en handling med koordinater. Desktop-appen utfører handlingen lokalt eller eksternt. Agent TARS er CLI og web-UI med MCP-verktøy. Kilder: https://github.com/bytedance/UI-TARS-desktop og https://arxiv.org/abs/2501.12326
- **For oss:** bekrefter retningen med en egen modell for å finne klikkpunkter (UI-TARS-1.5-7B eller Holo2-4B) ved siden av 9B-modellen. Dette står allerede i modellrapporten.

### 20. Cline / Roo Code
- **Arkitektur:** Plan-modus (bare lesing) og Act-modus. Brukeren godkjenner hver fil- og terminalhandling. Sjekkpunkter tas som skygge-git-snapshots etter hvert steg, slik at man kan rulle tilbake. Roo har egne moduser og «Boomerang»-orkestrering. Kilder: https://github.com/cline/cline og https://github.com/RooCodeInc/Roo-Code
- **For oss:** Plan- og Act-moduser for computer-use. 9B lager først en plan som Gemini eller brukeren godkjenner, og så kjører den uten å improvisere (vurdering: dette reduserer «fortsetter etter at målet er nådd»).

### 21. Aider
- **Arkitektur:** et «repo map» der tree-sitter henter ut symboler, rangert med PageRank på avhengighetsgrafen og tilpasset et tokenbudsjett. Redigering skjer i formatene diff, whole og udiff, valgt per modell, og hver endring commites automatisk. Kilder: https://aider.chat/docs/repomap.html og https://aider.chat/docs/more/edit-formats.html
- **For oss:** redigeringsformat valgt per modell, der svake modeller skriver hele filen eller en enkel diff. Repo map er nyttig hvis Hermes skal kode i majere-core.

### 22. n8n AI Agent-node
- **Arkitektur:** en agent (via LangChain) er én node i en visuell, deterministisk arbeidsflyt. Verktøy er andre noder eller underflyter, og minnet kan kobles til (Postgres, Redis). Kilde: https://docs.n8n.io/advanced-ai/
- **For oss:** lite nytt. Hermes-cron dekker det meste.

## 3. Prioriterte ideer for Hermes

| Prio | Idé | Inspirert av | Hvorfor | Innsats (estimat) |
|---|---|---|---|---|
| 1 | Hard sikkerhets-hook før verktøykall (blokkerer innlogging, betaling, sletting og passord i kode) + «takeover»-pause med skjermbilde til Telegram | Claude SDK hooks, OpenHands SecurityAnalyzer, ChatGPT Agent | Sikkerhet som ikke avhenger av at 9B følger prompten | 1–2 dager |
| 2 | Stabil prompt og verktøyliste + `cache_prompt` i llama-server, todo.md-fil for lange oppgaver | Manus | Raskere steg, og agenten holder målet og stopper når den er ferdig | 1 dag |
| 3 | Plan → godkjenning → Act-modus i computer-use | Cline/Roo, Codex | Mindre improvisering og færre ekstra handlinger | 1–2 dager |
| 4 | Head+tail-condenser lagret som hendelse | OpenHands | Lange økter på 9B uten at kvaliteten faller | 2 dager |
| 5 | Koble inn Desktop Commander MCP (terminal, interaktive prosesser, utdata i sider) | Desktop Commander | Gir det brukeren ba om, gratis og MIT-lisensiert | 0,5 dag |
| 6 | «Code mode»-verktøy (Python-skript med verktøy som funksjoner) testet i evalen mot JSON-kall | smolagents/CodeAct | Kan løse feil i argumentene til 9B | 2–3 dager inkludert eval |
| 7 | Egen modell for klikkpunkter ved siden av 9B (UI-TARS-1.5-7B / Holo2-4B) | UI-TARS, browser-use | Bedre klikkpresisjon på skrivebordet | 3–5 dager |
| 8 | Sjekkpunkter i council_round.py og i lange kjøringer | LangGraph | Kan fortsette etter at PC-en har vært offline | 1 dag |
| 9 | Git-versjonert minne og skills + nattlig «sleep-time»-opprydding på 9B | Letta, Hermes background review | Sporbarhet, tilbakerulling og bedre minne | 1–2 dager |
| 10 | Replay-tidslinje (HTML) for økter + mock-modus for verktøy i eval | Vellum | Enklere feilsøking og trygg testing | 2 dager |

## 4. Hull og forbehold
- Lisensene for OpenClaw og Agent Zero er oppgitt fra repoene slik jeg kjenner dem. Sjekk LICENSE-filen før vi kopierer kode.
- Manus og ChatGPT Agent er lukkede. Det som står om dem, bygger på deres egne blogginnlegg.
- Ingen av ideene er testet i vårt oppsett ennå. Effekten må måles med eval-planen ([`results/2026-10-12-hermes-local-model-eval.md`](../results/2026-10-12-hermes-local-model-eval.md)).
