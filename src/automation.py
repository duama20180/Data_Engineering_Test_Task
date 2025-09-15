from extract import extract_data
from transform import transforming_stage
from load import loading_stage
from analytics import analysing_stage

#stage extracting
extract_data()

#stage transforming
transforming_stage()

#stage loading to db
loading_stage()

#data analysis stage
analysing_stage()