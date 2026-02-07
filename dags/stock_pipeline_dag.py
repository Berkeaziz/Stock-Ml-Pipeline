from datetime import datetime
from airflow import dag
from airflow.operators.python import PythonOperator

from src.etl.run_etl import main as etl_main
from src.qualities.checks import run_quality_checks
from src.features.run_features import main as features_main
from src.train.train import main as train_main
from src.config import DB_URL

default_args ={"owner":"berke","retries":1}

with DAG(
    dag_id="stock_ml_pipeline",
    default_args=default_args,
    start_date=datetime(2025, 1, 1),
    schedule=None,  # manuel trigger (istersen sonra weekly yaparız)
    catchup=False,
    tags=["de", "ds", "ml"],
) as dag:
    
    etl=PythonOperator(
        task_id ="etl_extract_transform_load",
        python_callable=etl_main,
    )

    quality =PythonOperator(
        task_id ="data_quality_checks",
        python_callable=lambda:run_quality_checks(DB_URL)
    )

    features= PythonOperator(
        task_id = "feature_engineering",
        python_callable =features_main,
    )
        train = PythonOperator(
        task_id="train_model",
        python_callable=train_main,
    )

    etl>>quality>>features>>train