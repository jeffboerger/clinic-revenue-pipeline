import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

def load_data():
    """Load Data from SQLite db"""
    conn = sqlite3.connect('data/clinic_revenue.db')
    df = pd.read_sql('SELECT * FROM clinic_revenue', conn)
    conn.close()
    
    return df

df = load_data()
# st.write(df.columns.tolist())

# Filter Section
st.sidebar.title('Filters')

years = sorted(df['year'].unique().astype(int))
selected_years = []

for year in years:
    if st.sidebar.checkbox(str(year), value=True):
        selected_years.append(year)

df = df[df['year'].astype(int).isin(selected_years)]

# Key Metrics Section 
st.subheader('Key Metrics')

col1, col2, col3, col4 = st.columns(4)
total_revenue = df['total_revenue'].sum()
best_year = df.groupby('year')['total_revenue'].sum().idxmax()
avg_daily = df[df['total_revenue'] > 0]['total_revenue'].mean()
best_day = df['total_revenue'].max()

col1.metric("Total Revenue (7yr)", f'${total_revenue:,.0f}')
col2.metric('Best Year', best_year)
col3.metric('Avg Daily Revenue', f'${avg_daily:,.0f}')
col4.metric('Best Single Day', f'${best_day:,.0f}')

st.caption('*Avg Daily Revenue excludes days with no revenue (clinic closed, holidays, pre-opening period)')

st.title('Body Traxx Clinic Revenue Dashboard')
st.write(f'Data loaded: {len(df)} rows')


# Graph Section

st.subheader('Annual Revenue')

fig, ax = plt.subplots(figsize=(10, 5))
yearly = df.groupby('year')['total_revenue'].sum()
yearly.index = yearly.index.astype(int)
bars = yearly.plot(kind='bar', ax=ax, color='steelblue')

for i, val in enumerate(yearly):
    ax.text(i, val + 1000, f'${val:,.0f}', ha='center', fontsize=9)

ax.set_xlabel('Year')
ax.set_ylabel('Total Revenue ($)')
plt.tight_layout()
st.pyplot(fig)



st.subheader('Revenue by Stream')

fig2, ax2 = plt.subplots(figsize=(10, 5))

df['total_btx'] = df['cc_btx'] + df['cash_btx'] + df['check_btx']
df['total_supp'] = df['cc_supp'] + df['cash_supp'] + df['check_supp']
df['total_wl'] = df['cc_wl'] + df['cash_wl'] + df['check_wl']

stream = df.groupby('year')[['total_btx', 'total_supp', 'total_wl']].sum()
stream.index = stream.index.astype(int)
stream.plot(kind='bar', stacked=True, ax=ax2, 
            color=['steelblue', 'coral', 'mediumseagreen'])

ax2.set_xlabel('Year')
ax2.set_ylabel('Total Revenue ($)')
ax2.legend(['BTX', 'Supplements', 'Weight Loss'])
plt.tight_layout()
st.pyplot(fig2)


# AVG Revenue by Day of the Month 
st.subheader('Average Revenue by Day of Month')

fig3, ax3 = plt.subplots(figsize=(10, 5))

dom = df.groupby('day_of_month')['total_revenue'].mean()
dom.plot(kind='bar', ax=ax3, color='steelblue')

ax3.set_xlabel('Day of Month')
ax3.set_ylabel('Average Revenue ($)')
ax3.axhline(y=dom.mean(), color='red', linestyle='--', label='Monthly Average')
ax3.legend()
plt.tight_layout()
st.pyplot(fig3)


st.subheader('Raw Data')
st.dataframe(df)