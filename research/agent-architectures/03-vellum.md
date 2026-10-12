# 3. Vellum
- **Slik fungerer det:** du chatter med en «Agent Builder» som stiller oppfølgingsspørsmål, bekrefter en plan og genererer en arbeidsflyt med noder og integrasjoner. Arbeidsflyten kan eksporteres som kode via deres åpne SDK. Kilde: https://www.vellum.ai/blog/introducing-vellum-for-agents
- **Kvalitet:** kjøringstabeller, en replay-scrubber for å bla gjennom agentløkker steg for steg, et «Actuals»-API for fasit og online-evalueringer på hver kjøring. Kilde: https://docs.vellum.ai/product/deployments/observability.mdx
- **Mocking:** den bygger med falske data for integrasjoner, slik at testing ikke skriver til ekte systemer. Kilde: changelog januar 2026.
- **For oss:** en replay-visning av Hermes-økter (JSON-logg til HTML-tidslinje) og mock-modus for verktøy under eval. Begge passer godt sammen med eval-planen vår.
