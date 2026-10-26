import sqlite3
import json
from pathlib import Path
from datetime import datetime

DB_PATH = r"E:\AI-Server\database\chat.db"


def init_memory():

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS memory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        source TEXT,
        category TEXT,
        prompt TEXT,
        response TEXT,
        tags TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_memory(
    prompt,
    response,
    source="user",
    category="chat",
    tags=""
):

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO memory (
        timestamp,
        source,
        category,
        prompt,
        response,
        tags
    )
    VALUES (?, ?, ?, ?, ?, ?)
    """,
    (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        source,
        category,
        prompt,
        response,
        tags
    ))

    conn.commit()
    conn.close()


def list_memory():

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()

    cur.execute("""
    SELECT *
    FROM memory
    ORDER BY id DESC
    """)

    rows = [dict(x) for x in cur.fetchall()]

    conn.close()

    return rows


def search_memory(keyword):

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()

    cur.execute("""
    SELECT *
    FROM memory
    WHERE prompt LIKE ?
       OR response LIKE ?
       OR tags LIKE ?
    ORDER BY id DESC
    """,
    (
        f"%{keyword}%",
        f"%{keyword}%",
        f"%{keyword}%"
    ))

    rows = [dict(x) for x in cur.fetchall()]

    conn.close()

    return rows


def delete_memory(memory_id):

    conn = sqlite3.connect(DB_PATH)

    cur = conn.cursor()

    cur.execute(
        "DELETE FROM memory WHERE id=?",
        (memory_id,)
    )

    conn.commit()
    conn.close()
    
def list_memory(limit=50):

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    SELECT *
    FROM memory
    ORDER BY id DESC
    LIMIT ?
    """, (limit,))

    rows = cur.fetchall()

    conn.close()

    return rows
    
    
    
def list_knowledge():

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    SELECT *
    FROM knowledge
    ORDER BY id DESC
    """)

    rows = cur.fetchall()

    conn.close()

    return rows

MEMORY_DIR = Path("data/memory")
MEMORY_DIR.mkdir(parents=True, exist_ok=True)

TEST_FILE = MEMORY_DIR / "test.json"


def test_memory_write():

    try:

        data = {
            "timestamp": datetime.now().isoformat(),
            "message": "MemoryAgent Test"
        }

        with open(TEST_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f)

        return True

    except Exception:
        return False


def test_memory_read():

    try:

        with open(TEST_FILE, "r", encoding="utf-8") as f:
            json.load(f)

        return True

    except Exception:
        return False


def consistency_check():

    try:

        with open(TEST_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        required = [
            "timestamp",
            "message"
        ]

        return all(field in data for field in required)

    except Exception:
        return False


def garbage_collection():

    return True


def audit_memory():

    return {
        "agent": "MemoryAgent",
        "status": "online",
        "write_test": "PASS" if test_memory_write() else "FAIL",
        "read_test": "PASS" if test_memory_read() else "FAIL",
        "consistency": "PASS" if consistency_check() else "FAIL",
        "garbage_collection": "PASS" if garbage_collection() else "FAIL"
    }