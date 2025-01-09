from celery import shared_task
from django.utils.timezone import now
from .models import Kebab, Rating
from .fetchers import GoogleRatingsFetcher, PyszneRatingsFetcher

@shared_task
def update_ratings_task():
    """Pobiera oceny dla każdego kebaba i zapisuje je w bazie."""
    for kebab in Kebab.objects.all():
        google_data = GoogleRatingsFetcher.fetch_google_rating(kebab.name)
        if google_data is not None:
            Rating.objects.update_or_create(
                kebab=kebab,
                source='google',
                defaults={
                    'rating': google_data.get('rating'),
                    'extra_data': {'place_id': google_data.get('place_id')}
                }
            )

        pyszne_data = PyszneRatingsFetcher.fetch_pyszne_rating(kebab.name)
        if pyszne_data is not None:
            Rating.objects.update_or_create(
                kebab=kebab,
                source='pyszne',
                defaults={
                    'rating': pyszne_data.get('rating'),
                    'extra_data': {'restaurant_url': pyszne_data.get('restaurant_url')}
                }
            )

    Kebab.objects.update(last_updated=now())