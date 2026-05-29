import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
import numpy as np

st.set_page_config(page_title="Nassau Candy Analysis", layout="wide")
st.title("🏭 Nassau Candy Advanced Logistics Dashboard")

@st.cache_data
def load_data():
    df = pd.read_csv('data/Nassau Candy Distributor (1).csv')

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

    df['Lead Time'] = (df['Ship Date'] - df['Order Date']).dt.days
    df['Gross Profit'] = df['Sales'] - df['Cost']

    
    df = df.dropna(subset=['Lead Time', 'Gross Profit', 'Order Date'])

    return df


df = load_data()


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


df_filtered = df[
    (df['State/Province'].isin(selected_region)) &
    (df['Ship Mode'].isin(selected_mode))
]


df_filtered = df_filtered.copy()

df_filtered['Status'] = df_filtered['Lead Time'].apply(
    lambda x: 'On-Time' if x <= 5 else 'Delayed'
)


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

st.subheader("⚠️ Bottleneck Detection")

bottlenecks = (
    df_filtered.groupby('State/Province')['Lead Time']
    .mean()
    .sort_values(ascending=False)
    .head(5)
)

st.bar_chart(bottlenecks)


st.subheader("✅ Shipping Efficiency Benchmark")

status_counts = df_filtered['Status'].value_counts()

fig_pie = px.pie(
    values=status_counts.values,
    names=status_counts.index,
    title="On-Time vs Delayed Shipments"
)

st.plotly_chart(fig_pie, use_container_width=True)


st.subheader("⚖️ Comparison Tool: Ship Mode Performance")

mode_comp = df_filtered.groupby('Ship Mode')[
    ['Lead Time', 'Gross Profit']
].mean()

st.table(mode_comp)


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


st.dataframe(
    route_data.sort_values(by='Lead Time', ascending=False),
    use_container_width=True
)


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


st.subheader("🔮 Predictive Analytics: Lead Time Forecast")


df['Days_Since_Start'] = (
    df['Order Date'] - df['Order Date'].min()
).dt.days

X = df[['Days_Since_Start']]
y = df['Lead Time']


model = LinearRegression()
model.fit(X, y)


last_day = df['Days_Since_Start'].max()

future_days = np.array([[last_day + 30]])

prediction = model.predict(future_days)

st.info(
    f"🚀 Predicted Average Lead Time for next 30 days: "
    f"{prediction[0]:.1f} days"
)


st.sidebar.subheader("⚙️ Advanced Settings")

st.sidebar.write(
    "You can add more filters here like Date Range, Product Category, etc."
)


st.subheader("🔔 Smart Alerts: Performance Monitor")

avg_lead_time = df_filtered['Lead Time'].mean()

if avg_lead_time > 1300: 
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
    
    
    st.warning("Simulated Email Sent: " + message_body)

if avg_lead_time > 1300:
    if st.button("Send Manager Alert"):
        send_alert(f"Critical Lead Time: {avg_lead_time:.1f} days")


st.subheader("📍 Geospatial Analysis: Distance vs. Lead Time Correlation")


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

st.set_page_config(page_title="Nassau Candy Logistics", layout="wide")
st.title("🏭 Nassau Candy Advanced Logistics Dashboard")


@st.cache_data
def load_data():
    df = pd.read_csv('data/Nassau Candy Distributor (1).csv')
    df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d-%m-%Y', errors='coerce')
    df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='%d-%m-%Y', errors='coerce')
    df['Lead Time'] = (df['Ship Date'] - df['Order Date']).dt.days
    df['Gross Profit'] = df['Sales'] - df['Cost']
    
    
    st.sidebar.write("Available Columns:", df.columns.tolist()) 
    return df.dropna(subset=['Lead Time', 'Gross Profit', 'Order Date'])

df = load_data()


st.sidebar.header("Filter Controls")
states = st.sidebar.multiselect("Select State", options=df['State/Province'].unique(), default=df['State/Province'].unique())
df_f = df[df['State/Province'].isin(states)]


col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${df_f['Sales'].sum():,.0f}")
col2.metric("Avg Lead Time", f"{df_f['Lead Time'].mean():.1f} days")
col3.metric("Total Profit", f"${df_f['Gross Profit'].sum():,.0f}")


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


