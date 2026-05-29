import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.cluster import KMeans
from prophet import Prophet
import numpy as np

st.set_page_config(page_title="Nassau Candy Logistics", layout="wide")
st.title("🏭 Nassau Candy Advanced Logistics Dashboard")

@st.cache_data
def load_data():
    df = pd.read_csv('data/Nassau Candy Distributor (1).csv')
    df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d-%m-%Y', errors='coerce')
    df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='%d-%m-%Y', errors='coerce')
    df['Lead Time'] = (df['Ship Date'] - df['Order Date']).dt.days
    df['Gross Profit'] = df['Sales'] - df['Cost']
    return df.dropna(subset=['Lead Time', 'Gross Profit', 'Order Date', 'Product Name'])

df = load_data()


st.sidebar.header("Filter Controls")
states = st.sidebar.multiselect("Select State", options=df['State/Province'].unique(), default=df['State/Province'].unique())
df_f = df[df['State/Province'].isin(states)]


col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${df_f['Sales'].sum():,.0f}")
col2.metric("Avg Lead Time", f"{df_f['Lead Time'].mean():.1f} days")
col3.metric("Total Profit", f"${df_f['Gross Profit'].sum():,.0f}")


st.subheader("🗺️ Geographic Performance & AI Clustering")
c1, c2 = st.columns(2)
with c1:
    df_map = df_f.groupby('State/Province')['Gross Profit'].sum().reset_index()
    fig = px.choropleth(df_map, locations='State/Province', locationmode="USA-states", color='Gross Profit', scope="usa")
    st.plotly_chart(fig, use_container_width=True)

with c2:
    df_c = df_f.groupby('State/Province')[['Lead Time', 'Gross Profit']].mean().dropna()
    kmeans = KMeans(n_clusters=3, random_state=42, n_init='auto').fit(df_c)
    df_c['Cluster'] = kmeans.labels_
    fig_cl = px.scatter(df_c, x='Lead Time', y='Gross Profit', color='Cluster', title="Regional Segmentation")
    st.plotly_chart(fig_cl, use_container_width=True)


st.subheader("📈 Meta Prophet: Advanced Sales Forecasting")
df_p = df_f.groupby('Order Date')['Sales'].sum().reset_index().rename(columns={'Order Date': 'ds', 'Sales': 'y'})
m = Prophet(yearly_seasonality=True).fit(df_p)
forecast = m.predict(m.make_future_dataframe(periods=30))
st.plotly_chart(px.line(forecast, x='ds', y='yhat', title="Sales Trend"), use_container_width=True)


st.subheader("⚠️ Supply Chain Risk Analysis")
df['Risk Score'] = (df['Lead Time'] * 0.6) - (df['Sales'] * 0.4)
st.dataframe(df[['Product Name', 'Risk Score']].sort_values(by='Risk Score', ascending=False).head(5))


st.subheader("🧪 Financial Impact Stimulation (What-If)")
discount = st.slider("Apply Discount (%)", 0, 20, 5)
projected_profit = df_f['Gross Profit'].sum() * (1 - discount/100)
st.write(f"Projected Profit after {discount}% discount: ${projected_profit:,.2f}")
