import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Settings
st.set_page_config(page_title="Nassau Candy Analysis", layout="wide")
st.title("🏭 Nassau Candy Logistics Dashboard")

# 2. Load Data
@st.cache_data
def load_data():
    df = pd.read_csv('data/Nassau Candy Distributor (1).csv')
    df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)
    df['Ship Date'] = pd.to_datetime(df['Ship Date'], dayfirst=True)
    df['Lead Time'] = (df['Ship Date'] - df['Order Date']).dt.days
    return df

df = load_data()

# 3. Add Charts (Visualization)
st.subheader("📊 Shipping Performance Analysis")

# Chart 1: Average Lead Time by Ship Mode
fig1 = px.bar(df.groupby('Ship Mode')['Lead Time'].mean().reset_index(), 
             x='Ship Mode', y='Lead Time', title="Avg Lead Time by Shipping Mode")
st.plotly_chart(fig1, use_container_width=True)

# Chart 2: Ship Mode Distribution
fig2 = px.pie(df, names='Ship Mode', title="Most Used Shipping Modes")
st.plotly_chart(fig2, use_container_width=True)
