import os
import requests
from dotenv import load_dotenv

load_dotenv()

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")  # Remember .env file!


# TODO Appending not working for the time table

def get_id(key, search):
    url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?"
    params = {
        "key": key,
        "input": search,
        "inputtype": "textquery"
    }
    response = requests.get(url=url, params=params)
    return response.json()


def get_place(key, search_id):
    url = "https://maps.googleapis.com/maps/api/place/details/json?"
    params = {
        "key": key,
        "place_id": search_id
    }
    response = requests.get(url=url, params=params)
    return response.json()


def get_times(key, search_id):
    url = "https://maps.googleapis.com/maps/api/place/details/json?"
    params = {
        "key": key,
        "fields": "current_opening_hours/weekday_text",
        "place_id": search_id
    }
    response = requests.get(url=url, params=params)
    return response.json()


def reformat_string(list_input, term):
    results = list_input[term]
    return results


def compile_hours_list(list_input, time):  # weekdays versus weekends
    compiled_list = list()
    for i in range(time - 1):
        day_times = list_input[i]
        day_times_list = ""
        for a in range(len(day_times)):
            if day_times[a] == "'\'":
                day_times_list = day_times_list + " "
                a += 6
            day_times_list = day_times_list + day_times[a]
        print(day_times_list)
        compiled_list.append(day_times_list)
    return compiled_list


place_id = get_id(GOOGLE_MAPS_API_KEY, "Wallgreens")
place_id_string = reformat_string(place_id["candidates"][0], "place_id")
place = get_place(GOOGLE_MAPS_API_KEY, place_id_string)

address_string = reformat_string(place["result"], "formatted_address")
phone_number_string = reformat_string(place["result"], "international_phone_number")  # might not work for everywhere
# hours_string = compile_hours_list(place["results"]["opening_hours"], "periods", 7)
is_open = place["result"]["opening_hours"]["open_now"]
times = get_times(GOOGLE_MAPS_API_KEY, place_id_string)
times_list = compile_hours_list(times["result"]["current_opening_hours"]["weekday_text"], 7)

print("Closest location: ", address_string)
print("Phone number: ", phone_number_string)
print("Times: ", times_list)

if is_open == "True":
    print("The location is  open at this time")
else:
    print("The location is not open at this time")
