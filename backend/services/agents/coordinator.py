from typing import Dict, Any

class AgentCoordinator:
    def __init__(self):
        pass

    def run_agent(self, agent_name: str, context: Dict[str, Any]) -> Any:
        if agent_name == "market":
            profile = context.get("profile", {})
            scenarios = context.get("scenarios", [])
            
            business_type = profile.get("business_type", "General Business").title()
            location = profile.get("location", "Urban Center").title()
            target_customers = profile.get("target_customers", "General Public").title()
            investment = float(profile.get("investment", 100000))
            
            total_demand_adj = sum(float(s.get("adjustments", {}).get("demand", 0)) for s in scenarios)
            avg_demand_adj = total_demand_adj / len(scenarios) if scenarios else 0
            
            growth_base = 5.0
            biz_lower = business_type.lower()
            if "tech" in biz_lower or "software" in biz_lower:
                growth_base = 15.0
            elif "retail" in biz_lower or "store" in biz_lower:
                growth_base = 3.0
            elif "food" in biz_lower or "restaurant" in biz_lower:
                growth_base = 4.0
                
            growth_val = growth_base + (avg_demand_adj / 2)
            growth = f"The projected annual growth for a {business_type} in {location} is {growth_val:.1f}%."
            
            competition_score = 50
            loc_lower = location.lower()
            if "city" in loc_lower or "urban" in loc_lower or "downtown" in loc_lower:
                competition_score += 20
            elif "rural" in loc_lower or "suburb" in loc_lower:
                competition_score -= 10
                
            if investment > 500000:
                competition_score -= 10
                
            if competition_score >= 60:
                # Basic pluralization to avoid "Businesss"
                biz_plural = business_type + "es" if business_type.endswith("s") else business_type + "s"
                competition = f"There is high market saturation in {location} for {biz_plural}."
            elif competition_score >= 40:
                competition = f"There is moderate competition targeting {target_customers}."
            else:
                competition = f"There is low competition, which presents a clear market gap for a {business_type}."
            
            demand_score = 50 + avg_demand_adj
            tgt_lower = target_customers.lower()
            if "niche" in tgt_lower or "specialty" in tgt_lower:
                demand_score -= 10
            elif "mass" in tgt_lower or "general" in tgt_lower or "all" in tgt_lower:
                demand_score += 15
                
            if demand_score >= 60:
                demand = f"There is a strong established demand among {target_customers} (Scenario Adjustment: {avg_demand_adj:+.1f}%)."
            elif demand_score >= 40:
                demand = f"There is moderate demand, requiring active marketing to {target_customers}."
            else:
                demand = f"There is weak or unproven demand among {target_customers}."
            
            opportunity_score = (growth_base * 2) - competition_score + demand_score
            
            if opportunity_score > 20:
                market_opportunity = f"This represents an excellent opportunity to deploy ${investment:,.0f} in {location}."
            elif opportunity_score > 0:
                market_opportunity = f"This is a good opportunity for a {business_type} targeting {target_customers}."
            else:
                market_opportunity = f"This is a fair opportunity, but it carries high execution risk for a ${investment:,.0f} investment."
            
            confidence = min(100, max(0, int(70 + (len(scenarios) * 5) - (competition_score / 10))))
            
            return {
                "growth": growth,
                "competition": competition,
                "demand": demand,
                "opportunity": market_opportunity,
                "confidence": confidence,
                "score": confidence
            }
            
        elif agent_name == "risk":
            profile = context.get("profile", {})
            metrics = context.get("metrics", {})
            scenarios = context.get("scenarios", [])
            market_data = context.get("market_analysis", {})

            investment = float(profile.get("investment", 100000))
            avg_roi = metrics.get("avg_roi", 0)
            avg_profit = metrics.get("avg_profit", 0)
            
            # 1. Financial Risk
            if investment > 500000 and avg_roi < 10:
                fin_risk = 80
                fin_reason = f"High financial risk due to large capital requirement (${investment:,.0f}) paired with a low expected ROI ({avg_roi:.1f}%)."
            elif avg_profit < 0:
                fin_risk = 90
                fin_reason = f"Critical financial risk because average projected profitability is negative (${avg_profit:,.0f})."
            elif investment < 50000:
                fin_risk = 20
                fin_reason = f"Low financial risk due to minimal upfront capital requirement (${investment:,.0f})."
            else:
                fin_risk = 40
                fin_reason = f"Moderate financial risk with stable expected returns (ROI: {avg_roi:.1f}%)."

            # 2. Operational Risk
            max_cost_adj = max([float(s.get("adjustments", {}).get("cost", 0)) for s in scenarios]) if scenarios else 0
            if max_cost_adj > 20:
                op_risk = 75
                op_reason = f"High operational risk due to potential {max_cost_adj}% spikes in operating costs modeled in scenarios."
            elif max_cost_adj > 0:
                op_risk = 45
                op_reason = f"Moderate operational risk with potential {max_cost_adj}% cost variations."
            else:
                op_risk = 25
                op_reason = "Low operational risk as cost structures remain stable across tested scenarios."

            # 3. Market Risk
            market_competition = market_data.get("competition", "Medium")
            market_demand = market_data.get("demand", "Moderate")
            if market_competition == "High" and market_demand == "Weak":
                mkt_risk = 85
                mkt_reason = "High market risk due to intense competition and weak demand."
            elif market_competition == "High":
                mkt_risk = 60
                mkt_reason = "Elevated market risk due to high competition level in the target area."
            elif market_demand == "Weak":
                mkt_risk = 70
                mkt_reason = "Elevated market risk caused by weak projected customer demand."
            else:
                mkt_risk = 30
                mkt_reason = "Low market risk due to favorable competitive landscape and demand."

            # 4. Supply Chain Risk
            biz_type = profile.get("business_type", "").lower()
            if "retail" in biz_type or "food" in biz_type or "restaurant" in biz_type or "store" in biz_type:
                if max_cost_adj >= 10:
                    sc_risk = 70
                    sc_reason = "High supply chain risk due to physical inventory reliance and modeled cost volatility."
                else:
                    sc_risk = 50
                    sc_reason = "Moderate supply chain risk inherent to physical goods and inventory management."
            elif "tech" in biz_type or "software" in biz_type:
                sc_risk = 15
                sc_reason = "Low supply chain risk due to digital product delivery and minimal physical inventory."
            else:
                sc_risk = 40
                sc_reason = "Standard supply chain risk associated with general business operations."

            # Overall Risk
            overall_score = (fin_risk * 0.4) + (op_risk * 0.2) + (mkt_risk * 0.2) + (sc_risk * 0.2)
            level = "High" if overall_score > 65 else "Medium" if overall_score > 35 else "Low"

            factors = [
                f"**Financial Risk ({fin_risk}/100)**: {fin_reason}",
                f"**Operational Risk ({op_risk}/100)**: {op_reason}",
                f"**Market Risk ({mkt_risk}/100)**: {mkt_reason}",
                f"**Supply Chain Risk ({sc_risk}/100)**: {sc_reason}"
            ]

            return {
                "level": level,
                "score": int(overall_score),
                "factors": factors
            }
            
        elif agent_name == "prediction":
            from .prediction.prediction_agent import PredictionAgent
            from .prediction.models import ForecastInput
            
            agent = PredictionAgent()
            scenarios = context.get("scenarios", [])
            profile = context.get("profile", {})
            
            base_revenue = float(profile.get("expected_revenue", 100000))
            base_costs = float(profile.get("operating_costs", 50000))
            
            predictions = {}
            for sc in scenarios:
                name = sc.get("name", "Unknown Scenario")
                adj = sc.get("adjustments", {})
                demand_adj = float(adj.get("demand", 0)) / 100.0
                price_adj = float(adj.get("price", 0)) / 100.0
                cost_adj = float(adj.get("cost", 0)) / 100.0
                
                # Exact scenario metrics
                sc_revenue = base_revenue * (1 + demand_adj) * (1 + price_adj)
                sc_costs = base_costs * (1 + cost_adj)
                sc_profit = sc_revenue - sc_costs
                
                # Trend derives exclusively from scenario assumptions, no fixed base percentage.
                # Normal (0) -> 0 trend (stable)
                # Worst Case (-demand, +cost) -> negative trend (declining)
                # Best Case (+demand, -cost) -> positive trend (growing)
                trend_factor = (demand_adj * 1.5) + (price_adj * 0.5) - (cost_adj * 1.0)
                
                f_input = ForecastInput(
                    historical_data={"revenue": sc_revenue, "profit": sc_profit},
                    time_horizon_months=6,
                    assumptions={
                        "growth_rate": trend_factor,
                        "variance": 0.05
                    }
                )
                
                try:
                    res = agent.predict(f_input)
                    profit_forecast = res.get("forecasts", {}).get("profit")
                    if profit_forecast and profit_forecast.values:
                        base_val = profit_forecast.values[0]
                        if base_val != 0:
                            curve = [val * (sc_profit / base_val) for val in profit_forecast.values]
                        else:
                            curve = profit_forecast.values
                    else:
                        raise ValueError("Forecast missing")
                except Exception:
                    # Fallback math prediction
                    curve = []
                    current_val = sc_profit
                    for _ in range(6):
                        curve.append(current_val)
                        current_val *= (1 + (trend_factor / 12.0))
                        
                predictions[name] = curve
                
            return predictions
            
        elif agent_name == "timeline":
            metrics = context.get("metrics", {})
            profile = context.get("profile", {})
            scenarios = context.get("scenarios", [])
            risk_data = context.get("risk_analysis", {})
            
            business_type = profile.get("business_type", "Business").title()
            investment = float(profile.get("investment", 100000))
            team_size = int(profile.get("team_size", 5))
            complexity = len(scenarios)
            risk_score = risk_data.get("score", 50)
            risk_level = risk_data.get("level", "Medium")
            
            # Dynamic total duration in weeks
            base_weeks = 8.0
            base_weeks += (investment / 25000.0) # More money = longer deployment
            base_weeks -= min(10.0, team_size * 0.5) # Larger team = faster execution (up to a point)
            base_weeks += (complexity * 2.5) # More scenarios/complexity = longer planning
            base_weeks += (risk_score / 5.0) # Higher risk = more padded timeline
            
            total_months = min(12, max(1, int(base_weeks / 4.33)))
            
            # Dynamically build phase structures based on business attributes
            phase_blueprints = []
            
            phase_blueprints.append({
                "name": f"Initial {business_type} Strategy & Planning",
                "weight": 0.2
            })
            
            phase_blueprints.append({
                "name": f"Resource Assembly & Team Onboarding ({team_size} FTEs)",
                "weight": 0.2 if team_size < 20 else 0.3
            })
            
            phase_blueprints.append({
                "name": f"Core Execution & Infrastructure ({complexity} operational models)",
                "weight": 0.3
            })
            
            if risk_score > 40:
                phase_blueprints.append({
                    "name": f"Risk Mitigation & Quality Assurance ({risk_level} Risk Profile)",
                    "weight": 0.15 + (risk_score / 400.0)
                })
                
            phase_blueprints.append({
                "name": f"Official Launch & Capital Deployment (${investment:,.0f})",
                "weight": 0.15
            })
            
            # Distribute total_months across the blueprints proportionally
            total_weight = sum(p["weight"] for p in phase_blueprints)
            
            phases = []
            current_month = 1
            for idx, pb in enumerate(phase_blueprints):
                # Ensure the last phase eats any rounding remainders to match total_months
                if idx == len(phase_blueprints) - 1:
                    duration = max(1, total_months - current_month + 1)
                else:
                    duration = max(1, int(total_months * (pb["weight"] / total_weight)))
                
                end_month = current_month + duration - 1
                if end_month == current_month:
                    duration_str = f"Month {current_month}"
                else:
                    duration_str = f"Month {current_month} to {end_month}"
                    
                phases.append({
                    "name": pb["name"],
                    "duration": duration_str
                })
                current_month = end_month + 1
                
            return phases
            
        elif agent_name == "evidence":
            metrics = context.get("metrics", {})
            profile = context.get("profile", {})
            scenarios = context.get("scenarios", [])
            risk_data = context.get("risk_analysis", {})
            decision_data = context.get("decision_result", {})

            avg_revenue = metrics.get("avg_revenue", 0)
            avg_profit = metrics.get("avg_profit", 0)
            avg_roi = metrics.get("avg_roi", 0)
            base_revenue = float(profile.get("expected_revenue", 0))
            investment = float(profile.get("investment", 0))

            revenue_reasoning = f"The strategic analysis models an average projected revenue of ${avg_revenue:,.2f} across all simulated environments. "
            if base_revenue > 0:
                diff = ((avg_revenue - base_revenue) / base_revenue) * 100
                if diff >= 0:
                    revenue_reasoning += f"This represents a positive variance of {diff:.1f}% relative to the baseline projection of ${base_revenue:,.2f}, driven by favorable demand and pricing adjustments."
                else:
                    revenue_reasoning += f"This indicates a negative variance of {abs(diff):.1f}% relative to the baseline projection of ${base_revenue:,.2f}, suggesting structural revenue pressure in the simulated scenarios."

            profit_reasoning = f"The composite operational modeling yields an average net profit of ${avg_profit:,.2f}. "
            if avg_profit > 0:
                profit_reasoning += "The enterprise demonstrates robust financial sustainability and maintains positive operating margins across the tested stress conditions."
            else:
                profit_reasoning += "The enterprise exhibits severe financial vulnerability, operating at a net loss under the current capital assumptions and scenario adjustments."

            roi_reasoning = f"Capital efficiency analysis indicates an average Return on Investment (ROI) of {avg_roi:.2f}% on the base capital allocation of ${investment:,.0f}. "
            if avg_roi > 20:
                roi_reasoning += "The projected yields significantly outperform standard market benchmarks, qualifying this as a high-performance capital deployment opportunity."
            elif avg_roi > 0:
                roi_reasoning += "The investment generates positive but moderated yields, requiring strict operational discipline to maximize shareholder value."
            else:
                roi_reasoning += "The capital deployment fails to break even, resulting in value destruction and negative yields."

            risk_level = risk_data.get("level", "Unknown")
            risk_score = risk_data.get("score", 0)
            risk_reasoning = f"The comprehensive risk assessment calculates an aggregate risk score of {risk_score}/100, categorizing the operational profile as {risk_level} risk. "
            if risk_data.get("factors"):
                clean_factors = [f.replace("**", "").replace("__", "") for f in risk_data["factors"]]
                risk_reasoning += f"Primary contributors to this rating include: {'; '.join(clean_factors)}."

            adjustments = []
            for sc in scenarios:
                adj = sc.get("adjustments", {})
                adjustments.append(f"{sc.get('name', 'Unknown')} (Cost Variance: {adj.get('cost', 0)}%, Demand Shift: {adj.get('demand', 0)}%, Pricing Delta: {adj.get('price', 0)}%)")
            scenario_reasoning = f"The analysis synthesized {len(scenarios)} discrete operational models: {'; '.join(adjustments)}."

            decision_rationale = decision_data.get("rationale", "No rationale provided by the decision engine.").replace("**", "").replace("__", "")
            decision_score = decision_data.get("score", 0)
            decision_reasoning = f"The decision engine issued a confidence score of {decision_score}/100. {decision_rationale}"

            return [
                {"title": "Revenue", "description": revenue_reasoning},
                {"title": "Profit", "description": profit_reasoning},
                {"title": "ROI", "description": roi_reasoning},
                {"title": "Risk", "description": risk_reasoning},
                {"title": "Scenario Adjustments", "description": scenario_reasoning},
                {"title": "Decision", "description": decision_reasoning}
            ]
            
        elif agent_name == "decision":
            from backend.services.agents.decision_score.decision_score_agent import DecisionScoreAgent
            
            agent = DecisionScoreAgent()
            decision_score = agent.calculate_absolute_score(context)
            
            roi = context.get("metrics", {}).get("avg_roi", 0.0)
            risk = context.get("risk_analysis", {}).get("score", 50)
            confidence = context.get("market_analysis", {}).get("confidence", 50)
            metrics_ref = f"(ROI: {roi:.1f}%, Risk: {risk}/100, Market Confidence: {confidence}%)"

            if decision_score >= 90:
                rec = "APPROVE"
                reason = f"Outstanding financials with low risk and strong market outlook. {metrics_ref}"
            elif decision_score >= 80:
                rec = "APPROVE"
                reason = f"Strong investment opportunity with manageable risks. {metrics_ref}"
            elif decision_score >= 70:
                rec = "PROCEED WITH CAUTION"
                reason = f"Business is viable but has identifiable risks requiring mitigation. {metrics_ref}"
            elif decision_score >= 55:
                rec = "REVIEW"
                reason = f"Further analysis is recommended before investment. {metrics_ref}"
            else:
                rec = "REJECT"
                reason = f"Risk outweighs expected returns. {metrics_ref}"

            rationale_str = f"{rec}\n\nReason:\n{reason}"

            return {
                "score": decision_score,
                "rationale": rationale_str
            }
            
        return None
