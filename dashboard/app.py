import streamlit as st
from src.pbpe_engine import PBPEEngine

st.title("PBPE Coffee Investment Dashboard")

ha = st.slider("Hectares (ha)", 10, 1000, 100)
carbon_price = st.slider("Carbon Price ($/tCO2)", 10, 200, 80)
yield_increase = st.slider("Yield Increase (%)", 0.0, 0.5, 0.2)

inputs = {
    "years": 5,
    "discount_rate": 0.08,
    "initial_investment": 500000,

    "ha": ha,
    "yield_base": 1.5,
    "yield_increase_pct": yield_increase,
    "fertilizer_cost_savings": 200,

    "price_per_ton": 3000,

    "co2_reduction_per_ton": 1.0,
    "carbon_price": carbon_price,

    "healthcare_cost_avoidance": 50,
    "health_discount_rate": 0.03
}

engine = PBPEEngine(inputs)

npv, irr = engine.compute_npv_irr()

st.metric("NPV (USD)", f"{npv:,.0f}")
st.metric("IRR", f"{irr:.2%}")
