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


import smtplib
from email.message import EmailMessage

def send_alert(message_body):
    msg = EmailMessage()
    msg.set_content(message_body)
    msg['Subject'] = 'Supply Chain Alert!'
    msg['From'] = 'your-email@gmail.com'
    msg['To'] = 'manager@example.com'
    
    # Iske liye aapko 'App Password' ki zaroorat padegi
    # server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    # server.login('your-email@gmail.com', 'your-app-password')
    # server.send_message(msg)
    # server.quit()
    st.warning("Simulated Email Sent: " + message_body)

if avg_lead_time > 1300:
    if st.button("Send Manager Alert"):
        send_alert(f"Critical Lead Time: {avg_lead_time:.1f} days")

# --- ADVANCE GEOSPATIAL ANALYSIS ---
st.subheader("📍 Geospatial Analysis: Distance vs. Lead Time Correlation")

# Scatter plot: Har state ka avg lead time vs profit
# Agar aapke paas 'Distance' column nahi hai, toh hum 'Lead Time' ko 'State' ke hisaab se analyze karenge
fig_geo = px.scatter(
    df_filtered.groupby('State/Province')[['Lead Time', 'Gross Profit']].mean().reset_index(),
    x='Lead Time', 
    y='Gross Profit',
    size='Gross Profit',
    color='State/Province',
    title="Correlation: Lead Time Impact on Profitability by State",
    hover_name='State/Province'
)

st.plotly_chart(fig_geo, width='stretch')

import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
import numpy as np

# 1. Page Config
st.set_page_config(page_title="Nassau Candy Logistics", layout="wide")
st.title("🏭 Nassau Candy Advanced Logistics Dashboard")

# 2. Data Loading
@st.cache_data
def load_data():
    df = pd.read_csv('data/Nassau Candy Distributor (1).csv')
    df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d-%m-%Y', errors='coerce')
    df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='%d-%m-%Y', errors='coerce')
    df['Lead Time'] = (df['Ship Date'] - df['Order Date']).dt.days
    df['Gross Profit'] = df['Sales'] - df['Cost']
    
    # Yahan columns check karein
    st.sidebar.write("Available Columns:", df.columns.tolist()) 
    return df.dropna(subset=['Lead Time', 'Gross Profit', 'Order Date'])

df = load_data()

# 3. Sidebar Filter
st.sidebar.header("Filter Controls")
states = st.sidebar.multiselect("Select State", options=df['State/Province'].unique(), default=df['State/Province'].unique())
df_f = df[df['State/Province'].isin(states)]

# 4. Overview
col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${df_f['Sales'].sum():,.0f}")
col2.metric("Avg Lead Time", f"{df_f['Lead Time'].mean():.1f} days")
col3.metric("Total Profit", f"${df_f['Gross Profit'].sum():,.0f}")

# 5. Geo Visuals & Correlation
st.subheader("🗺️ Geographic Performance & Correlation Analysis")
c1, c2 = st.columns(2)
with c1:
    df_map = df_f.groupby('State/Province')['Gross Profit'].sum().reset_index()
    fig = px.choropleth(df_map, locations='State/Province', locationmode="USA-states", color='Gross Profit', scope="usa")
    st.plotly_chart(fig, width='stretch')
with c2:
    fig_geo = px.scatter(df_f.groupby('State/Province')[['Lead Time', 'Gross Profit']].mean().reset_index(),
                         x='Lead Time', y='Gross Profit', size='Gross Profit', color='State/Province')
    st.plotly_chart(fig_geo, width='stretch')

# 6. Predictive & Alerts
st.subheader("🔮 Predictive Analytics & Smart Alerts")
df['Days_Since_Start'] = (df['Order Date'] - df['Order Date'].min()).dt.days
model = LinearRegression().fit(df[['Days_Since_Start']], df['Lead Time'])
prediction = model.predict(np.array([[df['Days_Since_Start'].max() + 30]]))
st.info(f"🚀 Predicted Lead Time: {prediction[0]:.1f} days")

# 7. Financial Simulation
st.subheader("💰 Financial Impact: What-If Simulation")
reduction = st.slider("Simulate Shipping Cost Reduction (%)", 0, 20, 5)
projected = df_f['Gross Profit'].sum() + (df_f['Cost'].sum() * (reduction / 100))
st.metric("Projected Profit", f"${projected:,.0f}")

# Is code ko apne app.py mein wahan add karein jahan aapne metrics define kiye hain
st.subheader("💰 Cost Optimization Analysis")

# 1. Profit Margin Calculation
df_f['Profit Margin'] = ((df_f['Sales'] - df_f['Cost']) / df_f['Sales']) * 100

# 2. High Cost Bottlenecks (Cost optimization ke liye)
st.write("Products with lowest profit margins (High Cost Areas):")
low_margin_products = df_f.sort_values(by='Profit Margin').head(5)
st.dataframe(low_margin_products[['Product Name', 'Sales', 'Cost', 'Profit Margin']])

# 3. Cost vs Profit Chart
st.subheader("Sales vs Cost Analysis")
fig = px.scatter(df_f, x='Cost', y='Sales', color='State/Province', 
                 title="Relationship between Sales and Cost per Region")
