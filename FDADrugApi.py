import os
import requests
from dotenv import load_dotenv

load_dotenv()

FDA_API_KEY = os.getenv("FDA_API_KEY")  # Remember .env file!


# TODO: set a final variable for the number of searches and interactions with other drugs

def get_drug_name(api_key, search, limit):
    url = "https://api.fda.gov/drug/event.json?"
    params = {
        "api_key": api_key,
        "search": search,
        "limit": limit,
        "count": "patient.drug.openfda.brand_name.exact"
    }
    response = requests.get(url=url, params=params)
    return response.json()


def get_form(api_key, search, limit):
    url = "https://api.fda.gov/drug/event.json?"
    params = {
        "api_key": api_key,
        "search": search,
        "limit": limit,
        "count": "patient.drug.drugdosageform.exact"
    }
    response = requests.get(url=url, params=params)
    return response.json()


def get_ingredients(api_key, search, limit):
    url = "https://api.fda.gov/drug/label.json?"
    params = {
        "api_key": api_key,
        "search": "drug_interactions:" + search,
        "limit": limit,
        "count": "openfda.substance_name.exact"
    }
    response = requests.get(url=url, params=params)
    return response.json()


def get_drug_reaction(api_key, search, limit):
    url = "https://api.fda.gov/drug/event.json?"
    params = {
        "api_key": api_key,
        "search": "patient.drug.openfda.pharm_class_epc:" + search,
        "limit": limit,
        "count": "patient.reaction.reactionmeddrapt.exact"
    }
    response = requests.get(url=url, params=params)
    return response.json()


def convert_list(response, length, term):
    addList = list()
    addList.append((response[0][term]).lower())
    if length > 1:
        for i in (1, length - 1, 1):
            addList.append((response[i][term]).lower())
    addList = list(set(addList))  # conversion into a set then into a list for duplicates
    return addList


search_number = 3
form = get_form(FDA_API_KEY, "nonsteroidal+anti-inflammatory+drug", search_number)
form_list = convert_list(form["results"], search_number, "term")

reactions = get_drug_reaction(FDA_API_KEY, "nonsteroidal+anti-inflammatory+drug", 5)  # number of results
reaction_list = convert_list(reactions["results"], 5, "term")

name = get_drug_name(FDA_API_KEY, "nonsteroidal+anti-inflammatory+drug", 1)
name_list = convert_list(name["results"], 1, "term")

ingredients = get_ingredients(FDA_API_KEY, "nonsteroidal+anti-inflammatory+drug", 1)
ingredients_list = convert_list(ingredients["results"], 1, "term")

print("A good brand for this product: ", name_list)
print("Forms of use: ", form_list)
print("Side effects: ", reaction_list)
print("Ingredients: ", ingredients_list)
