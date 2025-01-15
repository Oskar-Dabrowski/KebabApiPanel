from celery import shared_task
from .models import Kebab
from .fetchers import GoogleRatingsFetcher, PyszneRatingsFetcher

@shared_task
def update_kebab_details():
    """
    Pobiera i aktualizuje dane kebabów.
    """
    for kebab in Kebab.objects.all():
        try:
            google_data = GoogleRatingsFetcher.fetch_google_rating(kebab.name)
            if google_data:
                kebab.google_rating = google_data['rating']

            pyszne_data = PyszneRatingsFetcher.fetch_pyszne_rating(kebab.name)
            if pyszne_data:
                kebab.pyszne_rating = pyszne_data['rating']

            kebab.save()
        except Exception as e:
            print(f"Error updating {kebab.name}: {e}")
