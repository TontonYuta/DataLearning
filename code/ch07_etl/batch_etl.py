"""
PROJECT 5: IDEMPOTENT PRODUCTION BATCH ETL PIPELINE
Data Mastery All-In-One (2026 Edition)
Implements Extract-Transform-Load with Data Quality Validation and Idempotent Loading.
"""

import sys
import logging
import sqlite3
import pandas as pd
from pathlib import Path
from datetime import datetime

# Setup paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
RAW_DATA_PATH = BASE_DIR / "data" / "raw_transactions.csv"
DB_PATH = BASE_DIR / "data" / "analytics_warehouse.db"

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("ETL_Pipeline")

def extract(file_path: Path) -> pd.DataFrame:
    """Step 1: Extract raw data with error handling."""
    logger.info(f"Extracting raw data from: {file_path}")
    if not file_path.exists():
        raise FileNotFoundError(f"Source file not found: {file_path}")
    df = pd.read_csv(file_path)
    logger.info(f"Successfully extracted {len(df):,} raw records.")
    return df

def validate_and_transform(df: pd.DataFrame) -> pd.DataFrame:
    """
    Step 2: Data Quality Validation & Business Transformation.
    - Drops invalid / null primary keys
    - Enforces positive amounts and non-negative discounts
    - Derives net_amount and spending_tier
    - Ensures idempotency by deduplicating on order_id
    """
    initial_count = len(df)
    logger.info("Starting data quality validation and transformations...")

    # 1. Deduplicate by order_id keeping latest
    df = df.drop_duplicates(subset=["order_id"], keep="last").copy()
    logger.info(f"Deduplication complete. Remaining records: {len(df):,}")

    # 2. Validation: Filter out malformed records
    valid_mask = (
        df["order_id"].notna() &
        df["customer_id"].notna() &
        (df["amount"] > 0) &
        (df["discount"] >= 0) &
        (df["discount"] <= df["amount"])
    )
    dropped_count = initial_count - valid_mask.sum()
    if dropped_count > 0:
        logger.warning(f"Data Quality: Dropped {dropped_count} invalid records failing constraint checks.")
    
    clean_df = df[valid_mask].copy()

    # 3. Transformations
    clean_df["created_at"] = pd.to_datetime(clean_df["created_at"]).dt.strftime("%Y-%m-%d %H:%M:%S")
    clean_df["net_amount"] = (clean_df["amount"] - clean_df["discount"]).round(2)
    clean_df["spending_tier"] = clean_df["amount"].apply(
        lambda x: "VIP" if x >= 500 else ("MEDIUM" if x >= 100 else "STANDARD")
    )
    from datetime import timezone
    clean_df["etl_processed_at"] = datetime.now(timezone.utc).isoformat()

    logger.info(f"Transformation complete. Clean records ready for load: {len(clean_df):,}")
    return clean_df

def load_idempotent(df: pd.DataFrame, db_file: Path, target_table: str = "fact_transactions"):
    """
    Step 3: Idempotent Load into SQLite Data Warehouse.
    Uses UPSERT (INSERT OR REPLACE) to guarantee that re-running the pipeline
    never creates duplicate rows.
    """
    logger.info(f"Loading data into Data Warehouse at: {db_file}")
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Ensure target table exists with primary key
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {target_table} (
            order_id TEXT PRIMARY KEY,
            customer_id TEXT NOT NULL,
            amount REAL NOT NULL,
            discount REAL NOT NULL,
            net_amount REAL NOT NULL,
            order_status TEXT NOT NULL,
            created_at TEXT NOT NULL,
            spending_tier TEXT NOT NULL,
            etl_processed_at TEXT NOT NULL
        );
    """)

    # Perform Idempotent Upsert
    records = df[[
        "order_id", "customer_id", "amount", "discount", "net_amount",
        "order_status", "created_at", "spending_tier", "etl_processed_at"
    ]].values.tolist()

    cursor.executemany(f"""
        INSERT OR REPLACE INTO {target_table} (
            order_id, customer_id, amount, discount, net_amount,
            order_status, created_at, spending_tier, etl_processed_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, records)

    conn.commit()
    
    # Validation count
    cursor.execute(f"SELECT COUNT(*) FROM {target_table}")
    total_in_dw = cursor.fetchone()[0]
    conn.close()

    logger.info(f"Load complete! Total rows in '{target_table}': {total_in_dw:,}")

def main():
    logger.info("=" * 60)
    logger.info("BATCH ETL PIPELINE EXECUTION STARTED")
    logger.info("=" * 60)
    try:
        raw_df = extract(RAW_DATA_PATH)
        clean_df = validate_and_transform(raw_df)
        load_idempotent(clean_df, DB_PATH)
        logger.info("=" * 60)
        logger.info("PIPELINE COMPLETED SUCCESSFULLY (STATUS: SUCCESS)")
        logger.info("=" * 60)
    except Exception as e:
        logger.error(f"Pipeline Failed: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
