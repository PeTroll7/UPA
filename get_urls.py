import requests
from bs4 import BeautifulSoup
import time

import sys

base_url = "https://www.impactguns.com/handguns/?page={}"

headers = {
    "User-Agent": "my_scraper/1.0"
}

product_urls = set()
page = 1

#print("Začínám stahovat URL adresy produktů...", file=sys.stderr)

while len(product_urls) < 150:
    #print(f"Stahuji stránku {page}...", file=sys.stderr)
    url = base_url.format(page)
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            #print(f"Chyba při stahování stránky: HTTP {response.status_code}", file=sys.stderr)
            break
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        links = soup.find_all('a', class_='card-figure__link')
        
        if not links:
            #print("Nebyly nalezeny žádné další produkty (pravděpodobně konec katalogu).", file=sys.stderr)
            break
            
        for link in links:
            href = link.get('href')
            if href:
                product_urls.add(href)
                    
        page += 1
        
        if len(product_urls) < 150:
            #print("Čekám 10 vteřin podle pravidla Crawl-delay z robots.txt...", file=sys.stderr)
            time.sleep(10)
            
    except Exception as e:
        print(f"Nastala chyba: {e}", file=sys.stderr)
        break

# Převod množiny na list
final_urls = list(product_urls)

for url in final_urls:
    print(url)

#print(f"Hotovo! Získáno {len(final_urls)} unikátních URL adres a uloženo do souboru urls.txt.", file=sys.stderr)