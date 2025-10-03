import sqlite3
import json
from datetime import datetime

DB_PATH = "analyses.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS analyses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT,
        summary TEXT,
        title TEXT,
        topics TEXT,
        keywords TEXT,
        sentiment TEXT,
        metadata TEXT,
        created_at TEXT
    )
    """)
    conn.commit()
    conn.close()

def insert_analysis(text, summary, title, topics, keywords, sentiment, metadata):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
      INSERT INTO analyses (text, summary, title, topics, keywords, sentiment, metadata, created_at)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (text, summary, title, ",".join(topics) if topics else "", ",".join(keywords) if keywords else "", sentiment, json.dumps(metadata), datetime.utcnow().isoformat()))
    conn.commit()
    rowid = cur.lastrowid
    conn.close()
    return rowid

def search_by_term(term):
    t = f"%{term}%"
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
      SELECT id, text, summary, title, topics, keywords, sentiment, metadata, created_at
      FROM analyses
      WHERE topics LIKE ? OR keywords LIKE ? OR title LIKE ?
      ORDER BY created_at DESC
    """, (t, t, t))
    rows = cur.fetchall()
    conn.close()
    results = []
    for r in rows:
        metadata = {}
        try:
            metadata = json.loads(r[7]) if r[7] else {}
        except:
            metadata = {"raw": r[7]}
        results.append({
            "id": r[0],
            "text": r[1],
            "summary": r[2],
            "title": r[3],
            "topics": r[4].split(",") if r[4] else [],
            "keywords": r[5].split(",") if r[5] else [],
            "sentiment": r[6],
            "metadata": metadata,
            "created_at": r[8]
        })
    return results

def get_all():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
      SELECT id, text, summary, title, topics, keywords, sentiment, metadata, created_at
      FROM analyses
      ORDER BY created_at DESC
    """)
    rows = cur.fetchall()
    conn.close()
    results = []
    for r in rows:
        metadata = {}
        try:
            metadata = json.loads(r[7]) if r[7] else {}
        except:
            metadata = {"raw": r[7]}
        results.append({
            "id": r[0],
            "text": r[1],
            "summary": r[2],
            "title": r[3],
            "topics": r[4].split(",") if r[4] else [],
            "keywords": r[5].split(",") if r[5] else [],
            "sentiment": r[6],
            "metadata": metadata,
            "created_at": r[8]
        })
    return results
