import os
import time
import django
from django.db import connections
from django.db.utils import OperationalError

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'KEBABAPIPANEL.settings')
django.setup()

from django.contrib.auth.models import User

def wait_for_db():
    """Wait for the database to be available."""
    max_retries = 10
    retry_delay = 5  # seconds
    retries = 0

    while retries < max_retries:
        try:
            connections['default'].ensure_connection()
            print("Database is ready!")
            return True
        except OperationalError:
            print(f"Database not ready, retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
            retries += 1
    print("Failed to connect to the database after multiple retries.")
    return False

def create_superuser():
    """Create a superuser if it doesn't already exist."""
    username = os.getenv('DJANGO_SUPERUSER_USERNAME', 'admin')
    email = os.getenv('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
    password = os.getenv('DJANGO_SUPERUSER_PASSWORD', 'admin')

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)
        print(f"Superuser {username} created successfully.")
    else:
        print(f"Superuser {username} already exists.")

if __name__ == '__main__':
    if wait_for_db():
        create_superuser()
    else:
        print("Superuser creation skipped due to database connection issues.")