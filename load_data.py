import sqlite3
import os

def load_to_db(df):
    os.makedirs("data/warehouse", exist_ok=True)
    conn = sqlite3.connect("data/warehouse/shopping_warehouse.db")

    # One-to-Many Relationship Architecture [cite: 60]
    # Primary Key Table
    df[["customer_id", "age", "location", "review_rating"]].drop_duplicates().to_sql(
        "dim_customers", conn, if_exists="replace", index=False
    )

    # Foreign Key Table
    df[["transaction_id", "customer_id", "purchase_amount", "tax_amount", "category", "season", "payment_method", "timestamp"]].to_sql(
        "fact_transactions", conn, if_exists="replace", index=False
    )
    
    conn.close()
