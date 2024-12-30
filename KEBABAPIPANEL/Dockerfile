# Wybieramy bazowy obraz z Pythonem
FROM python:3.10-slim

# Ustawiamy katalog roboczy
WORKDIR /app

# Instalujemy brakujące zależności systemowe
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    libjpeg-dev \
    libfreetype6-dev \
    && rm -rf /var/lib/apt/lists/*

# Aktualizacja pip
RUN python -m pip install --upgrade pip

# Kopiujemy plik requirements.txt i instalujemy zależności Pythonowe
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiujemy kod aplikacji do obrazu Dockera
COPY . .

# Eksportujemy port dla Django
EXPOSE 8000

# Ustawiamy domyślne polecenie uruchomienia serwera Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
