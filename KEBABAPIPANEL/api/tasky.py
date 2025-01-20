from celery import shared_task
from .models import Kebab
from .fetchers import GoogleRatingsFetcher, PyszneRatingsFetcher

@shared_task
def update_kebab_details():
    """
    Updates kebab ratings and verifies social media links.
    """
    incomplete_social_links = []  # List of kebabs missing social media links

    for kebab in Kebab.objects.all():
        try:
            # Fetch and update Google ratings
            google_data = GoogleRatingsFetcher.fetch_google_rating(kebab.name)
            if google_data:
                kebab.google_rating = google_data.get('rating')
                kebab.logo = google_data.get('logo_url') or None

            # Fetch and update Pyszne ratings
            pyszne_data = PyszneRatingsFetcher.fetch_pyszne_details(kebab.pyszne_url)
            if pyszne_data:
                kebab.pyszne_rating = pyszne_data.get('rating')

            # Check if social media links are present
            if not kebab.social_links or not isinstance(kebab.social_links, dict):
                incomplete_social_links.append(kebab.name)

            kebab.save()

        except Exception as e:
            print(f"Error updating {kebab.name}: {e}")

    # Log kebabs missing social media links
    if incomplete_social_links:
        print(f"Kebabs without social media links: {incomplete_social_links}")