"""
Script tu dong sinh toan bo 11 tap du lieu mau (Mock Datasets)
cho cac du an thuc chien trong sach 'DATA MASTERY ALL-IN-ONE'.
Nguoi hoc chi can chay:
    python scripts/generate_all_datasets.py
Toan bo cac file .csv se duoc luu vao thu muc data/ de chay ngay lap tuc!
"""

import os
import random
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(DATA_DIR, exist_ok=True)

print(f"[*] Bat dau sinh du lieu tai thu muc: {os.path.abspath(DATA_DIR)}")

# 1. Dataset cho Project 0 & Level 0: input.csv
print("--> Dang sinh data/input.csv (5,000 ban ghi)...")
np.random.seed(42)
random.seed(42)

n_rows = 5000
ages = [random.randint(18, 70) if random.random() > 0.03 else np.nan for _ in range(n_rows)]
incomes = [round(random.gauss(50000, 15000), 2) if random.random() > 0.01 else np.nan for _ in range(n_rows)]
cities = random.choices(['Hanoi', 'Ho Chi Minh', 'Da Nang', 'Can Tho', 'Hai Phong'], k=n_rows)
scores = np.random.uniform(10.0, 100.0, n_rows).round(2)

df_input = pd.DataFrame({
    'customer_id': [f"CUST_{i:05d}" for i in range(1, n_rows + 1)],
    'age': ages,
    'income': incomes,
    'city': cities,
    'spending_score': scores,
    'signup_date': [datetime(2025, 1, 1) + timedelta(days=random.randint(0, 400)) for _ in range(n_rows)]
})
# Chen them 17 dong duplicate nhu mo ta roadmap
dup_rows = df_input.iloc[:17]
df_input = pd.concat([df_input, dup_rows], ignore_index=True)
df_input.to_csv(os.path.join(DATA_DIR, "input.csv"), index=False)

# 2. Dataset cho Project 1 & 2: E-commerce Dataset (customers, orders, order_items, payments)
print("--> Dang sinh cac tap du lieu E-commerce (customers, orders, order_items, payments)...")
n_cust = 2000
n_orders = 10000

cust_ids = [f"CUST_{i:05d}" for i in range(1, n_cust + 1)]
df_customers = pd.DataFrame({
    'customer_id': cust_ids,
    'customer_name': [f"Khach Hang {i}" for i in range(1, n_cust + 1)],
    'city': random.choices(['Hanoi', 'Ho Chi Minh', 'Da Nang', 'Hai Phong', 'Can Tho'], k=n_cust),
    'signup_date': [datetime(2024, 1, 1) + timedelta(days=random.randint(0, 700)) for _ in range(n_cust)]
})
df_customers.to_csv(os.path.join(DATA_DIR, "customers.csv"), index=False)

order_ids = [f"ORD_{i:06d}" for i in range(1, n_orders + 1)]
order_custs = random.choices(cust_ids, k=n_orders)
order_dates = [datetime(2025, 1, 1) + timedelta(days=random.randint(0, 450), hours=random.randint(0, 23)) for _ in range(n_orders)]
order_statuses = random.choices(['COMPLETED', 'CANCELLED', 'REFUNDED'], weights=[0.85, 0.10, 0.05], k=n_orders)

df_orders = pd.DataFrame({
    'order_id': order_ids,
    'customer_id': order_custs,
    'order_purchase_timestamp': order_dates,
    'order_status': order_statuses
})
df_orders.to_csv(os.path.join(DATA_DIR, "orders.csv"), index=False)

# Order items
item_records = []
categories = ['Electronics', 'Fashion', 'Home & Living', 'Beauty', 'Sports']
for oid in order_ids:
    items_in_order = random.randint(1, 4)
    for itm in range(items_in_order):
        price = round(random.uniform(10.0, 500.0), 2)
        item_records.append({
            'order_id': oid,
            'item_id': f"{oid}_ITM_{itm+1}",
            'category': random.choice(categories),
            'price': price,
            'quantity': random.choices([1, 2, 3], weights=[0.75, 0.20, 0.05])[0]
        })
df_items = pd.DataFrame(item_records)
df_items.to_csv(os.path.join(DATA_DIR, "order_items.csv"), index=False)

