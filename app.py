import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Settings
st.set_page_config(page_title="Nassau Candy Analysis", layout="wide")
st.title("🏭 Nassau Candy Logistics Dashboard")

# 2. Data Loading & Cleaning
@st.cache_data
def load_data():
    df = pd.read_csv('data/Nassau Candy Distributor (1).csv')
    df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d-%m-%Y', errors='coerce')
    df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='%d-%m-%Y', errors='coerce')
    df['Lead Time'] = (df['Ship Date'] - df['Order Date']).dt.days
    df['Gross Profit'] = df['Sales'] - df['Cost']
    return df.dropna(subset=['Lead Time', 'Gross Profit'])

df = load_data()

# 3. KPI Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${df['Sales'].sum():,.0f}")
col2.metric("Avg Lead Time", f"{df['Lead Time'].mean():.1f} days")
col3.metric("Total Profit", f"${df['Gross Profit'].sum():,.0f}")

st.markdown("---")

# 4. Bottleneck Detection
st.subheader("⚠️ Bottleneck Detection (High Lead Time States)")
bottlenecks = df.groupby('State/Province')['Lead Time'].mean().sort_values(ascending=False).head(5)
st.bar_chart(bottlenecks)

# 5. Efficiency Benchmarking
st.subheader("✅ Shipping Efficiency Benchmark")
df['Status'] = df['Lead Time'].apply(lambda x: 'On-Time' if x <= 5 else 'Delayed')
status_counts = df['Status'].value_counts()
fig_pie = px.pie(values=status_counts.values, names=status_counts.index)
st.plotly_chart(fig_pie)
