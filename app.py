import streamlit as st
import pandas as pd
import sqlite3

def load_data():
    """Load Data from SQLite db"""
    conn = sqlite3.connect('data/clinic_revenue.db')
    df = pd.read_sql('SELECT * FROM clinic_revenue', conn)
    conn.close()
    
    return df

df = load_data()
# st.write(df.columns.tolist())

st.title('Body Traxx Clinic Revenue Dashboard')
st.write(f'Data loaded: {len(df)} rows')

st.subheader('Annual Revenue')

yearly = df.groupby('year')['total_revenue'].sum().reset_index()
yearly.columns = ['Year', 'Total Revenue']

st.bar_chart(yearly.set_index('Year'))

st.subheader('Revenue by Stream')

df['total_btx'] = df['cc_btx'] + df['cash_btx'] + df['check_btx']
df['total_supp'] = df['cc_supp'] + df['cash_supp'] + df['check_supp']
df['total_wl'] = df['cc_wl'] + df['cash_wl'] + df['check_wl']

stream = df.groupby('year')[['total_btx', 'total_supp', 'total_wl']].sum()
stream.index = stream.index.astype(int)

st.bar_chart(stream)

st.subheader('Raw Data')
st.dataframe(df)