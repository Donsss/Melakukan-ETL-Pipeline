import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
from utils.load import store_to_mysql, store_to_csv, store_to_spreedsheet

# Sample data untuk testing
SAMPLE_DATA = pd.DataFrame({
    'Title': ['Kemeja', 'Celana Jeans'],
    'Price': [150000, 450000],
    'Rating': [4.2, 4.5],
    'Colors': [5, 3],
    'Size': ['M', 'L'],
    'Gender': ['Unisex', 'Male'],
    'Timestamp': ['2023-05-01T12:00:00', '2023-05-01T12:05:00']
})

# Test untuk store_to_mysql
@patch('utils.load.create_engine')
def test_store_to_mysql_success(mock_engine):
    """Test penyimpanan ke MySQL berhasil"""
    mock_con = MagicMock()
    mock_engine.return_value.connect.return_value.__enter__.return_value = mock_con
    
    mock_to_sql = MagicMock()
    pd.DataFrame.to_sql = mock_to_sql
    
    db_url = "mysql+mysqlconnector://user:pass@localhost:5432/db"
    store_to_mysql(SAMPLE_DATA, db_url)
    
    mock_engine.assert_called_once_with(db_url)
    mock_to_sql.assert_called_once_with(
        'bfpd', 
        con=mock_con, 
        if_exists='append', 
        index=False
    )

@patch('utils.load.create_engine')
def test_store_to_mysql_failure(mock_engine):
    """Test penyimpanan ke mysqlSQL gagal"""
    mock_engine.side_effect = Exception("Connection failed")
    
    db_url = "mysql+mysqlconnector://user:pass@localhost:5432/db"
    store_to_mysql(SAMPLE_DATA, db_url)
    
    mock_engine.assert_called_once_with(db_url)

# Test untuk store_to_csv
@patch('pandas.DataFrame.to_csv')
def test_store_to_csv_success(mock_to_csv):
    """Test penyimpanan ke CSV berhasil"""
    store_to_csv(SAMPLE_DATA)
    
    mock_to_csv.assert_called_once_with(
        'fashion_data.csv', 
        index=False
    )

@patch('pandas.DataFrame.to_csv')
def test_store_to_csv_failure(mock_to_csv):
    """Test penyimpanan ke CSV gagal"""
    mock_to_csv.side_effect = Exception("Write failed")

    store_to_csv(SAMPLE_DATA)
    
    mock_to_csv.assert_called_once_with(
        'fashion_data.csv', 
        index=False
    )

@patch('utils.load.Credentials.from_service_account_file')
@patch('utils.load.build')
def test_store_to_spreedsheet_success(mock_build, mock_cred):
    """Test penyimpanan ke Google Sheets berhasil"""
    mock_service = MagicMock()
    mock_sheet = MagicMock()
    mock_result = MagicMock()
    
    mock_cred.return_value = "credentials"
    mock_build.return_value = mock_service
    mock_service.spreadsheets.return_value = mock_sheet
    mock_sheet.values.return_value.append.return_value.execute.return_value = mock_result
    
    store_to_spreedsheet(SAMPLE_DATA)
    
    # Perbaikan: Sesuaikan dengan path di kode utama
    mock_cred.assert_called_once_with(
        './google-sheets-api.json',  # Diubah sesuai kode utama
        scopes=['https://www.googleapis.com/auth/spreadsheets']
    )
    
    expected_values = [
        ['Title', 'Price', 'Rating', 'Colors', 'Size', 'Gender', 'Timestamp'],
        ['Kemeja', 150000, 4.2, 5, 'M', 'Unisex', '2023-05-01T12:00:00'],
        ['Celana Jeans', 450000, 4.5, 3, 'L', 'Male', '2023-05-01T12:05:00']
    ]
    
    mock_sheet.values.return_value.append.assert_called_once_with(
        spreadsheetId='1mYb2HVAmiUnBmjNQF3U7GGItsfSEnJvdsDymKey2bpk',
        range='Sheet1!A1:G',
        valueInputOption='RAW',
        body={'values': expected_values}
    )

@patch('utils.load.Credentials.from_service_account_file')
def test_store_to_spreedsheet_failure(mock_cred):
    """Test penyimpanan ke Google Sheets gagal"""
    mock_cred.side_effect = Exception("Authentication failed")

    store_to_spreedsheet(SAMPLE_DATA)
    
    mock_cred.assert_called_once_with(
        './google-sheets-api.json',
        scopes=['https://www.googleapis.com/auth/spreadsheets']
    )