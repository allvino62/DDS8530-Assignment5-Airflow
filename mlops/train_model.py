
import json
from pathlib import Path

import joblib
import mlflow
import mlflow.sklearn

# Project directory
BASE_DIR = Path(__file__).resolve().parents[1]

MODEL_PATH = BASE_DIR / "models" / "sales_prediction_model.pkl"
METRICS_PATH = BASE_DIR / "models" / "model_metrics.json"
DATA_PATH = BASE_DIR / "data" / "sales_cleaned.csv"

# Connect to MLflow
mlflow.set_tracking_uri("http://127.0.0.1:5000")

mlflow.set_experiment(
    "DDS8530-Assignment5-Customer-Sales"
)

# Load the original locally trained model
model = joblib.load(MODEL_PATH)

# Load original performance metrics
with open(METRICS_PATH, "r") as f:
    metrics = json.load(f)

# Start MLflow experiment run
with mlflow.start_run(
    run_name="Customer-Sales-Random-Forest"
) as run:

    # Log model parameters
    mlflow.log_params(model.get_params())

    mlflow.log_param("dataset", DATA_PATH.name)
    mlflow.log_param("algorithm", type(model).__name__)
    mlflow.log_param("test_size", 0.20)
    mlflow.log_param("training_size", 0.80)
    mlflow.log_param("R2_threshold", 0.80)

    # Log original performance metrics
    mlflow.log_metrics({
        "MAE": float(metrics["MAE"]),
        "RMSE": float(metrics["RMSE"]),
        "R2": float(metrics["R2"]),
        "training_records": metrics["training_records"],
        "testing_records": metrics["testing_records"]
    })

    # Log project information
    mlflow.set_tag("course", "DDS8530")
    mlflow.set_tag("assignment", "Assignment 5")
    mlflow.set_tag("pipeline", "Apache Airflow")
    mlflow.set_tag("model_source", "Original Customer Sales model")

    # Log performance report
    mlflow.log_artifact(str(METRICS_PATH))

    # Log the locally trained Random Forest model
    mlflow.sklearn.log_model(
        sk_model=model,
        name="sales_prediction_model",
        serialization_format="skops",
        skops_trusted_types=[
            "sklearn.tree._tree.Tree"
        ]
    )

    print("CUSTOMER SALES MLFLOW TRACKING COMPLETED")
    print("Run ID:", run.info.run_id)
    print("Model:", type(model).__name__)
    print("MAE:", metrics["MAE"])
    print("RMSE:", metrics["RMSE"])
    print("R-squared:", metrics["R2"])

    if metrics["R2"] >= 0.80:
        print("Model performance: PASSED")
    else:
        print("Model performance: FAILED")
