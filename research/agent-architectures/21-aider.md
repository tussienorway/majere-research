# 21. Aider
- **Arkitektur:** et «repo map» der tree-sitter henter ut symboler, rangert med PageRank på avhengighetsgrafen og tilpasset et tokenbudsjett. Redigering skjer i formatene diff, whole og udiff, valgt per modell, og hver endring commites automatisk. Kilder: https://aider.chat/docs/repomap.html og https://aider.chat/docs/more/edit-formats.html
- **For oss:** redigeringsformat valgt per modell, der svake modeller skriver hele filen eller en enkel diff. Repo map er nyttig hvis Hermes skal kode i majere-core.
