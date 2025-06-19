import streamlit as st
import pandas as pd
from timetable import TimetableGenerator, DAYS, TIME_SLOTS

st.set_page_config(page_title="Timetable Management App", layout="centered")
st.title("🗓️ Timetable Management App")

gen = TimetableGenerator()
gen.generate()

# Section Timetable Viewer
st.subheader("📘 Timetable for Section")
section = st.selectbox("Choose Section:", ["A", "B", "C"])
timetable = gen.get_section_timetable(section)

df = pd.DataFrame(index=DAYS, columns=TIME_SLOTS)
for day in DAYS:
    df.loc[day] = timetable[day]
st.dataframe(df.style.set_properties(**{'text-align': 'center'}), use_container_width=True)

# Teacher Timetable Viewer
st.subheader("👩‍🏫 Timetable for Teacher")
teacher_ids = list(gen.teachers.keys())
selected_tid = st.selectbox("Choose Teacher ID:", teacher_ids)
teacher_table = gen.get_teacher_timetable(selected_tid)

df_teacher = pd.DataFrame(index=DAYS, columns=TIME_SLOTS)
for day in DAYS:
    df_teacher.loc[day] = teacher_table[day]
st.dataframe(df_teacher.style.set_properties(**{'text-align': 'center'}), use_container_width=True)

# Workload Summary
st.subheader("📊 Teacher Workload Summary")
workload = gen.get_teacher_workload()
df_workload = pd.DataFrame([
    {"Teacher ID": tid, "Name": name, "Assigned Units": assigned, "Max Units": max_u}
    for tid, (name, assigned, max_u) in workload.items()
])
st.dataframe(df_workload, use_container_width=True)
