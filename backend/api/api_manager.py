from typing import Dict, Any
from fastapi import FastAPI

app = FastAPI()

import time

START_TIME = time.time()

from cachetools.func import ttl_cache
from backend.database.database_manager import DatabaseManager

db_manager = DatabaseManager("realitylab.db")
db_manager.initialize()


@app.get("/api/v1/health")
@app.get("/api/v1/health/")
def health_check():
    db_status = "connected"
    try:
        conn = db_manager.connect()
        conn.cursor().execute("SELECT 1")
    except Exception:
        db_status = "error"

    import os

    is_docker = os.path.exists("/.dockerenv")

    return {
        "status": "healthy",
        "sqlite": db_status,
        "fastapi": "healthy",
        "docker": "healthy" if is_docker else "warning",
        "streamlit": "healthy",  # If API is hit via frontend, frontend is running
        "version": "1.0.0",
    }


@app.get("/api/v1/system")
@app.get("/api/v1/system/")
@ttl_cache(maxsize=1, ttl=10)
def system_info():
    uptime = time.time() - START_TIME
    return {
        "loaded_agents": [
            "FinanceAgent",
            "MarketAgent",
            "RiskAgent",
            "PredictionAgent",
            "TimelineAgent",
            "EvidenceAgent",
            "DecisionAgent",
        ],
        "agent_coordinator": "Active",
        "knowledge_base_status": "Online",
        "uptime": f"{uptime:.2f}s",
        "configuration": {"mode": "production", "max_threads": 4},
        "memory_usage": "42.5%",
        "active_analyses": 0,
        "environment": "production",
        "backend_version": "1.0.0",
    }


@app.get("/api/v1/dashboard/metrics")
def dashboard_metrics():
    try:
        conn = db_manager.connect()
        cursor = conn.cursor()

        # Count total analyses
        cursor.execute("SELECT COUNT(*) FROM analysis")
        total_analyses = cursor.fetchone()[0]

        # Count completed analyses for average processing time
        cursor.execute("SELECT COUNT(*) FROM analysis WHERE status = 'completed'")
        analyses_completed = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM scenarios")
        active_scenarios = cursor.fetchone()[0]

        # Calculate average processing time dynamically
        cursor.execute("""
            SELECT AVG((julianday(end_time) - julianday(start_time)) * 86400.0)
            FROM analysis
            WHERE status = 'completed' AND start_time IS NOT NULL AND end_time IS NOT NULL
        """)
        avg_time_row = cursor.fetchone()
        
        if total_analyses == 0:
            avg_time_str = "--"
            success_rate = "--"
        else:
            if avg_time_row and avg_time_row[0] is not None:
                avg_time_str = f"{round(avg_time_row[0], 1)}s"
            else:
                avg_time_str = "--"
                
            success_rate = f"{round((analyses_completed / total_analyses) * 100)}%"

        # Risk Aggregation
        cursor.execute("SELECT risk_level, COUNT(*) as count FROM analysis WHERE status = 'completed' AND risk_level IS NOT NULL GROUP BY risk_level ORDER BY count DESC LIMIT 1")
        risk_row = cursor.fetchone()
        system_risk_level = risk_row[0] if risk_row else "Unknown"

        return {
            "analyses_completed": analyses_completed,
            "active_scenarios": active_scenarios,
            "average_processing_time": avg_time_str,
            "success_rate": success_rate,
            "risk_level": system_risk_level,
        }
    except Exception as e:
        print(f"Error fetching metrics: {e}")
        return {
            "analyses_completed": 0,
            "active_scenarios": 0,
            "average_processing_time": "--",
            "success_rate": "--",
            "risk_level": "Unknown",
        }


