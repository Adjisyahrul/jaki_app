# Database Utilities for JAKI App
import sqlite3
import os

DATABASE_DIR = "/home/ubuntu/jaki_app/database"
DATABASE_PATH = os.path.join(DATABASE_DIR, "jaki_reports.db")

def init_db():
    """Initializes the database and creates the reports table if it doesn't exist."""
    os.makedirs(DATABASE_DIR, exist_ok=True)
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        image_path TEXT NOT NULL,
        category TEXT NOT NULL,
        description TEXT,
        latitude REAL,
        longitude REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        status TEXT DEFAULT 'pending'
    );
    """)
    conn.commit()
    conn.close()

def add_report(image_path: str, category: str, description: str, latitude: float, longitude: float) -> int:
    """Adds a new report to the database and returns the report ID."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO reports (image_path, category, description, latitude, longitude)
    VALUES (?, ?, ?, ?, ?)
    """, (image_path, category, description, latitude, longitude))
    report_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return report_id

def get_all_reports():
    """Retrieves all reports from the database."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, image_path, category, description, latitude, longitude, timestamp, status FROM reports ORDER BY timestamp DESC")
    reports = cursor.fetchall()
    conn.close()
    return reports

if __name__ == "__main__":
    # Initialize the database when this script is run directly (for setup)
    init_db()
    print(f"Database initialized at {DATABASE_PATH}")
    # Example usage (optional - for testing)
    # test_report_id = add_report("test_image.jpg", "Jalan Rusak", "Lubang besar di jalan utama", -6.175392, 106.827153)
    # print(f"Added test report with ID: {test_report_id}")
    # print("All reports:", get_all_reports())

