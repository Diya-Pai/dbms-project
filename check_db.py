import sqlite3

conn = sqlite3.connect("timetable.db")
cursor = conn.cursor()

try:
    print("\n--- Teachers Table ---")
    cursor.execute("SELECT * FROM teachers")
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            print(row)
    else:
        print("No teachers found.")

    print("\n--- Subjects Table ---")
    cursor.execute("SELECT * FROM subjects")
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            print(row)
    else:
        print("No subjects found.")
except sqlite3.OperationalError as e:
    print(f"Database error: {e}")

conn.close()
