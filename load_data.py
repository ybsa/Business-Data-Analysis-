import pandas as pd
import sqlite3
import os
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("data_loading.log"),
        logging.StreamHandler()
    ]
)

DATA_DIR = r"C:\Users\wind xebec\Downloads\Buiness Data\data"
DB_PATH = "inventory_sales.db"

def load_csv_to_sqlite(csv_name, table_name, chunksize=None):
    csv_path = os.path.join(DATA_DIR, csv_name)
    if not os.path.exists(csv_path):
        logging.error(f"File not found: {csv_path}")
        return

    logging.info(f"Starting to load {csv_name} into table '{table_name}'...")
    
    conn = sqlite3.connect(DB_PATH)
    
    try:
        if chunksize:
            chunk_count = 0
            for chunk in pd.read_csv(csv_path, chunksize=chunksize):
                chunk_count += 1
                chunk.to_sql(table_name, conn, if_exists='append' if chunk_count > 1 else 'replace', index=False)
                logging.info(f"Loaded chunk {chunk_count} of {csv_name}")
        else:
            df = pd.read_csv(csv_path)
            df.to_sql(table_name, conn, if_exists='replace', index=False)
            logging.info(f"Successfully loaded {csv_name} (Rows: {len(df)})")
            
    except Exception as e:
        logging.error(f"Error loading {csv_name}: {e}")
    finally:
        conn.close()

def main():
    logging.info("Starting data loading process...")
    
    # Define files and their target tables
    files_map = {
        "begin_inventory.csv": "begin_inventory",
        "end_inventory.csv": "end_inventory",
        "purchase_prices.csv": "purchase_prices",
        "purchases.csv": "purchases",
        "vendor_invoice.csv": "vendor_invoice",
        "sales.csv": "sales" 
    }
    
    for csv_file, table_name in files_map.items():
        # Use chunking for large files
        if csv_file in ["sales.csv", "purchases.csv"]:
             load_csv_to_sqlite(csv_file, table_name, chunksize=100000)
        else:
             load_csv_to_sqlite(csv_file, table_name)

    logging.info("Data loading process completed.")

if __name__ == "__main__":
    main()
