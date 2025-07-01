from sqlalchemy import create_engine
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
 
def store_to_mysql(data, db_url):
    """Fungsi untuk menyimpan data ke dalam MYSQL."""
    try:
        # Membuat engine database
        engine = create_engine(db_url)
        
        # Menyimpan data ke tabel 'bfpd' jika tabel sudah ada, data akan ditambahkan (append)
        with engine.connect() as con:
            data.to_sql('bfpd', con=con, if_exists='append', index=False)
            print("Data berhasil ditambahkan Ke dalam Database!")
    
    except Exception as e:
        print(f"Terjadi kesalahan saat menyimpan data: {e}")

def store_to_csv(data):
    """Fungsi untuk menyimpan data ke dalam CSV."""
    try:
        data.to_csv('fashion_data.csv', index=False)
        print("Data berhasil ditambahkan Ke format  CSV!")
    
    except Exception as e :
        print(f"Terjadi kesalahan saat menyimpan data: {e}")

def store_to_spreedsheet(data):
    """Fungsi untuk menyimpan data ke dalam Spreedsheet."""
    try:
        SERVICE_ACCOUNT_FILE = './google-sheets-api.json'
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

        credential = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

        SPREADSHEET_ID = '1mYb2HVAmiUnBmjNQF3U7GGItsfSEnJvdsDymKey2bpk'
        RANGE_NAME = 'Sheet1!A1:G'
        
        # Membangun layanan API Google Sheets
        service = build('sheets', 'v4', credentials=credential)
        sheet = service.spreadsheets()

         # Mengonversi DataFrame menjadi list dan Mengambil header kolom
        values = data.values.tolist()
        header = data.columns.tolist()
        values.insert(0, header) 

        body = {
            'values': values
        }

        # Mengirim permintaan untuk menambah data ke Google Sheets
        result = sheet.values().append(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME,
            valueInputOption='RAW',
            body=body
        ).execute()

        print("Data berhasil disimpan ke Google Sheets!")

    except Exception as e :
        print(f"Terjadi kesalahan saat menyimpan data: {e}")