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
    df['Gross Profit'] = df['Sales'] - df['Cost']
    return df.dropna(subset=['Lead Time', 'Gross Profit'])

df = load_data()

# --- SIDEBAR FILTERS ---
st.sidebar.header("Filter Data")
selected_region = st.sidebar.multiselect("Select State/Province", options=df['State/Province'].unique(), default=df['State/Province'].unique())
selected_mode = st.sidebar.multiselect("Select Shipping Mode", options=df['Ship Mode'].unique(), default=df['Ship Mode'].unique())

# Filter data based on selection
df_filtered = df[(df['State/Province'].isin(selected_region)) & (df['Ship Mode'].isin(selected_mode))]

# --- DASHBOARD CONTENT ---
col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${df_filtered['Sales'].sum():,.0f}")
col2.metric("Avg Lead Time", f"{df_filtered['Lead Time'].mean():.1f} days")
col3.metric("Total Profit", f"${df_filtered['Gross Profit'].sum():,.0f}")

st.markdown("---")

# Bottleneck Detection (Filtered)
st.subheader("⚠️ Bottleneck Detection")
bottlenecks = df_filtered.groupby('State/Province')['Lead Time'].mean().sort_values(ascending=False).head(5)
st.bar_chart(bottlenecks)

# Efficiency Benchmarking
st.subheader("✅ Shipping Efficiency Benchmark")
df_filtered['Status'] = df_filtered['Lead Time'].apply(lambda x: 'On-Time' if x <= 5 else 'Delayed')
status_counts = df_filtered['Status'].value_counts()
fig_pie = px.pie(values=status_counts.values, names=status_counts.index)
st.plotly_chart(fig_pie)

# --- ROUTE AGGREGATION SECTION ---
st.subheader("🚚 Route Aggregation Analysis")

# Data ko aggregate karna (State aur Ship Mode ke basis par)
route_data = df_filtered.groupby(['State/Province', 'Ship Mode']).agg({
    'Lead Time': 'mean',
    'Gross Profit': 'sum',
    'Order ID': 'count'
}).rename(columns={'Order ID': 'Total Orders'}).reset_index()

# Table format mein dikhana (Taaki user har route ki detail dekh sake)
st.dataframe(route_data.sort_values(by='Lead Time', ascending=False), use_container_width=True)

# Plotting: Route Efficiency chart
fig_route = px.scatter(route_data, x='Lead Time', y='Gross Profit', 
                       size='Total Orders', color='Ship Mode',
                       hover_name='State/Province', 
                       title="Route Efficiency: Profit vs Lead Time (Size = Order Volume)")
st.plotly_chart(fig_route, use_container_width=True)

# 1. Overview Module (KPIs)
st.subheader("📊 Executive Overview")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Total Sales", f"${df_filtered['Sales'].sum():,.0f}")
kpi2.metric("Avg Lead Time", f"{df_filtered['Lead Time'].mean():.1f} days")
kpi3.metric("Total Profit", f"${df_filtered['Gross Profit'].sum():,.0f}")
kpi4.metric("Efficiency", f"{(df_filtered['Status']=='On-Time').mean()*100:.1f}%")

# 2. Geo Visuals
st.subheader("🗺️ Geographic Performance")
fig_map = px.choropleth(df_filtered, locations='State/Province', locationmode="USA-states", 
                       color='Gross Profit', scope="usa", title="Profit Heatmap by State")
st.plotly_chart(fig_map, use_container_width=True)

# 3. Comparison Tools
st.subheader("⚖️ Comparison Tool: Ship Mode Performance")
mode_comp = df_filtered.groupby('Ship Mode')[['Lead Time', 'Gross Profit']].mean()
st.table(mode_comp)

# 4. User Controls (Already in Sidebar)
st.sidebar.subheader("Advanced Settings")
# Yahan aap naye controls (jaise Date Range) add kar sakti hain
# Geo Visuals: Heatmap by State
st.subheader("🗺️ Geographic Performance: Profit Heatmap")

# Grouping data by state to get total profit per state
df_map = df_filtered.groupby('State/Province')['Gross Profit'].sum().reset_index()

# Choropleth map create karna
fig_map = px.choropleth(
    df_map, 
    locations='State/Province', 
    locationmode="USA-states", 
    color='Gross Profit', # Isse colors change honge
    scope="usa", 
    color_continuous_scale="Viridis", # Aap 'Blues', 'Reds' ya 'Viridis' try kar sakte hain
    title="Total Profit by State"
)

st.plotly_chart(fig_map, use_container_width=True)
