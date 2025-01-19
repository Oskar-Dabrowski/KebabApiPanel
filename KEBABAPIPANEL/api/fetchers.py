import requests
from bs4 import BeautifulSoup
from django.conf import settings

class GoogleRatingsFetcher:
    @staticmethod
    def fetch_google_rating(kebab_name):
        base_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
        params = {
            "input": kebab_name,
            "inputtype": "textquery",
            "fields": "rating,place_id",
            "key": settings.GOOGLE_API_KEY
        }
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        if "candidates" in data and data["candidates"]:
            candidate = data["candidates"][0]
            rating = candidate.get("rating")
            place_id = candidate.get("place_id")
            return {
                "rating": rating,
                "place_id": place_id
            }
        return None
        

class PyszneRatingsFetcher:
    @staticmethod
    def fetch_pyszne_rating(kebab_name):
        search_url = f"https://www.pyszne.pl/search?q={kebab_name}"
        response = requests.get(search_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        restaurant_card = soup.find('a', class_='restaurant')
        if restaurant_card:
            rating_tag = restaurant_card.find('span', class_='rating-value')
            if rating_tag:
                try:
                    return {
                        "rating": float(rating_tag.text.strip()),
                        "restaurant_url": restaurant_card['href']
                    }
                except ValueError:
                    return None
        return None