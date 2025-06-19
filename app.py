import streamlit as st
import pandas as pd
from timetable import TimetableGenerator, DAYS, TIME_SLOTS

# Initialize and generate timetable
gen = TimetableGenerator()
gen.generate()

st.title("📘 Timetable Management App")

view_option = st.selectbox("Select View", ["Section Timetable", "Teacher Timetable", "Teacher Workload Chart"])

if view_option == "Section Timetable":
    section = st.selectbox("Select Section", ["A", "B", "C"])
    timetable = gen.get_section_timetable(section)

    st.subheader(f"🗓️ Timetable for Section {section}")
    df = pd.DataFrame({day: timetable[day] for day in DAYS}, index=TIME_SLOTS).T
    st.dataframe(df.style.set_properties(**{'text-align': 'center'}))

elif view_option == "Teacher Timetable":
    teacher_map = {tid: data['name'] for tid, data in gen.teachers.items()}
    selected_tid = st.selectbox("Select Teacher", list(teacher_map.keys()), format_func=lambda x: teacher_map[x])

    ttable = gen.get_teacher_timetable(selected_tid)
    st.subheader(f"📚 Timetable for {teacher_map[selected_tid]}")
    df = pd.DataFrame({day: ttable[day] for day in DAYS}, index=TIME_SLOTS).T
    st.dataframe(df.style.set_properties(**{'text-align': 'center'}))

elif view_option == "Teacher Workload Chart":
    workload = gen.get_teacher_workload()
    df = pd.DataFrame([(name, assigned, maxu) for _, (name, assigned, maxu) in workload.items()],
                      columns=["Name", "Assigned Units", "Max Units"])
    df["% Used"] = (df["Assigned Units"] / df["Max Units"] * 100).round(1)

    teacher_name = st.selectbox("Toggle Teacher", df["Name"].tolist())
    tdata = df[df["Name"] == teacher_name].iloc[0]

    st.metric("Assigned Units", tdata["Assigned Units"])
    st.metric("Max Units", tdata["Max Units"])
    st.progress(min(1.0, tdata["% Used"] / 100))
