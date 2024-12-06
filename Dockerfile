# imagem base do python
FROM python:3.8-slim

# Dirc de trabalhgo dentro do contiener
WORKDIR /app

# Copiar o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt .

# Instalar as dependências listadas em requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

# Definir a variável de ambiente para que o Flask saiba que está em produção
ENV FLASK_ENV=production

CMD [ "python", "app.py" ]