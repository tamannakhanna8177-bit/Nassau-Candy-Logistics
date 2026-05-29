import streamlit as st
import pandas as pd

# Dashboard ka Title
st.title("🏭 Nassau Candy Logistics Dashboard")

# Data Load
try:
    # Yahan apni CSV file ka sahi path ensure karein
    df = pd.read_csv('data/nassau_candy_data.csv') 
    
    # Sidebar Filter
    st.sidebar.header("Filter Controls")
    states = st.sidebar.multiselect("Select State", df['State/Province'].unique(), default=df['State/Province'].unique())
    
    # Data Filtering
    df_f = df[df['State/Province'].isin(states)]
    
    # Basic Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Sales", f"${df_f['Sales'].sum():,.0f}")
    col2.metric("Avg Lead Time", f"{df_f['Lead Time'].mean():.1f} days")
    col3.metric("Total Profit", f"${df_f['Gross Profit'].sum():,.0f}")
    
    # Bar Chart
    st.subheader("Gross Profit by State")
    st.bar_chart(df_f.groupby('State/Province')['Gross Profit'].sum())
    
except Exception as e:
    st.error(f"Error: {e}. Please check if your CSV file is in the 'data' folder.")
