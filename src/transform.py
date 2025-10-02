import pandas as pd
import json
from config import BASE_DIR
from datetime import date
import os

def transform(path_file):

    try:
        with open(path_file, 'r') as f:
            raw_data = json.load(f)
    except Exception as e:
        raise RuntimeError (f"Transform stage failed to read input {e}") from e

    df = pd.json_normalize(raw_data)

    #prefer these columns to be deleted
    columns_erase = (['base', 'timezone', 'weather', 'cod', 'sys.country', 'id', 'visibility',
                      'coord.lon','main.temp_min', 'main.temp_max','coord.lat','main.sea_level',
                      'main.grnd_level', 'wind.deg', 'wind.gust', 'clouds.all'])

    try:
        df = df.drop(columns = [col for col in columns_erase])

        df = df.dropna()

        df = df.rename(columns=lambda x: x.split('.')[-1])
        df = df.rename(columns={'speed' : 'wind_speed', 'dt': 'date'})

        #for a more logical location of temp's columns in Celsius, they should be added near the og. temp. columns
        df.insert(3, "temp_Celsius", (df['temp']-273.15).round(2), True)
        df.insert(5, "feels_like_Celsius", (df['feels_like'] - 273.15).round(2), True)

        #convert sunrise and sunset from unix timestamp to a hh:mm and add 3 hours to adjust to a local Ukraine time
        df['sunrise'] = pd.to_datetime( df['sunrise'] + 3 * 3600, unit='s').dt.strftime('%H:%M')
        df['sunset'] = pd.to_datetime(df['sunset'] + 3 * 3600, unit='s').dt.strftime('%H:%M')
        df['date'] = pd.to_datetime(df['date'] + 3 * 3600, unit='s').dt.strftime('%Y-%m-%d')

        return df

    except Exception as e:
        raise RuntimeError(f"❌ Transform stage failed during processing: {e}") from e


def to_parquet (dataframe):
    today = date.today().strftime("%Y-%m-%d")

    output_path = os.path.join(BASE_DIR, 'data', 'processed', today)
    os.makedirs(output_path, exist_ok=True)

    output_file = os.path.join(output_path, 'data.parquet')

    try:
        dataframe.to_parquet(output_file)
    except Exception as e:
        raise RuntimeError(f"Failed to save parquet: {e}") from e
    return output_file

def generate_file_path():
    path = os.path.join(BASE_DIR, 'data', 'raw', date.today().strftime("%Y-%m-%d"), 'response.json')
    return path

def transforming_stage():
    return to_parquet( transform( generate_file_path() ) )


if __name__ == '__main__':
    transforming_stage()
