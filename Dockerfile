FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE = 1 #evita che python scriva i file .pyc sul disco
ENV PYTHONUNBUFFERED = 1 #Forza python a mostrare i log sul terminale in tempo reale

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . . 
EXPOSE 5000
CMD ["python","main.py"]