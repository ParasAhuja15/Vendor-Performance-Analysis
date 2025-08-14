import pandas as pd
import os
from sqlalchemy import create_engine
import logging
import time

# Create logs folder
logs_dir = '/kaggle/working/logs'
os.makedirs(logs_dir, exist_ok=True)
print(f"Logs folder created at: {logs_dir}")

# Configure logging
log_file = os.path.join(logs_dir, 'ingestion.log')
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    force=True
)

# Database connection
db_path = '/kaggle/working/vendor_dataset.db'
engine = create_engine(f'sqlite:///{db_path}')

# Data directory
data_dir = '/kaggle/input/vendor-dataset-analytics-project/data'

def ingest_db(df, table_name, engine):
    df.to_sql(table_name, con=engine, if_exists='replace', index=False)

def load_raw_data():
    start = time.time()
    
    for file in os.listdir(data_dir):
        if file.endswith('.csv'):
            file_path = os.path.join(data_dir, file)
            df = pd.read_csv(file_path)
            logging.info(f'Ingesting {file} into database')
            print(file, df.shape)
            
            table_name = os.path.splitext(file)[0]
            ingest_db(df, table_name, engine)

    total_time = (time.time() - start) / 60
    logging.info('--------------Ingestion Complete--------------')
    logging.info(f'Total Time taken: {total_time:.2f} minutes')

def show_logs():
    if os.path.exists(logs_dir):
        files = os.listdir(logs_dir)
        print("Files in logs folder:", files)
        for file in files:
            file_path = os.path.join(logs_dir, file)
            if os.path.isfile(file_path):
                print(f"\n--- Contents of {file} ---")
                with open(file_path, 'r') as f:
                    print(f.read())
    else:
        print("Logs folder does not exist.")

if __name__ == '__main__':
    load_raw_data()
    show_logs()
