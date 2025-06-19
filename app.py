import streamlit as st
import pandas as pd
from timetable import TimetableGenerator, DAYS, TIME_SLOTS

# Initialize and generate timetable
gen = TimetableGenerator()
gen.generate(balance_workload=True)

st.title("📅 Timetable Management App")

# Section selection
sections = ["A", "B", "C"]
selected_section = st.selectbox("Choose Section:", sections)

section_tt = gen.get_section_timetable(selected_section)

st.markdown(f"### 📘 Timetable for Section {selected_section}")

df_section = pd.DataFrame(section_tt).T
df_section.columns = TIME_SLOTS
st.dataframe(df_section, use_container_width=True)

st.divider()

# Teacher selection
teacher_options = [(tid, f"{tid} - {info['name']}") for tid, info in gen.teachers.items()]
selected_teacher_id = st.selectbox("Choose Teacher:", [t[1] for t in teacher_options])
selected_teacher_id = selected_teacher_id.split(" - ")[0]

st.markdown(f"### 🧑‍🏫 Timetable for {selected_teacher_id} - {gen.teachers[selected_teacher_id]['name']}")

teacher_tt = gen.get_teacher_timetable(selected_teacher_id)
df_teacher = pd.DataFrame(teacher_tt).T
df_teacher.columns = TIME_SLOTS
st.dataframe(df_teacher, use_container_width=True)

# Weekly workload
workload = sum(slot is not None for day in teacher_tt.values() for slot in day)
st.markdown(f"#### 💼 Weekly Workload: `{workload}` hours")
