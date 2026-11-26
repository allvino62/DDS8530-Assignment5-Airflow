# DDS 8530 Assignment 5: Design a Scalable ETL and MLOps Pipeline on AWS Using Python

## 1. Project Overview

This project was developed for DDS 8530 – Big Data Integration at National University. The objective is to design and implement a scalable Extract, Transform, and Load (ETL) pipeline integrated with Machine Learning Operations (MLOps) for customer sales prediction, automated workflow orchestration, model deployment, continuous integration, and performance monitoring.

## 2. Technologies and Tools

- Python – programming and pipeline development
- pandas – data cleaning and transformation
- Dask – parallel data processing
- SQLAlchemy – database integration
- AWS S3 – cloud storage
- Apache Airflow – workflow orchestration
- scikit-learn – machine learning
- MLflow – experiment tracking and model management
- FastAPI – REST API model serving
- Uvicorn – application server
- GitHub Actions – continuous integration and automated testing
- Docker Desktop – monitoring service containerization
- Prometheus – metrics collection
- Grafana – performance visualization
- Ubuntu WSL – development environment

## 3. Project Architecture

The project integrates the following stages:

Data Sources → Data Extraction → Data Transformation → Data Loading → Machine Learning Training → MLflow Tracking → FastAPI Deployment → Prometheus Monitoring → Grafana Dashboard.

Apache Airflow supports workflow orchestration, while GitHub Actions supports automated software testing and version-controlled development.

## 4. ETL Pipeline

The ETL pipeline processes customer sales data through extraction, cleaning, transformation, feature engineering, and loading. pandas supports data manipulation, while Dask provides parallel processing capabilities for larger datasets.

The design supports integration with CSV files, relational databases, web APIs, and cloud storage.

## 5. Machine Learning and MLflow

A Random Forest Regressor was used to predict total customer sales based on quantity, unit price, and discount. MLflow supports experiment tracking, model performance evaluation, and trained model management.

## 6. FastAPI Model Deployment

The trained machine learning model is served through a REST API using FastAPI and Uvicorn.

The application provides the following endpoints:

- /docs – Interactive API documentation
- /predict – Customer sales prediction
- /health – Application health verification
- /metrics – Prometheus-compatible monitoring metrics

A successful prediction request using a quantity of 10, unit price of 150, and discount of 0.10 returned predicted total sales of 1336.71.

## 7. Apache Airflow Automation

Apache Airflow provides workflow orchestration through a Directed Acyclic Graph (DAG). The pipeline configuration is located in the airflow/dags directory.

## 8. GitHub Actions and Automated Testing

GitHub Actions provides continuous integration through the python-ci.yml workflow. Automated tests are stored in the tests directory.

The automated testing workflow completed successfully in 11 seconds, demonstrating successful continuous integration.

## 9. Monitoring and Logging

Prometheus collects application and infrastructure metrics, while Grafana provides interactive monitoring dashboards.

The monitoring dashboard includes:

- Customer Sales API Availability
- Prometheus Target Availability
- Process Memory Usage
- Prometheus HTTP Request Rate

Both the customer sales API and Prometheus targets successfully reported an UP status during testing.

## 10. Project Setup

Clone the GitHub repository:

`git clone https://github.com/allvino62/DDS8530-Assignment5-Airflow.git`

Navigate to the project directory:

`cd DDS8530-Assignment5-Airflow`

Create and activate a Python virtual environment:

`python3 -m venv .venv`

`source .venv/bin/activate`

Install project dependencies using the requirements.txt file once provided:

`python -m pip install -r requirements.txt`

After configuring the required dataset, trained model, and environment variables, start the FastAPI application:

`python -m uvicorn deployment.app:app --host 0.0.0.0 --port 8001`

Start the monitoring services from the monitoring directory:

`cd monitoring`

`docker compose up -d`

## 11. Application Access

- FastAPI: http://localhost:8001/docs
- API Health: http://localhost:8001/health
- API Metrics: http://localhost:8001/metrics
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000

## 12. Security

AWS credentials, passwords, access tokens, and confidential information should not be committed to the GitHub repository. Environment variables and secure credential management should be used instead.

## 13. Conclusion

The project demonstrates the integration of scalable data processing, machine learning, REST API model serving, automated testing, and operational monitoring. The combination of Python, Apache Airflow, MLflow, FastAPI, GitHub Actions, Prometheus, and Grafana provides a foundation for reliable and scalable ETL and MLOps workflows.

## Academic Information

Course: DDS 8530 – Big Data Integration

Institution: National University

Assignment: Assignment 5 – Design a Scalable ETL and MLOps Pipeline on AWS Using Python

November 2026
