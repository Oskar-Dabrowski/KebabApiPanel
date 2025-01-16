import os
from celery import Celery

# DJANGO_SETTINGS_MODULE
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'KEBABAPIPANEL.settings')

# Initialize the Celery app
app = Celery('KEBABAPIPANEL')

# Load Celery configuration from Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in Django apps
app.autodiscover_tasks()

@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    """
    Configure periodic tasks after Celery app finalization.
    Uses django-celery-beat to schedule tasks.
    """
    from django_celery_beat.models import PeriodicTask, IntervalSchedule

    # Create or fetch an interval schedule (daily interval)
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=1,
        period=IntervalSchedule.DAYS,  # Interval set to one day
    )

    # Create or update a periodic task for updating kebab details
    PeriodicTask.objects.update_or_create(
        interval=schedule,
        name='Update Kebab Details Daily',  # Task name displayed in Django Admin
        task='api.tasks.update_kebab_details',  # Path to the task function
        defaults={
            'description': 'Automatyczna aktualizacja danych o kebabach z Legnicy',
        }
    )
