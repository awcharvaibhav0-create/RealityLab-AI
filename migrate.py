import sqlite3
try:
    conn = sqlite3.connect(r'c:\Users\HP\project2.0\realitylab.db')
    cursor = conn.cursor()
    cursor.execute("ALTER TABLE analysis ADD COLUMN results_payload TEXT")
    conn.commit()
    print("Migration successful.")
except sqlite3.OperationalError as e:
    print(f"Migration error (already run?): {e}")
