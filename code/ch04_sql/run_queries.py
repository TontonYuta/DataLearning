"""
Runner script for Project 2: E-commerce Analytics Database
Imports mock CSV datasets into an in-memory SQLite database and executes queries.
"""

import sqlite3
import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"

def main():
    print("=" * 60)
    print("PROJECT 2: E-COMMERCE SQL ANALYTICS RUNNER")
    print("=" * 60)
    
    conn = sqlite3.connect(":memory:")
    
    # 1. Load CSVs into SQLite
    datasets = {
        "customers": "customers.csv",
        "orders": "orders.csv",
        "order_items": "order_items.csv",
        "payments": "payments.csv"
    }
    
    for table, filename in datasets.items():
        filepath = DATA_DIR / filename
        if filepath.exists():
            df = pd.read_csv(filepath)
            df.to_sql(table, conn, index=False, if_exists="replace")
            print(f"[LOADED] Table '{table}': {len(df):,} rows.")
        else:
            print(f"[WARNING] File {filepath} not found!")

    # 2. Run Query: Top Cities
    q1 = """
    SELECT city, COUNT(customer_id) AS total_customers
    FROM customers
    GROUP BY city
    ORDER BY total_customers DESC
    LIMIT 5;
    """
    print("\n--- Top 5 Cities by Customer Count ---")
    print(pd.read_sql_query(q1, conn).to_string(index=False))

    # 3. Run Query: Order Status Breakdown
    q2 = """
    SELECT 
        order_status,
        COUNT(order_id) AS order_count,
        ROUND(COUNT(order_id) * 100.0 / (SELECT COUNT(*) FROM orders), 2) AS percentage
    FROM orders
    GROUP BY order_status
    ORDER BY order_count DESC;
    """
    print("\n--- Order Status Distribution ---")
    print(pd.read_sql_query(q2, conn).to_string(index=False))

    # 4. Run Query: Top Category Revenue
    q3 = """
    SELECT 
        category,
        SUM(quantity) AS total_units_sold,
        ROUND(SUM(price * quantity), 2) AS total_revenue
    FROM order_items
    GROUP BY category
    ORDER BY total_revenue DESC
    LIMIT 5;
    """
    print("\n--- Top 5 Categories by Revenue ---")
    print(pd.read_sql_query(q3, conn).to_string(index=False))

    # 5. Run Query: VIP Customers (CTE + Window Function)
    q4 = """
    WITH customer_spending AS (
        SELECT 
            c.customer_id,
            c.customer_name,
            c.city,
            COUNT(DISTINCT o.order_id) AS order_count,
            ROUND(SUM(oi.price * oi.quantity), 2) AS total_spend
        FROM customers c
        JOIN orders o ON c.customer_id = o.customer_id
        JOIN order_items oi ON o.order_id = oi.order_id
        WHERE o.order_status = 'COMPLETED'
        GROUP BY c.customer_id, c.customer_name, c.city
    )
    SELECT 
        customer_id,
        customer_name,
        city,
        order_count,
        total_spend,
        DENSE_RANK() OVER (ORDER BY total_spend DESC) AS spending_rank
    FROM customer_spending
    ORDER BY spending_rank
    LIMIT 5;
    """
    print("\n--- Top 5 VIP Customers (Window Function) ---")
    print(pd.read_sql_query(q4, conn).to_string(index=False))
    
    conn.close()
    print("\n" + "=" * 60)
    print("SQL Execution Completed Successfully!")
    print("=" * 60)

if __name__ == "__main__":
    main()
