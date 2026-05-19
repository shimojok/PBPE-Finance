# PBPE‑Finance I/O Specification

### Financial Structuring Layer — Input/Output Contract

### Version 1.0 (Canonical English Edition)

---

## 1. Purpose

This document defines the **input/output contract** for PBPE‑Finance.  
PBPE‑Finance receives economic outputs and credits from PBPE‑Dashboard and produces:

- Credit pricing
- Financial products
- Portfolio analytics
- Marketplace‑ready financial data

This specification is authoritative for all PBPE‑Finance integrations.

---

# 2. Upstream Inputs

PBPE‑Finance receives data exclusively from PBPE‑Dashboard.

---

## 2.1 Entity: `FinanceInput`

### **Core Economic Inputs**

|Field|Type|Description|
|---|---|---|
|pbpe_biosecurity_value_usd|float|Total PBPE value (USD)|
|farmer_income_uplift_pct|float|% increase in farmer income|
|regional_pbpe_value_usd|float|Regional PBPE value|
|sector_pbpe_value_usd|float|Sector‑level PBPE value|

---

### **Credit Inputs**

|Field|Type|Description|
|---|---|---|
|biosecurity_credits|float|PBPE‑BIO units|
|carbon_credits_tco2|float|tCO₂|
|food_loss_credits_t|float|Tons|
|quality_credits_score|float|0–100|
|price_stability_credits_score|float|0–100|

---

### **Risk & Stability Inputs**

|Field|Type|Description|
|---|---|---|
|price_stability_index|float|0–1|
|yield_cv_before|float|Coefficient of variation|
|yield_cv_after|float|Coefficient of variation|
|supply_risk_score|float|0–1|

---

### **Climate & Health Inputs**

|Field|Type|Description|
|---|---|---|
|delta_c_tc_per_ha|float|Soil carbon change|
|ghg_reduction_tco2e|float|CH₄ + N₂O reduction|
|one_health_index|float|0–1|
|antibiotic_reduction_pct|float|% reduction|

---

# 3. Internal Processing

PBPE‑Finance performs three internal transformations.

---

## 3.1 Credit Pricing Model

### **Entity: `CreditPricingOutput`**

|Field|Type|Description|
|---|---|---|
|credit_price_usd_per_unit|object|Price per credit type|
|credit_volatility|object|Volatility per credit type|
|risk_adjusted_price|object|Risk‑adjusted price|

---

## 3.2 Portfolio Model

### **Entity: `PortfolioOutput`**

|Field|Type|Description|
|---|---|---|
|aum_usd|float|Assets under management|
|portfolio_risk_score|float|0–1|
|sector_allocation|object|% by sector|
|region_allocation|object|% by region|
|expected_return_pct|float|%|

---

## 3.3 Product Structuring

### **Entity: `FinancialProduct`**

|Field|Type|Description|
|---|---|---|
|product_id|string|Unique ID|
|product_type|string|bond, fund, rbf, guarantee|
|underlying_credits|object|All credit quantities|
|notional_usd|float|Notional value|
|expected_return_pct|float|%|
|tenor_years|float|Duration|
|risk_score|float|0–1|
|impact_metrics|object|Climate & social metrics|

---

# 4. Downstream Outputs

PBPE‑Finance outputs data to PBPE‑Marketplace.

---

## 4.1 Entity: `FinanceOutput`

|Field|Type|Description|
|---|---|---|
|product_id|string|Financial product ID|
|product_type|string|Product category|
|underlying_credits|object|Credits included|
|notional_usd|float|Notional value|
|expected_return_pct|float|Expected return|
|tenor_years|float|Duration|
|risk_score|float|0–1|
|impact_metrics|object|Climate & social metrics|

---

# 5. API Specification

---

## 5.1 POST /finance/credit/issue

**Request:**  
`FinanceInput`

**Response:**

- credit_issuance_record
- credit_price_usd_per_unit
- credit_id

---

## 5.2 GET /finance/portfolio

**Returns:**  
`PortfolioOutput`

---

## 5.3 GET /finance/report/{farm_id}

**Returns:**

- Credits
- PBPE value
- ROI
- Verification data

---

# 6. Data Model Mapping

PBPE‑Finance consumes:

```
PBPE-Dashboard/docs/IO_Spec_Biosecurity_Input.md
```

Mapping:

|Dashboard Field|Finance Field|
|---|---|
|pbpe_biosecurity_value_usd|pbpe_biosecurity_value_usd|
|biosecurity_credits|biosecurity_credits|
|carbon_credits_tco2|carbon_credits_tco2|
|food_loss_credits_t|food_loss_credits_t|
|quality_credits_score|quality_credits_score|
|price_stability_credits_score|price_stability_credits_score|
|farmer_income_uplift_pct|farmer_income_uplift_pct|
|regional_pbpe_value_usd|regional_pbpe_value_usd|
|sector_pbpe_value_usd|sector_pbpe_value_usd|

---
