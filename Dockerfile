FROM python:3.13

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

# Comando para rodar a app
# CMD ["streamlit", "run", "./app/main.py", "--server.port=8080", "--server.address=0.0.0.0"]
