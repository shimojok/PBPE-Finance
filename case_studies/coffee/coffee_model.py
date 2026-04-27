import pandas as pd
from src.pbpe_engine import PBPEEngine

inputs = {
    "years": 5,
    "discount_rate": 0.08,
    "initial_investment": 500000,

    # AGRIX
    "ha": 100,
    "yield_base": 1.5,
    "yield_increase_pct": 0.2,
    "fertilizer_cost_savings": 200,

    # Market
    "price_per_ton": 3000,

    # M3-Core
    "co2_reduction_per_ton": 1.0,
    "carbon_price": 80,

    # HealthBook
    "healthcare_cost_avoidance": 50,
    "health_discount_rate": 0.03
}

engine = PBPEEngine(inputs)

cashflows = engine.compute_cashflows()
npv, irr = engine.compute_npv_irr()

df = pd.DataFrame({
    "Year": range(1, 6),
    "Cashflow": cashflows
})

summary = pd.DataFrame({
    "Metric": ["NPV", "IRR"],
    "Value": [npv, irr]
})

print(df)
print(summary)

df.to_csv("coffee_cashflows.csv", index=False)
summary.to_csv("coffee_summary.csv", index=False)
