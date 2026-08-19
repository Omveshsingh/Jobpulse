import sqlite3

connection = sqlite3.connect("jobs.db")

cursor = connection.cursor()

cursor.execute("""
    DELETE FROM jobs
    WHERE id IN ('123', '456')
    AND source IN ('remoteok', 'arbeitnow')
""")

connection.commit()

print("Test jobs removed:", cursor.rowcount)

connection.close()