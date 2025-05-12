import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook

url = "https://bina.az/baki/alqi-satqi/menziller/4-otaqli"

headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

wb = Workbook()
ws = wb.active
ws.title = "Flat Listings"
ws.append(["Location", "Price","Datetime"])

flats = soup.find_all("div", class_="items-i")

for flat in flats:
    location = flat.find("div", class_="location")
    price = flat.find("div", class_="price")
    datetime = flat.find("div", class_="city_when")

    ws.append([
        location.get_text(strip=True) if location else "",
        price.get_text(strip=True) if price else "",
        datetime.get_text(strip=True) if datetime else ""
    ])


wb.save("flat.xlsx")
print("Done: flat.xlsx")
