import requests
from bs4 import BeautifulSoup
import time
import argparse

import sys

headers = {
    "User-Agent": "my_scraper/1.0"
}

TARGET_PARAMS = [
    "SKU", 
    "BRAND", 
    "Manufacturer Number", 
    "Caliber", 
    "Model", 
    "Rounds", 
    "Unit of Measure", 
    "Classification"
]

def get_parameters(url):
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Chyba při stahování stránky: HTTP {response.status_code}", file=sys.stderr)
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    name_elem = soup.find('h1', class_='productView-title')
    price_elem = soup.find('span', class_='price price--withoutTax')

    name = name_elem.get_text(strip=True) if name_elem else "Název nebyl nalezen"
    price = price_elem.get_text(strip=True) if price_elem else "Cena nebyla nalezena"

    params = {}
    paramTable = soup.find('dl', class_='productView-info')
    if paramTable:
        for dt in paramTable.find_all('dt'):
            next = dt.find_next_sibling()
            if next and next.name == 'dd' and dt.get_text(strip=True) and next.get_text(strip=True):
                params[dt.get_text(strip=True).replace(":", "")] = next.get_text(strip=True)

    extracted_values = [params.get(param, "") for param in TARGET_PARAMS]

    return [url, name, price] + extracted_values

def main():
    # získání argumentu pro testovací režim
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', action='store_true', help='Aktivuje testovací režim, který zpracuje pouze prvních 10 URL.')
    args = parser.parse_args()

    # načtení URL adres z stdin
    urls = sys.stdin.read().strip().splitlines()

    if args.test:
        urls = urls[:10]

    # zpracování každé URL a získání parametrů
    for i, url in enumerate(urls, 1):
        result = get_parameters(url)
        if result is not None:
            print("\t".join(str(val) for val in result))

        #print(f"\nZpracováno URL: {i}", file=sys.stderr)

if __name__ == "__main__":
    main()