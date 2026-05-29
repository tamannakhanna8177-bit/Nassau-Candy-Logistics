import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Nassau Candy Analysis", layout="wide")
st.title("🏭 Nassau Candy Logistics Dashboard")

@st.cache_data
def load_data():
    df = pd.read_csv('data/Nassau Candy Distributor (1).csv')
    
    # Date format ko explicitly define kar rahe hain
    df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d-%m-%Y', errors='coerce')
    df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='%d-%m-%Y', errors='coerce')
    
    # Lead Time Calculate karna
    df['Lead Time'] = (df['Ship Date'] - df['Order Date']).dt.days
    
    # Sirf sahi data rakhein
    df = df.dropna(subset=['Lead Time'])
    return df

df = load_data()

# Charts
st.subheader("📊 Shipping Performance Analysis")

# Sahi calculation ke liye groupby
chart_data = df.groupby('Ship Mode')['Lead Time'].mean().reset_index()

fig1 = px.bar(chart_data, x='Ship Mode', y='Lead Time', 
             title="Avg Lead Time by Shipping Mode",
             color='Ship Mode', template="plotly_dark")

st.plotly_chart(fig1, use_container_width=True)
