# Wybieramy bazowy obraz z Pythonem
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

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

# Run migrations, create superuser, seed database, and start server
CMD ["sh", "-c", "python manage.py migrate && python manage.py shell < create_superuser.py && python manage.py seed_kebabs && python manage.py runserver 0.0.0.0:8000"]
