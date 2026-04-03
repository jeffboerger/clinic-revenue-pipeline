import streamlit as st
import pandas as pd
# import sqlite3
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

def load_data():
    """Load data — tries Supabase first, falls back to SQLite."""
    # Try Supabase (production)
    try:
        s = st.secrets["supabase"]
        url = f"postgresql://{s['user']}:{s['password']}@{s['host']}:{s['port']}/{s['database']}"
        engine = create_engine(url)
        df = pd.read_sql('SELECT * FROM stg_clinic_revenue', engine)
        engine.dispose()
        print("Connected to Supabase")
        return df
    except Exception as e:
        print(f"Supabase connection failed: {e}")
    
    # Fall back to SQLite (local)
    try:
        import sqlite3
        conn = sqlite3.connect('data/clinic_revenue.db')
        df = pd.read_sql('SELECT * FROM clinic_revenue', conn)
        conn.close()
        print("Connected to SQLite fallback")
        return df
    except Exception as e:
        print(f"SQLite fallback failed: {e}")
        raise Exception("All database connections failed")

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

col1.metric("Total Revenue (2017-2025)", f'${total_revenue:,.0f}')
col2.metric('Best Year', best_year)
col3.metric('Avg Daily Revenue', f'${avg_daily:,.0f}')
col4.metric('Best Single Day', f'${best_day:,.0f}')

st.caption('*Avg Daily Revenue excludes days with no revenue (clinic closed, holidays, pre-opening period) | Data spans 2017-2025')

st.title('Body Traxx Clinic Revenue Dashboard')
st.write(f'Data loaded: {len(df)} rows')

# Key Insights Section

st.subheader('Key Insights')

st.info("""
📈 **Subscription model drives everything** — BTX chiropractic subscriptions grew from 
65% of revenue in 2017 to over 97% by 2023, and remain the sole revenue driver 
through 2024-2025.

🦠 **COVID resilience** — Only a 6% revenue drop in 2020 despite clinic closures, 
demonstrating the stickiness of the subscription model.

📅 **Billing cycles are visible in the data** — Revenue spikes consistently on the 5th, 
15th, and 20th of each month, confirming recurring subscription payment patterns.

📊 **Post-peak stabilization** — Revenue peaked at \$187,025 in 2022 and has stabilized 
around \$165K-\$168K through 2024-2025, suggesting a mature subscription base.

🔍 **Outlier identified** — 16 checks over \$1,000 concentrated between 2020-2023 
(largest: \$9,645 on June 15, 2022) do not follow subscription patterns and may 
represent bulk or investor payments.
""")


# Graph Section
# Annual Revenue Chart
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


# REV by Stream Chart
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
ax3.legend(['Monthly Average'])

ax3.set_title('Subscription Billing Cycles Visible in Daily Revenue Patterns', 
              fontsize=11, pad=10)
ax3.annotate('Billing cycle\nspike', 
             xy=(14, dom.iloc[14]), 
             xytext=(17, dom.iloc[14] + 50),
             arrowprops=dict(arrowstyle='->', color='white'),
             color='white', fontsize=9)

plt.tight_layout()
st.pyplot(fig3)

# YOY Chart
st.subheader('Year over Year Growth')

fig4, ax4 = plt.subplots(figsize=(10, 5))

yearly_rev = df.groupby('year')['total_revenue'].sum()
yearly_rev.index = yearly_rev.index.astype(int)
yoy = yearly_rev.pct_change() * 100

# Drop 2017 since it has no prior year to compare
yoy = yoy.dropna()

colors = ['steelblue' if x >= 0 else 'coral' for x in yoy]
bars = ax4.bar(yoy.index.astype(str), yoy.values, color=colors)

# Add value labels on top of each bar
for bar, val in zip(bars, yoy.values):
    ax4.text(bar.get_x() + bar.get_width()/2, 
             bar.get_height() + (1 if val >= 0 else -3),
             f'{val:.1f}%', ha='center', fontsize=9)

ax4.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
ax4.set_xlabel('Year')
ax4.set_ylabel('Growth (%)')
ax4.legend(handles=[
    plt.Rectangle((0,0),1,1, color='steelblue', label='Growth'),
    plt.Rectangle((0,0),1,1, color='coral', label='Decline')
])
plt.tight_layout()
st.pyplot(fig4)

# Raw Data Section
# st.subheader('Raw Data')
# st.dataframe(df)