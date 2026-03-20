import pandas as pd
import os

def extract(filepath):
    """Read all sheets from Excel file."""
    return pd.read_excel(filepath, sheet_name=None)

def standardize_columns(all_sheets):
    """Rename columns to consisten names across all years"""
    standard_columns = {
        'Full Date': 'full_date',
        'Credit Cards BTX': 'cc_btx',
        'Credit Card BTX': 'cc_btx', 
        'Credit Card Supp': 'cc_supp',
        'Credit Card IP': 'cc_wl',
        'Credit Card WL': 'cc_wl',
        'Cash BTX': 'cash_btx',
        'Cash Supp': 'cash_supp',
        'Cash IP': 'cash_wl',
        'Cash WL': 'cash_wl',
        'Check BTX': 'check_btx',
        'Check Supp': 'check_supp',
        'Check IP': 'check_wl',
        'Check WL': 'check_wl',
    }
    for year, sheet in all_sheets.items():
        all_sheets[year] = sheet.rename(columns=standard_columns)
    
    return all_sheets

def combine_sheets(all_sheets):
    """concatinate all sheets into one dataframe"""
    dfs = []

    for sheet in all_sheets.values():
        dfs.append(sheet)
    df = pd.concat(dfs, ignore_index = True)

    return df

def clean_data(df):
    """Fill NaNs and handle missing values."""
    df = df.dropna(subset=['full_date'])
    df = df.fillna(0)

    return df

def add_columns(df):
    """Add derived columns like month, year, total_revenue."""
    df['month'] = df['full_date'].dt.month
    df['month_name'] = df['full_date'].dt.strftime('%B')
    df['day_of_week'] = df['full_date'].dt.day_name()
    df['quarter'] = df['full_date'].dt.quarter
    df['day_of_month'] = df['full_date'].dt.day
    df['total_revenue'] = df[['cc_btx', 'cc_supp', 'cc_wl', 
                                    'cash_btx', 'cash_supp', 'cash_wl',
                                    'check_btx', 'check_supp', 'check_wl']].sum(axis=1)

    return df

def transform(all_sheets):
    """Orchestrate the full transformation."""
    all_sheets = standardize_columns(all_sheets)
    df = combine_sheets(all_sheets)
    df = clean_data(df)
    df = add_columns(df)
    return df


def load(df, output_path):
    """Save the clean data to CSV."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Data saved to {output_path}")


if __name__ == '__main__':
    raw = extract('data/BTX_17-23_Yearly_Totals.xlsx')
    clean = transform(raw)
    load(clean, 'data/clinic_revenue_clean.csv')