import time
from backend.database.database_manager import DatabaseManager


def test_database_insert_performance():
    """
    Benchmarks database insertion speeds.
    Target: <100ms per standard batch
    """
    db_manager = DatabaseManager(":memory:")
    db_manager.initialize()

    start_time = time.time()

    db_manager.begin_transaction()
    conn = db_manager.connect()
    conn.execute(
        "INSERT INTO business (id, name, type, category, location, created_date, updated_date, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (
            "b1",
            "B",
            "T",
            "C",
            "L",
            "2026-06-30 00:00:00",
            "2026-06-30 00:00:00",
            "active",
        ),
    )
    conn.execute(
        "INSERT INTO analysis (id, business_id, start_time, version, status) VALUES (?, ?, ?, ?, ?)",
        ("a1", "b1", "2026-06-30 00:00:00", "1.0", "initialized"),
    )

    # Simulate saving 100 scenarios
    for i in range(100):
        conn.execute(
            "INSERT INTO scenarios (id, analysis_id, name) VALUES (?, ?, ?)",
            (f"s{i}", "a1", f"Scenario {i}"),
        )

    db_manager.commit()

    duration = time.time() - start_time
    assert duration < 0.1, f"Database insert too slow: {duration}s"
