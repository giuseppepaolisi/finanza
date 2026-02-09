FROM python:3.14-slim

# Imposta la directory di lavoro
WORKDIR /app

# Installa le dipendenze di sistema per psycopg
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copia i requirements
COPY requirements.txt .

# Installa le dipendenze Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia tutto il codice dell'app
COPY . .

# Esponi la porta (se usi Flask/FastAPI)
EXPOSE 8000

# Comando di avvio
CMD ["python", "app/app.py"]