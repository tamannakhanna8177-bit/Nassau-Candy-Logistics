import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv('data/nassau_candy_data.csv') # Yahan apni file ka path check karein


st.sidebar.header("Filter Controls")
states = st.sidebar.multiselect("Select State", df['State/Province'].unique(), default=df['State/Province'].unique())


df_f = df[df['State/Province'].isin(states)]


st.title("🏭 Nassau Candy Logistics Dashboard")


col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${df_f['Sales'].sum():,.2f}")
col2.metric("Avg Lead Time", f"{df_f['Lead Time'].mean():.2f} days")
col3.metric("Total Profit", f"${df_f['Gross Profit'].sum():,.2f}")

st.subheader("Route Aggregation (Gross Profit by State)")
route_data = df_f.groupby('State/Province')['Gross Profit'].sum().reset_index()
st.bar_chart(route_data.set_index('State/Province'))

st.subheader("Bottleneck Detection (High Lead Time)")
bottleneck = df_f[df_f['Lead Time'] > df_f['Lead Time'].mean()]
st.dataframe(bottleneck[['State/Province', 'Lead Time', 'Product Name']].head())
