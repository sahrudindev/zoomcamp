import os
import argparse
from time import time
import pandas as pd
from sqlalchemy import create_engine

def main(params):
    user = params.user
    password = params.password
    host = params.host 
    port = params.port 
    db = params.db
    table_name = params.table_name
    url = params.url
    
    # Mengunduh file dataset
    file_name = 'output.parquet' if url.endswith('.parquet') else 'output.csv'
    print(f"Mengunduh data dari {url}...")
    os.system(f"wget {url} -O {file_name}")

    # Membuka koneksi ke PostgreSQL
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    
    # Membaca data dan memasukkan ke database
    print("Memproses data ke dalam database...")
    if file_name.endswith('.parquet'):
        df = pd.read_parquet(file_name)
    else:
        df = pd.read_csv(file_name)
        
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
    df.to_sql(name=table_name, con=engine, if_exists='append')
    print("Proses ETL Selesai!")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV/Parquet data to Postgres')
    parser.add_argument('--user', help='Username PostgreSQL')
    parser.add_argument('--password', help='Password PostgreSQL')
    parser.add_argument('--host', help='Host PostgreSQL')
    parser.add_argument('--port', help='Port PostgreSQL')
    parser.add_argument('--db', help='Nama Database')
    parser.add_argument('--table_name', help='Nama Tabel')
    parser.add_argument('--url', help='URL file dataset')
    args = parser.parse_args()
    main(args)