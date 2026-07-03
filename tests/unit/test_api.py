from fastapi.testclient import TestClient
from backend.api.api_manager import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/v1/health/")
    assert response.status_code == 200
    assert "status" in response.json()
    assert response.json()["status"] == "healthy"
    assert "sqlite" in response.json()
    assert "fastapi" in response.json()

def test_system_info():
    response = client.get("/api/v1/system/")
    assert response.status_code == 200
    assert "loaded_agents" in response.json()
    assert "agent_coordinator" in response.json()

def test_average_processing_time_dynamic():
    import sqlite3
    import uuid
    from backend.api.api_manager import db_manager
    from backend.database.schema_manager import SchemaManager
    
    # Use an in-memory database for testing
    test_conn = sqlite3.connect(':memory:', check_same_thread=False)
    
    # Patch the connect method
    original_connect = db_manager.connect
    db_manager.connect = lambda: test_conn
    
    try:
        # Initialize schema
        sm = SchemaManager(test_conn)
        sm.create_tables()
        
        # Test 1: No analyses
        resp1 = client.get("/api/v1/dashboard/metrics")
        assert resp1.status_code == 200
        assert resp1.json()["average_processing_time"] == "--"
        
        # Insert a business first due to foreign key
        b_id = str(uuid.uuid4())
        test_conn.execute("INSERT INTO business (id, name, type, category, location, created_date, updated_date, status) VALUES (?, 'Test', 'Retail', 'Tech', 'NYC', '2026-07-02 10:00:00', '2026-07-02 10:00:00', 'active')", (b_id,))
        
        # Insert Analysis 1: completed, took 2.5 seconds
        a1 = str(uuid.uuid4())
        test_conn.execute(
            "INSERT INTO analysis (id, business_id, start_time, end_time, version, status, confidence) VALUES (?, ?, '2026-07-02 10:00:00', '2026-07-02 10:00:02.500', '1.0', 'completed', 90)",
            (a1, b_id)
        )
        test_conn.commit()
        
        from backend.api.api_manager import dashboard_metrics
        # Removed cache_clear as ttl_cache was removed
        resp2 = client.get("/api/v1/dashboard/metrics")
        assert resp2.json()["average_processing_time"] == "2.5s"
        
        # Insert Analysis 2: completed, took 1.5 seconds
        a2 = str(uuid.uuid4())
        test_conn.execute(
            "INSERT INTO analysis (id, business_id, start_time, end_time, version, status, confidence) VALUES (?, ?, '2026-07-02 11:00:00', '2026-07-02 11:00:01.500', '1.0', 'completed', 90)",
            (a2, b_id)
        )
        test_conn.commit()
        
        # Average of 2.5 and 1.5 should be 2.0
        # Removed cache_clear as ttl_cache was removed
        resp3 = client.get("/api/v1/dashboard/metrics")
        assert resp3.json()["average_processing_time"] == "2.0s"
        
        # Insert Analysis 3: failed, should be ignored
        a3 = str(uuid.uuid4())
        test_conn.execute(
            "INSERT INTO analysis (id, business_id, start_time, end_time, version, status, confidence) VALUES (?, ?, '2026-07-02 12:00:00', '2026-07-02 12:00:10.000', '1.0', 'failed', 0)",
            (a3, b_id)
        )
        test_conn.commit()
        
        # Average should still be 2.0s
        # Removed cache_clear as ttl_cache was removed
        resp4 = client.get("/api/v1/dashboard/metrics")
        assert resp4.json()["average_processing_time"] == "2.0s"
        
    finally:
        # Restore the original connect method
        db_manager.connect = original_connect


