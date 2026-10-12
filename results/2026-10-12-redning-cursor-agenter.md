# Redning av arbeid fra Cursor-agenter (12.10.2026)

Brukeren ba om at alt arbeid fra Cursor-skyagentene skulle samles i `tussienorway/majere-core`. Det er gjort slik:

| Hva | Fra | PR i majere-core | Tester |
|---|---|---|---|
| Hermes-skill bevist-ai-arkitektur | Origin multi-mind-ai PR #15 | [#26](https://github.com/tussienorway/majere-core/pull/26) | 7 passed |
| Dialograpport per cast (`eval --dialogue-casts`) med de 10 testene | Origin multi-mind-ai PR #16 | [#27](https://github.com/tussienorway/majere-core/pull/27) | multimind 228 passed (var 218) |
| `lab/cua-training` (treningssett for computer-use-VLM) | Origin cua-small-model-training main 04535988 | [#28](https://github.com/tussienorway/majere-core/pull/28) | 32 passed |
| DeskForge-1M-konverterer | Origin cua PR #2 | [#29](https://github.com/tussienorway/majere-core/pull/29) | 37 passed |
| Stage 0-baselines | Origin cua PR #1 | [#30](https://github.com/tussienorway/majere-core/pull/30) | 48 passed, 1 skipped |

Alle er merget. `lab/cua-training` er importert uten git-historikk (Origin krever innlogging for kloning), men alle filene er sjekket mot blob-SHA-ene i Origin.

Origin multi-mind-ai PR #3–#13 er lukket med en kommentar om at koden ligger i majere-core. PR #14 (demo-hello) er urørt.
