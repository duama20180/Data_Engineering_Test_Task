import json
import os
import requests
from config import API_KEY, LAT, LON, BASE_DIR
from datetime import date

def extract_data():

    today = date.today().strftime("%Y-%m-%d")

    output_path = os.path.join(BASE_DIR, 'data', 'raw', today)
    os.makedirs(output_path, exist_ok=True)

    output_file = os.path.join(output_path, 'response.json')

    url = f'https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={API_KEY}'

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"error: {e}")


    with open(output_file, mode='w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

    return output_file


if __name__ == "__main__":
    extract_data()