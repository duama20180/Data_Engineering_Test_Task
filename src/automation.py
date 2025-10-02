from extract import extract_data
from transform import transforming_stage
from load import loading_stage
from analytics import analysing_stage
import sys

def main():
    try:
        print("Starting pipeline")

        print("Extracting data")
        extract_data()

        print("Transforming data")
        transforming_stage()

        print("Loading data into DB")
        loading_stage()

        print("Running analytics")
        analysing_stage()

        print("Pipeline finished successfully!")

    except Exception as e:
        print(f"Pipeline failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
