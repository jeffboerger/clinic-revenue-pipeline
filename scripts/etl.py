import pandas as pd
import os
import sqlite3

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
        all_sheets[year]['year'] = year
    
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

# Adding 2024 and 2025 data
def extract_new(filepath):
    """Extract Monthly Sheets from 2024-2025 format files."""
    return pd.read_excel(filepath, sheet_name=None)

def transform_new(all_sheets, year):
    """
    Transform 2024-2025 clinic data into unified schema.
    New Format has monthly sheets, different column structure.
    BTX/Supp/WL breakdown not available - all revenue mapped to BTX based on 2023 trend showing >97% is BTX Revenue
    """

    dfs = []

    for month, sheet in all_sheets.items():
        # Read only the relevant columns , skip blanks 
        sheet = sheet.iloc[:, [0, 1, 2, 3, 5, 7, 8]]

        # rename to standard column names
        sheet.columns = [
            'full_date', 'cash_btx', 'check_btx', 'cc_btx', 'total_revenue', 'square_fees', 'total_deposit'
        ]

        # Drop rows where full_date is null or noat a real date
        sheet = sheet.dropna(subset=['full_date'])
        sheet = sheet[pd.to_datetime(sheet['full_date'], errors='coerce').notna()]

        #add year column
        sheet['year'] = year

        dfs.append(sheet)

    df = pd.concat(dfs, ignore_index=True)
    
    # Add missing revenue stream columns as zeros
    df['cc_supp'] = 0
    df['cc_wl'] = 0
    df['cash_supp'] = 0
    df['cash_wl'] = 0
    df['check_supp'] = 0
    df['check_wl'] = 0

    # Standardize date format
    df['full_date'] = pd.to_datetime(df['full_date'])

    # Fill any remaining NaNs with 0
    df = df.fillna(0)

    return df



def load(df, output_path):
    """Save the clean data to CSV."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Data saved to {output_path}")

def load_to_db(df, db_path):
    """Load clean data into a SQLite db"""
    conn = sqlite3.connect(db_path)
    df.to_sql('clinic_revenue', conn, if_exists='replace', index=False)
    conn.close()
    print(f"Data loaded to database at {db_path}")



if __name__ == '__main__':
    print("Extracting data...")

    # Original format 2017-2023
    raw_original = extract('data/BTX_17-23_Yearly_Totals.xlsx')
    df_original = transform(raw_original)

    # New format 2024
    raw_2024 = extract_new('data/Totals_2024.xlsx')
    df_2024 = transform_new(raw_2024, year=2024)

    # New format 2025
    raw_2025 = extract_new('data/Totals_2025.xlsx')
    df_2025 = transform_new(raw_2025, year=2025)

    # Combine all years
    print("Combining all years...")
    df_all = pd.concat([df_original, df_2024, df_2025], ignore_index=True)
    df_all = df_all.sort_values('full_date').reset_index(drop=True)

    print(f"Total rows: {len(df_all)}")
    print(f"Years covered: {sorted(df_all['year'].unique())}")

    # Load
    load(df_all, 'data/clinic_revenue_clean.csv')
    load_to_db(df_all, 'data/clinic_revenue.db')