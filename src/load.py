import os
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

import pandas as pd
import psycopg2

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
        print("db created successfully.")
    except psycopg2.errors.DuplicateDatabase:
        print("db already exists.")

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
        sunset TIME
    )
    """)

    conn.commit()

    cursor.close()
    conn.close()

def load(file):
    conn, cursor = connect_db()

    df = pd.read_parquet(file)

    values = [(
        row ['date'], row['name'], row['temp'], row['temp_Celsius'],row['feels_like'],
        row['feels_like_Celsius'],row['pressure'], row['humidity'], row['wind_speed'],
        row['sunrise'], row['sunset']
    ) for _, row in df.iterrows()]

    cursor.executemany("""
        INSERT INTO weather (
            observe_date, city,temp, temp_Celsius,
            feels_like, feels_like_Celsius,
            pressure, humidity, wind_speed, sunrise, sunset
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, values)

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    create_database()
    create_table()
    load('data.parquet')