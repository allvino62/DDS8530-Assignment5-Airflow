from datetime import datetime

from airflow.sdk import DAG, task

with DAG(
    dag_id="dds8530_assignment5_pipeline",
    description="DDS 8530 Assignment 5 ETL and MLOps Pipeline",
    start_date=datetime(2026, 11, 1),
    schedule=None,
    catchup=False,
    tags=["DDS8530", "ETL", "MLOps"]
) as dag:

    @task
    def extract_data():
        print("Step 1: Extracting data")
        return "Extraction completed"

    @task
    def transform_data():
        print("Step 2: Transforming data")
        return "Transformation completed"

    @task
    def load_data():
        print("Step 3: Loading processed data")
        return "Loading completed"

    @task
    def train_model():
        print("Step 4: Running machine learning workflow")
        return "Machine learning completed"

    @task
    def monitor_pipeline():
        print("Step 5: Monitoring pipeline")
        return "Monitoring completed"

    extract = extract_data()
    transform = transform_data()
    load = load_data()
    train = train_model()
    monitor = monitor_pipeline()

    extract >> transform >> load >> train >> monitor
