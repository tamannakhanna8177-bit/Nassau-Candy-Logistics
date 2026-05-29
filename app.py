import streamlit as st
import pandas as pd

# 1. Sabse upar load karein
df = pd.read_csv('data/nassau_candy_data.csv') 

# 2. Filter logic (Default mein sab select rakhein)
selected_states = st.sidebar.multiselect("Select State", df['State/Province'].unique(), default=df['State/Province'].unique())

# 3. Yahan 'df_f' define karein (Yeh line bahut zaroori hai!)
df_f = df[df['State/Province'].isin(selected_states)]

# 4. Ab neeche kahin bhi 'df_f' use karein
st.metric("Total Sales", f"${df_f['Sales'].sum():,.2f}")
