from prisma import Prisma

prisma = Prisma()

async def find_analysis(session_id: int):
    """Verifica se já existe uma análise para a sessão no banco de dados usando Prisma"""
    await prisma.connect()  # Garante que o banco de dados está conectado

    analysis = await prisma.analysis.find_first(
        where={'session_id': session_id}
    )

    await prisma.disconnect()  # Fecha a conexão após a consulta
    return analysis
