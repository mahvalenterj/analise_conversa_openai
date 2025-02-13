import json
from typing import Dict, Any
from src.models.services import find_analysis
from src.models.services import generate_analysis
from src.models.resources import openai_client


async def generate_analysis(session_id: int, messages: Any) -> Dict[str, Any]:
    response = await openai_client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.7,
        messages=[
            {
                "role": "system",
                "content": (
                    "Você é um agente especializado em gerar análises de sessões "
                    "de conversação sobre agendamento de horários em motéis. "
                    f"Por favor, analise a sessão {session_id} e responda com um "
                    "resumo e sugestões de melhoria."
                ),
            },
            {
                "role": "user",
                "content": (
                        "Baseado nas informações da conversa abaixo, gere um JSON com:\n"
                        "- `summary`: Resumo da conversa entre usuário e agente\n"
                        "- `satisfaction`: Nota de satisfação (0 a 10)\n"
                        "- `improvement`: Sugestões de melhoria no atendimento\n\n"
                        "## Mensagens da sessão\n"
                        + "\n".join(
                    [f"{'Usuário' if msg.remote else 'Agente'}: {msg.content}" for msg in messages]
                )
                        + "\n\n"
                          "## Exemplo de JSON esperado\n"
                          "{\n"
                          "    \"satisfaction\": 8,\n"
                          "    \"summary\": \"O usuário conseguiu agendar o horário desejado.\",\n"
                          "    \"improvement\": \"O agente poderia ter informado sobre promoções.\"\n"
                          "}"
                ),
            },
        ],
    )

    # Verifica se há resposta válida
    if response.choices and response.choices[0].message.content:
        return json.loads(response.choices[0].message.content)

    return {"error": "Falha ao gerar análise"}
