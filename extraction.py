# Misellaneous operating system interfacesw
# Examples: open, read, load variables
import os

# Reads .env files for loading in environment variables
from dotenv import load_dotenv

# Imports the Fred class from fredapi
# fredapi is a Python wrapper for the Federal Reserve Economic Data API
from fredapi import Fred

# Data manipulation api, Pandas
import pandas as pd

# Custom cash flow formula
from cashFlow import analyze_duplex_margins

# Import sqlite3 for sending to database
import sqlite3



# Loads environment variables into the active environment
load_dotenv()

# Retrives the API key we just loaded
FRED_API_KEY = os.getenv('FRED_API_KEY')



# Initialize by using the Fred class to assign the api key
fred = Fred(api_key=FRED_API_KEY)

# use the Fred object to fetch 30-Year Fixed Mortgage rates in the US
# Labeled as a DataFrame for using pd later
df_mort = fred.get_series('MORTGAGE30US')

# Fetch Consuper Price Index (All Urban Consumers) data 
# NOTE: CPI data is reported monthly
df_cpi = fred.get_series('CPIAUCSL')



# Merge mortgage and CPI data
# NOTE: Because these two data sets report differently, there will be
# NaN values on dates on certain dates
# Merge is done based on date values
df_combined = pd.concat([df_mort, df_cpi], axis=1, sort=True)

# Rename columns mortgage_ rate and CPI
df_combined.columns = ['mortgage_rate', 'cpi']

# Mortgage dates begin later so set the start date
# based on the mortgage data
start_date = df_combined['mortgage_rate'].first_valid_index()

# Move back to the beginning of the month to grab
# the CPI value for that month
start_date = start_date.replace(day = 1)

# Reassign the combined DataFrame based on the start date
df_combined = df_combined.loc[start_date:]

# Regroup the DataFrame by the Date at the end of the month
# Interpolate NaN values with a linear fit
df_combined = df_combined.resample('ME').interpolate(method='linear')

# Print the first and last five rows of the final, formatted DataFrame
print(df_combined.head())
print(df_combined.tail())


recent_df = df_combined.tail(36).copy()

records = []

for date_idx, row in recent_df.iterrows():

    m_rate = row['mortgage_rate']
    res = analyze_duplex_margins(
        mortgage_rate = m_rate,
        loan_amount = 400000,
        base_rent = 3200,
        inflation_rat = 0.03,
        operational_expenses = 800
    )
    records.append({
        'date': date_idx.strfttime('%y-%m-%d'),
        'mortgage_rate': round(m_rate, 3),
        'cpi': round(row['cpi'], 3),
        'monthly_debt_service': res['monthly_debt_service'],
        'gross_rental_revenue': res['gross_rental_revenue'],
        'net_operating_income': res['net_operating_income'],
        'cash_flow': res['cash_flow'],
        'margin_pct': res['margin_pct']
    })

dashboard_df = pd.DataFrame(records)

db_path = 'montco_macro.db'

conn = sqlite3.connect(db_path)

dashboard_df.to_sql('duplex timeline', conn, if_exists='replace', index=False)

cursor = conn.cursor()

cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_date ON duplex_timeline(date);")
conn.commit()
conn.close()

print(f"Stored {len(dashboard_df)} records into {db_path} successfully.")