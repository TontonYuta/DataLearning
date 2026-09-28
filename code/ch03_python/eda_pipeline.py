#!/usr/bin/env python3
"""
PROJECT 1: E-Commerce Sales Explorer
Thuc hien lam sach du lieu, phan tich tang truong MoM va kiem chung quy luat Pareto.
"""

import os
import pandas as pd
import numpy as np

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")

def run_ecommerce_eda():
    print("=" * 65)
    print("       PROJECT 1: E-COMMERCE SALES EXPLORER PIPELINE")
    print("=" * 65)

    orders_file = os.path.join(DATA_DIR, "orders.csv")
    items_file = os.path.join(DATA_DIR, "order_items.csv")
    payments_file = os.path.join(DATA_DIR, "payments.csv")
    customers_file = os.path.join(DATA_DIR, "customers.csv")

    orders = pd.read_csv(orders_file, parse_dates=['order_purchase_timestamp'])
    items = pd.read_csv(items_file)
    payments = pd.read_csv(payments_file)
    customers = pd.read_csv(customers_file)

    # 1. Merge datasets
    df = orders.merge(items, on='order_id', how='inner')
    df = df.merge(payments, on='order_id', how='inner')
    df = df.merge(customers, on='customer_id', how='inner')

    print(f"[*] Tong so dong sau khi ket hop (Merged): {len(df):,}")

    # 2. Doanh thu theo thang va tang truong MoM
    df['order_month'] = df['order_purchase_timestamp'].dt.to_period('M')
    monthly = df.groupby('order_month').agg(
        total_revenue=('price', 'sum'),
        total_orders=('order_id', 'nunique'),
        active_customers=('customer_id', 'nunique')
    ).reset_index()

    monthly['revenue_growth_mom_%'] = (monthly['total_revenue'].pct_change() * 100).round(2)
    monthly['total_revenue'] = monthly['total_revenue'].round(2)

    print("\n--- 1. TANG TRUONG DOANH THU THEO THANG (MoM GROWTH) ---")
    print(monthly.to_string(index=False))

    # 3. Kiem dinh Quy luat Pareto (80/20)
    cust_revenue = df.groupby('customer_id')['price'].sum().sort_values(ascending=False).reset_index()
    total_revenue = cust_revenue['price'].sum()
    cust_revenue['cum_revenue'] = cust_revenue['price'].cumsum()
    cust_revenue['cum_pct'] = (cust_revenue['cum_revenue'] / total_revenue) * 100

    top_20_count = int(len(cust_revenue) * 0.20)
    pareto_share = cust_revenue.iloc[top_20_count]['cum_pct']

    print("\n--- 2. PHAN TICH QUY LUAT PARETO TRONG KINH DOANH ---")
    print(f"Tong so khach hang doc lap: {len(cust_revenue):,}")
    print(f"Top 20% khach hang ({top_20_count:,} nguoi) dong gop: {pareto_share:.2f}% tong doanh thu!")

    # 4. Hieu nang Danh muc San pham (Category Performance)
    category_summary = df.groupby('category').agg(
        revenue=('price', 'sum'),
        items_sold=('quantity', 'sum'),
        avg_unit_price=('price', 'mean')
    ).reset_index().sort_values(by='revenue', ascending=False)
    category_summary['revenue'] = category_summary['revenue'].round(2)
    category_summary['avg_unit_price'] = category_summary['avg_unit_price'].round(2)

    print("\n--- 3. HIEU NANG DANH MUC SAN PHAM ---")
    print(category_summary.to_string(index=False))

    # 5. Ty le hoan thanh don hang theo Phuong thuc thanh toan
    payment_status = pd.crosstab(df['payment_method'], df['order_status'], normalize='index') * 100
    print("\n--- 4. TY LE TRANG THAI DON HANG THEO PHUONG THUC THANH TOAN (%) ---")
    print(payment_status.round(2).to_string())

if __name__ == "__main__":
    run_ecommerce_eda()
