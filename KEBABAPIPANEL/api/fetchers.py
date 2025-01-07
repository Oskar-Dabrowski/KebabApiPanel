import requests
from bs4 import BeautifulSoup
from django.conf import settings
from .models import Kebab

class GoogleRatingsFetcher:
    @staticmethod
    def fetch_google_rating(kebab_name):
        base_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
        params = {
            "input": kebab_name,
            "inputtype": "textquery",
            "fields": "rating",
            "key": settings.GOOGLE_API_KEY
        }
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        if "candidates" in data and data["candidates"]:
            return data["candidates"][0].get("rating")
        return None

class PyszneRatingsFetcher:
    @staticmethod
    def fetch_pyszne_rating(kebab_name):
        search_url = f"https://www.pyszne.pl/search?q={kebab_name}"
        response = requests.get(search_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        rating_tag = soup.find('span', class_='rating-value')
        if rating_tag:
            return float(rating_tag.text.strip())
        return None