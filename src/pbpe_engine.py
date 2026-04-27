import numpy as np
import numpy_financial as npf


class PBPEEngine:
    def __init__(self, inputs: dict):
        self.inputs = inputs

    # ----------------------------
    # GOLD: 生産性
    # ----------------------------
    def compute_gold(self):
        yield_base = self.inputs["yield_base"]
        yield_increase = self.inputs["yield_increase_pct"]
        price = self.inputs["price_per_ton"]
        ha = self.inputs["ha"]
        fert_savings = self.inputs["fertilizer_cost_savings"]

        production_base = yield_base * ha
        production_new = yield_base * (1 + yield_increase) * ha

        revenue_base = production_base * price
        revenue_new = production_new * price

        return (revenue_new - revenue_base) + fert_savings * ha

    # ----------------------------
    # GREEN: 炭素
    # ----------------------------
    def compute_green(self):
        production = self.inputs["yield_base"] * (1 + self.inputs["yield_increase_pct"]) * self.inputs["ha"]
        co2_per_ton = self.inputs["co2_reduction_per_ton"]
        carbon_price = self.inputs["carbon_price"]

        return production * co2_per_ton * carbon_price

    # ----------------------------
    # BLUE: 健康
    # ----------------------------
    def compute_blue(self, year):
        production = self.inputs["yield_base"] * (1 + self.inputs["yield_increase_pct"]) * self.inputs["ha"]
        health_value = self.inputs["healthcare_cost_avoidance"]
        discount = self.inputs["health_discount_rate"]

        return (production * health_value) / ((1 + discount) ** year)

    # ----------------------------
    # CASHFLOW
    # ----------------------------
    def compute_cashflows(self):
        years = self.inputs["years"]
        cashflows = []

        for t in range(1, years + 1):
            gold = self.compute_gold()
            green = self.compute_green()
            blue = self.compute_blue(t)

            cashflows.append(gold + green + blue)

        return cashflows

    # ----------------------------
    # NPV / IRR
    # ----------------------------
    def compute_npv_irr(self):
        discount_rate = self.inputs["discount_rate"]
        initial_investment = self.inputs["initial_investment"]

        cashflows = self.compute_cashflows()

        npv = sum([cf / ((1 + discount_rate) ** (i + 1)) for i, cf in enumerate(cashflows)])
        irr = npf.irr([-initial_investment] + cashflows)

        return npv, irr
