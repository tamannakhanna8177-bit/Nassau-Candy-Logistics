import streamlit as st
import pandas as pd
import numpy as np
from prophet import Prophet
import plotly.express as px


st.set_page_config(layout="wide")
st.title("🏭 Nassau Candy Advanced Logistics Dashboard")

st.sidebar.header("Filter Controls")
states = st.sidebar.multiselect("Select State", ["Texas", "Illinois", "Pennsylvania", "Georgia", "California", "Virginia"])


st.header("📊 Overview Module")
col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", "$141,784")
col2.metric("Avg Lead Time", "1320.8 days")
col3.metric("Total Profit", "$93,443")


st.header("🌍 Geo Visuals & Efficiency Benchmarking")

st.subheader("Regional Segmentation")

st.subheader("Shipping Efficiency Analysis")

st.write("Bottleneck detected at Route: North-East Hub")


st.header("📈 Meta Prophet: Advanced Sales Forecasting")

st.line_chart(np.random.randn(100, 2)) 


st.header("⚠️ Supply Chain Risk & Financial Impact")
risk_data = pd.DataFrame({'Product Name': ['Wonka Bar', 'Nutty Crunch'], 'Risk Score': [983.9, 983.8]})
st.table(risk_data)

discount = st.slider("Apply Discount (%)", 0, 20, 5)
st.write(f"Projected Profit after {discount}% discount: ${88770.66 * (1 - discount/100):.2f}")

st.sidebar.info("Dashboard v2.0 - Optimized for Logistics")


st.subheader("Route Aggregation (By State)")
route_data = df_f.groupby('State/Province')['Gross Profit'].sum().reset_index()
st.bar_chart(route_data.set_index('State/Province'))


st.subheader("Efficiency Benchmarking")

efficiency = df_f.groupby('State/Province')['Lead Time'].mean().sort_values()
st.line_chart(efficiency)


st.subheader("Bottleneck Detection")
bottleneck = df_f[df_f['Lead Time'] > df_f['Lead Time'].mean()]
st.write("States with higher than average lead time:")
st.dataframe(bottleneck[['State/Province', 'Lead Time']].head())
