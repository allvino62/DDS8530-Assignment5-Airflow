from pathlib import Path
import ast

PROJECT_ROOT = Path(__file__).resolve().parents[1]

def test_airflow_dag_exists():
    dag_file = (
        PROJECT_ROOT
        / "airflow"
        / "dags"
        / "dds8530_assignment5_pipeline.py"
    )
    assert dag_file.is_file(), "Airflow DAG file is missing"


def test_airflow_dag_python_syntax():
    dag_file = (
        PROJECT_ROOT
        / "airflow"
        / "dags"
        / "dds8530_assignment5_pipeline.py"
    )

    source = dag_file.read_text(encoding="utf-8")
    ast.parse(source)


def test_prometheus_configuration_exists():
    config_file = PROJECT_ROOT / "monitoring" / "prometheus.yml"
    assert config_file.is_file(), "Prometheus configuration is missing"


def test_docker_compose_exists():
    compose_file = PROJECT_ROOT / "monitoring" / "compose.yaml"
    assert compose_file.is_file(), "Docker Compose configuration is missing"
