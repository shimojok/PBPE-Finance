import pandas as pd
from src.pbpe_engine import PBPEEngine

inputs = {
    "years": 5,
    "discount_rate": 0.08,
    "initial_investment": 500000,
    "ha": 100,
    "yield_base": 1.5,
    "yield_increase_pct": 0.2,
    "fertilizer_cost_savings": 200,
    "price_per_ton": 3000,
    "co2_reduction_per_ton": 1.0,
    "carbon_price": 80,
    "healthcare_cost_avoidance": 50,
    "health_discount_rate": 0.03
}

engine = PBPEEngine(inputs)

# --- Cashflow
cf = engine.compute_cashflows()
npv, irr = engine.compute_npv_irr()

# --- Food Price Simulation
prices = engine.simulate_food_price(10)

# --- Scope 3 (Starbucks scale)
scope3 = engine.scope3_value(400000)

# --- Capital Flow
capital = engine.capital_multiplier(1_000_000)

# --- Investor Metrics
metrics = engine.investor_metrics()

df_cf = pd.DataFrame({"Year": range(1, 6), "Cashflow": cf})
df_price = pd.DataFrame({"Year": range(1, 11), "Price": prices})

print(df_cf)
print(df_price)
print("NPV:", npv, "IRR:", irr)
print("Scope3 Value:", scope3)
print("Capital Flow:", capital)
print("Investor Metrics:", metrics)
