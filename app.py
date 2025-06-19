# app.py
import streamlit as st
import pandas as pd
from timetable import TimetableGenerator, DAYS, TIME_SLOTS
from io import BytesIO
import base64
import mysql.connector

# Initialize timetable generator
gen = TimetableGenerator()

# Insert initial teacher and subject data into MySQL (if empty)
def seed_database():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="timetable_db"
    )
    cursor = conn.cursor()

    # Insert teachers if table is empty
    cursor.execute("SELECT COUNT(*) FROM teachers")
    if cursor.fetchone()[0] == 0:
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
        cursor.executemany("INSERT INTO teachers (t_id, name, role, max_units) VALUES (%s, %s, %s, %s)", teachers)

    # Insert sections
    cursor.execute("SELECT COUNT(*) FROM sections")
    if cursor.fetchone()[0] == 0:
        sections = [("A", "T1"), ("B", "T2"), ("C", "T3")]
        cursor.executemany("INSERT INTO sections (section_name, class_teacher_id) VALUES (%s, %s)", sections)

    # Insert subjects if empty
    cursor.execute("SELECT COUNT(*) FROM subjects")
    if cursor.fetchone()[0] == 0:
        subject_template = [
            ("ADA", "ADA", "T3", 3, 4, "Theory"),
            ("MC", "MC", "T4", 4, 3, "Theory"),
            ("DBMS", "DBMS", "T5", 4, 3, "Theory"),
            ("Math", "Math", "T6", 3, 4, "Theory"),
            ("Bio", "Bio", "T999", 2, 2, "Theory"),
            ("UHV", "UHV", "T7", 1, 1, "Theory"),
            ("UIUX Lab", "UI/UX Lab", "T8", 1, 1, "Lab"),
            ("ADA Lab", "ADA Lab", "T9", 1, 1, "Lab"),
            ("MC Lab", "MC Lab", "T10", 1, 1, "Lab"),
            ("DBMS Lab", "DBMS Lab", "T11", 1, 1, "Lab")
        ]
        all_subjects = []
        for sec in ["A", "B", "C"]:
            for s in subject_template:
                all_subjects.append((s[0], s[1], s[2], s[3], s[4], s[5], sec))
        cursor.executemany(
            "INSERT INTO subjects (course_code, sname, t_id, credit, hr_per_week, type, section_name) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            all_subjects
        )

    conn.commit()
    cursor.close()
    conn.close()

# Load from MySQL
def load_from_mysql():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="timetable_db"
    )
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM teachers")
    for row in cursor.fetchall():
        gen.add_faculty(row['t_id'], row['name'], row['role'])

    cursor.execute("SELECT * FROM subjects")
    for row in cursor.fetchall():
        gen.assign_subject(
            row['course_code'], row['sname'], row['type'],
            row['hr_per_week'], row['section_name'], row['t_id']
        )

    cursor.execute("SELECT section_name FROM sections")
    sections = [r['section_name'] for r in cursor.fetchall()]

    cursor.close()
    conn.close()
    return sections

def save_to_mysql(timetable_data):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="timetable_db"
    )
    cursor = conn.cursor()
    cursor.execute("DELETE FROM timetable")
    for entry in timetable_data:
        cursor.execute(
            "INSERT INTO timetable (section_name, course_code, teacher_id, day, time_slot) VALUES (%s, %s, %s, %s, %s)",
            (entry["section"], entry["subject"], entry["teacher"], entry["day"], entry["slot"])
        )
    conn.commit()
    cursor.close()
    conn.close()

def color_map(subject):
    if not subject:
        return "#2e2e2e"
    key = subject.split()[0]
    color_dict = {
        "ADA": "#EF9A9A", "MC": "#A5D6A7", "DBMS": "#90CAF9", "Math": "#CE93D8",
        "Bio": "#FFCC80", "UHV": "#80CBC4", "Lab": "#F48FB1", "UI/UX": "#FFF59D"
    }
    for k, v in color_dict.items():
        if k in key:
            return v
    return "#B0BEC5"

def display_timetable(tt, title):
    st.subheader(title)
    df_data = []
    for day in DAYS:
        row = tt[day]
        styled_row = [f"<div style='padding:4px; background-color:{color_map(cell)}; border-radius:6px'>{cell or '-'}</div>" for cell in row]
        df_data.append(styled_row)
    df = pd.DataFrame(df_data, columns=TIME_SLOTS, index=DAYS)
    st.write(df.to_html(escape=False), unsafe_allow_html=True)
    return df

def convert_df_to_excel(df, name):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=True, sheet_name='Timetable')
    output.seek(0)
    b64 = base64.b64encode(output.read()).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{name}.xlsx">📥 Download as Excel</a>'
    return href

# Seed & generate
seed_database()
sections = load_from_mysql()
gen.generate()

# Flatten timetable
timetable_data = []
for section in sections:
    tt = gen.get_section_tt(section)
    for day in DAYS:
        for i, slot in enumerate(TIME_SLOTS):
            val = tt[day][i]
            if val:
                subject, *teacher = val.split(" - ")
                timetable_data.append({
                    "section": section,
                    "subject": subject.strip(),
                    "teacher": teacher[0].strip() if teacher else "TBD",
                    "day": day,
                    "slot": slot
                })
save_to_mysql(timetable_data)

# Streamlit UI
st.set_page_config(layout="wide")
st.title("📅 Timetable Management App")

selected_section = st.selectbox("Select Section", options=sections)
view_mode = st.radio("View Mode", ["Section Timetable", "Faculty Timetable"])

if view_mode == "Section Timetable":
    tt = gen.get_section_tt(selected_section)
    df = display_timetable(tt, f"Section {selected_section}")
    st.markdown(convert_df_to_excel(df, f"Section_{selected_section}_Timetable"), unsafe_allow_html=True)

elif view_mode == "Faculty Timetable":
    teacher_names = [(tid, f.name) for tid, f in gen.faculties.items()]
    selected = st.selectbox("Select Faculty", options=teacher_names, format_func=lambda x: x[1])
    if selected:
        tid, tname = selected
        tt = gen.get_faculty_tt(tid)
        df = display_timetable(tt, f"Timetable for {tname}")
        st.markdown(convert_df_to_excel(df, f"Timetable_{tname.replace(' ', '_')}"), unsafe_allow_html=True)
