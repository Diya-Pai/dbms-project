import sqlite3

conn = sqlite3.connect("timetable.db")
cursor = conn.cursor()

# Drop existing tables
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

# 👩‍🏫 All Teachers (added more to balance the load)
teachers = [
    ("T1", "Dr Ashwini N", "Assistant Professor", 18),
    ("T2", "Prof Shilpa M", "Assistant Professor", 18),
    ("T3", "Prof Chaitanya V", "Assistant Professor", 18),
    ("T4", "Dr Nagabhushan S V", "Assistant Professor", 18),
    ("T5", "Dr Dhanalakshmi B K", "Associate Professor", 18),
    ("T6", "Prof Goutami Chunumalla", "Assistant Professor", 18),
    ("T7", "Dr Ramya M R", "Associate Professor", 12),
    ("T8", "Prof Sandeep M", "Assistant Professor", 18),
    ("T9", "Dr Shruti A", "Assistant Professor", 18),
    ("T10", "Prof Beerappa Belasakarge", "Assistant Professor", 18),
    ("T11", "Dr Yogish H K", "Professor", 18),
    ("T12", "Prof Keerthi Kulkarni", "Assistant Professor", 18),
    ("T13", "Prof Sneha Patil", "Assistant Professor", 18),
    ("T14", "Prof Deepa R", "Assistant Professor", 18),
]

cursor.executemany("INSERT INTO teachers VALUES (?, ?, ?, ?)", teachers)

# 📚 Subjects repeated per section
subjects = []
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

for section in ["A", "B", "C"]:
    for subj in base_subjects:
        subjects.append((subj[0], subj[1], subj[2], subj[3], subj[4], section))

cursor.executemany("INSERT INTO subjects VALUES (?, ?, ?, ?, ?, ?)", subjects)

conn.commit()
conn.close()

print("✅ timetable.db created with all teachers and subjects.")
