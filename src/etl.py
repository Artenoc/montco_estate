import os
from dotenv import load_dotenv
from fredapi import Fred
import pandas as pd
from cashFlow import analyze_duplex_margins

load_dotenv()

FRED_API_KEY = os.getenv('FRED_API_KEY')

fred = Fred(api_key=FRED_API_KEY)
df_mort = fred.get_series('MORTGAGE30US')
df_cpi = fred.get_series('CPIAUCSL')

df_combined = pd.concat([df_mort, df_cpi], axis = 1, sort=True)
df_combined.columns = ['mortgage_rate', 'cpi']

start_date = df_combined['mortgage_rate'].first_valid_index()
start_date = start_date.replace(day = 1)
df_combined = df_combined.loc[start_date:]

df_combined = df_combined.resample('ME').interpolate(method='linear')

october_rate = df_combined.loc['2025-10-31', 'mortgage_rate']

scenario = analyze_duplex_margins(
  mortgage_rate = october_rate,
  loan_amount = 400000,
  base_rent = 3200,
  inflation_rate = 0.03,
  operational_expenses = 800
)

print(f"Monthly Cash Flow: ${scenario['cash_flow']}")
print(f"Margin: {scenario['margin_pct']}%")

