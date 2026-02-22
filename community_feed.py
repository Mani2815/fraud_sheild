"""
Feature 9: Community Scam Feed
Anonymized HIGH-risk message feed — crowdsourced threat intelligence.
"""
import sqlite3
import os
import re

DB_PATH = os.path.join(os.path.dirname(__file__), "logs.db")


def anonymize_message(message):
    """Remove personal identifiers before sharing."""
    text = message

    # Remove phone numbers
    text = re.sub(r'\b[\d\s\-\+]{10,15}\b', '[PHONE REDACTED]', text)

    # Remove email addresses
    text = re.sub(r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}', '[EMAIL REDACTED]', text)

    # Partially redact URLs (keep domain for analysis)
    def redact_url(m):
        url = m.group(0)
        try:
            from urllib.parse import urlparse
            domain = urlparse(url).netloc
            return f'[LINK: {domain}]'
        except Exception:
            return '[LINK REDACTED]'
    text = re.sub(r'https?://\S+', redact_url, text)

    # Remove Aadhaar-like 12-digit numbers
    text = re.sub(r'\b\d{4}\s?\d{4}\s?\d{4}\b', '[AADHAAR REDACTED]', text)

    # Remove account numbers (8-18 digit sequences)
    text = re.sub(r'\b\d{8,18}\b', '[ACCOUNT REDACTED]', text)

    return text.strip()


def get_community_feed(limit=15):
    """
    Return recent HIGH and MEDIUM risk messages for the community feed.
    Messages are anonymized before display.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, message, final_score, risk_level, flags, analyzed_at
            FROM analysis_logs
            WHERE risk_level IN ('HIGH', 'MEDIUM')
            ORDER BY id DESC
            LIMIT ?
        """, (limit,))
        rows = cursor.fetchall()
        conn.close()

        feed = []
        for row in rows:
            feed.append({
                'id': row['id'],
                'message': anonymize_message(row['message']),
                'score': row['final_score'],
                'risk_level': row['risk_level'],
                'flags': row['flags'],
                'time': row['analyzed_at'],
                'flag_count': len(row['flags'].split(', ')) if row['flags'] else 0,
            })

        return feed
    except Exception:
        return []


def get_top_flags(limit=10):
    """Get the most frequently detected fraud keywords across all logs."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT flags FROM analysis_logs WHERE flags != ''")
        rows = cursor.fetchall()
        conn.close()

        counter = {}
        for (flags_str,) in rows:
            for flag in flags_str.split(', '):
                flag = flag.strip()
                if flag:
                    counter[flag] = counter.get(flag, 0) + 1

        sorted_flags = sorted(counter.items(), key=lambda x: x[1], reverse=True)
        return sorted_flags[:limit]
    except Exception:
        return []
