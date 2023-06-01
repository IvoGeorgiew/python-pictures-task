import sqlite3

conn = sqlite3.connect('coordinates.db')
cursor = conn.cursor()
cursor.execute("DELETE FROM coordinates")
conn.commit()
conn.close()