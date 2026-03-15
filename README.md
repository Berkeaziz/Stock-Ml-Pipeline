# Stock Price ML Pipeline

An end-to-end Data Engineering + Data Science project that demonstrates how financial time-series data can be ingested, validated, transformed, and used to train a time-aware machine learning model, fully orchestrated with Apache Airflow.

This project focuses on production-oriented pipeline design rather than notebook-based experimentation.

---

## Project Highlights

- End-to-End Pipeline: From external AlphaVantage API to a trained ML model.
- Idempotent ETL: Robust data ingestion using Pandas and PostgreSQL.
- Data Quality (DQ): Explicit validation checks before downstream processing.
- Feature Engineering: Time-series specific features designed to prevent data leakage.
- ML Training: Time-based splitting and training using XGBoost.
- Orchestration: Fully automated workflow with Apache Airflow.
- Containerization: Easy-to-deploy Dockerized PostgreSQL and Airflow environments.

---

## Architecture

```mermaid
flowchart LR

    A[AlphaVantage API]
    B[ETL Pipeline<br>(Pandas)]
    C[PostgreSQL<br>(Dockerized)]
    D[Airflow Orchestration]
    E[Feature Engineering]
    F[XGBoost Model Training]
    G[Evaluation & Artifacts]

    A --> B
    B --> C
    C --> D
    D --> E
    E --> F
    F --> G
```
---

## Tech Stack

- Language: Python 3.11
- Orchestration: Apache Airflow
- Storage: PostgreSQL, Docker Volumes
- Data Processing: Pandas, SQLAlchemy
- Machine Learning: XGBoost, Scikit-learn
- Infrastructure: Docker, Docker Compose

---

## Pipeline Overview

### 1. Data Engineering (ETL)
* Extract: Weekly financial data fetched from AlphaVantage API with error handling.
* Transform: JSON normalization, column standardization, and explicit type casting.
* Load: UPSERT logic to ensure idempotency (no duplicate records on re-runs).

### 2. Data Quality & Validation
* Row count and null value checks on critical columns.
* Uniqueness checks on the time dimension.
* Early-stop strategy: Pipeline fails if data quality doesn't meet thresholds.

### 3. Feature Engineering & ML
* Features: Lag-based features, rolling averages, and volatility metrics.
* Target: Next-week closing price prediction.
* Validation: Time-based train/test split (no shuffling) to respect chronological order.

### 4. Airflow Orchestration
* DAG-based workflow managing task dependencies.
* Automatic retries and logging for observability.
* Scheduled for weekly execution to match stock market cycles.

---

## How to Run

1. Clone the repository:
   git clone https://github.com/your-username/stock-ml-pipeline.git

2. Set up Environment Variables:
   Create a .env file and add your AlphaVantage API Key and DB credentials.

3. Start Infrastructure (PostgreSQL & Airflow):
   docker-compose up -d

4. Run Pipeline Components (Manual Trigger):
   python -m src.etl.run_etl
   python -m src.features.run_features
   python -m src.train.train

---

## Future Enhancements
- MLflow Integration: For experiment tracking and model versioning.
- dbt (data build tool): Moving transformations into the warehouse.
- Drift Detection: Monitoring for data and model drift over time.
- Slack/Email Notifications: For pipeline failures in Airflow.

---
