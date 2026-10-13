import sqlite3

conn = sqlite3.connect(r"E:\AI-Server\database\chat.db")

cur = conn.cursor()

cur.execute("""
SELECT id,
       timestamp,
       source,
       category,
       prompt,
       response
FROM memory
ORDER BY id DESC
LIMIT 20
""")

for row in cur.fetchall():
    print(row)

conn.close()