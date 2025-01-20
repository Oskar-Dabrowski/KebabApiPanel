import os
from celery import Celery

# Set the default Django settings module for Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'KEBABAPIPANEL.settings')

# Initialize the Celery app
app = Celery('KEBABAPIPANEL')

# Load Celery config from Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in installed apps
app.autodiscover_tasks()

@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    """
    Set up periodic tasks using django-celery-beat.
    """
    from django_celery_beat.models import PeriodicTask, IntervalSchedule

    # Create or get the daily interval schedule
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=1,
        period=IntervalSchedule.DAYS,  # Daily schedule
    )

    # Create or update the periodic task
    PeriodicTask.objects.update_or_create(
        interval=schedule,
        name='Update Kebab Details Daily',  # Name visible in Django Admin
        task='api.tasky.update_kebab_details',  # Path to the task
        defaults={
            'description': 'Automatically updates kebab details daily.',
        }
    )



