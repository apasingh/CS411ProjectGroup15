import os
import requests
from dotenv import load_dotenv

load_dotenv()

FDA_API_KEY = os.getenv("FDA_API_KEY")  # Remember .env file!


# TODO: connect this to google maps for location (manufacture name)

# def get_drug_name(api_key, search, limit):
#     url = "https://api.fda.gov/drug/event.json?"
#     params = {
#         "api_key": api_key,
#         "search": search,
#         "limit": limit,
#         "count": "patient.drug.openfda.brand_name.exact"
#     }
#     response = requests.get(url=url, params=params)
#     return response.json()


def get_drug(api_key, search, limit):
    url = "https://api.fda.gov/drug/label.json?"
    params = {
        "api_key": api_key,
        "search": search,
        "limit": limit,
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


#
#
# def get_ingredients(api_key, search, limit):
#     url = "https://api.fda.gov/drug/label.json?"
#     params = {
#         "api_key": api_key,
#         "search": "drug_interactions:" + search,
#         "limit": limit,
#         "count": "active_ingredient"
#     }
#     response = requests.get(url=url, params=params)
#     return response.json()
#
#

def get_patient_drug_reaction(api_key, search, limit):
    url = "https://api.fda.gov/drug/event.json?"
    params = {
        "api_key": api_key,
        "search": search,
        "limit": limit,
        "count": "patient.reaction.reactionmeddrapt.exact"
    }
    response = requests.get(url=url, params=params)
    return response.json()


#
#
def convert_list(response, term, length):
    addList = list()
    addList.append((response[0][term]).lower().capitalize())
    if length > 1:
        for i in (1, length - 1, 1):
            addList.append((response[i][term]).lower().capitalize())
    addList = list(set(addList))  # conversion into a set then into a list for duplicates
    return addList


class_name = "advil"
search_number = 3

drug = get_drug(FDA_API_KEY, class_name, 1)["results"][0]

# noinspection PyBroadException
try:
    do_not_use = ", ".join(drug["do_not_use"])
except Exception as e:
    do_not_use = ""

# noinspection PyBroadException
try:
    warning = drug["warnings"]
except Exception as e:
    warning = drug["boxed_warning"]

warning_string = ', '.join(warning)

# noinspection PyBroadException
try:
    brand_name = " ".join(drug["openfda"]["brand_name"])
except Exception as e:
    brand_name = class_name

form = get_form(FDA_API_KEY, class_name, search_number)
form_list_string = convert_list(form["results"], "term", search_number)

reactions = get_patient_drug_reaction(FDA_API_KEY, class_name, 5)["results"]  # number of results
reaction_list = convert_list(reactions, "term", 5)

print("Best product name:", brand_name)

# print("This is known as: ", name_list)
print("Forms of use:", ', '.join(form_list_string))

if do_not_use != "":
    print("\n--[Important]--\n" + do_not_use)

print("\n--[Warnings]--\n" + warning_string[9:len(warning_string)])

print("\n--[Reported Side Effects]--\n" + ", ".join(reaction_list))
# print("Ingredients: ", ingredients_list)