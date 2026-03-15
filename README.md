# Customer_shopping_trends
>>>>>>> 61a78b5950912ddc8407f802b81bedc8cc50d107
=======
# Customer Shopping Trends Pipeline 📊

## 🏢 Project Overview
This is an **end-to-end data engineering pipeline** for analyzing customer shopping trends. The pipeline ingests mock retail data (15,000 transactions + 50 customer profiles), performs ETL (Extract, Transform, Load), and provides interactive insights via Streamlit dashboard and SQL queries.

**Key Business Objectives**:
- Average purchase value by product category
- Seasonal shopping trends
- Impact of payment methods on transaction size
- Demographic spending analysis (age groups, location)
- Review rating correlation with spending

**Repository:** https://github.com/Niteshlo/Customer_shopping_trends

## 🏗️ System Architecture
Modular **ETL Pipeline** orchestrated by `run_pipeline.py`:

1. **Extract** (`ingest_data.py`): 
   - Generates mock data simulating cloud CSV (transactions) + local JSON (customers)
   - `data/source_transactions/transactions.csv` (15k rows)
   - `data/source_customers/customer_profiles.json` (50 customers)

2. **Transform** (`transform_data.py`): 
   - Cleans data (remove duplicates)
   - Merges on `customer_id`
   - Adds features: `tax_amount` (8.5% of purchase)

3. **Load** (`load_data.py`): 
   - SQLite star schema: `data/warehouse/shopping_warehouse.db`
   - **dim_customers**: `customer_id`, `age`, `location`, `review_rating`
   - **fact_transactions**: `transaction_id`, `customer_id`, `purchase_amount`, `tax_amount`, `category`, `season`, `payment_method`, `timestamp`

## 📁 Project Structure
```
Customer_Shopping_Pipeline_Project/
├── README.md                 # This file
├── run_pipeline.py           # Main ETL orchestrator
├── ingest_data.py            # Data generation/loading
├── transform_data.py         # Data cleaning/feature engineering
├── load_data.py              # SQLite loading
├── business queries.sql      # Key analytics queries
├── TODO.md                   # Progress tracking
├── ui/
│   └── dashboard.py          # Streamlit interactive dashboard
├── data/
│   ├── source_customers/
│   │   └── customer_profiles.json
│   ├── source_transactions/
│   │   └── transactions.csv
│   └── warehouse/
│       └── shopping_warehouse.db
└── outputs/                  # Screenshots of results
    └── Screenshot*.png
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install streamlit plotly pandas numpy sqlite3
```

### 2. Run ETL Pipeline
```bash
python run_pipeline.py
```
*Generates data → ETL → Loads warehouse.db → Prints category averages*

### 3. Launch Interactive Dashboard
```bash
streamlit run ui/dashboard.py
```
*Opens browser dashboard with charts, query tabs, pipeline runner*

### 4. Run Business Queries
Connect to `data/warehouse/shopping_warehouse.db` and execute `business queries.sql` for:
- Regional sales & sentiment
- Seasonal category performance
- Demographic revenue analysis
- Payment method efficiency
- Age-based spending trends

## 📈 Key Insights (from queries)
| Query | Focus |
|-------|-------|
| 1 | Total sales, avg sentiment by **location** |
| 2 | Sales by **season** + **category** |
| 3 | Revenue by **age group** + location |
| 4 | Avg tx size, tax rate by **payment method** |
| 5 | Spending trends by **age group** |

## 📷 Screenshots
See `outputs/` folder for pipeline execution and dashboard visualizations.

## 🔮 Next Steps
- Deploy to cloud (replace mock data with real S3/PostgreSQL)
- Add Airflow orchestration
- ML model for spending prediction

**Built for Data Engineering best practices: modular ETL, star schema, automated reporting.**

=======
# Customer_shopping_trends
>>>>>>> 61a78b5950912ddc8407f802b81bedc8cc50d107
