import sqlite3

conn = sqlite3.connect("timetable.db")
cursor = conn.cursor()

# Drop existing tables if any
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
    credit INTEGER,
    hr_per_week INTEGER,
    type TEXT CHECK(type IN ('theory', 'lab')),
    section_name TEXT
)
""")

# Teachers data
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

# Subjects data for all sections
base_subjects = [
    ("CS301", "ADA", 3, 4, "theory"),
    ("CS302", "MC", 3, 3, "theory"),
    ("CS303", "DBMS", 3, 3, "theory"),
    ("MA301", "Math", 4, 4, "theory"),
    ("BT301", "Bio", 2, 2, "theory"),
    ("UHV01", "UHV", 0, 1, "theory"),
    ("CS301L", "ADA Lab", 1, 2, "lab"),
    ("CS302L", "MC Lab", 1, 2, "lab"),
    ("CS303L", "DBMS Lab", 1, 2, "lab"),
    ("CS304L", "UI/UX Lab", 1, 2, "lab")
]

subjects = []
for section in ["A", "B", "C"]:
    for subj in base_subjects:
        subjects.append((subj[0], subj[1], subj[2], subj[3], subj[4], section))

cursor.executemany("INSERT INTO subjects VALUES (?, ?, ?, ?, ?, ?)", subjects)

conn.commit()
conn.close()

print("✅ timetable.db created with all teachers and subjects.")