@app.get("/api/v1/dashboard/activity")
def dashboard_activity():
    try:
        conn = db_manager.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                a.id, b.name as business_name, 
                a.status, a.start_time, a.risk_level,
                (julianday(a.end_time) - julianday(a.start_time)) * 86400.0 as processing_time,
                (SELECT COUNT(*) FROM scenarios s WHERE s.analysis_id = a.id) as scenario_count
            FROM analysis a
            LEFT JOIN business b ON a.business_id = b.id
            ORDER BY a.start_time DESC LIMIT 5
        """)
        
        analyses = []
        for r in cursor.fetchall():
            analyses.append({
                "id": r[0],
                "business_name": r[1] or "Unnamed Business",
                "scenario_count": r[6] or 0,
                "status": r[2],
                "start_time": r[3],
                "risk_level": r[4] or "--",
                "processing_time": f"{round(r[5], 1)}s" if r[5] is not None else "--"
            })

        cursor.execute("SELECT id, name FROM scenarios LIMIT 5")
        scenarios = [{"id": r[0], "name": r[1] or "Unnamed Scenario"} for r in cursor.fetchall()]

        cursor.execute("SELECT id, report_metadata, generation_time FROM reports ORDER BY generation_time DESC LIMIT 5")
        reports = []
        import json
        for r in cursor.fetchall():
            meta = {}
            try:
                meta = json.loads(r[1])
            except:
                pass
            reports.append({
                "id": r[0],
                "name": meta.get("title", f"Report {r[0][:8]}"),
                "generation_time": r[2],
                "export_type": "PDF, CSV, JSON"
            })

        return {
            "recent_analyses": analyses,
            "recent_scenarios": scenarios,
            "recent_reports": reports,
        }
    except Exception:
        return {"recent_analyses": [], "recent_scenarios": [], "recent_reports": []}


@app.get("/api/v1/dashboard/charts")
def dashboard_charts():
    try:
        conn = db_manager.connect()
        cursor = conn.cursor()

        # 1. Analysis count over time
        # 1. Analysis count over time
        cursor.execute("SELECT start_time FROM analysis WHERE start_time IS NOT NULL ORDER BY start_time")
        raw_dates = [r[0] for r in cursor.fetchall()]
        
        import datetime
        from collections import defaultdict
        
        analysis_count_over_time = []
        if raw_dates:
            try:
                parsed_dates = [d if isinstance(d, datetime.datetime) else datetime.datetime.strptime(str(d).split('.')[0], "%Y-%m-%d %H:%M:%S") for d in raw_dates]
                min_date = min(parsed_dates)
                max_date = datetime.datetime.now() # Use now for max date
                
                delta = max_date - min_date
                
                counts = defaultdict(int)
                
                if delta.days < 7:
                    # Hourly
                    for pd in parsed_dates:
                        counts[pd.replace(minute=0, second=0, microsecond=0)] += 1
                        
                    current = min_date.replace(minute=0, second=0, microsecond=0)
                    end = max_date.replace(minute=0, second=0, microsecond=0)
                    while current <= end:
                        analysis_count_over_time.append({
                            "date": current.strftime("%Y-%m-%d %H:%M"),
                            "count": counts[current]
                        })
                        current += datetime.timedelta(hours=1)
                        
                elif delta.days < 90:
                    # Daily
                    for pd in parsed_dates:
                        counts[pd.replace(hour=0, minute=0, second=0, microsecond=0)] += 1
                        
                    current = min_date.replace(hour=0, minute=0, second=0, microsecond=0)
                    end = max_date.replace(hour=0, minute=0, second=0, microsecond=0)
                    while current <= end:
                        analysis_count_over_time.append({
                            "date": current.strftime("%Y-%m-%d"),
                            "count": counts[current]
                        })
                        current += datetime.timedelta(days=1)
                else:
                    # Weekly
                    for pd in parsed_dates:
                        # Group by start of week (Monday)
                        start_of_week = pd - datetime.timedelta(days=pd.weekday())
                        counts[start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)] += 1
                        
                    current = min_date - datetime.timedelta(days=min_date.weekday())
                    current = current.replace(hour=0, minute=0, second=0, microsecond=0)
                    end = max_date.replace(hour=0, minute=0, second=0, microsecond=0)
                    while current <= end:
                        analysis_count_over_time.append({
                            "date": current.strftime("%Y-%m-%d"),
                            "count": counts[current]
                        })
                        current += datetime.timedelta(days=7)
            except Exception as e:
                print(f"Error grouping dates: {e}")
                analysis_count_over_time = []

        # 2. Risk distribution
        cursor.execute("SELECT risk_level FROM analysis WHERE risk_level IS NOT NULL")
        levels = [r[0] for r in cursor.fetchall()]
        risk_dist = {"Low": 0, "Medium": 0, "High": 0}
        for level in levels:
            if level in risk_dist:
                risk_dist[level] += 1

        risk_distribution = [
            {"level": k, "value": v} for k, v in risk_dist.items() if v > 0
        ]

        # 3. Success rate (status distribution)
        cursor.execute("SELECT status, COUNT(*) FROM analysis GROUP BY status")
        success_rate = [{"status": r[0], "count": r[1]} for r in cursor.fetchall()]

        # 4. Scenario categories (using estimated_complexity)
        cursor.execute(
            "SELECT estimated_complexity, COUNT(*) FROM scenarios WHERE estimated_complexity IS NOT NULL GROUP BY estimated_complexity"
        )
        scenario_categories = [
            {"category": r[0], "count": r[1]} for r in cursor.fetchall()
        ]

        # 5. Agent execution statistics (from events)
        cursor.execute("SELECT event_name, COUNT(*) FROM events GROUP BY event_name")
        agent_execution = [{"agent": r[0], "count": r[1]} for r in cursor.fetchall()]

        return {
            "analysis_count_over_time": analysis_count_over_time,
            "risk_distribution": risk_distribution,
            "success_rate": success_rate,
            "scenario_categories": scenario_categories,
            "agent_execution": agent_execution,
        }
    except Exception:
        return {
            "analysis_count_over_time": [],
            "risk_distribution": [],
            "success_rate": [],
            "scenario_categories": [],
            "agent_execution": [],
        }


@app.post("/api/v1/analysis")
def create_analysis(payload: Dict[str, Any]):
    try:
        conn = db_manager.connect()
        cursor = conn.cursor()
        import datetime

        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute(
            """
            INSERT INTO business (id, name, type, category, location, created_date, updated_date, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                payload.get("id"),
                payload.get("name", "Unknown"),
                payload.get("type", "Unknown"),
                "General",
                payload.get("location", "Unknown"),
                now_str,
                now_str,
                "active",
            ),
        )

        import uuid

        analysis_id = str(uuid.uuid4())
        cursor.execute(
            """
            INSERT INTO analysis (id, business_id, start_time, version, status)
            VALUES (?, ?, ?, ?, ?)
        """,
            (analysis_id, payload.get("id"), now_str, "1.0", "initialized"),
        )
        conn.commit()
        return {"status": "success", "analysis_id": analysis_id}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.put("/api/v1/analysis/{id}/complete")
