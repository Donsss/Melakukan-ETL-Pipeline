from utils.extract import scrape_fashion
from utils.transform import transform_data, transform_to_DataFrame
from utils.load import store_to_mysql, store_to_csv, store_to_spreedsheet

def main():
    """Fungsi utama untuk keseluruhan proses scraping hingga menyimpannya."""
    BASE_URL = 'https://fashion-studio.dicoding.dev/page{}'
    all_fashions_data = scrape_fashion(BASE_URL)
    dataframe = transform_to_DataFrame(all_fashions_data)
    dataframe = transform_data(dataframe, 16000)
    
    #koneksi ke Database
    db_url = 'mysql+mysqlconnector://root:@localhost/dicoding'

    #Menyimpan data
    store_to_mysql(dataframe, db_url)
    store_to_csv(dataframe)
    store_to_spreedsheet(dataframe)
 
 
if __name__ == '__main__':
    main()