# Use uma imagem base com Python
FROM python:3.9-slim

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie os arquivos de dependências para dentro do contêiner
COPY requirements.txt .

# Instale dependências do sistema para Postgres e outras models necessárias
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Instale as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante dos arquivos da aplicação
COPY src .

# Garanta que as variáveis do .env sejam carregadas corretamente
ENV PYTHONUNBUFFERED=1

# Aguarde o banco estar pronto antes de iniciar a aplicação
CMD ["sh", "-c", "sleep 5 && python main.py"]
