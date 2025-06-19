import sqlite3

# Connect (or create) timetable.db
conn = sqlite3.connect("timetable.db")
cursor = conn.cursor()

# Drop tables if they exist (for clean rebuild)
cursor.execute("DROP TABLE IF EXISTS teachers")
cursor.execute("DROP TABLE IF EXISTS subjects")

# Create teachers table
cursor.execute("""
CREATE TABLE teachers (
    t_id TEXT PRIMARY KEY,
    name TEXT,
    role TEXT,
    max_units INTEGER
)
""")

# Create subjects table
cursor.execute("""
CREATE TABLE subjects (
    course_code TEXT,
    sname TEXT,
    t_id TEXT,
    credit INTEGER,
    hr_per_week INTEGER,
    sub_type TEXT,
    section_name TEXT
)
""")

# Insert sample teachers
teachers_data = [
    ('T1', 'Alice', 'Professor', 12),
    ('T2', 'Bob', 'Professor', 12),
    ('T3', 'Charlie', 'Assistant Professor', 10),
    ('T4', 'Diana', 'Lecturer', 10),
]

cursor.executemany("INSERT INTO teachers VALUES (?, ?, ?, ?)", teachers_data)

# Insert sample subjects
subjects_data = [
    ('CS101', 'ADA', 'T1', 4, 4, 'Theory', 'A'),
    ('CS102', 'DBMS', 'T2', 3, 3, 'Theory', 'A'),
    ('CS103', 'MC', 'T3', 3, 3, 'Theory', 'A'),
    ('CS104', 'Math', 'T4', 4, 4, 'Theory', 'A'),
    ('CS105', 'ADA Lab', 'T1', 1, 1, 'Lab', 'A'),
    ('CS106', 'DBMS Lab', 'T2', 1, 1, 'Lab', 'A'),
    ('CS107', 'MC Lab', 'T3', 1, 1, 'Lab', 'A'),
    ('CS108', 'UI/UX', 'T4', 2, 1, 'Lab', 'A'),

    ('CS101', 'ADA', 'T1', 4, 4, 'Theory', 'B'),
    ('CS102', 'DBMS', 'T2', 3, 3, 'Theory', 'B'),
    ('CS103', 'MC', 'T3', 3, 3, 'Theory', 'B'),
    ('CS104', 'Math', 'T4', 4, 4, 'Theory', 'B'),

    ('CS101', 'ADA', 'T1', 4, 4, 'Theory', 'C'),
    ('CS102', 'DBMS', 'T2', 3, 3, 'Theory', 'C'),
    ('CS103', 'MC', 'T3', 3, 3, 'Theory', 'C'),
    ('CS104', 'Math', 'T4', 4, 4, 'Theory', 'C'),
]

cursor.executemany("INSERT INTO subjects VALUES (?, ?, ?, ?, ?, ?, ?)", subjects_data)

# Commit and close
conn.commit()
conn.close()

print("✅ timetable.db created successfully with sample data!")
