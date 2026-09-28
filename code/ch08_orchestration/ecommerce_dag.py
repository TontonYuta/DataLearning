"""
PROJECT 6: APACHE AIRFLOW E-COMMERCE ORCHESTRATION PIPELINE
Data Mastery All-In-One (2026 Edition)
Implements modern Airflow TaskFlow API (@dag, @task) with Retry logic,
Data Quality Checks, and Slack Alerting hooks.
"""

from datetime import datetime, timedelta
import logging

# Configure dummy DAG / Task fallbacks if apache-airflow is not installed in local environment
try:
    from airflow.decorators import dag, task
    from airflow.operators.empty import EmptyOperator
except ImportError:
    # Graceful mock decorator so the file is syntactically valid and testable in standalone Python
    def dag(*args, **kwargs):
        def decorator(f):
            def wrapper(*f_args, **f_kwargs):
                return f(*f_args, **f_kwargs)
            wrapper.__dag_configured__ = True
            return wrapper
        return decorator

    def task(*args, **kwargs):
        def decorator(f):
            return f
        return decorator

logger = logging.getLogger("Airflow_DAG")

default_args = {
    "owner": "data_engineering_team",
    "depends_on_past": False,
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    "email_on_failure": True,
    "email": ["data-alerts@company.com"],
}

@dag(
    dag_id="ecommerce_batch_etl_v2",
    default_args=default_args,
    description="Daily automated ingestion and analytics transformation pipeline",
    schedule="0 2 * * *",  # Run daily at 02:00 AM UTC
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["ecommerce", "etl", "production", "analytics"],
)
def ecommerce_orchestration_pipeline():
    """
    End-to-End Orchestration Workflow:
    1. extract_raw_orders: Ingest daily transactions
    2. quality_check: Validate data schemas and bounds
    3. transform_and_enrich: Calculate financial metrics
    4. load_data_mart: Upsert into Data Warehouse marts
    5. notify_slack: Trigger alert upon completion
    """

    @task(task_id="extract_raw_data")
    def extract_raw_data() -> dict:
        logger.info("Extracting transactions from cloud landing zone...")
        # Simulated extraction returning metadata payload
        return {
            "source": "s3://company-datalake/raw/2026-03-29/",
            "record_count": 15420,
            "status": "extracted"
        }

    @task(task_id="data_quality_gate")
    def data_quality_gate(meta: dict) -> dict:
        logger.info(f"Running Great Expectations / Pydantic checks on {meta['record_count']} records...")
        if meta["record_count"] == 0:
            raise ValueError("Zero records found! Pipeline aborted to prevent empty partition overwrite.")
        meta["dq_passed"] = True
        logger.info("Data Quality Gate: PASSED.")
        return meta

    @task(task_id="transform_enrich")
    def transform_enrich(meta: dict) -> dict:
        logger.info("Enriching customer records with RFM tiers and calculating net amounts...")
        meta["transformed_count"] = meta["record_count"] - 12  # Dropped 12 anomalies
        meta["status"] = "transformed"
        return meta

    @task(task_id="load_to_warehouse")
    def load_to_warehouse(meta: dict) -> str:
        logger.info(f"Idempotent loading {meta['transformed_count']} records to fact_orders...")
        return "SUCCESS"

    @task(task_id="send_slack_notification", trigger_rule="all_done")
    def send_slack_notification(load_status: str):
        logger.info(f"Slack Notification Sent: Pipeline finished with status '{load_status}'")

    # Workflow Dependency Chain via TaskFlow
    raw = extract_raw_data()
    checked = data_quality_gate(raw)
    enriched = transform_enrich(checked)
    loaded = load_to_warehouse(enriched)
    send_slack_notification(loaded)

# Instantiate the DAG
dag_instance = ecommerce_orchestration_pipeline()

if __name__ == "__main__":
    print("=" * 60)
    print("APACHE AIRFLOW DAG: ecommerce_batch_etl_v2")
    print("Verification: DAG parsed and initialized without syntax errors.")
    print("=" * 60)
