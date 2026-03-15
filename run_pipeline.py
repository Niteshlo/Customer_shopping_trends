from ingest_data import generate_mock_data, load_cloud_data, load_local_data
from transform_data import merge_data, clean_data, add_features
from load_data import load_to_db

if __name__ == "__main__":
    print("Starting Pipeline...")
    generate_mock_data()
    
    # Execute ETL steps [cite: 6]
    df = merge_data(load_cloud_data(), load_local_data())
    df = add_features(clean_data(df))
    load_to_db(df)
    
    print("Pipeline Complete.")
    # Business Objectives Analysis [cite: 62]
    print("\nObjective 1: Avg Purchase by Category")
    print(df.groupby('category')['purchase_amount'].mean())
