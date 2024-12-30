from celery import shared_task
from .models import Kebab, Rating
from .fetchers import GoogleRatingsFetcher, PyszneRatingsFetcher

@shared_task
def update_ratings_task():
    """Pobiera oceny dla każdego kebaba i zapisuje je w bazie."""
    for kebab in Kebab.objects.all():
        google_rating = GoogleRatingsFetcher.fetch_google_rating(kebab.name)
        if google_rating is not None:
            Rating.objects.update_or_create(
                kebab=kebab,
                source='google',
                defaults={'rating': google_rating}
            )

        pyszne_rating = PyszneRatingsFetcher.fetch_pyszne_rating(kebab.name)
        if pyszne_rating is not None:
            Rating.objects.update_or_create(
                kebab=kebab,
                source='pyszne',
                defaults={'rating': pyszne_rating}
            )
