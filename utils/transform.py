import pandas as pd

def transform_to_DataFrame(data):
    """Mengubah data menjadi DataFrame."""
    try:
        if not data:  # Jika data kosong (empty list atau None)
            return None
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        return None

def transform_data(data, exchange_rate):
    """Menggabungkan semua transformasi data menjadi satu fungsi."""
    try:
        if data.empty:
            return None
            
        # Copy dataframe untuk menghindari SettingWithCopyWarning
        df = data.copy()
        
        # Transform Rating
        df['Rating'] = df['Rating'].str.extract(r'(\d+\.\d+)').astype(float)
        
        # Transform Price - akan menghasilkan NaN untuk format tidak valid
        df['Price'] = df['Price'].replace({'\$': '', '[^\d.]': ''}, regex=True)
        df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
        df['Price'] = df['Price'] * exchange_rate
        
        # Hapus baris dengan nilai NaN (data invalid)
        df = df.dropna()
        
        # Hapus duplikat
        df = df.drop_duplicates()
        
        return df if not df.empty else None
        
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        return None