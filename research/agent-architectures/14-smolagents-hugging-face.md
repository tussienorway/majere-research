# 14. smolagents (Hugging Face)
- **Arkitektur:** CodeAgent, der modellen skriver Python-kodeblokker som kaller verktøyene som funksjoner. Kjøringen skjer i en begrenset lokal tolk eller i en sandkasse (E2B/Docker). Ifølge CodeAct-artikkelen gir det færre steg og høyere suksess enn JSON-kall. Kilder: https://github.com/huggingface/smolagents og https://arxiv.org/abs/2402.01030
- **For oss:** test et «code mode»-verktøy for 9B, der flere handlinger skrives i ett Python-skript. Det kan løse problemet med feil argumenter, fordi Python-syntaks er godt trent (vurdering, må måles i evalen).
