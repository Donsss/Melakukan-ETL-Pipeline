import pytest
import requests
from unittest.mock import patch, Mock
from bs4 import BeautifulSoup
from datetime import datetime
from utils.extract import fetching_content, extract_fashion_data, clean_data, scrape_fashion, HEADERS


SAMPLE_ARTICLE_HTML = """
<div class="product-details">
    <h3>Thsirt 123</h3>
    <p class="price">$49.99</p>
    <p>Rating: 4.7/5</p>
    <p>4 Colors</p>
    <p>Size: M</p>
    <p>Gender: Men</p>
</div>
"""

INVALID_ARTICLE_HTML = """
<div class="product-details">
    <h3>Unknown Product</h3>
    <p class="price">Price Unavailable</p>
    <p>Rating: Not Rated</p>
</div>
"""

@patch('utils.extract.requests.Session')
def test_fetching_content_success(mock_session):
    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.content = b"<html>content</html>"
    mock_session.return_value.get.return_value = mock_response
    
    result = fetching_content("http://test.com")
    assert result == b"<html>content</html>"

@patch('utils.extract.requests.Session')
def test_fetching_content_failure(mock_session):
    mock_session.return_value.get.side_effect = requests.exceptions.RequestException("Request failed")
    
    result = fetching_content("http://test.com")
    assert result is None

def test_extract_fashion_data_success():
    soup = BeautifulSoup(SAMPLE_ARTICLE_HTML, 'html.parser')
    article = soup.find('div', class_='product-details')
    result = extract_fashion_data(article)
    
    assert result == {
        "Title": "Thsirt 123",
        "Price": "$49.99",
        "Rating": "4.7/5",
        "Colors": "4",
        "Size": "M",
        "Gender": "Men",
        "Timestamp": result["Timestamp"] 
    }
    
    datetime.strptime(result["Timestamp"], "%Y-%m-%d %H:%M:%S")

def test_extract_fashion_data_invalid():
    soup = BeautifulSoup(INVALID_ARTICLE_HTML, 'html.parser')
    article = soup.find('div', class_='product-details')
    result = extract_fashion_data(article)
    assert result is None

def test_extract_fashion_data_missing_element():
    soup = BeautifulSoup("<div></div>", 'html.parser')
    article = soup.find('div')
    result = extract_fashion_data(article)
    assert result is None

def test_clean_data_valid():
    valid_data = {
        "Title": "Valid Product",
        "Price": "$19.99",
        "Rating": "4/5",
        "Colors": "3",
        "Size": "S",
        "Gender": "Female",
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    result = clean_data(valid_data)
    assert result == valid_data

def test_clean_data_invalid_title():
    invalid_data = {
        "Title": "Unknown Product",
        "Price": "$19.99",
        "Rating": "4/5",
        "Colors": "3",
        "Size": "S",
        "Gender": "Female",
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    result = clean_data(invalid_data)
    assert result is None

def test_clean_data_invalid_price():
    invalid_data = {
        "Title": "Valid Product",
        "Price": "Price Unavailable",
        "Rating": "4/5",
        "Colors": "3",
        "Size": "S",
        "Gender": "Female",
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    result = clean_data(invalid_data)
    assert result is None

def test_clean_data_invalid_rating():
    invalid_data = {
        "Title": "Valid Product",
        "Price": "$19.99",
        "Rating": "Not Rated",
        "Colors": "3",
        "Size": "S",
        "Gender": "Female",
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    result = clean_data(invalid_data)
    assert result is None

@patch('utils.extract.fetching_content')
@patch('utils.extract.time.sleep')
def test_scrape_fashion(mock_sleep, mock_fetch):

    mock_soup_initial = BeautifulSoup("""
        <html>
            <div class="product-details">
                <h3>Product 0</h3>
                <p class="price">$5.00</p>
                <p>Rating: 3/5</p>
                <p>1 Colors</p>
                <p>Size: M</p>
                <p>Gender: Unisex</p>
            </div>
        </html>
    """, 'html.parser')
    
    mock_soup1 = BeautifulSoup("""
        <html>
            <div class="product-details">
                <h3>Product 1</h3>
                <p class="price">$10.00</p>
                <p>Rating: 5/5</p>
                <p>2 Colors</p>
                <p>Size: L</p>
                <p>Gender: Male</p>
            </div>
            <li class="page-item next"></li>
        </html>
    """, 'html.parser')

    mock_soup2 = BeautifulSoup("""
        <html>
            <div class="product-details">
                <h3>Product 2</h3>
                <p class="price">$20.00</p>
                <p>Rating: 4/5</p>
                <p>3 Colors</p>
                <p>Size: S</p>
                <p>Gender: Female</p>
            </div>
        </html>
    """, 'html.parser')

    mock_fetch.side_effect = [
        str(mock_soup_initial).encode(),
        str(mock_soup1).encode(),
        str(mock_soup2).encode()
    ]
    
    result = scrape_fashion("http://test.com/page-{}", start_page=2, delay=2)
    
    assert len(result) == 3
    assert result[0]["Title"] == "Product 0"
    assert result[1]["Title"] == "Product 1"
    assert result[2]["Title"] == "Product 2"
    mock_sleep.assert_called_once_with(2)

@patch('utils.extract.fetching_content')
def test_scrape_fashion_failure(mock_fetch):
    mock_fetch.return_value = None
    result = scrape_fashion("http://test.com/page-{}")
    assert result == []