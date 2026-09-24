# 🌍 Global Intelligence Pipeline

An orchestrated data engineering pipeline that collects global
weather, economic, country, and news data, transforms it into
analytics-ready datasets, and generates AI-assisted insights.

## Architecture

External APIs
      ↓
Apache Airflow
      ↓
Raw Data
      ↓
Validation
      ↓
Transformation
      ↓
PostgreSQL
      ↓
Metrics
      ↓
LLM Insights

## Tech Stack

- Python
- Apache Airflow
- PostgreSQL
- Docker
- REST APIs
- pytest
- Ruff
- LLM API
