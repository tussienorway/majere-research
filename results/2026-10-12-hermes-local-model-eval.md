# 2026-10-12: Lokal modell som hjerne i Hermes (evaluering, runde 1)

**Status:** pågår. PC-en gikk offline kl. 23:07 (norsk tid).

## Mål
Finne en lokal modell som kan være hjernen i Hermes Agent på et RTX 5060 Ti 16 GB (llama.cpp). Modellen skal:
- snakke godt norsk bokmål
- gjøre verktøykall med riktige argumenter
- bruke datamaskinen (nettleser og skrivebord)

## Runde 1: finjustering av Qwen3.5-4B
- 16-bit LoRA (Unsloth), 1 epoke, 883 steg.
- Data: 6 000 eksempler fra NbAiLab/norwegian-alpaca og 1 823 fra hermes-function-calling-v1.
- Loss: 1,27 → ~1,05.

## Resultater
| Modell | Norsk | Likhet | Riktig verktøy | Eksakte argumenter | Benchmark |
|---|---|---|---|---|---|
| Qwen3.5-9B (baseline) | 98,3 % | 37,4 | 81,7 % | 70,0 % | 15/16 (2 kjøringer) |
| Qwen3.5-4B + LoRA | 90,0 % (5 dansk/svensk, 1 engelsk) | 41,5 | 63,3 % | 53,3 % | 8/8 |

**Konklusjon:** 4B-modellen tas ikke i bruk. Den er for svak på norsk og på verktøyargumenter.

## Kandidater
- Gemma 4 26B-A4B UD-Q3_K_XL: lastet ned, ikke testet.
- Hermes-4-14B Q4_K_M: lastes ned.
- willhar/Qwen3.5-9B-AgentTuned: hoppet over, fordi den bare finnes i F16 og mangler lisens.

## Byttekriterium
En ny modell tas bare i bruk hvis den oppfyller alle tre:
- minst 95 % norsk
- minst 70 % eksakte argumenter
- ikke dårligere enn baseline på benchmarken

## Evalueringsplan
Se [majere-core PR #25](https://github.com/tussienorway/majere-core/pull/25) og [planfilen](plans/2026-10-12-hermes-model-eval-plan.md). Kort oppsummert:
- **Kategorier:** norsk, Hermes-verktøykall, BFCL-utvalg, flerstegsflyt, computer use, klikkpresisjon, rådet, lang kontekst (needle 8K–88K), hastighet/VRAM og EuroEval norsk.
- **Gjentak:** 3 kjøringer per oppgave, med rapportering av pass^k.
- **Statistikk:** parvis sammenligning (Wilson-konfidensintervall, McNemar, bootstrap). Med 120 oppgaver er usikkerheten rundt ±8 poeng.
- **Vurdering:** programmatisk der det går. Der en LLM-dommer trengs, brukes en dommer fra en annen modellfamilie, med byttet rekkefølge og flere gjentak.

## Hastighet for baseline (9B, 96K kontekst)
- Lesing: ~1 840–2 015 tok/s.
- Generering: 35–46 tok/s.
- VRAM: 11,5 GB.

## Runde 2
Datasettet er bygget (12 409 eksempler). Runden er satt på pause til kandidatmodellene er testet.
