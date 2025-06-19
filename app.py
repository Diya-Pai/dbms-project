# app.py
import streamlit as st
import pandas as pd
from timetable import TimetableGenerator, DAYS, TIME_SLOTS
import sqlite3

# Initialize timetable generator with constraints
gen = TimetableGenerator()
gen.generate(balance_workload=True, avoid_back_to_back=True, allow_subject_split=True)

# Load teachers list for selection
conn = sqlite3.connect("timetable.db")
cursor = conn.cursor()
cursor.execute("SELECT t_id, name FROM teachers")
teachers_list = cursor.fetchall()
conn.close()

st.set_page_config(page_title="Timetable Management App", layout="wide")
st.title("📅 Timetable Management App")

# Sidebar view selector
view_option = st.sidebar.radio("Select View:", ("Section Timetable", "Teacher Timetable", "Weekly Workload Chart"))

if view_option == "Section Timetable":
    section = st.selectbox("Choose Section:", ["A", "B", "C"])
    timetable = gen.get_section_timetable(section)
    st.subheader(f"📘 Timetable for Section {section}")

    df = pd.DataFrame(timetable).T
    df.columns = TIME_SLOTS
    st.dataframe(df.style.applymap(lambda x: "background-color: lightpink" if "ADA" in str(x) else
                                             "background-color: lightblue" if "DBMS" in str(x) else
                                             "background-color: lightgreen" if "MC" in str(x) else
                                             "background-color: plum" if "Math" in str(x) else
                                             "background-color: lemonchiffon" if "UI/UX" in str(x) else
                                             "background-color: moccasin" if "Bio" in str(x) else
                                             "background-color: palegreen" if "UHV" in str(x) else ""))

elif view_option == "Teacher Timetable":
    teacher_choice = st.selectbox("Choose Teacher:", [f"{tid} - {name}" for tid, name in teachers_list])
    teacher_id = teacher_choice.split(" - ")[0]
    teacher_schedule = gen.get_teacher_timetable(teacher_id)
    st.subheader(f"👩‍🏫 Timetable for {teacher_choice}")

    df = pd.DataFrame(teacher_schedule).T
    df.columns = TIME_SLOTS
    st.dataframe(df.style.applymap(lambda x: "background-color: lightcoral" if x else ""))

elif view_option == "Weekly Workload Chart":
    teacher_chart_choice = st.selectbox("Select a teacher to view workload chart:", [f"{tid} - {name}" for tid, name in teachers_list])
    teacher_id = teacher_chart_choice.split(" - ")[0]
    teacher_data = gen.teachers[teacher_id]

    schedule = teacher_data['schedule']
    workload_by_day = {day: sum(1 for x in schedule[day] if x) for day in DAYS}

    df = pd.DataFrame({"Day": list(workload_by_day.keys()), "Sessions": list(workload_by_day.values())})
    st.subheader(f"📊 Weekly Workload for {teacher_chart_choice}")
    st.bar_chart(df.set_index("Day"))
