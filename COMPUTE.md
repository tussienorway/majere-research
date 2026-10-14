# Majere – gratis compute tracker (oppdatert 2026-10-14, Europe/Oslo)
Kontakt: mail@thomasaustenaa.no (sekundær: thomasaustenaa@gmail.com) · Site: https://majere.thomasaustenaa.no · Uavhengig forsker, Grimstad. Ingen org.

| # | Program | Odds×verdi | Krav | Skjema | Status (2026-10-14) |
|---|---------|-----------|------|--------|--------|
| 1 | Google TPU Research Cloud | Høy | Forskning, publiser resultater, Google-konto | https://sites.research.google/trc/about/ | Interesseskjema sendt 12. okt. Ingen svar ennå. |
| 2 | Hugging Face community GPU grant (Space) | Høy | Offentlig Space, be om grant i Space Settings | https://huggingface.co/spaces/tussienorway/majere-demo/discussions/1 | Forespurt 13. okt via Space-diskusjon. Ingen svar fra HF-ansatte ennå. **Merk:** diskusjonsteksten beskriver fortsatt den gamle Archetype Council / Qwen3.5-9B-demoen med tilhørende tall. En korrigerende oppfølging må postes (ikke gjort ennå). |
| 3 | Lambda Research Grant | Middels | Forskningsprosjekt, kort søknad | https://lambda.ai/research | Sendt 12. okt. Bekreftelse mottatt. Ingen beslutning. |
| 4 | CloudRift AI Grant | Ikke vurdert | Søknad | https://www.cloudrift.ai/ai-grant | Sendt 13. okt. Bekreftelse «Application received». Ingen beslutning. |
| 5 | Yotta Labs research credit | Ikke vurdert | Søknad | https://www.yottalabs.ai/research-credit | Draft ready, awaiting user approval. Utkast ligger lokalt i majere-compute applications (ikke i dette repoet). IKKE sendt. |
| 6 | EuroHPC AI for Science | Middels (krever ofte EU-tilknytning) | Vertsinstitusjon, prosjektbeskrivelse | https://eurohpc-ju.europa.eu/access-our-supercomputers_en | Vertsforespørsel sendt til Per-Arne Andersen (UiA). Frist 30. okt 2026 kl. 10:00 CET. Ikke en full søknad ennå. |
| 7 | Sigma2/NRIS | Lav (krever norsk forskningsinstitusjon/PI) | Institusjon | https://www.sigma2.no/apply-e-infrastructure-resources | Blokkert uten PI ved norsk institusjon. |
| 8 | Modal/RunPod/Together, AWS/Azure/GCP, NVIDIA | Lav / ikke kvalifisert | Skjema eller institusjon | respektive sider | Ikke kvalifisert eller lave odds. Ikke prioritert. |

**Status 2026-10-14:** Ingen grant er innvilget. Venter på svar fra TRC (1), HF (2), Lambda (3, bekreftet) og CloudRift (4, bekreftet). Yotta (5) er ikke sendt. EuroHPC (6) har bare en vertsforespørsel. Sigma2 (7) er blokkert.

**Compute-ønske (offentlig på siden):** ca. 275 H100 GPU-timer for NO-FC / Qwen3-8B (thinking off). Full pilot-SFT og baseline-score for hard-temporal-settet er ikke kjørt ennå (trenger GPU på PC-en).

Mål: trene/destillere modeller i skyen optimalisert for 16 GB forbrukerkort, publisert som GGUF. Hovedsporet er norsk (bokmål/nynorsk) og verktøykall (NO-FC), ikke Archetype Council.
