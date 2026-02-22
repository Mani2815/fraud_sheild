import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "logs.db")


def init_db():
    """Create the logs table if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analysis_logs (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            message     TEXT    NOT NULL,
            rule_score  INTEGER NOT NULL,
            ai_score    INTEGER NOT NULL,
            final_score INTEGER NOT NULL,
            risk_level  TEXT    NOT NULL,
            flags       TEXT    NOT NULL,
            analyzed_at TEXT    NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def log_analysis(message, rule_score, ai_score, final_score, risk_level, detected_phrases):
    """Insert one analysis record into the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO analysis_logs
            (message, rule_score, ai_score, final_score, risk_level, flags, analyzed_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        message,
        rule_score,
        ai_score,
        final_score,
        risk_level,
        ", ".join(detected_phrases),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))
    conn.commit()
    conn.close()


def get_recent_logs(limit=10):
    """Fetch the most recent analysis records."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM analysis_logs
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows


def get_stats():
    """Return aggregate statistics across all logs."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM analysis_logs")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM analysis_logs WHERE risk_level = 'HIGH'")
    high = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM analysis_logs WHERE risk_level = 'MEDIUM'")
    medium = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM analysis_logs WHERE risk_level = 'LOW'")
    low = cursor.fetchone()[0]

    cursor.execute("SELECT ROUND(AVG(final_score), 1) FROM analysis_logs")
    avg_score = cursor.fetchone()[0] or 0

    conn.close()
    return {
        "total": total,
        "high": high,
        "medium": medium,
        "low": low,
        "avg_score": avg_score
    }
