from django.core.management.base import BaseCommand
from api.models import Kebab, OpeningHour

class Command(BaseCommand):
    help = 'Seed kebabs into the database'

    def handle(self, *args, **kwargs):
        kebabs_data = [
            {"name": "Stambul kebab", "location_details": "Chojnowska 21A, 59-220 Legnica, Poland", "latitude": 51.207173, "longitude": 16.15698, "status": "open", "meats": ["baranina", "kurczak", "wołowina"], "sauces": ["czosnkowy", "ostry", "łagodny"], "opening_year": None, "closing_year": None, "craft_rating": False, "in_chain": False, "order_methods": "dostawa, na miejscu, na wynos", "social_links": None, "logo": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQC0pKj4LVLo2ZSHwq4zZyiTF8h5O6XMtbHMg&s", "google_rating": 3.7, "pyszne_rating": 0.0,
             "opening_hours": {
                 "monday": {
                     "open": "10:00",
                     "close": "22:00"
                 },
                 "tuesday": {
                     "open": "10:00",
                     "close": "22:00"
                 },
                 "wednesday": {
                     "open": "10:00",
                     "close": "22:00"
                 },
                 "thursday": {
                     "open": "10:00",
                     "close": "22:00"
                 },
                 "friday": {
                     "open": "10:00",
                     "close": "23:00"
                 },
                 "saturday": {
                     "open": "10:00",
                     "close": "23:00"
                 },
                 "sunday": {
                     "open": "10:00",
                     "close": "20:00"
                 }
             }},
            {"name": "Cyrus Kebab Restauracja Kurdyjska", "location_details": "Rynek 20, 59-200 Legnica, Poland", "latitude": 51.2078832, "longitude": 16.1610674, "status": "open", "meats": ["baranina", "kurczak", "wołowina", "wieprzowina"], "sauces": ["czosnkowy", "ostry", "łagodny"], "opening_year": None, "closing_year": None, "craft_rating": True, "in_chain": False, "order_methods": "dostawa, na miejscu, na wynos", "social_links": "http://www.cyrus.pl/", "logo": "https://glovoapp.com/static/img/cyrus-kebab-logo.png", "google_rating": 4, "pyszne_rating": 0.0,"opening_hours": {
                "monday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "tuesday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "wednesday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "thursday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "friday": {
                    "open": "10:00",
                    "close": "23:00"
                },
                "saturday": {
                    "open": "10:00",
                    "close": "23:00"
                },
                "sunday": {
                    "open": "10:00",
                    "close": "20:00"
                }
            }},
            {"name": "Had Food - Pizza Kebab Burger", "location_details": "Fabryczna 13, 59-220 Legnica, Poland", "latitude": 51.20677389999999, "longitude": 16.1786968, "status": "open", "meats": ["kurczak", "wołowina"], "sauces": ["czosnkowy", "ostry", "łagodny"], "opening_year": None, "closing_year": None, "craft_rating": False, "in_chain": False, "order_methods": "dostawa, na miejscu, na wynos", "social_links": "https://www.facebook.com/share/oJisRGHuprTimrsU/", "logo": "https://scontent-ber1-1.xx.fbcdn.net/v/t39.30808-6/392961103_6659007470821068_1704781470570580247_n.jpg?_nc_cat=106&ccb=1-7&_nc_sid=6ee11a&_nc_ohc=9Jx1B5TdLDEQ7kNvgETLNuD&_nc_zt=23&_nc_ht=scontent-ber1-1.xx&_nc_gid=AtutaO5rTyfs8ppDG7vP5BG&oh=00_AYBsI91gm6s5AuVZ6R7fJJ70Va2yk73oR2RDiCrmcKsmQA&oe=679493CE", "google_rating": 4.4, "pyszne_rating": 0.0,"opening_hours": {
                "monday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "tuesday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "wednesday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "thursday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "friday": {
                    "open": "10:00",
                    "close": "23:00"
                },
                "saturday": {
                    "open": "10:00",
                    "close": "23:00"
                },
                "sunday": {
                    "open": "10:00",
                    "close": "20:00"
                }
            }},
            {"name": "Nogor Kebab - Legnica", "location_details": "Jaworzyńska 41, 59-220 Legnica, Poland", "latitude": 51.2006473, "longitude": 16.1594436, "status": "open", "meats": ["kurczak", "baranina"], "sauces": ["czosnkowy", "ostry", "łagodny"], "opening_year": None, "closing_year": None, "craft_rating": False, "in_chain": False, "order_methods": "dostawa, na miejscu, na wynos", "social_links": "https://www.facebook.com/profile.php?id=61567421895998", "logo": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSJnQWFZapZYvNqVs1c0CMxRcYUR7O5IbBNWQ&s", "google_rating": 4.7, "pyszne_rating": 0.0,"opening_hours": {
                "monday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "tuesday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "wednesday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "thursday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "friday": {
                    "open": "10:00",
                    "close": "23:00"
                },
                "saturday": {
                    "open": "10:00",
                    "close": "23:00"
                },
                "sunday": {
                    "open": "10:00",
                    "close": "20:00"
                }
            }},
            {"name": "Leo Kebab , Legnica", "location_details": "Jaworzyńska 4, 59-220 Legnica, Poland", "latitude": 51.2043883, "longitude": 16.1599134, "status": "open", "meats": ["baranina", "kurczak", "falafel"], "sauces": ["czosnkowy", "ostry", "łagodny"], "opening_year": None, "closing_year": None, "craft_rating": False, "in_chain": False, "order_methods": "dostawa, na miejscu, na wynos", "social_links": "https://www.leokebab-legnica.pl/", "logo": "https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/restaurant-71.png", "google_rating": 4.4, "pyszne_rating": 0.0,"opening_hours": {
                "monday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "tuesday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "wednesday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "thursday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "friday": {
                    "open": "10:00",
                    "close": "23:00"
                },
                "saturday": {
                    "open": "10:00",
                    "close": "23:00"
                },
                "sunday": {
                    "open": "10:00",
                    "close": "20:00"
                }
            }},
            {"name": "King House Kebab", "location_details": "aleja Piłsudskiego 38, 59-220 Legnica, Poland", "latitude": 51.20461840000001, "longitude": 16.1885512, "status": "open", "meats": ["baranina", "kurczak", "wołowina"], "sauces": ["czosnkowy", "ostry", "łagodny", "ketchup", "BBQ"], "opening_year": None, "closing_year": None, "craft_rating": False, "in_chain": False, "order_methods": "dostawa, na miejscu, na wynos, odbiór na miejscu", "social_links": "https://www.facebook.com/profile.php?id=100088738987179", "logo": "https://www.pyszne.pl/king-house-logo.jpg", "google_rating": 4.4, "pyszne_rating": 0.0,"opening_hours": {
                "monday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "tuesday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "wednesday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "thursday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "friday": {
                    "open": "10:00",
                    "close": "23:00"
                },
                "saturday": {
                    "open": "10:00",
                    "close": "23:00"
                },
                "sunday": {
                    "open": "10:00",
                    "close": "20:00"
                }
            }},
            {"name": "BAFRA Kebab Legnica ul. Gwiezdna", "location_details": "Gwiezdna 4, 59-220 Legnica, Poland", "latitude": 51.20852619999999, "longitude": 16.181662, "status": "open", "meats": ["kurczak", "wołowina"], "sauces": ["czosnkowy", "ostry", "łagodny"], "opening_year": None, "closing_year": None, "craft_rating": False, "in_chain": True, "order_methods": "dostawa, na miejscu, na wynos, odbiór na miejscu", "social_links": "https://www.bafrakebablegnica.pl/", "logo": "https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/restaurant-71.png", "google_rating": 4.3, "pyszne_rating": 0.0,"opening_hours": {
                "monday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "tuesday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "wednesday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "thursday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "friday": {
                    "open": "10:00",
                    "close": "23:00"
                },
                "saturday": {
                    "open": "10:00",
                    "close": "23:00"
                },
                "sunday": {
                    "open": "10:00",
                    "close": "20:00"
                }
            }},
            {"name": "BAFRA Kebab Legnica ul. Złotoryjska", "location_details": "Złotoryjska 170, 59-220 Legnica, Poland", "latitude": 51.1929884, "longitude": 16.1289271, "status": "open", "meats": ["kurczak", "wołowina"], "sauces": ["czosnkowy", "ostry", "łagodny"], "opening_year": None, "closing_year": None, "craft_rating": False, "in_chain": True, "order_methods": "dostawa, na miejscu, na wynos, odbiór na miejscu", "social_links": "https://www.bafrakebablegnica.pl/", "logo": "https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/restaurant-71.png", "google_rating": 4.6, "pyszne_rating": 0.0,"opening_hours": {
                "monday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "tuesday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "wednesday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "thursday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "friday": {
                    "open": "10:00",
                    "close": "23:00"
                },
                "saturday": {
                    "open": "10:00",
                    "close": "23:00"
                },
                "sunday": {
                    "open": "10:00",
                    "close": "20:00"
                }
            }},
            {"name": "Lara Döner Kebab Legnica", "location_details": "Wrocławska 13, 59-220 Legnica, Poland", "latitude": 51.2095676, "longitude": 16.1677994, "status": "open", "meats": ["kurczak", "wołowina"], "sauces": ["czosnkowy", "ostry", "łagodny"], "opening_year": None, "closing_year": None, "craft_rating": False, "in_chain": False, "order_methods": "na miejscu, na wynos, odbiór na miejscu", "social_links": None, "logo": "https://glovoapp.com/static/img/lara-doner-logo.png", "google_rating": 4.6, "pyszne_rating": 0.0,"opening_hours": {
                "monday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "tuesday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "wednesday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "thursday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "friday": {
                    "open": "10:00",
                    "close": "23:00"
                },
                "saturday": {
                    "open": "10:00",
                    "close": "23:00"
                },
                "sunday": {
                    "open": "10:00",
                    "close": "20:00"
                }
            }},
            {"name": "Kebab&Gyros", "location_details": "Roberta Schumana 17, 59-220 Legnica, Poland", "latitude": 51.1854498, "longitude": 16.1723735, "status": "open", "meats": ["kurczak", "wołowina"], "sauces": ["czosnkowy", "ostry", "łagodny", "ketchup", "BBQ"], "opening_year": None, "closing_year": None, "craft_rating": False, "in_chain": False, "order_methods": "dostawa, na miejscu, na wynos, odbiór na miejscu", "social_links": "https://www.kebablegnica.pl/", "logo": "https://www.kebablegnica.pl/static/img/logo.jpg", "google_rating": 3.1, "pyszne_rating": 0.0,"opening_hours": {
                "monday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "tuesday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "wednesday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "thursday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "friday": {
                    "open": "10:00",
                    "close": "23:00"
                },
                "saturday": {
                    "open": "10:00",
                    "close": "23:00"
                },
                "sunday": {
                    "open": "10:00",
                    "close": "20:00"
                }
            }},
            {"name": "Karmnik - Kebab Legnica", "location_details": "Wrocławska, 59-200 Legnica, Poland", "latitude": 51.2096928, "longitude": 16.1686235, "status": "open", "meats": ["kurczak", "wołowina"], "sauces": ["czosnkowy", "ostry", "łagodny"], "opening_year": None, "closing_year": None, "craft_rating": True, "in_chain": False, "order_methods": "na miejscu, na wynos", "social_links": None, "logo": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTSZws_g1qjEn-7YspPtG_xRSj7lwUYkvJMiQ&s", "google_rating": 5, "pyszne_rating": 0.0,"opening_hours": {
                "monday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "tuesday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "wednesday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "thursday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "friday": {
                    "open": "10:00",
                    "close": "23:00"
                },
                "saturday": {
                    "open": "10:00",
                    "close": "23:00"
                },
                "sunday": {
                    "open": "10:00",
                    "close": "20:00"
                }
            }},
            {"name": "Kebab domowy Maru", "location_details": "Wrocławska 41A, 59-220 Legnica, Poland", "latitude": 51.2090762, "longitude": 16.1717437, "status": "open", "meats": ["kurczak", "wołowina"], "sauces": ["czosnkowy", "ostry", "łagodny"], "opening_year": None, "closing_year": None, "craft_rating": False, "in_chain": False, "order_methods": "na miejscu, na wynos", "social_links": None, "logo": "https://glovoapp.com/static/img/kebab-domowy-maru-logo.png", "google_rating": 0.0, "pyszne_rating": 0.0, "opening_hours": {
                "monday": {
                    "open": "00:00",
                    "close": "00:00"
                },
                "tuesday": {
                    "open": "00:00",
                    "close": "0:00"
                },
                "wednesday": {
                    "open": "00:00",
                    "close": "0:00"
                },
                "thursday": {
                    "open": "00:00",
                    "close": "0:00"
                },
                "friday": {
                    "open": "00:00",
                    "close": "0:00"
                },
                "saturday": {
                    "open": "00:00",
                    "close": "0:00"
                },
                "sunday": {
                    "open": "00:00",
                    "close": "00:00"
                }
            }},
            {"name": "Grill House Kebab (KAVOVARKA)", "location_details": "Górnicza 10B, 59-220 Legnica, Poland", "latitude": 51.2059746, "longitude": 16.1867794, "status": "open", "meats": ["kurczak", "wołowina"], "sauces": ["czosnkowy", "ostry", "łagodny"], "opening_year": None, "closing_year": None, "craft_rating": True, "in_chain": False, "order_methods": "dostawa, na miejscu, na wynos, odbiór na miejscu", "social_links": "https://www.facebook.com/profile.php?id=61571429693132", "logo": "https://glovoapp.com/static/img/grill-house-logo.png", "google_rating": 5, "pyszne_rating": 0.0,"opening_hours": {
                "monday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "tuesday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "wednesday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "thursday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "friday": {
                    "open": "10:00",
                    "close": "23:00"
                },
                "saturday": {
                    "open": "10:00",
                    "close": "23:00"
                },
                "sunday": {
                    "open": "10:00",
                    "close": "20:00"
                }
            }},
            {"name": "KEBAB TRUCK", "location_details": "Iwaszkiewicza 1, 59-220 Legnica, Poland", "latitude": 51.2079282, "longitude": 16.2134147, "status": "open", "meats": ["kurczak", "wołowina"], "sauces": ["czosnkowy", "ostry", "łagodny"], "opening_year": None, "closing_year": None, "craft_rating": False, "in_chain": False, "order_methods": "na miejscu, na wynos", "social_links": None, "logo": "https://glovoapp.com/static/img/kebab-truck-logo.png", "google_rating": 3.4, "pyszne_rating": 0.0,"opening_hours": {
                "monday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "tuesday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "wednesday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "thursday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "friday": {
                    "open": "10:00",
                    "close": "23:00"
                },
                "saturday": {
                    "open": "10:00",
                    "close": "23:00"
                },
                "sunday": {
                    "open": "10:00",
                    "close": "20:00"
                }
            }},
            {"name": "Döner Kebab. Legnica", "location_details": "Rynek 32, 59-200 Legnica, Poland", "latitude": 51.2077641, "longitude": 16.1605772, "status": "open", "meats": ["kurczak", "wołowina"], "sauces": ["czosnkowy", "ostry", "łagodny"], "opening_year": None, "closing_year": None, "craft_rating": False, "in_chain": False, "order_methods": "na miejscu", "social_links": None, "logo": "https://glovoapp.com/static/img/doner-kebab-logo.png", "google_rating": 3.4, "pyszne_rating": 0.0,"opening_hours": {
                "monday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "tuesday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "wednesday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "thursday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "friday": {
                    "open": "10:00",
                    "close": "23:00"
                },
                "saturday": {
                    "open": "10:00",
                    "close": "23:00"
                },
                "sunday": {
                    "open": "10:00",
                    "close": "20:00"
                }
            }},
            {"name": "MAXI Kebab Legnica", "location_details": "parking Carrefour, aleja Piłsudskiego 84, 59-220 Legnica, Poland", "latitude": 51.20109069999999, "longitude": 16.2147705, "status": "open", "meats": ["kurczak", "wołowina"], "sauces": ["czosnkowy", "ostry", "łagodny"], "opening_year": None, "closing_year": None, "craft_rating": False, "in_chain": False, "order_methods": "na miejscu, na wynos, odbiór na miejscu", "social_links": None, "logo": "https://glovoapp.com/static/img/maxi-kebab-logo.png", "google_rating": 4.6, "pyszne_rating": 0.0,"opening_hours": {
                "monday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "tuesday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "wednesday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "thursday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "friday": {
                    "open": "10:00",
                    "close": "23:00"
                },
                "saturday": {
                    "open": "10:00",
                    "close": "23:00"
                },
                "sunday": {
                    "open": "10:00",
                    "close": "20:00"
                }
            }},
            {"name": "Hallo Kebap Legnica", "location_details": "Stefana Czarnieckiego 19c, 59-220 Legnica, Poland", "latitude": 51.2116999, "longitude": 16.1752255, "status": "open", "meats": ["kurczak", "wołowina"], "sauces": ["czosnkowy", "ostry", "łagodny"], "opening_year": None, "closing_year": None, "craft_rating": False, "in_chain": False, "order_methods": "na miejscu, na wynos, odbiór na miejscu", "social_links": None, "logo": "https://glovoapp.com/static/img/hallo-kebap-logo.png", "google_rating": 3.8, "pyszne_rating": 0.0,"opening_hours": {
                "monday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "tuesday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "wednesday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "thursday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "friday": {
                    "open": "10:00",
                    "close": "23:00"
                },
                "saturday": {
                    "open": "10:00",
                    "close": "23:00"
                },
                "sunday": {
                    "open": "10:00",
                    "close": "20:00"
                }
            }},
                  {"name": "Piri-Piri Kebab Legnica", "location_details": "Szkolna 1, 59-220 Legnica, Poland", "latitude": 51.20413730000001, "longitude": 16.1606567, "status": "open", "meats": ["kurczak", "wołowina"], "sauces": ["czosnkowy", "ostry", "łagodny"], "opening_year": None, "closing_year": None, "craft_rating": False, "in_chain": True, "order_methods": "na miejscu, na wynos", "social_links": None, "logo": "https://glovoapp.com/static/img/piri-piri-logo.png", "google_rating": 3.7, "pyszne_rating": 0.0,"opening_hours": {
                "monday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "tuesday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "wednesday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "thursday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "friday": {
                    "open": "10:00",
                    "close": "23:00"
                },
                "saturday": {
                    "open": "10:00",
                    "close": "23:00"
                },
                "sunday": {
                    "open": "10:00",
                    "close": "20:00"
                }
            }},
            {"name": "AM AM Kebab", "location_details": "Wrocławska 155, 59-220 Legnica, Poland", "latitude": 51.20962660000001, "longitude": 16.1870814, "status": "open", "meats": ["kurczak", "wołowina", "falafel"], "sauces": ["czosnkowy", "ostry", "łagodny"], "opening_year": None, "closing_year": None, "craft_rating": False, "in_chain": True, "order_methods": "dostawa, na miejscu, na wynos, odbiór na miejscu", "social_links": None, "logo": "https://glovoapp.com/static/img/am-am-logo.png", "google_rating": 4.1, "pyszne_rating": 0.0,"opening_hours": {
                "monday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "tuesday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "wednesday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "thursday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "friday": {
                    "open": "10:00",
                    "close": "23:00"
                },
                "saturday": {
                    "open": "10:00",
                    "close": "23:00"
                },
                "sunday": {
                    "open": "10:00",
                    "close": "20:00"
                }
            }},
            {"name": "MIX Kebab", "location_details": "Wrocławska 23a, 59-220 Legnica, Poland", "latitude": 51.2092196, "longitude": 16.169304, "status": "open", "meats": None, "sauces": ["czosnkowy", "ostry", "łagodny"], "opening_year": None, "closing_year": None, "craft_rating": False, "in_chain": False, "order_methods": "dostawa, na miejscu, na wynos", "social_links": None, "logo": "https://glovoapp.com/static/img/mix-kebab-logo.png", "google_rating": 4.3, "pyszne_rating": 0.0,"opening_hours": {
                "monday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "tuesday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "wednesday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "thursday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "friday": {
                    "open": "10:00",
                    "close": "23:00"
                },
                "saturday": {
                    "open": "10:00",
                    "close": "23:00"
                },
                "sunday": {
                    "open": "10:00",
                    "close": "20:00"
                }
            }},
            {"name": "Kavovarka - kebab kraft", "location_details": "Górnicza 10B, 59-220 Legnica, Poland", "latitude": 51.2055278, "longitude": 16.1865556, "status": "open", "meats": ["kurczak", "wołowina"], "sauces": ["czosnkowy", "ostry", "łagodny"], "opening_year": None, "closing_year": None, "craft_rating": True, "in_chain": False, "order_methods": "dostawa, na miejscu, na wynos, odbiór na miejscu", "social_links": "http://www.kavovarka.pl/", "logo": "https://glovoapp.com/static/img/kavovarka-logo.png", "google_rating": 3.8, "pyszne_rating": 0.0,"opening_hours": {
                "monday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "tuesday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "wednesday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "thursday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "friday": {
                    "open": "10:00",
                    "close": "23:00"
                },
                "saturday": {
                    "open": "10:00",
                    "close": "23:00"
                },
                "sunday": {
                    "open": "10:00",
                    "close": "20:00"
                }
            }},
            {"name": "Zahir Kebab", "location_details": "Kolejowa 3, 59-222 Legnica, Poland", "latitude": 51.2123488, "longitude": 16.1686632, "status": "open", "meats": None, "sauces": ["czosnkowy", "ostry", "łagodny", "BBQ"], "opening_year": None, "closing_year": None, "craft_rating": False, "in_chain": True, "order_methods": "dostawa, na miejscu, na wynos", "social_links": "https://zahirkebab.pl/lokale/legnica/legnica-kolejowa/", "logo": "https://zahirkebab.pl/wp-content/uploads/2023/01/zahir-logo.jpg", "google_rating": 4, "pyszne_rating": 0.0,"opening_hours": {
                "monday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "tuesday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "wednesday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "thursday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "friday": {
                    "open": "10:00",
                    "close": "23:00"
                },
                "saturday": {
                    "open": "10:00",
                    "close": "23:00"
                },
                "sunday": {
                    "open": "10:00",
                    "close": "20:00"
                }
            }},
            {"name": "Zahir Kebab", "location_details": "Jaworzyńska 8, 52-220 Legnica, Poland", "latitude": 51.2042381, "longitude": 16.1602144, "status": "open", "meats": ["kurczak", "wołowina", "baranina"], "sauces": ["czosnkowy", "ostry", "łagodny", "BBQ"], "opening_year": None, "closing_year": None, "craft_rating": False, "in_chain": True, "order_methods": "dostawa, na miejscu, na wynos", "social_links": "https://zahirkebab.pl/lokale/legnica/legnica-jaworzynska/", "logo": "https://zahirkebab.pl/wp-content/uploads/2023/01/zahir-logo.jpg", "google_rating": 4, "pyszne_rating": 0.0,"opening_hours": {
                "monday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "tuesday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "wednesday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "thursday": {
                    "open": "10:00",
                    "close": "22:00"
                },
                "friday": {
                    "open": "10:00",
                    "close": "23:00"
                },
                "saturday": {
                    "open": "10:00",
                    "close": "23:00"
                },
                "sunday": {
                    "open": "10:00",
                    "close": "20:00"
                }
            }},
            {"name": "Rulo Kebab", "location_details": "Nowy Świat, 59-220 Legnica, Poland", "latitude": 51.2050912, "longitude": 16.1545148, "status": "closed", "meats": ["kurczak", "wołowina"], "sauces": ["czosnkowy", "ostry", "łagodny"], "opening_year": None, "closing_year": None, "craft_rating": False, "in_chain": False, "order_methods": "na miejscu", "social_links": "https://www.facebook.com/RuloKebab/", "logo": "https://glovoapp.com/static/img/rulo-kebab-logo.png", "google_rating": 3.6, "pyszne_rating": 0.0,"opening_hours": {
                "monday": {
                    "open": "00:00",
                    "close": "00:00"
                },
                "tuesday": {
                    "open": "00:00",
                    "close": "0:00"
                },
                "wednesday": {
                    "open": "00:00",
                    "close": "0:00"
                },
                "thursday": {
                    "open": "00:00",
                    "close": "0:00"
                },
                "friday": {
                    "open": "00:00",
                    "close": "0:00"
                },
                "saturday": {
                    "open": "00:00",
                    "close": "0:00"
                },
                "sunday": {
                    "open": "00:00",
                    "close": "00:00"
                }
            }},
        ]

        for kebab_data in kebabs_data:
            opening_hours_data = kebab_data.pop("opening_hours")  # Extract opening hours separately
            kebab, created = Kebab.objects.get_or_create(**kebab_data)

            if created:
                OpeningHour.objects.create(kebab=kebab, hours=opening_hours_data)
                self.stdout.write(self.style.SUCCESS(f'Successfully added {kebab.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'{kebab.name} already exists'))