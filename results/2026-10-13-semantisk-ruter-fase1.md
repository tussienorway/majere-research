# 2026-10-13: Semantisk ruter, fase 1 («liten hjerne»)

Kode: [majere-core PR #31](https://github.com/tussienorway/majere-core/pull/31), `hermes/router/`.
Plan: [research/plan-semantisk-ruting.md](../research/plan-semantisk-ruting.md).

**Status:** bygget og testet frittstående på CPU. **Ikke koblet inn i Hermes**; ingenting i
eksisterende oppsett er endret. Ruteren utfører aldri noe selv.

**Oppsett:** `intfloat/multilingual-e5-small` (MIT), int8-ONNX, sentencepiece, egen minimal kode
(ingen Aurelio). 8 ruter + `usikker` → 9B. 205 ruteeksempler, 340 merkede norske testytringer
holdt utenfor. Terskler kalibrert 3-fold (1/3 kalibrering, 2/3 test).

| Mål | Krav | Resultat |
|---|---|---|
| Presisjon på det som rutes | > 0.95 | **0.951** ✔ (knapt) |
| Andel som rutes (resten → 9B) | – | 69 % |
| Makro-F1 (8 ruter) | > 0.90 (plan) | **0.81** ✘ |
| Latens p50 / p95 (CPU, 2 tråder) | < 15 ms | **2.3 / 3.0 ms** ✔ |
| RAM | < 200 MB | **~250 MB** ✘ |

Sterkest: `raad` (F1 0.99), `systemstyring` (0.91), `stopp` (0.89, presisjon 0.96).
Svakest: `fakta` og `koding` (lav recall, men presisjon 1.00 – de går trygt til 9B),
`verktoy`/`computer_use` (presisjon 0.89).

**Konklusjon:** Godt nok som hurtigsti for `stopp`, `raad` og `systemstyring`, og som hint til 9B for
resten. Ikke godt nok som eneste beslutningstaker. Neste steg: flere eksempler fra ekte
Hermes-samtaler og vokabular-beskjæring for å komme under 200 MB.
