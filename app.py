import streamlit as st
import pandas as pd

st.title("🏭 Nassau Candy Logistics Dashboard")

# 1. Data load hamesha sabse upar
df = pd.read_csv('data/nassau_candy_data.csv') 

# 2. Sidebar filter
st.sidebar.header("Filter Controls")
states = st.sidebar.multiselect("Select State", df['State/Province'].unique(), default=df['State/Province'].unique())

# 3. Filtered data ko try block ke bahar define karein taaki kahin bhi use ho sake
df_f = df[df['State/Province'].isin(states)]

# 4. Ab display ka kaam karein
col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${df_f['Sales'].sum():,.0f}")
col2.metric("Avg Lead Time", f"{df_f['Lead Time'].mean():.1f} days")
col3.metric("Total Profit", f"${df_f['Gross Profit'].sum():,.0f}")

st.subheader("Gross Profit by State")
st.bar_chart(df_f.groupby('State/Province')['Gross Profit'].sum())
