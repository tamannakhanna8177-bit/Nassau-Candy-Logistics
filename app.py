import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Config
st.set_page_config(page_title="Nassau Candy Analysis", layout="wide")
st.title("🏭 Nassau Candy Logistics Dashboard")

# 2. Data Load Function (Pehle define karein)
@st.cache_data
def load_data():
    df = pd.read_csv('data/Nassau Candy Distributor (1).csv')
    df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)
    df['Ship Date'] = pd.to_datetime(df['Ship Date'], dayfirst=True)
    df['Lead Time'] = (df['Ship Date'] - df['Order Date']).dt.days
    
    # Negative values ko yahan remove karein
    df = df[df['Lead Time'] >= 0] 
    return df

# 3. Ab Data Load karein (Yeh call karna zaroori hai)
df = load_data()

# 4. Ab Charts banayein
st.subheader("📊 Shipping Performance Analysis")

fig1 = px.bar(df.groupby('Ship Mode')['Lead Time'].mean().reset_index(), 
             x='Ship Mode', y='Lead Time', title="Avg Lead Time by Shipping Mode")
st.plotly_chart(fig1, use_container_width=True)
