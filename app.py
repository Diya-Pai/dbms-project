# app.py
import streamlit as st
from timetable import TimetableGenerator

# Initialize timetable generator
gen = TimetableGenerator()

# Sample faculties
gen.add_faculty("T1", "Dr. A", "HOD")
gen.add_faculty("T2", "Dr. B", "Cluster Head")
gen.add_faculty("T3", "Dr. C", "Associate Professor")
gen.add_faculty("T4", "Dr. D", "Assistant Professor")

# Assigning subjects
gen.assign_subject("CS101", "DSA", "Theory", 3, "A", "T1")
gen.assign_subject("CS101", "DSA", "Theory", 3, "B", "T1")
gen.assign_subject("CS102", "OS", "Theory", 3, "A", "T2")
gen.assign_subject("CS103", "DBMS", "Theory", 3, "C", "T3")
gen.assign_subject("CS104", "CN Lab", "Lab", 2, "A", "T4")

# Generate timetable
gen.generate()

st.title("📅 Timetable Management App")

menu = st.sidebar.selectbox("View Timetable", ["Section", "Faculty"])

if menu == "Section":
    section = st.selectbox("Select Section", ["A", "B", "C"])
    st.subheader(f"Timetable for Section {section}")
    tt = gen.get_section_tt(section)
    for day in tt:
        st.markdown(f"**{day}**")
        row = tt[day]
        st.table({slot: val if val else "-" for slot, val in zip(range(1, 7), row)})

elif menu == "Faculty":
    faculty_id = st.selectbox("Select Faculty", list(gen.faculties.keys()))
    faculty = gen.faculties[faculty_id]
    st.subheader(f"Timetable for {faculty.name} ({faculty.role})")
    tt = gen.get_faculty_tt(faculty_id)
    for day in tt:
        st.markdown(f"**{day}**")
        row = tt[day]
        st.table({slot: val if val else "-" for slot, val in zip(range(1, 7), row)})