# Payments
payment_methods = ['credit_card', 'e_wallet', 'bank_transfer', 'cod']
df_payments = pd.DataFrame({
    'order_id': order_ids,
    'payment_method': random.choices(payment_methods, weights=[0.4, 0.3, 0.2, 0.1], k=n_orders),
    'payment_value': [round(random.uniform(20.0, 800.0), 2) for _ in range(n_orders)]
})
df_payments.to_csv(os.path.join(DATA_DIR, "payments.csv"), index=False)

# 3. Dataset cho Project 3: A/B Testing
print("--> Dang sinh data/ab_test_checkout.csv (50,000 phien nguoi dung)...")
n_ab = 50000
groups = ['control'] * 25000 + ['treatment'] * 25000
# Control conversion rate: 12%, Treatment conversion rate: 13%
conversions = [1 if random.random() < 0.12 else 0 for _ in range(25000)] + \
              [1 if random.random() < 0.13 else 0 for _ in range(25000)]
df_ab = pd.DataFrame({
    'user_id': [f"USR_{i:06d}" for i in range(1, n_ab + 1)],
    'group': groups,
    'converted': conversions,
    'device': random.choices(['mobile', 'desktop'], weights=[0.7, 0.3], k=n_ab),
    'timestamp': [datetime(2026, 3, 1) + timedelta(days=random.randint(0, 14)) for _ in range(n_ab)]
})
df_ab.to_csv(os.path.join(DATA_DIR, "ab_test_checkout.csv"), index=False)

# 4. Dataset cho Project 7 & 10: Customer Churn
print("--> Dang sinh data/customer_churn_features.csv (10,000 khach hang)...")
n_churn = 10000
tenures = [random.randint(1, 72) for _ in range(n_churn)]
monthly = [round(random.uniform(20.0, 120.0), 2) for _ in range(n_churn)]
logins = [random.randint(0, 60) for _ in range(n_churn)]
contracts = random.choices(['Month-to-Month', 'One-Year', 'Two-Year'], weights=[0.55, 0.25, 0.20], k=n_churn)

churn_prob = []
for t, m, l, c in zip(tenures, monthly, logins, contracts):
    p = 0.2
    if c == 'Month-to-Month': p += 0.25
    if l > 20: p += 0.2
    if t < 12: p += 0.15
    if m > 80: p += 0.1
    churn_prob.append(min(max(p, 0.05), 0.95))

is_churn = [1 if random.random() < p else 0 for p in churn_prob]

df_churn = pd.DataFrame({
    'customer_id': [f"CUST_CH_{i:05d}" for i in range(1, n_churn + 1)],
    'tenure_months': tenures,
    'monthly_charges': monthly,
    'total_transactions': [random.randint(1, 50) for _ in range(n_churn)],
    'days_since_last_login': logins,
    'contract_type': contracts,
    'payment_method': random.choices(['Credit Card', 'Bank Transfer', 'Electronic Check'], k=n_churn),
    'gender': random.choices(['Male', 'Female'], k=n_churn),
    'is_churn': is_churn
})
df_churn.to_csv(os.path.join(DATA_DIR, "customer_churn_features.csv"), index=False)

# 5. Dataset cho Project 5: Batch ETL
print("--> Dang sinh data/raw_transactions.csv (10,000 giao dich thuc nghiem ETL)...")
df_etl = pd.DataFrame({
    'order_id': [f"ETL_ORD_{i:06d}" for i in range(1, 10001)],
    'customer_id': random.choices(cust_ids, k=10000),
    'amount': [round(random.uniform(5.0, 1500.0), 2) if random.random() > 0.02 else -10.0 for _ in range(10000)], # co tinh chen gia tri am de test Pydantic
    'order_status': random.choices(['COMPLETED', 'PENDING', 'CANCELLED', 'INVALID_STATUS'], weights=[0.8, 0.1, 0.08, 0.02], k=10000),
    'created_at': [datetime(2026, 3, 1) + timedelta(days=random.randint(0, 28)) for _ in range(10000)],
    'discount': [round(random.uniform(0, 50), 2) for _ in range(10000)]
})
df_etl.to_csv(os.path.join(DATA_DIR, "raw_transactions.csv"), index=False)

print("\n[V] HOAN TAT! Tat ca cac tap du lieu da duoc tao thanh cong tai thu muc data/:")
for f in os.listdir(DATA_DIR):
    fpath = os.path.join(DATA_DIR, f)
    size_kb = os.path.getsize(fpath) / 1024
    print(f"    - {f:<30} : {size_kb:>8.2f} KB")
