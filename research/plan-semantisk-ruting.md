# Plan: lokal, distribuert AI-assistent med semantisk rutingsarkitektur

*Brukerens forsknings- og testplan (2026-10-13), sammendrag. Originalteksten kom inn via chat og ble
avkortet i overføringen (~8 000 tegn manglet på midten), så dette er et strukturert sammendrag av
det som var tilgjengelig – ikke en ordrett kopi.*

## Kjerneidé
Ikke send alt til én stor modell. Bygg en hybrid orkestreringsplattform: en ultrarask «liten hjerne»
klassifiserer intensjon og ruter, og bare det som krever resonnering går til en generativ modell.
Beslutningstaking frikobles fra tung tekstgenerering.

## Rutingslaget («liten hjerne»)
- **Vektorbasert semantisk ruting** (f.eks. Aurelio semantic-router): embedding + cosinus mot
  eksempelytringer, ingen LLM, < 10 ms på CPU. Til verktøyvalg, avbrudd og kortsvar.
- **Klassifiseringsbasert ruting** (f.eks. RouteLLM: matrisefaktorisering / finjustert BERT):
  avgjør om en liten modell holder eller om en stor trengs.
- **Flersignals infrastrukturruting** (f.eks. vLLM Semantic Router): proxy-nivå, domene,
  nøkkelord, sikkerhetsregler; ruter til modeller eller LoRA-adaptere i vLLM.

## Orkestrering
- Primærlaget skal være deterministisk og rutingsbasert.
- **Mixture-of-Agents (MoA)** mangedobler minne og latens → bare som sekundær eskalering ved høy
  kompleksitet.

## Øvrige komponenter i planen
- Inferens: **vLLM med Multi-LoRA og PagedAttention** (flere spesialiserte adaptere på én base).
- Verktøy: **Model Context Protocol (MCP)** over stdio; skjemavalidering av verktøykall.
- Tale: **Parakeet** (ASR) og **Kokoro-82M** (TTS), RTF < 0.2 GPU / < 0.5 CPU, < 250 ms til første lyd.
- Sikkerhet: trusselmodell for indirekte prompt-injeksjon og «confused deputy»; MCP-tjenere uten
  admin-rettigheter, katalogbegrensninger, interaktiv godkjenning av kritiske skriveoperasjoner.
- Ressurser: preemption/KV-cache-swapping i vLLM; lydstrømming prioriteres over bakgrunnsjobber.
- **4 faser**, med start i rutingslaget + MCP-kjernetjenester før Multi-LoRA-motoren.

## Testprotokoll (akseptkriterier)
| Domene | Metrikk | Mål | Minimum |
|---|---|---|---|
| Semantisk ruting | beslutningslatens | < 10 ms | < 20 ms |
| Semantisk ruting | F1 | > 0.96 | > 0.90 |
| vLLM | TTFT | < 80 ms | < 150 ms |
| Kokoro TTS | TTFB | < 50 ms GPU | < 150 ms CPU |
| TTS | UTMOS/MOS | > 4.3 | > 4.0 |
| MCP | gyldig JSON-skjema | 100 % | > 98 % |
| System | maks VRAM | < 12 GB | < 16 GB |

Oppdragets presiseringer for rutingen: presisjon > 0.95, < 15 ms.

## Hva vi faktisk gjør
- **Kun fase 1 (semantisk ruter) implementeres**, frittstående i
  [majere-core `hermes/router/`](https://github.com/tussienorway/majere-core/tree/main/hermes/router).
- Vi **beholder llama.cpp** (`llama-server`, 9B på :8080). vLLM, Multi-LoRA, flere modeller samtidig,
  Parakeet/Kokoro (engelskspråklige) tas ikke inn nå – det ville krevd ombygging og konkurrert om GPU.
- Resultater: [results/2026-10-13-semantisk-ruter-fase1.md](../results/2026-10-13-semantisk-ruter-fase1.md).
