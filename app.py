import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Nassau Candy Analysis", layout="wide")
st.title("🏭 Nassau Candy Advanced Logistics Dashboard")

@st.cache_data
def load_data():
    df = pd.read_csv('data/Nassau Candy Distributor (1).csv')
    df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d-%m-%Y', errors='coerce')
    df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='%d-%m-%Y', errors='coerce')
    df['Lead Time'] = (df['Ship Date'] - df['Order Date']).dt.days
    
    # 1. Feature Engineering: Gross Profit Calculate karna
    # Note: Agar aapke CSV mein Sales aur Cost ke columns alag hain, toh naam sahi karein
    df['Gross Profit'] = df['Sales'] - df['Cost'] 
    
    df = df.dropna(subset=['Lead Time', 'Gross Profit'])
    return df

df = load_data()

# 2. KPI Metrics (Top par dikhane ke liye)
col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${df['Sales'].sum():,.0f}")
col2.metric("Avg Lead Time", f"{df['Lead Time'].mean():.1f} days")
col3.metric("Total Profit", f"${df['Gross Profit'].sum():,.0f}")

st.markdown("---")

# 3. Charts & Visualization
st.subheader("📊 Logistics & Financial Performance")

# Chart 1: Lead Time by State
fig1 = px.bar(df.groupby('State/Province')['Lead Time'].mean().reset_index(), 
             x='State/Province', y='Lead Time', title="Avg Lead Time by State")
st.plotly_chart(fig1, use_container_width=True)

# Chart 2: Profit by State
fig2 = px.bar(df.groupby('State/Province')['Gross Profit'].sum().reset_index(), 
             x='State/Province', y='Gross Profit', title="Total Profit by State", color='Gross Profit')
st.plotly_chart(fig2, use_container_width=True)

# Bottleneck Detection Section
st.subheader("⚠️ Bottleneck Detection (High Lead Time States)")

# Top 5 states jahan sabse zyada deri ho rahi hai
bottlenecks = df.groupby('State/Province')['Lead Time'].mean().sort_values(ascending=False).head(5)
st.bar_chart(bottlenecks)

# Efficiency Benchmarking
st.subheader("✅ Shipping Efficiency Benchmark")
df['Status'] = df['Lead Time'].apply(lambda x: 'On-Time' if x <= 4 else 'Delayed')
status_counts = df['Status'].value_counts()
st.pie_chart(status_counts)
