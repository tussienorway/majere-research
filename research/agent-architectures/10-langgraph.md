# 10. LangGraph
- **Arkitektur:** en StateGraph med noder og kanter. En checkpointer lagrer tilstanden etter hvert steg, og `interrupt()` brukes for menneskelig godkjenning og for å gjenoppta fra et hvilket som helst sjekkpunkt. Kilde: https://langchain-ai.github.io/langgraph/
- **For oss:** sjekkpunkter etter hvert steg i council_round.py. Da kan en runde fortsette etter at PC-en har vært offline, som har skjedd flere ganger.
