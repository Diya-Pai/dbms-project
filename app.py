import streamlit as st
import pandas as pd
from timetable import TimetableGenerator, DAYS, TIME_SLOTS

# Initialize generator
gen = TimetableGenerator()
gen.generate()

st.title("📘 Timetable Management App")

view_choice = st.radio("Select View:", ["Section Timetable", "Teacher Timetable"])

if view_choice == "Section Timetable":
    section = st.selectbox("Select Section:", ["A", "B", "C"])
    timetable = gen.get_section_timetable(section)
else:
    teacher_names = {tid: info['name'] for tid, info in gen.teachers.items()}
    tid = st.selectbox("Select Teacher:", list(teacher_names.keys()), format_func=lambda x: teacher_names[x])
    timetable = gen.get_teacher_timetable(tid)

# Display timetable as styled dataframe
df = pd.DataFrame.from_dict(timetable, orient='index', columns=TIME_SLOTS)

styled_df = df.style.applymap(
    lambda val: f'background-color: {gen.get_color(val)}' if val else ''
)

st.dataframe(styled_df, use_container_width=True)

# Show workload chart
if view_choice == "Teacher Timetable":
    st.subheader("📊 Weekly Workload")
    workload = gen.get_teacher_workload()
    data = pd.DataFrame([
        {"Teacher": name, "Assigned Units": assigned, "Max Units": max_u}
        for _, (name, assigned, max_u) in workload.items()
    ])
    selected = data[data["Teacher"] == teacher_names[tid]]
    st.bar_chart(selected.set_index("Teacher"))
