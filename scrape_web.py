import requests
from bs4 import BeautifulSoup

drug_name = input("Enter the drug name: ")
url = f"https://www.cvs.com/search/?query={drug_name}"

response = requests.get(url)

soup = BeautifulSoup(response.content, "html.parser")

# Example code to extract price, brand, stock status, and shipping information
price = soup.find("span", class_="product-price").text
brand = soup.find("div", class_="product-brand").text
stock_status = soup.find("span", class_="stock-status").text
shipping_info = soup.find("div", class_="shipping-info").text

print(f"Price: {price}")
print(f"Brand: {brand}")
print(f"Stock Status: {stock_status}")
print(f"Shipping Information: {shipping_info}")
