# === BASE IMAGE ===
FROM python:3.11-slim

# === AMBIENTE DI LAVORO NEL CONTAINER ===
WORKDIR /app

# === COPIA FILE NECESSARI ===
COPY requirements.txt requirements.txt

# === INSTALLA LE DIPENDENZE ===
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# === COPIA TUTTO IL PROGETTO ===
COPY . .

# === ESPONI LA PORTA USATA DA FLET ===
EXPOSE 8550

# === AVVIO DELL'APPLICAZIONE ===
CMD ["flet", "run", "--web", "main.py", "--host", "0.0.0.0", "--port", "8550"]