st.plotly_chart(fig)

# 4. Optimization Suggestion
st.info("💡 Suggestion: Focus on reducing cost for products in the bottom-left of the scatter plot with high cost but low sales.")

# Isse apne app.py mein niche ki taraf add karein

st.subheader("🔍 Categorical Deep Dive & Product Efficiency")

# 1. Product Specific Efficiency
# Efficiency = Sales per unit of Lead Time (Higher is better)
df_f['Product Efficiency'] = df_f['Sales'] / (df_f['Lead Time'] + 1) # +1 to avoid division by zero

st.write("Top 5 Most Efficient Products:")
top_products = df_f.groupby('Product Name')['Product Efficiency'].mean().sort_values(ascending=False).head(5)
st.bar_chart(top_products)

# 2. Categorical Analysis
# Agar aapke data mein 'Category' column hai, toh ye line kaam karegi
if 'Category' in df_f.columns:
    st.subheader("Category Performance")
    cat_data = df_f.groupby('Category')[['Sales', 'Gross Profit']].sum()
    st.dataframe(cat_data)
else:
    st.warning("Data mein 'Category' column nahi mila. 'Product Name' ka distribution dekh rahe hain:")
    st.bar_chart(df_f.groupby('Product Name')['Sales'].sum().sort_values(ascending=False).head(10))

# 3. Efficiency Benchmarking (Scatter plot)
st.subheader("Efficiency Benchmarking: Sales vs Lead Time")
import plotly.express as px
fig = px.scatter(df_f, x='Lead Time', y='Sales', color='Product Name', 
                 title="Product Efficiency: High Sales, Low Lead Time is Target")
st.plotly_chart(fig, use_container_width=True)

from sklearn.cluster import KMeans
import plotly.express as px

st.subheader("🤖 K-Means Clustering: Regional Segmentation")

# 1. Clustering ke liye data prepare karein
# Sirf numeric columns lein jo clustering ke liye zaroori hain
cluster_data = df_f.groupby('State/Province')[['Lead Time', 'Gross Profit']].mean().dropna()

# 2. K-Means Model
n_clusters = 3
kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init='auto')
cluster_data['Cluster'] = kmeans.fit_predict(cluster_data[['Lead Time', 'Gross Profit']])

# 3. Visualization
fig = px.scatter(cluster_data, x='Lead Time', y='Gross Profit', 
                 color='Cluster', 
                 text=cluster_data.index,
                 title="Regional Clusters based on Lead Time vs Profit")
fig.update_traces(textposition='top center')
st.plotly_chart(fig, use_container_width=True)

# 4. Cluster Description
st.write("Cluster Interpretation:")
st.write("Cluster 0: High Profit, Low Lead Time (Efficient)")
st.write("Cluster 1: Moderate Performance")
st.write("Cluster 2: High Lead Time, Low Profit (Optimization Required)")

from prophet import Prophet

st.subheader("📈 Meta Prophet: Advanced Sales Forecasting")

# 1. Data Prep for Prophet (Prophet ko 'ds' aur 'y' columns chahiye)
df_prophet = df_f.groupby('Order Date')['Sales'].sum().reset_index()
df_prophet.rename(columns={'Order Date': 'ds', 'Sales': 'y'}, inplace=True)

# 2. Model Training
m = Prophet(yearly_seasonality=True, daily_seasonality=False)
m.fit(df_prophet)

# 3. Future Forecasting (Agle 30 dino ke liye)
future = m.make_future_dataframe(periods=30)
forecast = m.predict(future)

# 4. Visualization
fig1 = m.plot(forecast)
st.pyplot(fig1)

# 5. Trend Components (Seasonality check)
st.subheader("Forecast Components")
fig2 = m.plot_components(forecast)
st.pyplot(fig2)

import streamlit as st
import pandas as pd
import plotly.express as px

st.subheader("📈 Historical Trend Analysis")

# 1. Trend Analysis ke liye Data Grouping
# Hum 'Order Date' ke basis par Sales aur Profit ka trend dekhenge
trend_data = df_f.groupby('Order Date')[['Sales', 'Gross Profit']].sum().reset_index()

# 2. Plotly Line Chart (Interactive)
fig = px.line(trend_data, x='Order Date', y=['Sales', 'Gross Profit'], 
              title="Sales and Gross Profit Trend over Time",
              labels={'value': 'Amount ($)', 'Order Date': 'Date'})

# Chart ko customize karna
fig.update_layout(hovermode="x unified")
st.plotly_chart(fig, use_container_width=True)

# 3. Monthly Trend (Agar daily data bahut zyada hai)
st.subheader("Monthly Sales Trend")
df_f['Order Date'] = pd.to_datetime(df_f['Order Date'])
monthly_trend = df_f.set_index('Order Date').resample('M')[['Sales']].sum().reset_index()

fig_m = px.area(monthly_trend, x='Order Date', y='Sales', title="Monthly Sales Volume")
st.plotly_chart(fig_m, use_container_width=True)
