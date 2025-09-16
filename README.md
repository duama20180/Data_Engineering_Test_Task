## Data ETL Pipeline

This project implements a mini ETL data pipeline that extracts weather data from the OpenWeatherMap API, processes and enriches the data, loads it into a PostgreSQL database, and generates basic analytics reports in JSON format.

## Description Of The Implementation Steps
### 1. Data Acquisition
- Public REST API used: OpenWeatherMap  
- API called with latitude, longitude, and API key.  
- Raw JSON response stored at: `/data/raw/yyyy-mm-dd/response.json`

### 2. Data Processing
- Flattened JSON using `pandas.json_normalize`.
- Selected Fields - retained only the following fields for analysis: dt, name, main.temp, main.feels_like, main.pressure, main.humidity, wind.speed, sys.sunrise, sys.sunset
- Renamed keys for readability (e.g., `dt → date`, `main.temp → temp`, `speed → wind_speed`).
- Created two new temperature columns: temp_Celsius and feels_like_Celsius (converted from Kelvin)
- Converted sunrise/sunset UNIX timestamps to local time (UTC+3, Ukraine).  
- Processed data saved as Parquet: `/data/processed/yyyy-mm-dd/data.parquet`  

### 3. Database Integration
- PostgreSQL database (`my_postgres`) created via docker-compose.  
- **Table weather schema includes:**  
  observe_date, city, temp, temp_Celsius, feels_like, feels_like_Celsius, pressure, humidity, wind_speed, sunrise, sunset  
- Data loaded into DB using `pandas` + `psycopg2`.  

### 4. Analytics
- SQL queries implemented:  
  * Unique observation dates per city  
  * Average weather conditions (temperature, humidity, pressure, feels_like)  
  * Length of daytime (sunrise → sunset) per city/day  
- Results saved as JSON report: `/reports/yyyy-mm-dd/report.json`  

### 5. Automation
- `automation.py` runs the entire ETL pipeline sequentially.  
- Airflow DAG (`etl_dag.py`) provided for orchestration with daily scheduling.

[detailed_description_of_the_implementation_steps.md](https://github.com/duama20180/Data_Engineering_Test_Task/blob/main/detailed_description_of_the_implementation_steps.md)
##  Project Structure
```
├── data/
│   ├── processed/         # Processed parquet data
│   └── raw/               # Raw API responses in JSON
│
├── reports/               # Analytics reports
│
├── src/
│   ├── analytics.py       # Run SQL analytics & save report
│   ├── automation.py      # ETL runner in one file
│   ├── config.py          # Env variables (API key, DB configs)
│   ├── etl_dag.py         # Airflow DAG
│   ├── load.py            # Loading data into PostgreSQL
│   ├── extract.py         # Extracting data from API
│   └── transform.py       # Clean & enrich data   
│
├── .env                   # API keys & DB credentials
├── docker-compose.yml     # PostgreSQL container setup
├── dump.sql               # SQL dump for initialize or restore PostgreSQL DB schema
├── README.md
└── requirements.txt       # Python dependencies for the project
```

## Setup & Run Instructions

#### 1. Clone Repo & Install Requirements
```bash
git clone https://github.com/duama20180/Data_Engineering_Test_Task
cd project-root
pip install -r requirements.txt
```

#### 2. Setup Environment Variables
Create a `.env` file:
```env
# OpenWeatherMap API key
API_KEY=your_openweathermap_api_key_here

# Coordinates of the desired location
LAT=latitude_here
LON=longitude_here

# PostgreSQL database connection details
DB_HOST=host_here
DB_PORT=port_here
DB_NAME=database_name_here
DB_USER=username_here
DB_PASSWORD=password_here
```

#### 3. Run PostgreSQL via Docker
```bash
docker-compose up -d
```

#### 4. Run ETL Pipeline
**Option A – Sequential Python script:**
```bash
python3 src/automation.py
```

**Option B – Individual steps:**
```bash
python3 src/extract.py
python3 src/transform.py
python3 src/load.py
python3 src/analytics.py
```

**Option C – With Airflow DAG:**
- Place `etl_dag.py` in Airflow `dags/` directory.  
- Trigger from Airflow UI.  

## Screenshots
![Example of data.parquet](https://github.com/duama20180/Data_Engineering_Test_Task/blob/main/screenshots/example_of_response_json.png)

![Example of response.json](https://github.com/duama20180/Data_Engineering_Test_Task/blob/main/screenshots/look_of_db_table_and_data_stored.png)

![Look of db table and data stored](https://github.com/duama20180/Data_Engineering_Test_Task/blob/main/screenshots/screenshot_of_files_saved_locally.png)

![Screenshot of files saved locally](https://github.com/duama20180/Data_Engineering_Test_Task/blob/main/screenshots/example_of_data_parquet.png)

## Example of `report.json`
Below is the content of the [report.json](https://github.com/duama20180/Data_Engineering_Test_Task/blob/main/reports/2025-09-15/report.json) file:
```
{
  "unique date of observation per city": [
    {
      "city": "Vinnytsia",
      "observe_date": 3
    }
  ],
  "average weather conditions": [
    {
      "city": "Vinnytsia",
      "average_temp_celsius": 16.44,
      "average_humidity": 62.75,
      "average_pressure": 1022.0,
      "average_feels_like_celsius": 15.78
    }
  ],
  "length of sun time per city per day": [
    {
      "city": "Vinnytsia",
      "observe_date": "2025-09-13",
      "sun_time_in_hours": "12:45"
    },
    {
      "city": "Vinnytsia",
      "observe_date": "2025-09-14",
      "sun_time_in_hours": "12:41"
    },
    {
      "city": "Vinnytsia",
      "observe_date": "2025-09-15",
      "sun_time_in_hours": "12:38"
    },
    {
      "city": "Vinnytsia",
      "observe_date": "2025-09-15",
      "sun_time_in_hours": "12:38"
    }
  ]
}
```