st.subheader("🔮 Predictive Analytics & Smart Alerts")
df['Days_Since_Start'] = (df['Order Date'] - df['Order Date'].min()).dt.days
model = LinearRegression().fit(df[['Days_Since_Start']], df['Lead Time'])
prediction = model.predict(np.array([[df['Days_Since_Start'].max() + 30]]))
st.info(f"🚀 Predicted Lead Time: {prediction[0]:.1f} days")


st.subheader("💰 Financial Impact: What-If Simulation")
reduction = st.slider("Simulate Shipping Cost Reduction (%)", 0, 20, 5)
projected = df_f['Gross Profit'].sum() + (df_f['Cost'].sum() * (reduction / 100))
st.metric("Projected Profit", f"${projected:,.0f}")


st.subheader("💰 Cost Optimization Analysis")


df_f['Profit Margin'] = ((df_f['Sales'] - df_f['Cost']) / df_f['Sales']) * 100


st.write("Products with lowest profit margins (High Cost Areas):")
low_margin_products = df_f.sort_values(by='Profit Margin').head(5)
st.dataframe(low_margin_products[['Product Name', 'Sales', 'Cost', 'Profit Margin']])


st.subheader("Sales vs Cost Analysis")
fig = px.scatter(df_f, x='Cost', y='Sales', color='State/Province', 
                 title="Relationship between Sales and Cost per Region")
st.plotly_chart(fig)


st.info("💡 Suggestion: Focus on reducing cost for products in the bottom-left of the scatter plot with high cost but low sales.")



st.subheader("🔍 Categorical Deep Dive & Product Efficiency")

df_f['Product Efficiency'] = df_f['Sales'] / (df_f['Lead Time'] + 1) 

st.write("Top 5 Most Efficient Products:")
top_products = df_f.groupby('Product Name')['Product Efficiency'].mean().sort_values(ascending=False).head(5)
st.bar_chart(top_products)


if 'Category' in df_f.columns:
    st.subheader("Category Performance")
    cat_data = df_f.groupby('Category')[['Sales', 'Gross Profit']].sum()
    st.dataframe(cat_data)
else:
    st.warning("Data mein 'Category' column nahi mila. 'Product Name' ka distribution dekh rahe hain:")
    st.bar_chart(df_f.groupby('Product Name')['Sales'].sum().sort_values(ascending=False).head(10))


st.subheader("Efficiency Benchmarking: Sales vs Lead Time")
import plotly.express as px
fig = px.scatter(df_f, x='Lead Time', y='Sales', color='Product Name', 
                 title="Product Efficiency: High Sales, Low Lead Time is Target")
st.plotly_chart(fig, use_container_width=True)

from sklearn.cluster import KMeans
import plotly.express as px

st.subheader("🤖 K-Means Clustering: Regional Segmentation")

cluster_data = df_f.groupby('State/Province')[['Lead Time', 'Gross Profit']].mean().dropna()

n_clusters = 3
kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init='auto')
cluster_data['Cluster'] = kmeans.fit_predict(cluster_data[['Lead Time', 'Gross Profit']])

fig = px.scatter(cluster_data, x='Lead Time', y='Gross Profit', 
                 color='Cluster', 
                 text=cluster_data.index,
                 title="Regional Clusters based on Lead Time vs Profit")
fig.update_traces(textposition='top center')
st.plotly_chart(fig, use_container_width=True)


st.write("Cluster Interpretation:")
st.write("Cluster 0: High Profit, Low Lead Time (Efficient)")
st.write("Cluster 1: Moderate Performance")
st.write("Cluster 2: High Lead Time, Low Profit (Optimization Required)")

from prophet import Prophet

st.subheader("📈 Meta Prophet: Advanced Sales Forecasting")


df_prophet = df_f.groupby('Order Date')['Sales'].sum().reset_index()
df_prophet.rename(columns={'Order Date': 'ds', 'Sales': 'y'}, inplace=True)


m = Prophet(yearly_seasonality=True, daily_seasonality=False)
m.fit(df_prophet)

future = m.make_future_dataframe(periods=30)
forecast = m.predict(future)


fig1 = m.plot(forecast)
st.pyplot(fig1)


st.subheader("Forecast Components")
fig2 = m.plot_components(forecast)
st.pyplot(fig2)

import streamlit as st
import pandas as pd
import plotly.express as px

st.subheader("📈 Historical Trend Analysis")

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("🏭 Nassau Candy Advanced Logistics Dashboard")

