import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Config
st.set_page_config(page_title="Nassau Candy Analysis", layout="wide")
st.title("🏭 Nassau Candy Advanced Logistics Dashboard")

# 2. Data Load & Clean
@st.cache_data
def load_data():
    df = pd.read_csv('data/Nassau Candy Distributor (1).csv')
    df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d-%m-%Y', errors='coerce')
    df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='%d-%m-%Y', errors='coerce')
    df['Lead Time'] = (df['Ship Date'] - df['Order Date']).dt.days
    df['Gross Profit'] = df['Sales'] - df['Cost']
    return df.dropna(subset=['Lead Time', 'Gross Profit'])

df = load_data()

# --- SIDEBAR (User Controls) ---
st.sidebar.header("Filter Data")
selected_region = st.sidebar.multiselect("Select State/Province", options=df['State/Province'].unique(), default=df['State/Province'].unique())
df_filtered = df[df['State/Province'].isin(selected_region)]

# 3. Overview Module
st.subheader("📊 Executive Overview")
kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric("Total Sales", f"${df_filtered['Sales'].sum():,.0f}")
kpi2.metric("Avg Lead Time", f"{df_filtered['Lead Time'].mean():.1f} days")
kpi3.metric("Total Profit", f"${df_filtered['Gross Profit'].sum():,.0f}")

# 4. Geo Visuals
st.subheader("🗺️ Geographic Performance")
fig_map = px.choropleth(df_filtered, locations='State/Province', locationmode="USA-states", 
                       color='Gross Profit', scope="usa", title="Profit Heatmap by State")
st.plotly_chart(fig_map, use_container_width=True)

# 5. Comparison Tool
st.subheader("⚖️ Comparison Tool")
mode_comp = df_filtered.groupby('Ship Mode')[['Lead Time', 'Gross Profit']].mean()
st.table(mode_comp)
