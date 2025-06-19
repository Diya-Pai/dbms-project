# app.py
import streamlit as st
from timetable import TimetableGenerator, DAYS, TIME_SLOTS

# Initialize timetable generator
gen = TimetableGenerator()

# Add faculty pool
gen.add_faculty("T1", "Dr. Ada", "HOD")
gen.add_faculty("T2", "Dr. Bob", "Cluster Head")
gen.add_faculty("T3", "Dr. Charlie", "Associate Professor")
gen.add_faculty("T4", "Dr. Dana", "Assistant Professor")
gen.add_faculty("T5", "Dr. Eva", "Assistant Professor")
gen.add_faculty("T6", "Dr. Frank", "Assistant Professor")

# Subjects and labs to be randomly assigned to teachers
theory_subjects = [
    ("ADA", 4),
    ("MC", 3),
    ("DBMS", 3),
    ("Math", 4),
    ("Bio", 2),
    ("UHV", 1)
]

labs = [
    ("ADA Lab",),
    ("UI/UX Lab",),
    ("MC Lab",),
    ("DBMS Lab",)
]

import random
sections = ["A", "B", "C"]
all_teachers = list(gen.faculties.keys())

# Assign theory subjects randomly
for section in sections:
    for sname, freq in theory_subjects:
        tid = random.choice(all_teachers)
        gen.assign_subject(sname, sname, "Theory", freq, section, tid)

# Assign labs randomly
for section in sections:
    for lname_tuple in labs:
        lname = lname_tuple[0]
        tid = random.choice(all_teachers)
        gen.assign_subject(lname, lname, "Lab", 1, section, tid)

# Generate timetable
gen.generate()

st.title("📅 Timetable Management App")

menu = st.sidebar.selectbox("View Timetable", ["All Sections", "All Faculty"])

if menu == "All Sections":
    for section in sections:
        st.subheader(f"📘 Timetable for Section {section}")
        tt = gen.get_section_tt(section)
        for day in DAYS:
            st.markdown(f"**{day}**")
            slots = tt[day]
            st.table({slot: val if val else "-" for slot, val in zip(TIME_SLOTS, slots)})

elif menu == "All Faculty":
    for faculty_id, faculty in gen.faculties.items():
        st.subheader(f"👨‍🏫 Timetable for {faculty.name} ({faculty.role})")
        tt = gen.get_faculty_tt(faculty_id)
        for day in DAYS:
            st.markdown(f"**{day}**")
            slots = tt[day]
            st.table({slot: val if val else "-" for slot, val in zip(TIME_SLOTS, slots)})
