import streamlit as st
import pandas as pd
from timetable import TimetableGenerator, DAYS, TIME_SLOTS

st.title("📘 Timetable Management App")

# Initialize generator
if 'gen' not in st.session_state:
    st.session_state.gen = TimetableGenerator()
    st.session_state.gen.generate()

gen = st.session_state.gen

view_choice = st.radio("Select View:", ["Section Timetable", "Teacher Timetable"])

if view_choice == "Section Timetable":
    section = st.selectbox("Select Section:", ["A", "B", "C"])
    timetable = gen.get_section_timetable(section)
    df = pd.DataFrame.from_dict(timetable, orient='index', columns=TIME_SLOTS)
    styled_df = df.style.applymap(lambda val: f'background-color: {gen.get_color(val)}' if val else '')
    st.dataframe(styled_df, use_container_width=True)

elif view_choice == "Teacher Timetable":
    teacher_names = {tid: info['name'] for tid, info in gen.teachers.items()}
    tid = st.selectbox("Select Teacher:", list(teacher_names.keys()), format_func=lambda x: teacher_names[x])
    timetable = gen.get_teacher_timetable(tid)
    df = pd.DataFrame.from_dict(timetable, orient='index', columns=TIME_SLOTS)
    styled_df = df.style.applymap(lambda val: f'background-color: {gen.get_color(val)}' if val else '')
    st.dataframe(styled_df, use_container_width=True)

    st.subheader("📊 Weekly Workload")
    workload = gen.get_teacher_workload()
    data = pd.DataFrame([
        {"Teacher": name, "Assigned Units": assigned, "Max Units": max_u}
        for _, (name, assigned, max_u) in workload.items()
    ])
    selected = data[data["Teacher"] == teacher_names[tid]]
    if not selected.empty:
        st.bar_chart(selected.set_index("Teacher")[["Assigned Units", "Max Units"]])
    else:
        st.info("No workload data available.")