def test_history_api():
    import sqlite3
    import uuid
    from backend.api.api_manager import db_manager
    from backend.database.schema_manager import SchemaManager
    
    # Use an in-memory database for testing
    test_conn = sqlite3.connect(':memory:', check_same_thread=False)
    
    # Patch the connect method
    original_connect = db_manager.connect
    db_manager.connect = lambda: test_conn
    
    try:
        # Initialize schema
        sm = SchemaManager(test_conn)
        sm.create_tables()
        
        # Test Empty History
        resp1 = client.get("/api/v1/history")
        assert resp1.status_code == 200
        assert len(resp1.json()["data"]) == 0
        
        # Insert test data
        b_id = str(uuid.uuid4())
        test_conn.execute("INSERT INTO business (id, name, type, category, location, created_date, updated_date, status) VALUES (?, 'HistTest', 'Retail', 'Tech', 'NYC', '2026-07-02 10:00:00', '2026-07-02 10:00:00', 'active')", (b_id,))
        
        a1 = str(uuid.uuid4())
        test_conn.execute(
            "INSERT INTO analysis (id, business_id, start_time, end_time, version, status, confidence, revenue, profit, roi, risk_level) VALUES (?, ?, '2026-07-02 10:00:00', '2026-07-02 10:00:02.500', '1.0', 'completed', 90, 1000, 400, 40, 'Low')",
            (a1, b_id)
        )
        
        a2 = str(uuid.uuid4())
        test_conn.execute(
            "INSERT INTO analysis (id, business_id, start_time, end_time, version, status, confidence, revenue, profit, roi, risk_level) VALUES (?, ?, '2026-07-02 11:00:00', '2026-07-02 11:00:01.500', '1.0', 'failed', 0, NULL, NULL, NULL, 'High')",
            (a2, b_id)
        )
        test_conn.commit()
        
        # Test GET History (Sorting Verification)
        resp2 = client.get("/api/v1/history")
        assert resp2.status_code == 200
        data = resp2.json()["data"]
        assert len(data) == 2
        # a2 was created at 11:00, a1 at 10:00. Newest first means a2 is first.
        assert data[0]["id"] == a2
        assert data[1]["id"] == a1
        
        # Test Complete API
        payload = {
            "metrics": {
                "revenue": 5000,
                "profit": 1000,
                "roi": 20.0,
                "risk_score": 10
            }
        }
        resp3 = client.put(f"/api/v1/analysis/{a2}/complete", json=payload)
        assert resp3.status_code == 200
        
        # Verify it updated
        resp4 = client.get("/api/v1/history")
        data4 = resp4.json()["data"]
        # a2 should now be completed and have revenue
        assert data4[0]["id"] == a2
        assert data4[0]["status"] == "completed"
        assert data4[0]["revenue"] == 5000
        assert data4[0]["risk_level"] == "Low"
        
        # Test Delete API
        resp5 = client.delete(f"/api/v1/history/{a1}")
        assert resp5.status_code == 200
        
        resp6 = client.get("/api/v1/history")
        data6 = resp6.json()["data"]
        assert len(data6) == 1
        assert data6[0]["id"] == a2
        
    finally:
        # Restore the original connect method
        db_manager.connect = original_connect

