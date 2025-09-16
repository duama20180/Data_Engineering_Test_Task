# Additional Information
This document provides additional details that may not fit directly into the main README, explaining why specific approaches were chosen to address several tricky steps in the task.

## 1) 2. Data Processing
- **Keep only necessary fields**: My list of necessary fields consists of columns that may be useful if the transformed dataset is used for generating daily weather statistics (in the future use of data). This use case was considered during the selection process.
- **Add a calculated field (e.g., temperature in Celsius)**: The task requested a single calculated field, but I created two. Converting only one value to Celsius while leaving the other unchanged would be inconsistent and could compromise the adequacy of the transformed data.

## 2) 4. Analytics / SQL Queries
- **Save the results to report.json or report.csv**: The task requires saving results in one of two formats; I chose JSON. However, the instructions do not specify the file path. Since the pipeline is designed to retrieve data at least once a day (based on the folder structure for raw and processed files), there is a risk that daily reports could be overwritten.  
  To follow best practices in data storage, reports are saved using the same folder structure as raw and processed data. This approach ensures all reports are stored without the risk of losing important insights from SQL queries.

## 3) response.json
- For demonstration purposes, data from three days for the city of Vinnytsia was extracted and processed.  
- To better illustrate SQL query results, two additional rows representing distinct cities (Kyiv and Lviv) were temporarily added. After obtaining the results shown in `response.json`, these rows were deleted.