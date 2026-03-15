import pandas as pd
import numpy as np
import json
import os

def generate_mock_data():
    # Requirement: Split between Cloud (Object Storage) and On-Premise [cite: 61]
    os.makedirs("data/source_customers", exist_ok=True) 
    os.makedirs("data/source_transactions", exist_ok=True)

    # Source B: On-Premise (Local JSON) - Customer Metadata
    customers = {
        "customer_id": [f"CUST-{i:03d}" for i in range(1, 51)],
        "age": np.random.randint(18, 70, 50).tolist(),
        "location": np.random.choice(["Hamburg", "Berlin", "Munich", "Frankfurt"], 50).tolist(),
        "review_rating": np.random.uniform(1.0, 5.0, 50).tolist()
    }
    with open("data/source_customers/customer_profiles.json", "w") as f:
        json.dump(customers, f, indent=4)

    # Source A: Object Storage (Cloud CSV) - 15,000 Transactional Rows
    rows = 15000
    transactions = {
        "transaction_id": range(1, rows + 1),
        "customer_id": [f"CUST-{np.random.randint(1, 51):03d}" for _ in range(rows)],
        "purchase_amount": np.random.uniform(10.0, 500.0, rows),
        "category": np.random.choice(["Electronics", "Clothing", "Home", "Books"], rows),
        "season": np.random.choice(["Winter", "Spring", "Summer", "Fall"], rows),
        "payment_method": np.random.choice(["Credit Card", "PayPal", "Bank Transfer"], rows),
        "timestamp": pd.date_range(start="2026-01-01", periods=rows, freq="min")
    }
    pd.DataFrame(transactions).to_csv("data/source_transactions/transactions.csv", index=False)

def load_cloud_data():
    return pd.read_csv("data/source_transactions/transactions.csv")

def load_local_data():
    return pd.read_json("data/source_customers/customer_profiles.json")
