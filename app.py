import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
import numpy as np

# 1. Page Configuration
st.set_page_config(page_title="Nassau Candy Analysis", layout="wide")
st.title("🏭 Nassau Candy Advanced Logistics Dashboard")

# 2. Data Loading & Cleaning
@st.cache_data
def load_data():
    df = pd.read_csv('data/Nassau Candy Distributor (1).csv')
    df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d-%m-%Y', errors='coerce')
    df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='%d-%m-%Y', errors='coerce')
    df['Lead Time'] = (df['Ship Date'] - df['Order Date']).dt.days
    df['Gross Profit'] = df['Sales'] - df['Cost']
    return df.dropna(subset=['Lead Time', 'Gross Profit', 'Order Date'])

df = load_data()

# 3. Sidebar (User Controls)
st.sidebar.header("Filter Data")
selected_region = st.sidebar.multiselect("Select State/Province", options=df['State/Province'].unique(), default=df['State/Province'].unique())
df_filtered = df[df['State/Province'].isin(selected_region)]

# 4. Overview Module
st.subheader("📊 Executive Overview")
kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric("Total Sales", f"${df_filtered['Sales'].sum():,.0f}")
kpi2.metric("Avg Lead Time", f"{df_filtered['Lead Time'].mean():.1f} days")
kpi3.metric("Total Profit", f"${df_filtered['Gross Profit'].sum():,.0f}")

# 5. Geo Visuals (Heatmap)
st.subheader("🗺️ Geographic Performance: Profit Heatmap")
df_map = df_filtered.groupby('State/Province')['Gross Profit'].sum().reset_index()
fig_map = px.choropleth(df_map, locations='State/Province', locationmode="USA-states", 
                       color='Gross Profit', scope="usa", color_continuous_scale="Viridis")
st.plotly_chart(fig_map, width='stretch')

# 6. Comparison Tool
st.subheader("⚖️ Comparison Tool: Ship Mode Performance")
mode_comp = df_filtered.groupby('Ship Mode')[['Lead Time', 'Gross Profit']].mean()
st.table(mode_comp)

# 7. Predictive Analytics Module
st.subheader("🔮 Predictive Analytics: Lead Time Forecast")
# Data prep: Date ko numeric mein convert karna
df['Days_Since_Start'] = (df['Order Date'] - df['Order Date'].min()).dt.days
X = df[['Days_Since_Start']]
y = df['Lead Time']

# Model Training
model = LinearRegression()
model.fit(X, y)

# Prediction for next 30 days
last_day = df['Days_Since_Start'].max()
future_days = np.array([[last_day + 30]])
prediction = model.predict(future_days)

st.info(f"🚀 Predicted Average Lead Time for next 30 days: {prediction[0]:.1f} days")