def test_decision_score_execute():
    import sqlite3
    import uuid
    from backend.api.api_manager import db_manager
    from backend.database.schema_manager import SchemaManager
    
    # Use an in-memory database for testing
    test_conn = sqlite3.connect(':memory:', check_same_thread=False)
    
    # Patch the connect method
    original_connect = db_manager.connect
    db_manager.connect = lambda: test_conn
    
    try:
        # Initialize schema
        sm = SchemaManager(test_conn)
        sm.create_tables()
        
        # Insert a business first due to foreign key
        b_id = str(uuid.uuid4())
        test_conn.execute("INSERT INTO business (id, name, type, category, location, created_date, updated_date, status) VALUES (?, 'DecisionTest', 'Retail', 'Tech', 'NYC', '2026-07-02 10:00:00', '2026-07-02 10:00:00', 'active')", (b_id,))
        
        a1 = str(uuid.uuid4())
        test_conn.execute(
            "INSERT INTO analysis (id, business_id, start_time, end_time, version, status, confidence) VALUES (?, ?, '2026-07-02 10:00:00', NULL, '1.0', 'initialized', NULL)",
            (a1, b_id)
        )
        test_conn.commit()

        # Run with normal positive scenarios
        payload1 = {
            "profile": {
                "investment": 100000,
                "expected_revenue": 200000,
                "operating_costs": 50000
            },
            "scenarios": [
                {
                    "id": "best",
                    "name": "Best Case",
                    "adjustments": {"demand": 20, "price": 10, "cost": -10}
                }
            ]
        }
        
        resp1 = client.post(f"/api/v1/analysis/{a1}/execute", json=payload1)
        assert resp1.status_code == 200
        data1 = resp1.json()
        assert data1["status"] == "success"
        score1 = data1["metrics"]["confidence"]
        assert score1 > 0
        
        # Run with terrible negative scenarios
        payload2 = {
            "profile": {
                "investment": 100000,
                "expected_revenue": 200000,
                "operating_costs": 50000
            },
            "scenarios": [
                {
                    "id": "worst",
                    "name": "Worst Case",
                    "adjustments": {"demand": -50, "price": -20, "cost": 50}
                }
            ]
        }
        
        resp2 = client.post(f"/api/v1/analysis/{a1}/execute", json=payload2)
        assert resp2.status_code == 200
        data2 = resp2.json()
        score2 = data2["metrics"]["confidence"]
        
        # The terrible scenario should have a significantly lower decision score!
        assert score2 < score1
        
    finally:
        # Restore the original connect method
        db_manager.connect = original_connect
def test_full_pipeline_execute():
    import sqlite3
    import uuid
    from backend.api.api_manager import db_manager
    from backend.database.schema_manager import SchemaManager
    
    test_conn = sqlite3.connect(':memory:', check_same_thread=False)
    original_connect = db_manager.connect
    db_manager.connect = lambda: test_conn
    
    try:
        sm = SchemaManager(test_conn)
        sm.create_tables()
        
        b_id = str(uuid.uuid4())
        test_conn.execute("INSERT INTO business VALUES (?, 'Test', 'Retail', 'Tech', 'NYC', '2026-07-02 10:00:00', '2026-07-02 10:00:00', 'active')", (b_id,))
        
        a1 = str(uuid.uuid4())
        test_conn.execute("INSERT INTO analysis VALUES (?, ?, '2026-07-02 10:00:00', NULL, '1.0', 'initialized', NULL, NULL, NULL, NULL, NULL, NULL)", (a1, b_id))
        test_conn.commit()
        
        payload = {
            "profile": {"investment": 100000, "expected_revenue": 200000, "operating_costs": 50000},
            "scenarios": []
        }
        
        resp = client.post(f"/api/v1/analysis/{a1}/execute", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "success"
        
        metrics = data["metrics"]
        assert "market_analysis" in metrics
        assert "risk_analysis" in metrics
        assert "predictions" in metrics
        assert "timeline" in metrics
        assert "evidence" in metrics
        
        # Verify schema
        assert "growth" in metrics["market_analysis"]
        assert "competition" in metrics["market_analysis"]
        assert "opportunity" in metrics["market_analysis"]
        assert "demand" in metrics["market_analysis"]
        assert isinstance(metrics["predictions"], dict)
        assert len(list(metrics["predictions"].values())[0]) == 6
        assert len(metrics["timeline"]) > 0
        
        # Test a second scenario to ensure dynamic differences
        payload2 = {
            "profile": {"investment": 500000, "expected_revenue": 100000, "operating_costs": 250000},
            "scenarios": [{"id": "bad", "name": "Worst Case", "adjustments": {"demand": -50, "price": -50, "cost": 50}}]
        }
        
        resp2 = client.post(f"/api/v1/analysis/{a1}/execute", json=payload2)
        assert resp2.status_code == 200
        metrics2 = resp2.json()["metrics"]
        
        assert resp.json()["metrics"]["confidence"] != resp2.json()["metrics"]["confidence"]
        
    finally:
        db_manager.connect = original_connect
