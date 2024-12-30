from celery import Celery

app = Celery('KEBABAPIPANEL')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    from django_celery_beat.models import PeriodicTask, IntervalSchedule

    # Tworzenie interwału (co 1 dzień)
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=1,
        period=IntervalSchedule.DAYS,
    )

    # Tworzenie zadania (update_ratings_task)
    PeriodicTask.objects.get_or_create(
        interval=schedule,
        name='Update Ratings Daily',
        task='api.tasks.update_ratings_task',
    )
