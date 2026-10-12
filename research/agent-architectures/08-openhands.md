# 8. OpenHands
- **Arkitektur:** en hendelseslogg der alt lagres og ingenting overskrives (event sourcing), og en agent uten tilstand som leser en «View». ActionEvent og Observation er typede hendelser. Kilde: https://arxiv.org/html/2511.03690v2
- **Condenser:** beholder de første N og siste M hendelsene og oppsummerer midten. Oppsummeringen lagres som en egen hendelse, slik at hele loggen bevares. Ifølge artikkelen opptil 2× lavere kostnad uten tap av ytelse. Kilde: https://docs.openhands.dev/sdk/arch/condenser.md
- **Sikkerhet:** en SecurityAnalyzer vurderer risikoen ved hver handling, og handlingen venter på bekreftelse (WAITING_FOR_CONFIRMATION). Kilde: https://docs.openhands.dev/sdk/arch/agent
- **For oss:** en head+tail-condenser for 9B-kontekst. Selv om vi har 96K, faller kvaliteten på lange kontekster (vurdering). Handlinger merket med risiko, med en pausetilstand.
