
from datetime import datetime
from pathlib import Path
import json
import sqlite3

from airflow.sdk import DAG, task

PROJECT = Path("/home/student/DDS8530-Assignment5-Airflow")
SOURCE = Path(
    "/mnt/c/Users/Owner/Documents/DDS8530-Assignment5/data/sales_transactions.csv"
)
DATA_DIR = PROJECT / "data"
MODEL_DIR = PROJECT / "models"


with DAG(
    dag_id="dds8530_assignment5_pipeline",
    description="DDS 8530 Assignment 5 - Sales ETL and MLOps",
    start_date=datetime(2026, 11, 1),
    schedule=None,
    catchup=False,
    max_active_runs=1,
    tags=["DDS8530", "ETL", "MLOps"],
) as dag:

    @task
    def extract_data():
        import pandas as pd

        DATA_DIR.mkdir(parents=True, exist_ok=True)

        df = pd.read_csv(SOURCE)

        if df.empty:
            raise ValueError("Source sales dataset is empty")

        output = DATA_DIR / "sales_extracted.csv"
        df.to_csv(output, index=False)

        print(f"Extracted {len(df)} sales records")
        return str(output)

    @task
    def transform_data(input_path):
        import pandas as pd

        df = pd.read_csv(input_path)

        required = [
            "quantity", "unit_price",
            "discount", "total_sales"
        ]

        df = df.dropna(subset=required).copy()

        if df.empty:
            raise ValueError("No valid records after cleaning")

        df["order_date"] = pd.to_datetime(
            df["order_date"], errors="coerce"
        )

        df = df.dropna(subset=["order_date"])

        output = DATA_DIR / "sales_cleaned.csv"
        df.to_csv(output, index=False)

        print(f"Transformed {len(df)} records")
        return str(output)

    @task
    def load_data(input_path):
        import pandas as pd

        df = pd.read_csv(input_path)

        database = DATA_DIR / "sales_ml.db"

        with sqlite3.connect(database) as conn:
            df.to_sql(
                "sales_transactions",
                conn,
                if_exists="replace",
                index=False
            )

        print(f"Loaded {len(df)} records into SQLite")
        return str(database)

    @task
    def train_model(database_path):
        import pandas as pd
        import joblib

        from sklearn.model_selection import train_test_split
        from sklearn.ensemble import RandomForestRegressor
        from sklearn.metrics import (
            mean_absolute_error,
            mean_squared_error,
            r2_score
        )

        with sqlite3.connect(database_path) as conn:
            df = pd.read_sql_query(
                "SELECT * FROM sales_transactions", conn
            )

        X = df[["quantity", "unit_price", "discount"]]
        y = df["total_sales"]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.20, random_state=42
        )

        model = RandomForestRegressor(
            n_estimators=100,
            random_state=42,
            n_jobs=-1
        )

        model.fit(X_train, y_train)
        predictions = model.predict(X_test)

        metrics = {
            "training_records": len(X_train),
            "testing_records": len(X_test),
            "MAE": float(mean_absolute_error(y_test, predictions)),
            "RMSE": float(
                mean_squared_error(y_test, predictions) ** 0.5
            ),
            "R2": float(r2_score(y_test, predictions))
        }

        MODEL_DIR.mkdir(parents=True, exist_ok=True)

        joblib.dump(
            model,
            MODEL_DIR / "sales_prediction_model.pkl"
        )

        metrics_path = MODEL_DIR / "model_metrics.json"

        with open(metrics_path, "w") as f:
            json.dump(metrics, f, indent=4)

        print("Model training completed")
        print(metrics)

        return str(metrics_path)

    @task
    def monitor_pipeline(metrics_path):
        with open(metrics_path) as f:
            metrics = json.load(f)

        print("===== PIPELINE MONITORING =====")
        print("MAE:", round(metrics["MAE"], 2))
        print("RMSE:", round(metrics["RMSE"], 2))
        print("R-squared:", round(metrics["R2"], 4))

        if metrics["R2"] < 0.80:
            raise ValueError(
                "Model performance below threshold"
            )

        print("PIPELINE COMPLETED SUCCESSFULLY")

    extracted = extract_data()
    transformed = transform_data(extracted)
    loaded = load_data(transformed)
    trained = train_model(loaded)
    monitor_pipeline(trained)