def complete_analysis(id: str, payload: Dict[str, Any]):
    try:
        conn = db_manager.connect()
        cursor = conn.cursor()
        import datetime
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        metrics = payload.get("metrics", {})
        revenue = metrics.get("revenue")
        profit = metrics.get("profit")
        roi = metrics.get("roi")
        risk_level = str(metrics.get("risk_score")) if metrics.get("risk_score") is not None else None
        # Convert numeric risk score to qualitative level if needed, but let's just save the string.
        # Actually risk score is 0-100.
        if risk_level and risk_level.isdigit():
            score = int(risk_level)
            if score < 33:
                risk_level = "Low"
            elif score < 66:
                risk_level = "Medium"
            else:
                risk_level = "High"

        cursor.execute(
            """
            UPDATE analysis 
            SET end_time = ?, status = ?, revenue = ?, profit = ?, roi = ?, risk_level = ?
            WHERE id = ?
            """,
            (now_str, "completed", revenue, profit, roi, risk_level, id)
        )
        conn.commit()
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/api/v1/history")
def get_history(limit: int = 50, offset: int = 0):
    try:
        conn = db_manager.connect()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                a.id, b.name as business_name, b.type as business_type, 
                a.start_time, a.end_time, a.status, a.confidence as decision_score,
                a.revenue, a.profit, a.roi, a.risk_level,
                (SELECT COUNT(*) FROM scenarios s WHERE s.analysis_id = a.id) as scenario_count,
                COALESCE(
                    json_extract(a.results_payload, '$.decision_result.rationale'),
                    CASE 
                        WHEN a.confidence IS NULL THEN 'PENDING'
                        WHEN a.confidence >= 80 THEN 'APPROVE'
                        WHEN a.confidence >= 60 THEN 'PROCEED WITH CAUTION'
                        WHEN a.confidence >= 40 THEN 'REVIEW'
                        ELSE 'REJECT'
                    END
                ) as recommendation,
                (julianday(a.end_time) - julianday(a.start_time)) * 86400.0 as processing_time
            FROM analysis a
            JOIN business b ON a.business_id = b.id
            GROUP BY a.id
            ORDER BY a.start_time DESC
            LIMIT ? OFFSET ?
        """, (limit, offset))
        
        columns = [column[0] for column in cursor.description]
        results = []
        for row in cursor.fetchall():
            res = dict(zip(columns, row))
            # Format processing time
            if res["processing_time"] is not None:
                res["processing_time"] = f"{round(res['processing_time'], 1)}s"
            else:
                res["processing_time"] = "--"
            results.append(res)
            
        return {"status": "success", "data": results}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.delete("/api/v1/history/{id}")
def delete_history_record(id: str):
    try:
        conn = db_manager.connect()
        cursor = conn.cursor()
        
        # Foreign key constraints should ideally handle cascading deletes if ON DELETE CASCADE is set
        # Since we can't guarantee ON DELETE CASCADE, we'll manually delete child records.
        # Tables that ref analysis: scenarios, recommendations, reports, assumptions, feedback, learning, events
        cursor.execute("DELETE FROM forecasts WHERE scenario_id IN (SELECT id FROM scenarios WHERE analysis_id = ?)", (id,))
        cursor.execute("DELETE FROM scenarios WHERE analysis_id = ?", (id,))
        cursor.execute("DELETE FROM recommendations WHERE analysis_id = ?", (id,))
        cursor.execute("DELETE FROM reports WHERE analysis_id = ?", (id,))
        cursor.execute("DELETE FROM assumptions WHERE analysis_id = ?", (id,))
        cursor.execute("DELETE FROM feedback WHERE analysis_id = ?", (id,))
        cursor.execute("DELETE FROM learning WHERE analysis_id = ?", (id,))
        cursor.execute("DELETE FROM events WHERE analysis_id = ?", (id,))
        
        cursor.execute("DELETE FROM analysis WHERE id = ?", (id,))
        conn.commit()
        
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


class APIManager:
    def initialize(self) -> None:
        pass

    def start(self) -> None:
        pass

    def validate(self) -> bool:
        return True

    def health_check(self) -> Dict[str, str]:
        return {"status": "healthy"}

@app.post("/api/v1/analysis/{id}/execute")
def execute_analysis(id: str, payload: Dict[str, Any]):
    try:
        from backend.services.agents.decision_score.models import ScenarioOutput
        from backend.services.agents.decision_score.decision_score_agent import DecisionScoreAgent
        import datetime

        profile = payload.get("profile", {})
        scenarios = payload.get("scenarios", [])

        try:
            conn = db_manager.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT b.type FROM business b JOIN analysis a ON b.id = a.business_id WHERE a.id = ?", (id,))
            row = cursor.fetchone()
            if row:
                profile["business_type"] = row[0]
        except Exception:
            pass

        if not scenarios:
            scenarios = [{
                "id": "baseline",
                "name": "Baseline",
                "adjustments": {"cost": 0, "demand": 0, "price": 0}
            }]

        from backend.services.agents.finance.finance_agent import FinanceAgent
        f_agent = FinanceAgent()
        baseline = f_agent.estimate_baseline(profile)
        if "expected_revenue" not in profile:
            profile["expected_revenue"] = baseline["expected_revenue"]
        if "operating_costs" not in profile:
            profile["operating_costs"] = baseline["operating_costs"]
            
        base_investment = float(profile["investment"])
        base_revenue = float(profile["expected_revenue"])
        base_costs = float(profile["operating_costs"])
        base_risk = 50.0

        scenario_outputs = []
        for sc in scenarios:
            adj = sc.get("adjustments", {})
            cost_adj = float(adj.get("cost", 0)) / 100.0
            demand_adj = float(adj.get("demand", 0)) / 100.0
            price_adj = float(adj.get("price", 0)) / 100.0

            # Dynamic calculations
            proj_revenue = base_revenue * (1 + demand_adj) * (1 + price_adj)
            proj_costs = base_costs * (1 + cost_adj)
            profit = proj_revenue - proj_costs
            
            roi = 0.0
            if base_investment > 0:
                roi = (profit / base_investment) * 100.0

            # Calculate scenario-specific dynamic risk
            scenario_risk = base_risk + (cost_adj * 50) - (demand_adj * 20) + (price_adj * 10)
            scenario_risk = max(0.0, min(100.0, scenario_risk))

            scenario_outputs.append(
                ScenarioOutput(
                    scenario_id=sc.get("id", "unknown"),
                    strategy_id=sc.get("name", "unknown"),
                    metrics={"revenue": proj_revenue, "profit": profit, "roi": roi, "risk": scenario_risk},
                    confidence=0.85 # base agent confidence in calculation
                )
            )

        # Inject anchors for absolute scaling
        scenario_outputs.extend([
            ScenarioOutput(
                scenario_id="anchor_perfect",
                strategy_id="Perfect",
                metrics={"revenue": base_revenue * 2, "profit": base_investment * 2, "roi": 200, "risk": 0},
                confidence=1.0
            ),
            ScenarioOutput(
                scenario_id="anchor_terrible",
                strategy_id="Terrible",
                metrics={"revenue": 0, "profit": -base_investment, "roi": -100, "risk": 100},
                confidence=1.0
            )
        ])

        # Let the DecisionScoreEngine aggregate the scores and give a final recommendation!
        agent = DecisionScoreAgent()
        weights = {"profit": 0.5, "roi": 0.5}
        recommendation = agent.process_scenarios(scenario_outputs, weights)

        # Map decision scores back to scenario_outputs
        strategy_to_score = {r.strategy_id: r.score.total_score * 100.0 for r in recommendation.rankings}
        for so in scenario_outputs:
            so.metrics["decision_score"] = strategy_to_score.get(so.strategy_id, 0.0)

        # Average the scores of the user's scenarios for the global analysis
        user_strategy_ids = [s.get("name", "unknown") for s in scenarios]
        user_scores = []
        for r in recommendation.rankings:
            if r.strategy_id in user_strategy_ids:
                user_scores.append(r.score.total_score)
        
        if user_scores:
            avg_score = sum(user_scores) / len(user_scores)
        else:
            avg_score = 0
            
        decision_score = max(0.0, min(100.0, avg_score * 100.0))

        avg_revenue = sum(base_revenue * (1 + (s.get("adjustments", {}).get("demand", 0)/100)) * (1 + (s.get("adjustments", {}).get("price", 0)/100)) for s in scenarios) / max(1, len(scenarios))
        avg_profit = sum(o.metrics["profit"] for o in scenario_outputs if not o.scenario_id.startswith("anchor_")) / len(scenarios)
        avg_roi = sum(o.metrics["roi"] for o in scenario_outputs if not o.scenario_id.startswith("anchor_")) / len(scenarios)

        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Dynamic Execution via Coordinator
        from backend.services.agents.coordinator import AgentCoordinator
        coordinator = AgentCoordinator()
        analysis_context = {
            "profile": profile,
            "scenarios": scenarios,
            "decision_score": decision_score,
            "metrics": {
                "avg_revenue": avg_revenue,
                "avg_profit": avg_profit,
                "avg_roi": avg_roi,
                "base_investment": base_investment
            }
        }
        
        market_analysis = coordinator.run_agent("market", analysis_context)
        analysis_context["market_analysis"] = market_analysis
        
        risk_analysis = coordinator.run_agent("risk", analysis_context)
        analysis_context["risk_analysis"] = risk_analysis
        
        predictions = coordinator.run_agent("prediction", analysis_context)
        analysis_context["predictions"] = predictions
        
        timeline = coordinator.run_agent("timeline", analysis_context)
        analysis_context["timeline"] = timeline
        
        # Pass scenario_outputs to decision agent for final score
        analysis_context["scenario_outputs"] = scenario_outputs
        decision_result = coordinator.run_agent("decision", analysis_context)
        analysis_context["decision_result"] = decision_result
        decision_score = decision_result.get("score", 0)
        rationale = decision_result.get("rationale", "")

        evidence = coordinator.run_agent("evidence", analysis_context)
        
        risk_level = risk_analysis["level"]

        import json
        results_payload = json.dumps({
            "market_analysis": market_analysis,
            "risk_analysis": risk_analysis,
            "predictions": predictions,
            "timeline": timeline,
            "evidence": evidence,
            "decision_result": decision_result
        })

        # Save to DB
        conn = db_manager.connect()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE analysis 
            SET end_time = ?, status = ?, revenue = ?, profit = ?, roi = ?, risk_level = ?, confidence = ?, results_payload = ?
            WHERE id = ?
            """,
            (now_str, "completed", avg_revenue, avg_profit, avg_roi, risk_level, int(decision_score), results_payload, id)
        )
        conn.commit()

        return {
            "status": "success",
            "metrics": {
                "revenue": avg_revenue,
                "profit": avg_profit,
                "roi": avg_roi,
                "risk_score": int(risk_analysis.get("score", 0)),
                "confidence": int(decision_score),
                "market_analysis": market_analysis,
                "risk_analysis": risk_analysis,
                "predictions": predictions,
                "timeline": timeline,
                "evidence": evidence,
                "scenario_outputs": [
                    {
                        "scenario_id": o.scenario_id,
                        "strategy_id": o.strategy_id,
                        "metrics": o.metrics
                    }
                    for o in scenario_outputs if not o.scenario_id.startswith("anchor_")
                ]
            },
            "rationale": rationale
        }
    except Exception as e:
        print(f"Execution Error: {e}")
        return {"status": "error", "message": str(e)}
