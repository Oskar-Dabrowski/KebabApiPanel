# Wybieramy bazowy obraz z Pythonem
FROM python:3.10-slim

# Ustawiamy katalog roboczy
WORKDIR /app

# Aktualizacja pip
RUN python -m pip install --upgrade pip

# Kopiujemy plik requirements.txt i instalujemy zależności
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiujemy kod aplikacji do obrazu Dockera
COPY . .

# Eksportujemy port, na którym działa Django (domyślnie 8000)
EXPOSE 8000

# Uruchamiamy komendę startową Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
