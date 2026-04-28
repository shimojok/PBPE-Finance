import sys
sys.path.append(".")
import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from src.pbpe_engine import PBPEEngine

st.set_page_config(page_title="PBPE Finance | BioNexus Platform", layout="wide")

st.title("💰 PBPE Finance Engine")
st.markdown("**Planetary Bio-Productivity Exchange | Climate Finance Market Creation**")

# ── Sidebar ──
st.sidebar.header("Investment Parameters")
ha = st.sidebar.slider("Hectares (ha)", 10, 500000, 100)
carbon_price = st.sidebar.slider("Carbon Price ($/tCO₂e)", 10, 200, 80)
yield_inc = st.sidebar.slider("Yield Increase (%)", 0.0, 0.5, 0.2)

inputs = {
    "years": 5, "discount_rate": 0.08, "initial_investment": 500000,
    "ha": ha, "yield_base": 1.5, "yield_increase_pct": yield_inc,
    "fertilizer_cost_savings": 200, "price_per_ton": 3000,
    "co2_reduction_per_ton": 1.0, "carbon_price": carbon_price,
    "healthcare_cost_avoidance": 50, "health_discount_rate": 0.03
}

engine = PBPEEngine(inputs)

# ── Tabs ──
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 IRR & NPV", "🏷️ SafetyChain™ Pricing", "🍃 Scope 3", "💊 m-ROI", "📈 Investor Metrics"
])

with tab1:
    st.header("Triple Ledger Investment Returns")
    npv, irr = engine.compute_npv_irr()
    col1, col2, col3 = st.columns(3)
    with col1: st.metric("NPV (USD)", f"${npv:,.0f}")
    with col2: st.metric("IRR", f"{irr:.2%}")
    with col3: st.metric("Farm ROI", "17.8x")

    cf = engine.compute_cashflows()
    fig = go.Figure()
    fig.add_trace(go.Bar(x=list(range(1, 6)), y=cf, name="Annual Cashflow"))
    fig.update_layout(title="5-Year Cashflow Projection")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Food Price Simulation (10-Year)")
# 食料価格シミュレーション
    prices = engine.simulate_food_price(years=10)   # 引数名を明示
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(y=prices, mode='lines+markers', name='Price'))
    fig2.update_layout(title="Projected Food Price Decline (Supply Increase Effect)")
    st.plotly_chart(fig2, use_container_width=True)

with tab2:
    st.header("🔗 SafetyChain™ 4-Layer Dynamic Pricing")

    col1, col2 = st.columns(2)
    with col1:
        P_market = st.slider("Market Price ($/ton)", 500, 5000, 3000)
        V_func = st.slider("V: Functionality Premium", 0, 500, 100)
        L_loss = st.slider("L: Loss Avoidance", 0, 300, 50)
    with col2:
        m_health = st.slider("m: Medical Savings", 0, 500, 120)
        C_seq = st.slider("C: Carbon Value", 0, 300, 80)

    P_total = P_market + V_func + L_loss + m_health + C_seq

    st.metric("MBT55 SafetyChain™ Price", f"${P_total}/ton")
    st.metric("Conventional Market Price", f"${P_market}/ton", delta=f"+${P_total - P_market}")

    fig3 = go.Figure()
    fig3.add_trace(go.Bar(x=["Market", "V (Functionality)", "L (Loss Avoidance)", "m (Medical)", "C (Carbon)"],
                          y=[P_market, V_func, L_loss, m_health, C_seq]))
    fig3.update_layout(title="Price Decomposition — SafetyChain™ Certified")
    st.plotly_chart(fig3, use_container_width=True)

with tab3:
    st.header("🍃 Corporate Scope 3 Value")

    coffee_tons = st.slider("Annual Coffee Procurement (tons)", 10000, 500000, 400000, step=10000)
    scope3_value = engine.scope3_value(coffee_tons)
    st.metric("Annual Scope 3 Reduction Value", f"${scope3_value:,.0f}")

    st.markdown("| Company | Annual Procurement | Scope 3 Value | ESG Market Cap Impact |")
    st.markdown("|---|---|---|---|")
    st.markdown(f"| Starbucks | 400,000 tons | ${engine.scope3_value(400000):,.0f} | +${engine.esg_market_cap_impact(100_000_000_000):,.0f} |")
    st.markdown(f"| Custom | {coffee_tons:,} tons | ${scope3_value:,.0f} | — |")

    st.subheader("Capital Multiplier Effect")
    layers = engine.capital_multiplier(1_000_000)
    fig4 = go.Figure(data=[go.Sankey(
        node=dict(label=list(layers.keys()), pad=15, thickness=20),
        link=dict(source=[0, 1, 2], target=[1, 2, 3],
                  value=[layers["AGRIX"], layers["SafelyChain"], layers["MABC"]])
    )])
    fig4.update_layout(title="Capital Flow: $1 → $94.10 Total Economic Value")
    st.plotly_chart(fig4, use_container_width=True)

with tab4:
    st.header("💊 m-ROI: Medical Return on Investment")

    scfa = st.slider("SCFA Precursor Content (mg/100g)", 0, 1000, 300)
    cost_d, cost_h, cost_c = 300000, 200000, 800000
    m_diab = scfa * 0.15 * cost_d / 1000
    m_hyper = scfa * 0.12 * cost_h / 1000
    m_cancer = scfa * 0.10 * cost_c / 1000
    m_total = m_diab + m_hyper + m_cancer

    df_mroi = pd.DataFrame({
        "Disease": ["Diabetes", "Hypertension", "Colon Cancer"],
        "Avoided Cost (¥)": [f"¥{m_diab:,.0f}", f"¥{m_hyper:,.0f}", f"¥{m_cancer:,.0f}"]
    })
    st.table(df_mroi)
    st.metric("Total m-ROI (per person/year)", f"¥{m_total:,.0f}")

    st.subheader("Carbon Micro-Transaction Simulator")
    co2_per_purchase = st.slider("CO₂ Reduced per Purchase (kg)", 0.1, 5.0, 1.0)
    purchases_per_year = st.slider("Purchases per Year", 1, 500, 100)
    annual_co2 = co2_per_purchase * purchases_per_year
    st.metric("Annual CO₂ Reduction", f"{annual_co2:.2f} kg")
    st.metric("Carbon Value", f"${(annual_co2/1000)*carbon_price:.2f}")

with tab5:
    st.header("📈 Institutional Investor Metrics")

    metrics = engine.investor_metrics()
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("10-Year NPV", f"${metrics['NPV_10Y_USD']/1e9:.1f}B")
    with col2: st.metric("IRR (10Y)", f"{metrics['IRR_10Y']*100:.0f}%")
    with col3: st.metric("Farm ROI", f"{metrics['Farm_ROI']}x")
    with col4: st.metric("Payback", f"{metrics['Payback_Years']} years")

    st.markdown("---")
    st.markdown("""
    ### 🌍 5 Million Hectare Deployment Scenario
    | Metric | Value |
    |:---|---:|
    | Total Investment | $1.885B/year |
    | Annual Carbon Revenue | $4.25B (Year 10) |
    | Annual Coffee Revenue | $12.25B (Year 10) |
    | 10-Year Cumulative Cash Flow | +$108.45B |
    | System Multiplier | 94.1× |
    """)

st.markdown("---")
st.caption("**PBPE-Finance Engine** | BioNexus Platform | IPCC AR6 GWP100 | EU ETS Carbon Pricing | IFRS S2 Aligned")
