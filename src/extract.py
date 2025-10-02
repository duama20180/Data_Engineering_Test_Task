import json
import os
import requests
from config import API_KEY, LAT, LON, BASE_DIR
from datetime import date

def extract_data():

    file = generate_path()

    url = f'https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={API_KEY}'

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        raise RuntimeError(f"Extract stage failed: {e}") from e

    try:
        with open(file, mode='w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        raise RuntimeError(f"Failed to save extracted data: {e}") from e

    return file

def generate_path():
    today = date.today().strftime("%Y-%m-%d")

    output_path = os.path.join(BASE_DIR, 'data', 'raw', today)
    os.makedirs(output_path, exist_ok=True)

    output_file = os.path.join(output_path, 'response.json')
    return output_file

if __name__ == "__main__":
    extract_data()