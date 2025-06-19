import sqlite3

conn = sqlite3.connect("timetable.db")
cursor = conn.cursor()

print("\n--- Teachers Table ---")
cursor.execute("SELECT * FROM teachers")
for row in cursor.fetchall():
    print(row)

print("\n--- Subjects Table ---")
cursor.execute("SELECT * FROM subjects")
for row in cursor.fetchall():
    print(row)

conn.close()
