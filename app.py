import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
import numpy as np

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Nassau Candy Analysis", layout="wide")
st.title("🏭 Nassau Candy Advanced Logistics Dashboard")

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    df = pd.read_csv('data/Nassau Candy Distributor (1).csv')

    # Date conversion
    df['Order Date'] = pd.to_datetime(
        df['Order Date'],
        format='%d-%m-%Y',
        errors='coerce'
    )

    df['Ship Date'] = pd.to_datetime(
        df['Ship Date'],
        format='%d-%m-%Y',
        errors='coerce'
    )

    # New calculated columns
    df['Lead Time'] = (df['Ship Date'] - df['Order Date']).dt.days
    df['Gross Profit'] = df['Sales'] - df['Cost']

    # Remove null values
    df = df.dropna(subset=['Lead Time', 'Gross Profit', 'Order Date'])

    return df


df = load_data()

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("📌 Filter Data")

selected_region = st.sidebar.multiselect(
    "Select State/Province",
    options=df['State/Province'].unique(),
    default=df['State/Province'].unique()
)

selected_mode = st.sidebar.multiselect(
    "Select Shipping Mode",
    options=df['Ship Mode'].unique(),
    default=df['Ship Mode'].unique()
)

# Filtered Data
df_filtered = df[
    (df['State/Province'].isin(selected_region)) &
    (df['Ship Mode'].isin(selected_mode))
]

# ---------------- STATUS COLUMN ----------------
df_filtered = df_filtered.copy()

df_filtered['Status'] = df_filtered['Lead Time'].apply(
    lambda x: 'On-Time' if x <= 5 else 'Delayed'
)

# ---------------- EXECUTIVE OVERVIEW ----------------
st.subheader("📊 Executive Overview")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

kpi1.metric(
    "Total Sales",
    f"${df_filtered['Sales'].sum():,.0f}"
)

kpi2.metric(
    "Avg Lead Time",
    f"{df_filtered['Lead Time'].mean():.1f} days"
)

kpi3.metric(
    "Total Profit",
    f"${df_filtered['Gross Profit'].sum():,.0f}"
)

kpi4.metric(
    "Efficiency",
    f"{(df_filtered['Status'] == 'On-Time').mean() * 100:.1f}%"
)

st.markdown("---")

# ---------------- GEOGRAPHIC PERFORMANCE ----------------
st.subheader("🗺️ Geographic Performance: Profit Heatmap")

df_map = df_filtered.groupby(
    'State/Province'
)['Gross Profit'].sum().reset_index()

fig_map = px.choropleth(
    df_map,
    locations='State/Province',
    locationmode="USA-states",
    color='Gross Profit',
    scope="usa",
    color_continuous_scale="Viridis",
    title="Total Profit by State"
)

st.plotly_chart(fig_map, use_container_width=True)

# ---------------- BOTTLENECK DETECTION ----------------
st.subheader("⚠️ Bottleneck Detection")

bottlenecks = (
    df_filtered.groupby('State/Province')['Lead Time']
    .mean()
    .sort_values(ascending=False)
    .head(5)
)

st.bar_chart(bottlenecks)

# ---------------- SHIPPING EFFICIENCY ----------------
st.subheader("✅ Shipping Efficiency Benchmark")

status_counts = df_filtered['Status'].value_counts()

fig_pie = px.pie(
    values=status_counts.values,
    names=status_counts.index,
    title="On-Time vs Delayed Shipments"
)

st.plotly_chart(fig_pie, use_container_width=True)

# ---------------- SHIP MODE COMPARISON ----------------
st.subheader("⚖️ Comparison Tool: Ship Mode Performance")

mode_comp = df_filtered.groupby('Ship Mode')[
    ['Lead Time', 'Gross Profit']
].mean()

st.table(mode_comp)

# ---------------- ROUTE AGGREGATION ----------------
st.subheader("🚚 Route Aggregation Analysis")

route_data = df_filtered.groupby(
    ['State/Province', 'Ship Mode']
).agg({
    'Lead Time': 'mean',
    'Gross Profit': 'sum',
    'Order ID': 'count'
}).rename(columns={
    'Order ID': 'Total Orders'
}).reset_index()

# Route Table
st.dataframe(
    route_data.sort_values(by='Lead Time', ascending=False),
    use_container_width=True
)

# Scatter Plot
fig_route = px.scatter(
    route_data,
    x='Lead Time',
    y='Gross Profit',
    size='Total Orders',
    color='Ship Mode',
    hover_name='State/Province',
    title="Route Efficiency: Profit vs Lead Time"
)

st.plotly_chart(fig_route, use_container_width=True)

# ---------------- PREDICTIVE ANALYTICS ----------------
st.subheader("🔮 Predictive Analytics: Lead Time Forecast")

# Convert date into numeric value
df['Days_Since_Start'] = (
    df['Order Date'] - df['Order Date'].min()
).dt.days

X = df[['Days_Since_Start']]
y = df['Lead Time']

# Train Model
model = LinearRegression()
model.fit(X, y)

# Future prediction
last_day = df['Days_Since_Start'].max()

future_days = np.array([[last_day + 30]])

prediction = model.predict(future_days)

st.info(
    f"🚀 Predicted Average Lead Time for next 30 days: "
    f"{prediction[0]:.1f} days"
)

# ---------------- ADVANCED SETTINGS ----------------
st.sidebar.subheader("⚙️ Advanced Settings")

st.sidebar.write(
    "You can add more filters here like Date Range, Product Category, etc."
)

# Threshold Alert Logic
st.subheader("🔔 Smart Alerts: Performance Monitor")

avg_lead_time = df_filtered['Lead Time'].mean()

if avg_lead_time > 1300: # Aap apni threshold value yahan set karein
    st.error(f"⚠️ ALERT: High Lead Time detected ({avg_lead_time:.1f} days)! Check North region routes.")
else:
    st.success("✅ Logistics performance is within acceptable thresholds.")
