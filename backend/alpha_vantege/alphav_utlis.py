from dotenv import load_dotenv
import os
import psycopg2
from psycopg2 import OperationalError

# get env variables
load_dotenv()
DB_HOST = os.getenv("RDS_ENDPOINT")
DB_NAME = "postgres"
DB_USERNAME = os.getenv("RDS_USERNAME")
DB_PASSWORD = os.getenv("RDS_PASSWORD")

def connect_to_db():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USERNAME,
            password=DB_PASSWORD)
        print(f"Connected to {DB_HOST} {DB_NAME}!")
        return conn
    except OperationalError as e:
        print(f"{e}")
        return None
    
   
def insert_data_from_tsv(conn, directory, table_name):
    cursor = conn.cursor()
    file_path = os.path.join(directory, f"{table_name}.tsv")
    
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    with open(file_path, 'r') as file:
        # SQL command to execute copy
        sql = f"COPY {table_name} FROM STDIN WITH CSV HEADER DELIMITER E'\t';"
        try:
            cursor.copy_expert(sql, file)
            conn.commit()
            print(f"Data copied successfully for table: {table_name}")
        except Exception as e:
            conn.rollback()
            print(f"Failed to copy data for table: {table_name}. Error: {str(e)}")
    cursor.close()
