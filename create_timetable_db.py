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
teachers = [
    ("T1", "Dr Thippeswamy G", "HOD", 8),
    ("T2", "Mahesh G", "Cluster Head", 12),
    ("T3", "Dr Bharathi R", "Associate Professor", 16),
    ("T4", "Dr Nagabhushan S V", "Associate Professor", 16),
    ("T5", "Dr Ashwini N", "Associate Professor", 16),
    ("T6", "Prof Jagadish P", "Assistant Professor", 24),
    ("T7", "Dr Shankar Rajagopal", "Assistant Professor", 24),
    ("T8", "Dr Dhanalakshmi B K", "Assistant Professor", 24),
    ("T9", "Prof Shilpa M", "Assistant Professor", 24),
    ("T10", "Prof Goutami Chunumalla", "Assistant Professor", 24),
    ("T11", "Dr Mohammed Khurram", "Assistant Professor", 24),
    ("T12", "Prof S Packiya Lekshmi", "Assistant Professor", 24),
    ("T13", "Prof Arpitha Shivanna", "Assistant Professor", 24),
    ("T14", "Prof Beerappa Belasakarge", "Assistant Professor", 24),
    ("T15", "Prof Chaitanya V", "Assistant Professor", 24),
    ("T16", "Prof Aruna N", "Assistant Professor", 24),
    ("T17", "Prof Anusha K L", "Assistant Professor", 24),
    ("T999", "Dr Ramya", "Assistant Professor", 24)
]

cursor.executemany("INSERT INTO teachers VALUES (?, ?, ?, ?)", teachers)

# Insert sample subjects
subjects_data = [
    ('CS101', 'ADA', 'T1', 4, 4, 'Theory', 'A'),
    ('CS102', 'DBMS', 'T2', 3, 3, 'Theory', 'A'),
    ('CS103', 'MC', 'T3', 3, 3, 'Theory', 'A'),
    ('CS104', 'Math', 'T4', 4, 4, 'Theory', 'A'),
    ('CS105', 'ADA Lab', 'T1', 1, 2, 'Lab', 'A'),
    ('CS106', 'DBMS Lab', 'T2', 1, 2, 'Lab', 'A'),
    ('CS107', 'MC Lab', 'T3', 1, 2, 'Lab', 'A'),
    ('CS108', 'UI/UX', 'T4', 1, 2, 'Lab', 'A'),

    ('CS101', 'ADA', 'T1', 4, 4, 'Theory', 'B'),
    ('CS102', 'DBMS', 'T2', 3, 3, 'Theory', 'B'),
    ('CS103', 'MC', 'T3', 3, 3, 'Theory', 'B'),
    ('CS104', 'Math', 'T4', 4, 4, 'Theory', 'B'),
    ('CS105', 'ADA Lab', 'T1', 1, 2, 'Lab', 'b'),
    ('CS106', 'DBMS Lab', 'T2', 1, 2, 'Lab', 'B'),
    ('CS107', 'MC Lab', 'T3', 1, 2, 'Lab', 'B'),
    ('CS108', 'UI/UX', 'T4', 1, 2, 'Lab', 'B'),

    ('CS101', 'ADA', 'T1', 4, 4, 'Theory', 'C'),
    ('CS102', 'DBMS', 'T2', 3, 3, 'Theory', 'C'),
    ('CS103', 'MC', 'T3', 3, 3, 'Theory', 'C'),
    ('CS104', 'Math', 'T4', 4, 4, 'Theory', 'C'),
    ('CS105', 'ADA Lab', 'T1', 1, 2, 'Lab', 'C'),
    ('CS106', 'DBMS Lab', 'T2', 1, 2, 'Lab', 'C'),
    ('CS107', 'MC Lab', 'T3', 1, 2, 'Lab', 'C'),
    ('CS108', 'UI/UX', 'T4', 1, 2, 'Lab', 'C'),
]

cursor.executemany("INSERT INTO subjects VALUES (?, ?, ?, ?, ?, ?, ?)", subjects_data)

# Commit and close
conn.commit()
conn.close()

print("✅ timetable.db created successfully with sample data!")
