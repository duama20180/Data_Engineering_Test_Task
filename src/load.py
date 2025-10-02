from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD, BASE_DIR
import os
import pandas as pd
import psycopg2
from datetime import date

def connect_db():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        dbname=DB_NAME
    )
    conn.autocommit = True
    cursor = conn.cursor()

    return conn, cursor

def create_database():

    conn, cursor = connect_db()

    try:
        cursor.execute('CREATE DATABASE "test-db";')
    except psycopg2.errors.DuplicateDatabase:
        pass

    cursor.close()
    conn.close()

def create_table():

    conn, cursor = connect_db()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS weather (
        observe_date DATE,
        city VARCHAR(100),
        temp NUMERIC(6, 2),
        temp_Celsius NUMERIC(5, 2),
        feels_like NUMERIC(6, 2),
        feels_like_Celsius NUMERIC(5, 2),
        pressure INT,
        humidity INT,
        wind_speed NUMERIC(5,2),
        sunrise TIME,
        sunset TIME,
        PRIMARY KEY (observe_date, city)
    )
    """)

    cursor.close()
    conn.close()

def load_process(file):
    conn, cursor = connect_db()

    df = pd.read_parquet(file)

    values = [(
        row['date'], row['name'], row['temp'], row['temp_Celsius'], row['feels_like'],
        row['feels_like_Celsius'], row['pressure'], row['humidity'], row['wind_speed'],
        row['sunrise'], row['sunset']
    ) for _, row in df.iterrows()]

    cursor.executemany("""
        INSERT INTO weather (
            observe_date, city, temp, temp_Celsius,
            feels_like, feels_like_Celsius,
            pressure, humidity, wind_speed, sunrise, sunset
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (observe_date, city) DO NOTHING
    """, values)

    cursor.close()
    conn.close()


def generate_file_path():
    path = os.path.join(BASE_DIR, 'data', 'processed', date.today().strftime("%Y-%m-%d"), 'data.parquet')
    return path


def loading_stage():
    create_table()

    load_process( generate_file_path() )


if __name__ == "__main__":
    loading_stage()
