import streamlit as st
import pandas as pd

# Page config
st.set_page_config(page_title="Nassau Candy Analysis", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv('data/Nassau Candy Distributor (1).csv')
    
    # Date columns ko sahi format mein convert karein
    df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)
    df['Ship Date'] = pd.to_datetime(df['Ship Date'], dayfirst=True)
    
    df['Lead Time'] = (df['Ship Date'] - df['Order Date']).dt.days
    return df

# Main logic
st.title("🏭 Nassau Candy Logistics Dashboard")
df = load_data()

st.write("### Data Preview", df.head())
