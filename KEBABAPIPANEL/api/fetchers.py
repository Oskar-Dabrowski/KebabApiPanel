import requests
from bs4 import BeautifulSoup
from django.conf import settings
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

class GoogleRatingsFetcher:
    @staticmethod
    def fetch_google_rating(kebab_name):
        """
        Fetch rating, place_id, and logo URL of a kebab shop from Google Places API.
        """
        base_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
        params = {
            "input": kebab_name,
            "inputtype": "textquery",
            "fields": "rating,place_id,photos",
            "key": settings.GOOGLE_API_KEY
        }
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        if "candidates" in data and data["candidates"]:
            candidate = data["candidates"][0]
            rating = candidate.get("rating")
            place_id = candidate.get("place_id")

            # Get logo URL from the photos array if available
            logo_url = None
            if "photos" in candidate:
                photo_reference = candidate["photos"][0].get("photo_reference")
                if photo_reference:
                    logo_url = (
                        f"https://maps.googleapis.com/maps/api/place/photo"
                        f"?maxwidth=400&photoreference={photo_reference}&key={settings.GOOGLE_API_KEY}"
                    )
            
            return {
                "rating": rating,
                "place_id": place_id,
                "logo_url": logo_url
            }
        return None


class PyszneRatingsFetcher:
    @staticmethod
    def fetch_pyszne_details(restaurant_url):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36")

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        try:
            driver.get(restaurant_url)

            # Dodanie ciasteczek (jeśli wymagane)
            cookies = [
                {"name": "sessionid", "value": "your-session-id", "domain": "www.pyszne.pl"},
            ]
            for cookie in cookies:
                driver.add_cookie(cookie)

            # Odśwież stronę po dodaniu ciasteczek
            driver.refresh()

            rating_element = driver.find_element(By.CLASS_NAME, "rating-value")
            rating = float(rating_element.text.strip())

            logo_element = driver.find_element(By.CLASS_NAME, "restaurant-logo")
            logo_url = logo_element.get_attribute("src")

            return {
                "rating": rating,
                "logo_url": logo_url,
            }
        except Exception as e:
            print(f"Error while fetching details: {e}")
            return None
        finally:
            driver.quit()