import pytest
import pandas as pd
import numpy as np
from utils.transform import transform_to_DataFrame, transform_data

SAMPLE_DATA = [
    {
        "Title": "Kemeja",
        "Price": "$10.99",
        "Rating": "4.2/5",
        "Colors": "5",
        "Size": "M",
        "Gender": "Unisex",
        "Timestamp": "2023-05-01T12:00:00"
    },
    {
        "Title": "jeans",
        "Price": "$29.99",
        "Rating": "4.5/5",
        "Colors": "3",
        "Size": "L",
        "Gender": "Male",
        "Timestamp": "2023-05-01T12:05:00"
    }
]

# Test untuk transform_to_DataFrame
def test_transform_to_DataFrame_success():
    """Test berhasil mengubah list of dict ke DataFrame"""
    result = transform_to_DataFrame(SAMPLE_DATA)
    
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2
    assert list(result.columns) == [
        "Title", "Price", "Rating", "Colors", "Size", "Gender", "Timestamp"
    ]

def test_transform_to_DataFrame_empty_data():
    """Test dengan data kosong"""
    result = transform_to_DataFrame([])
    assert result is None

def test_transform_to_DataFrame_invalid_data():
    """Test dengan data tidak valid"""
    result = transform_to_DataFrame("bukan_list_atau_dict")
    assert result is None

# Test untuk transform_data
def test_transform_data_success():
    """Test transformasi data berhasil"""
    exchange_rate = 16000
    df = pd.DataFrame(SAMPLE_DATA)
    
    result = transform_data(df.copy(), exchange_rate)
    
    # Test transformasi Rating
    assert result['Rating'].dtype == float
    assert result['Rating'].tolist() == [4.2, 4.5]
    
    # Test transformasi Price
    assert result['Price'].dtype == float
    expected_prices = [10.99 * exchange_rate, 29.99 * exchange_rate]
    assert result['Price'].tolist() == pytest.approx(expected_prices)
    
    # Test tidak ada data hilang atau duplikat
    assert result.isna().sum().sum() == 0
    assert len(result) == 2

def test_transform_data_with_missing_values():
    """Test dengan data yang ada nilai kosong"""
    exchange_rate = 15000
    incomplete_data = SAMPLE_DATA.copy()
    incomplete_data.append({
        "Title": "Jaket",
        "Price": None,
        "Rating": "3.8/5",
        "Colors": "2",
        "Size": "XL",
        "Gender": "Female",
        "Timestamp": "2023-05-01T12:10:00"
    })
    df = pd.DataFrame(incomplete_data)
    
    result = transform_data(df.copy(), exchange_rate)
    
    assert len(result) == 2
    assert "Jaket" not in result['Title'].values

def test_transform_data_with_duplicates():
    """Test dengan data duplikat"""
    exchange_rate = 16000
    duplicate_data = SAMPLE_DATA.copy()
    duplicate_data.append(SAMPLE_DATA[0])
    df = pd.DataFrame(duplicate_data)
    
    result = transform_data(df.copy(), exchange_rate)
    
    assert len(result) == 2

def test_transform_data_invalid_rating_format():
    """Test dengan format rating tidak valid"""
    exchange_rate = 15000
    invalid_data = SAMPLE_DATA.copy()
    invalid_data[0]["Rating"] = "Not Rated" 
    df = pd.DataFrame(invalid_data)
    
    result = transform_data(df.copy(), exchange_rate)
    
    assert len(result) == 1
    assert result['Title'].tolist() == ["jeans"]

def test_transform_data_invalid_price_format():
    """Test dengan format harga tidak valid"""
    exchange_rate = 16000
    invalid_data = SAMPLE_DATA.copy()
    invalid_data[0]["Price"] = "Harga Tidak Valid" 
    df = pd.DataFrame(invalid_data)
    
    result = transform_data(df.copy(), exchange_rate)
    
    assert len(result) == 1
    assert result['Title'].tolist() == ["jeans"]

def test_transform_data_empty_dataframe():
    """Test dengan DataFrame kosong"""
    exchange_rate = 16000
    df = pd.DataFrame([])
    
    result = transform_data(df.copy(), exchange_rate)
    assert result is None

def test_transform_data_invalid_input_type():
    """Test dengan input bukan DataFrame"""
    exchange_rate = 16000
    
    result = transform_data("bukan_dataframe", exchange_rate)
    assert result is None