from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD, BASE_DIR
import psycopg2
import pandas as pd
import json
import os
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

def analyse():
    conn, cursor = connect_db()

    queries = {
        "unique date of observation per city": """
        SELECT city,
        COUNT (DISTINCT observe_date) AS observe_date
        FROM weather
        GROUP BY city; 
        """,

        "average weather conditions": """
            SELECT city,
            ROUND(AVG(temp_Celsius),2) AS average_temp_celsius,
            ROUND(AVG(humidity),2) AS average_humidity,
            ROUND(AVG(pressure),2) AS average_pressure,
            ROUND(AVG(feels_like_celsius),2) AS average_feels_like_celsius
            FROM weather
            GROUP BY city;
        """,

        "length of sun time per city per day": """
            SELECT city,
            observe_date,
            TO_CHAR( 
                (sunset - sunrise),'HH24:MI') AS sun_time_in_hours
            FROM weather
            ORDER BY observe_date, city;
        """,
    }

    results = {}
    for key, sql in queries.items():
        df = pd.read_sql(sql, conn)
        results[key] = df.to_dict(orient="records")

    cursor.close()
    conn.close()

    return results

def save_report(result):
    today = date.today().strftime("%Y-%m-%d")
    output_dir = os.path.join(BASE_DIR, "reports", today)
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, "report.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, default=str)


if __name__ == '__main__':
    save_report( analyse() )

