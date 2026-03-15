import streamlit as st
import subprocess
import sqlite3
import pandas as pd
import plotly.express as px
import os

# Page config
st.set_page_config(page_title="Customer Shopping Dashboard", layout="wide")

st.title("🛒 Customer Shopping Trends Dashboard")
st.markdown("ETL Pipeline + Business Intelligence Queries")

# Sidebar
st.sidebar.header("Controls")
if st.sidebar.button("🚀 Run ETL Pipeline", type="primary"):
    with st.spinner("Running pipeline..."):
        result = subprocess.run(["python", "../run_pipeline.py"], capture_output=True, text=True)
        if result.returncode == 0:
            st.sidebar.success("✅ Pipeline completed!")
            st.sidebar.text_area("Logs:", result.stdout, height=150)
        else:
            st.sidebar.error("❌ Pipeline failed!")
            st.sidebar.text_area("Error:", result.stderr, height=150)


db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'warehouse', 'shopping_warehouse.db')
if not os.path.exists(db_path):
    st.error("❌ Database not found! Run ETL pipeline first.")
    st.stop()

@st.cache_data
def run_query(query):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📊 Regional Sales", "🌦️ Seasonal Category", "👥 Demographics", "💳 Payments", "🎂 Age Trends", "📈 Overview"])

# Tab 1: Regional
with tab1:
    st.subheader("Regional Sales & Sentiment Analysis")
    q1 = """SELECT dc.location, ROUND(SUM(ft.purchase_amount),2) total_sales, COUNT(*) transaction_count, 
            ROUND(AVG(dc.review_rating),2) avg_sentiment, ROUND(AVG(ft.purchase_amount),2) avg_tx_value
            FROM dim_customers dc JOIN fact_transactions ft ON dc.customer_id = ft.customer_id
            GROUP BY dc.location ORDER BY total_sales DESC"""
    try:
        df1 = run_query(q1)
        st.dataframe(df1, width='stretch')
        fig1 = px.bar(df1, x='location', y='total_sales', color='avg_sentiment', 
                      title="Sales by Location (colored by sentiment)")
        st.plotly_chart(fig1, width='stretch')
    except Exception as e:
        st.error(f"Error loading data: {e}")

# Tab 2: Seasonal
with tab2:
    st.subheader("Seasonal Category Performance")
    q2 = """SELECT season, category, ROUND(SUM(purchase_amount),2) total_sales, COUNT(*) transaction_count
            FROM fact_transactions GROUP BY season, category ORDER BY total_sales DESC"""
    try:
        df2 = run_query(q2)
        st.dataframe(df2.head(10), width='stretch')
        fig2 = px.sunburst(df2, path=['season','category'], values='total_sales', title="Sales Tree")
        st.plotly_chart(fig2, width='stretch')
    except Exception as e:
        st.error(f"Error loading data: {e}")

# Tab 3: Demographics
with tab3:
    st.subheader("Demographics Revenue Analysis")
    q3 = """SELECT CASE WHEN dc.age BETWEEN 18 AND 30 THEN '18-30' WHEN dc.age BETWEEN 31 AND 50 THEN '31-50' ELSE '51+' END age_group,
            dc.location, ROUND(SUM(ft.purchase_amount),2) total_revenue, COUNT(DISTINCT dc.customer_id) customers
            FROM dim_customers dc JOIN fact_transactions ft ON dc.customer_id = ft.customer_id 
            GROUP BY age_group, dc.location ORDER BY total_revenue DESC"""
    try:
        df3 = run_query(q3)
        st.dataframe(df3, width='stretch')
        fig3 = px.treemap(df3, path=['age_group','location'], values='total_revenue')
        st.plotly_chart(fig3, width='stretch')
    except Exception as e:
        st.error(f"Error loading data: {e}")

# Tab 4: Payments
with tab4:
    st.subheader("Payment Method Analysis")
    q4 = """SELECT payment_method, ROUND(AVG(purchase_amount),2) avg_size, ROUND(SUM(tax_amount),2) total_tax, 
            COUNT(*) tx_count FROM fact_transactions GROUP BY payment_method ORDER BY avg_size DESC"""
    try:
        df4 = run_query(q4)
        st.dataframe(df4, use_container_width=True)
        fig4 = px.bar(df4, x='payment_method', y=['avg_size','total_tax'], barmode='group')
        st.plotly_chart(fig4, width='stretch')
    except Exception as e:
        st.error(f"Error loading data: {e}")

# Tab 5: Age
with tab5:
    st.subheader("Age Group Spending Trends")
    q5 = """SELECT CASE WHEN dc.age BETWEEN 18 AND 30 THEN '18-30' WHEN dc.age BETWEEN 31 AND 50 THEN '31-50' ELSE '51+' END age_group,
            COUNT(DISTINCT dc.customer_id) customers, ROUND(SUM(ft.purchase_amount),2) total_spend, ROUND(AVG(ft.purchase_amount),2) avg_tx
            FROM dim_customers dc JOIN fact_transactions ft ON dc.customer_id=ft.customer_id GROUP BY age_group"""
    try:
        df5 = run_query(q5)
        st.dataframe(df5, use_container_width=True)
        fig5 = px.pie(df5, names='age_group', values='total_spend')
        st.plotly_chart(fig5, width='stretch')
    except Exception as e:
        st.error(f"Error loading data: {e}")

# Tab 6: Overview
with tab6:
    st.subheader("Quick Metrics Overview")
    col1, col2 = st.columns(2)
    with col1:
        q_cat = "SELECT category, ROUND(SUM(purchase_amount),2) total FROM fact_transactions GROUP BY category ORDER BY total DESC"
        df_cat = run_query(q_cat)
        fig_cat = px.bar(df_cat, x='category', y='total', title="Categories")
        st.plotly_chart(fig_cat, width='stretch')
    with col2:
        q_season = "SELECT season, ROUND(SUM(purchase_amount),2) total FROM fact_transactions GROUP BY season"
        df_season = run_query(q_season)
        fig_season = px.pie(df_season, names='season', values='total', title="Seasons")
        st.plotly_chart(fig_season, width='stretch')

    total_df = run_query('SELECT SUM(purchase_amount) as total_rev, COUNT(*) as total_tx FROM fact_transactions')
    st.metric("Total Revenue", f"${total_df['total_rev'][0]:.2f}")
    st.metric("Total Transactions", f"{int(total_df['total_tx'][0]):,}")

st.markdown("---")
st.caption("💾 Data: shopping_warehouse.db | Refresh: Run Pipeline button")

