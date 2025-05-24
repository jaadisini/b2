FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV MONGO_URI=mongodb+srv://dizaubot:dizaubot@cluster0.ise8rzn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
ENV BOT_TOKEN_UTAMA=7519673982:AAESvCiR8CdOASnO4MYcodV6EuB-nY28ZQA

CMD ["python", "main.py"]
