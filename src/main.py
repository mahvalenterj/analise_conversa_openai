import tkinter as tk
from tkinter import scrolledtext
import asyncio
from prisma import Prisma
from datetime import datetime
from models.services.find_analysis import find_analysis
from models.services.generate_analysis import generate_analysis

# Inicializando o cliente Prisma
prisma = Prisma()

async def verify_analysis():
    result = ""
    try:
        await prisma.connect()  # Conecta ao banco de dados

        # Obtém todas as sessões existentes no banco
        sessions = await prisma.session.find_many(select={'id': True})

        for session in sessions:
            session_id = session['id']
            analysis_found = await find_analysis(session_id)

            if not analysis_found:
                result += f"Não há análise para a sessão {session_id}, criando uma nova...\n"

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

                result += f"Análise da sessão {session_id} criada:\nSatisfação: {new_analysis.satisfaction}\nResumo: {new_analysis.summary}\nMelhoria: {new_analysis.improvement}\n\n"
            else:
                result += f"Análise da sessão {session_id}:\nSatisfação: {analysis_found.satisfaction}\nResumo: {analysis_found.summary}\nMelhoria: {analysis_found.improvement}\n\n"

    except Exception as error:
        result += f"Ocorreu um erro ao verificar análises: {error}\n"
    finally:
        await prisma.disconnect()  # Desconecta do banco ao finalizar
    return result


# Função para chamar a função async na interface gráfica
def run_verify_analysis():
    result = asyncio.run(verify_analysis())  # Chama a função que faz a análise
    text_output.delete(1.0, tk.END)  # Limpa o conteúdo anterior
    text_output.insert(tk.END, result)  # Exibe o resultado no campo de texto

# Configuração da interface gráfica com Tkinter
root = tk.Tk()
root.title("Verificador de Análises")

# Botão para executar a verificação
button = tk.Button(root, text="Verificar Análises", command=run_verify_analysis)
button.pack(pady=10)

# Caixa de texto para exibir os resultados
text_output = scrolledtext.ScrolledText(root, width=80, height=20)
text_output.pack(padx=10, pady=10)

# Rodar a interface gráfica
root.mainloop()
