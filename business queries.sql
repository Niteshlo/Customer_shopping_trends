-- Business Queries for Customer Shopping Pipeline
-- Database: data/warehouse/shopping_warehouse.db
-- Tables: dim_customers (customer_id, age, location, review_rating), fact_transactions (transaction_id, customer_id, purchase_amount, tax_amount, category, season, payment_method, timestamp)

-- 1. Regional Sales & Sentiment Analysis
-- Total sales, transaction count, and average sentiment (review_rating) by location (region)
SELECT 
    dc.location,
    ROUND(SUM(ft.purchase_amount), 2) AS total_sales,
    COUNT(*) AS transaction_count,
    ROUND(AVG(dc.review_rating), 2) AS avg_sentiment,
    ROUND(AVG(ft.purchase_amount), 2) AS avg_tx_value
FROM dim_customers dc
JOIN fact_transactions ft ON dc.customer_id = ft.customer_id
GROUP BY dc.location
ORDER BY total_sales DESC;

-- 2. Seasonal Category Performance
-- Total sales and transaction count by season and category
SELECT 
    ft.season,
    ft.category,
    ROUND(SUM(ft.purchase_amount), 2) AS total_sales,
    COUNT(*) AS transaction_count,
    ROUND(AVG(ft.purchase_amount), 2) AS avg_tx_value
FROM fact_transactions ft
GROUP BY ft.season, ft.category
ORDER BY total_sales DESC;

-- 3. Revenue Analysis by Customer Demographics
-- Total revenue by age group and location
SELECT 
    CASE 
        WHEN dc.age BETWEEN 18 AND 30 THEN '18-30'
        WHEN dc.age BETWEEN 31 AND 50 THEN '31-50'
        ELSE '51+'
    END AS age_group,
    dc.location,
    ROUND(SUM(ft.purchase_amount), 2) AS total_revenue,
    COUNT(DISTINCT dc.customer_id) AS unique_customers,
    ROUND(SUM(ft.purchase_amount) / COUNT(DISTINCT dc.customer_id), 2) AS avg_spend_per_customer
FROM dim_customers dc
JOIN fact_transactions ft ON dc.customer_id = ft.customer_id
GROUP BY age_group, dc.location
ORDER BY total_revenue DESC;

-- 4. Payment Method Efficiency & Tax Contribution
-- Average transaction size, total tax amount, tax rate, and tx count by payment method
SELECT 
    ft.payment_method,
    ROUND(AVG(ft.purchase_amount), 2) AS avg_tx_size,
    ROUND(SUM(ft.tax_amount), 2) AS total_tax,
    ROUND((SUM(ft.tax_amount) / SUM(ft.purchase_amount)) * 100, 2) AS tax_rate_pct,
    COUNT(*) AS transaction_count
FROM fact_transactions ft
GROUP BY ft.payment_method
ORDER BY avg_tx_size DESC;

-- 5. Age-Based Spending Trends
-- Average and total spending by age group
SELECT 
    CASE 
        WHEN dc.age BETWEEN 18 AND 30 THEN '18-30'
        WHEN dc.age BETWEEN 31 AND 50 THEN '31-50'
        ELSE '51+'
    END AS age_group,
    COUNT(DISTINCT dc.customer_id) AS customer_count,
    ROUND(SUM(ft.purchase_amount), 2) AS total_spending,
    ROUND(AVG(ft.purchase_amount), 2) AS avg_tx_value,
    ROUND(SUM(ft.purchase_amount) / COUNT(DISTINCT dc.customer_id), 2) AS avg_spend_per_customer,
    COUNT(*) AS total_transactions
FROM dim_customers dc
JOIN fact_transactions ft ON dc.customer_id = ft.customer_id
GROUP BY age_group
ORDER BY avg_spend_per_customer DESC;
