import { openai } from '../clients'

export type AnalysisResponse = {
    satisfaction: number
    summary: string
    improvement: string
}

export async function generateAnalysis (
    session_id: number,
    messages: any
): Promise<AnalysisResponse> {
    const response = await openai.chat.completions.create({
        model: 'gpt-4o-mini',
        temperature: 0.7,
        messages: [
            {
                role: 'developer',
                content: 'Você é um agente especializado em gerar análises de sessões ' +
                'de conversacionais sobre agendamento de horários em motéis. ' +
                `Por favor, analise a sessão ${session_id} e responda com um ` +
                'resumo e sugestões de melhoria.'
            },
            { role: 'user', content: `
                Com base nas informações da conversa abaixo, gere uma estrutura em JSON contendo:

                summary: Um resumo da conversa entre o usuário e o agente de IA, destacando os pontos principais.
                satisfaction: Um indicador numérico de 0 a 10 (inteiros), avaliando se as respostas foram coerentes com as perguntas do usuário.
                improvement: Sugestões de melhoria para o atendimento.

                ## Chain of thought // Cadeia de pensamento
                1 - Analise as mensagens da sessão considerando as interações do usuário.
                2 - Extraia as informações mais relevantes para determinar o nível de satisfação.
                3 - O campo satisfaction deve conter um valor inteiro entre 0 e 10.
                4 - O campo summary deve ser uma string de até 500 caracteres.
                5 - O campo improvement deve ser uma string de até 500 caracteres.
                6 - Preserve o contexto da conversa e identifique a intenção do usuário.
                7 - Baseie-se apenas no que foi dito, sem adicionar informações não mencionadas.
                8 - Revise sua resposta e compare com as mensagens do usuário para garantir a precisão da análise.
                9 - Estruture os dados em um objeto JSON contendo os campos satisfaction, summary e improvement.
                10 - A saída deve ser somente o objeto JSON, sem nenhuma informação adicional.

                ## Mensagens da sessão
                ${messages.map((message: any) => {
                    return `${message.remote ? 'Usuário' : 'Agente'}: ${message.content}`
                }).join('\n')}

                ## Exemplo de output
                {
                    "satisfaction": (0 a 10),
                    "summary": "O usuário está satisfeito com o atendimento e conseguiu agendar o horário desejado.",
                    "improvement": "O usuário poderia ter sido informado sobre a disponibilidade de quartos extras."
                }
                ` }
        ]
    })

    return JSON.parse(response.choices[0].message.content as string)
}