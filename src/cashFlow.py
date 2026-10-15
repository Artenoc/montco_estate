import numpy_financial as npf

def analyze_duplex_margins(mortgage_rate, loan_amount, base_rent, inflation_rate, operational_expenses):

  monthly_rate = (mortgage_rate / 100) / 12

  monthly_debt_service = -npf.pmt(rate = monthly_rate, nper = 360, pv = loan_amount)
  
  gross_rental_revenue = base_rent * (1 + inflation_rate)
  
  net_operating_income = gross_rental_revenue - operational_expenses
  
  cash_flow = net_operating_income - monthly_debt_service
  
  duplex_marginal_pct = (cash_flow / gross_rental_revenue) * 100
  
  return {
    "monthly_debt_service": round(monthly_debt_service, 2),
    "gross_rental_revenue": round(gross_rental_revenue, 2),
    "net_operating_income": round(net_operating_income, 2),
    "cash_flow": round(cash_flow, 2),
    "margin_pct": round(duplex_marginal_pct, 2),
  }
