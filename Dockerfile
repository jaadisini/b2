FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV MONGO_URI=mongodb://mongo:27017
ENV BOT_TOKEN_UTAMA=bot_utama_token_disini

CMD ["python", "main.py"]
