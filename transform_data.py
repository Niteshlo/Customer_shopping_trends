import pandas as pd

def merge_data(transactions, customers):
    # Join cloud transactions with local metadata via Customer ID [cite: 60]
    return transactions.merge(customers, on="customer_id")

def clean_data(df):
    return df.drop_duplicates()

def add_features(df):
    # Adding business logic for objective analysis
    df["tax_amount"] = df["purchase_amount"] * 0.19 
    return df
