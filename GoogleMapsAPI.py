import os
import requests
from dotenv import load_dotenv

load_dotenv()

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")  # Remember .env file!


# TODO fix accessing google maps API (might need to type into URL without params

def get_address(key, search):
    url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?"
    params = {
        "key": key,
        "input": search,
        "fields": "formatted_address%2Cname%2Copening_hours%2Cgeometry",
        "inputtype": "textquery"
    }
    response = requests.get(url=url, params=params)
    return response.json()


address = get_address(GOOGLE_MAPS_API_KEY, "Museum%20of%20Contemporary%20Art%20Australia")

print(address)
