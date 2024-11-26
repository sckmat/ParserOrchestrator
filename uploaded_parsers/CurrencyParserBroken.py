import requests
from datetime import datetime
import xml.etree.ElementTree as Et


class Parser:
    def __init__(self):
        self.date = datetime.now()
        self.url = f"https://www.cbr.ru/scripts/XML_XXXdaily.asp?date_req={self.date.strftime('%d/%m/%Y')}"

    def run(self):
        response = requests.get(self.url)
        response.raise_for_status()
        root = Et.fromstring(response.content)

        rates = {}
        for currency in root.findall("Valute"):
            code = currency.find("CharCode").text
            nominal = int(currency.find("Nominal").text)
            name = currency.find("Name").text
            value = float(currency.find("Value").text.replace(",", "."))

            rates[code] = {
                "name": name,
                "nominal": nominal,
                "rate": value
            }

        return {
            "date": self.date.strftime('%Y-%m-%d'),
            "rates": rates
        }
