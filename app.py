import streamlit as st
import pandas as pd

# 1. Sabse pehle Data Load (Yahan sahi path dein)
@st.cache_data
def get_data():
    return pd.read_csv('data/nassau_candy_data.csv') 

df = get_data()

# 2. Sidebar Filter (Isse pehle koi aur calculation nahi)
st.sidebar.header("Filter Controls")
states = st.sidebar.multiselect("Select State", df['State/Province'].unique(), default=df['State/Province'].unique())

# 3. Yahan Filter Define karein (Yeh line sabse zaroori hai)
df_f = df[df['State/Province'].isin(states)]

# 4. Ab dashboard ke modules banayein
st.title("🏭 Nassau Candy Logistics Dashboard")

# Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${df_f['Sales'].sum():,.0f}")
col2.metric("Avg Lead Time", f"{df_f['Lead Time'].mean():.1f} days")
col3.metric("Total Profit", f"${df_f['Gross Profit'].sum():,.0f}")

# Chart (Filter ke baad)
st.subheader("Gross Profit by State")
st.bar_chart(df_f.groupby('State/Province')['Gross Profit'].sum())

st.success("Dashboard successfully loaded!")
