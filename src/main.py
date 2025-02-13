from prisma import Prisma
from datetime import datetime
from libs.services.find_analysis import find_analysis
from libs.services.generate_analysis import generate_analysis

# Inicializando o cliente Prisma
prisma = Prisma()

async def verify_analysis():
    try:
        await prisma.connect()  # Conecta ao banco de dados

        # Obtém todas as sessões existentes no banco
        sessions = await prisma.session.find_many(select={'id': True})

        for session in sessions:
            session_id = session['id']
            analysis_found = await find_analysis(session_id)

            if not analysis_found:
                print("Não há análise para essa sessão, criando uma nova...")

                # Obtém todas as mensagens associadas à sessão
                messages = await prisma.message.find_many(
                    where={'session_id': session_id},
                    select={'content': True, 'created_at': True, 'remote': True}
                )

                # Gera a análise com base nas mensagens
                analysis = await generate_analysis(session_id, messages)

                # Insere a nova análise no banco
                new_analysis = await prisma.analysis.create({
                    'session_id': session_id,
                    'satisfaction': analysis.satisfaction,
                    'summary': analysis.summary,
                    'improvement': analysis.improvement,
                    'created_at': datetime.now()
                })

                print(f"Análise da sessão {session_id} criada:")
                print(f"Satisfação: {new_analysis.satisfaction}\nResumo: {new_analysis.summary}\nMelhoria: {new_analysis.improvement}")
            else:
                print(f"Análise da sessão {session_id}:")
                print(f"Satisfação: {analysis_found.satisfaction}\nResumo: {analysis_found.summary}\nMelhoria: {analysis_found.improvement}")

    except Exception as error:
        print(f"Ocorreu um erro ao verificar análises: {error}")
    finally:
        await prisma.disconnect()  # Desconecta do banco ao finalizar

# Executa a verificação quando o script for rodado
if __name__ == "__main__":
    import asyncio
    asyncio.run(verify_analysis())
