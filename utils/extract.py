import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}
    
def fetching_content(url):
    """Mengambil konten HTML dari URL yang diberikan."""
    session = requests.Session()
    try:
        response = session.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Terjadi kesalahan ketika melakukan requests terhadap {url}: {e}")
        return None
 
 
def extract_fashion_data(article):
    """Mengambil data fashion berupa judul, harga, ketersediaan, dan rating dari article (element HTML)."""
    try:
        fashion_title = article.find('h3').text
        price = article.find(class_='price').text
        rating = article.find('p', string=lambda x: x and 'Rating:' in x).text.split(': ')[1]
        colors = article.find('p', string=lambda x: x and 'Colors' in x).text.split(' ')[0]
        size = article.find('p', string=lambda x: x and 'Size:' in x).text.split(': ')[1]
        gender = article.find('p', string=lambda x: x and 'Gender:' in x).text.split(': ')[1]

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        fashions = {
            "Title": fashion_title,
            "Price": price,
            "Rating": rating,
            "Colors": colors,
            "Size": size,
            "Gender": gender,
            "Timestamp": timestamp,
        }

        return fashions

    except AttributeError as e:
        print(f"Kesalahan saat mengekstrak data: {e}")
        return None

    except Exception as e:
        print(f"Terjadi Kesalahan: {e}")
        return None


def clean_data(fashion_data):
    """Membersihkan data fashion dengan menghapus nilai yang tidak valid."""
    try:
        dirty_patterns = {
            "Title": ["Unknown Product"],
            "Rating": ["⭐ Invalid Rating / 5", "Not Rated"],
            "Price": ["Price Unavailable", None]
        }

        for column, invalid_values in dirty_patterns.items():
            if fashion_data.get(column) in invalid_values:
                return None
        
        return fashion_data

    except Exception as e:
        print(f"Kesalahan saat membersihkan data: {e}")
        return None 

def scrape_fashion(base_url, start_page=2, delay=2):
    """Fungsi utama untuk mengambil keseluruhan data, mulai dari requests hingga menyimpannya dalam variabel data."""
    data = []

    initial_url = 'https://fashion-studio.dicoding.dev/'
    print(f"Scraping halaman awal: {initial_url}")
    content = fetching_content(initial_url)
    if content:
        soup = BeautifulSoup(content, "html.parser")
        articles_element = soup.find_all('div', class_='product-details')
        for article in articles_element:
          fashion = extract_fashion_data(article)
          cleaned_fashion = clean_data(fashion)
          if cleaned_fashion:
              data.append(cleaned_fashion)

    page_number = start_page
 
    while True:
        url = base_url.format(page_number)
        print(f"Scraping halaman: {url}")
 
        content = fetching_content(url)
        if content:
            soup = BeautifulSoup(content, "html.parser")
            articles_element = soup.find_all('div', class_='product-details')
            for article in articles_element:
              fashion = extract_fashion_data(article)
              cleaned_fashion = clean_data(fashion)
              if cleaned_fashion:
                  data.append(cleaned_fashion)
 
            next_button = soup.find('li', class_='page-item next')
            if next_button:
                page_number += 1
                time.sleep(delay)
            else:
                break
        else:
            break
 
    return data
 
