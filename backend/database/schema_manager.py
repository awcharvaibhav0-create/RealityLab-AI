import sqlite3


class SchemaManager:
    """Manages the creation and initialization of the database schema."""

    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection

    def create_tables(self):
        """Creates all necessary tables if they do not exist."""
        cursor = self.connection.cursor()

        # 1. Business
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS business (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                category TEXT NOT NULL,
                location TEXT NOT NULL,
                created_date TIMESTAMP NOT NULL,
                updated_date TIMESTAMP NOT NULL,
                status TEXT NOT NULL
            )
        """)

        # 2. Business Settings
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS business_settings (
                business_id TEXT PRIMARY KEY,
                currency TEXT NOT NULL,
                language TEXT NOT NULL,
                timezone TEXT NOT NULL,
                preferred_forecast_horizon INTEGER NOT NULL,
                report_preferences TEXT NOT NULL,
                privacy_settings TEXT NOT NULL,
                FOREIGN KEY(business_id) REFERENCES business(id)
            )
        """)

        # 3. Analysis
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analysis (
                id TEXT PRIMARY KEY,
                business_id TEXT NOT NULL,
                start_time TIMESTAMP NOT NULL,
                end_time TIMESTAMP,
                version TEXT NOT NULL,
                status TEXT NOT NULL,
                confidence INTEGER,
                revenue REAL,
                profit REAL,
                roi REAL,
                risk_level TEXT,
                results_payload TEXT,
                FOREIGN KEY(business_id) REFERENCES business(id)
            )
        """)

        # 4. Scenarios
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scenarios (
                id TEXT PRIMARY KEY,
                analysis_id TEXT NOT NULL,
                name TEXT NOT NULL,
                description TEXT,
                estimated_investment REAL,
                estimated_complexity TEXT,
                FOREIGN KEY(analysis_id) REFERENCES analysis(id)
            )
        """)

        # 5. Forecasts
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS forecasts (
                id TEXT PRIMARY KEY,
                scenario_id TEXT NOT NULL,
                month INTEGER NOT NULL,
                revenue REAL NOT NULL,
                expenses REAL NOT NULL,
                profit REAL NOT NULL,
                customers INTEGER NOT NULL,
                cash_flow REAL NOT NULL,
                FOREIGN KEY(scenario_id) REFERENCES scenarios(id)
            )
        """)

        # 6. Recommendations
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS recommendations (
                id TEXT PRIMARY KEY,
                analysis_id TEXT NOT NULL,
                winning_scenario_id TEXT NOT NULL,
                overall_score INTEGER NOT NULL,
                confidence INTEGER NOT NULL,
                explanation TEXT NOT NULL,
                trade_offs TEXT NOT NULL,
                timestamp TIMESTAMP NOT NULL,
                FOREIGN KEY(analysis_id) REFERENCES analysis(id),
                FOREIGN KEY(winning_scenario_id) REFERENCES scenarios(id)
            )
        """)

        # 7. Reports
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reports (
                id TEXT PRIMARY KEY,
                analysis_id TEXT NOT NULL,
                report_metadata TEXT NOT NULL,
                pdf_path TEXT,
                json_path TEXT,
                csv_path TEXT,
                generation_time TIMESTAMP NOT NULL,
                checksum TEXT NOT NULL,
                version TEXT NOT NULL,
                FOREIGN KEY(analysis_id) REFERENCES analysis(id)
            )
        """)

        # 8. Assumptions
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS assumptions (
                id TEXT PRIMARY KEY,
                analysis_id TEXT NOT NULL,
                name TEXT NOT NULL,
                value REAL NOT NULL,
                source TEXT NOT NULL,
                confidence INTEGER NOT NULL,
                version TEXT NOT NULL,
                FOREIGN KEY(analysis_id) REFERENCES analysis(id)
            )
        """)

        # 9. Knowledge Versions
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS knowledge_versions (
                id TEXT PRIMARY KEY,
                knowledge_package TEXT NOT NULL,
                version TEXT NOT NULL,
                created TIMESTAMP NOT NULL,
                checksum TEXT NOT NULL,
                status TEXT NOT NULL
            )
        """)

        # 10. Feedback
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id TEXT PRIMARY KEY,
                analysis_id TEXT NOT NULL,
                implemented BOOLEAN NOT NULL,
                user_satisfaction TEXT NOT NULL,
                actual_monthly_revenue REAL,
                actual_monthly_profit REAL,
                comments TEXT,
                timestamp TIMESTAMP NOT NULL,
                FOREIGN KEY(analysis_id) REFERENCES analysis(id)
            )
        """)

        # 11. Learning
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS learning (
                id TEXT PRIMARY KEY,
                analysis_id TEXT NOT NULL,
                forecast_accuracy REAL NOT NULL,
                recommendation_success REAL NOT NULL,
                improvement_suggestions TEXT NOT NULL,
                timestamp TIMESTAMP NOT NULL,
                FOREIGN KEY(analysis_id) REFERENCES analysis(id)
            )
        """)

        # 12. Audit Logs
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_logs (
                id TEXT PRIMARY KEY,
                action TEXT NOT NULL,
                user_id TEXT NOT NULL,
                details TEXT NOT NULL,
                timestamp TIMESTAMP NOT NULL
            )
        """)

        # 13. Events
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id TEXT PRIMARY KEY,
                analysis_id TEXT,
                event_name TEXT NOT NULL,
                payload TEXT NOT NULL,
                timestamp TIMESTAMP NOT NULL,
                FOREIGN KEY(analysis_id) REFERENCES analysis(id)
            )
        """)

        # 14. Configuration
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS config (
                config_key TEXT PRIMARY KEY,
                config_value TEXT NOT NULL,
                updated_at TIMESTAMP NOT NULL
            )
        """)

        # 15. Cache
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cache (
                cache_key TEXT PRIMARY KEY,
                category TEXT NOT NULL,
                payload TEXT NOT NULL,
                expires_at TIMESTAMP NOT NULL,
                created_at TIMESTAMP NOT NULL
            )
        """)

        # Migrations
        migrations = [
            "ALTER TABLE analysis ADD COLUMN revenue REAL",
            "ALTER TABLE analysis ADD COLUMN profit REAL",
            "ALTER TABLE analysis ADD COLUMN roi REAL",
            "ALTER TABLE analysis ADD COLUMN risk_level TEXT"
        ]
        
        for mig in migrations:
            try:
                cursor.execute(mig)
            except sqlite3.OperationalError:
                # Column already exists
                pass

        self.connection.commit()
