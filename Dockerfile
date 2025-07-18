# === BASE IMAGE ===
FROM python:3.11-slim

# === EVITA PROBLEMI DI BUFFERING DEI LOG ===
ENV PYTHONUNBUFFERED=1

# === AMBIENTE DI LAVORO NEL CONTAINER ===
WORKDIR /app

# === COPIA FILE NECESSARI ===
COPY requirements.txt .

# === INSTALLA LE DIPENDENZE ===
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# === COPIA TUTTO IL PROGETTO ===
COPY . .

# === ESPONI LA PORTA USATA DA FLET ===
EXPOSE 8550

# === AVVIO DELL'APPLICAZIONE SOLO IN MODALITÀ WEB ===
CMD ["python", "main.py"]