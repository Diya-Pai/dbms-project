# app.py
import streamlit as st
import pandas as pd
from timetable import TimetableGenerator, DAYS, TIME_SLOTS
from io import BytesIO
import base64

# Initialize timetable generator
gen = TimetableGenerator()

# Sample subjects and labs with weekly frequencies
theory_subjects = [
    ("ADA", 4), ("MC", 3), ("DBMS", 3), ("Math", 4), ("Bio", 2), ("UHV", 1)
]
labs = ["ADA Lab", "UI/UX Lab", "MC Lab", "DBMS Lab"]
sections = ["A", "B", "C"]

# Add Dr Ramya manually if not present
if "T999" not in gen.faculties:
    gen.add_faculty("T999", "Dr Ramya", "Assistant Professor")

# Assign subjects
import random
all_teachers = list(gen.faculties.keys())

for section in sections:
    for sname, freq in theory_subjects:
        if sname == "Bio":
            tid = "T999"
        else:
            tid = random.choice(all_teachers)
        gen.assign_subject(sname, sname, "Theory", freq, section, tid)
    for lname in labs:
        tid = random.choice(all_teachers)
        gen.assign_subject(lname, lname, "Lab", 1, section, tid)

# Generate the timetable
gen.generate()

st.set_page_config(layout="wide")
st.title("📅 Timetable Management App")

selected_section = st.selectbox("Select Section", options=sections)
view_mode = st.radio("View Mode", ["Section Timetable", "Faculty Timetable"])

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

def color_map(subject):
    if not subject:
        return "#f0f0f0"
    key = subject.split()[0]
    color_dict = {
        "ADA": "#F44336", "MC": "#4CAF50", "DBMS": "#2196F3", "Math": "#9C27B0",
        "Bio": "#FF9800", "UHV": "#009688", "Lab": "#E91E63", "UI/UX": "#FFEB3B"
    }
    for k, v in color_dict.items():
        if k in key:
            return v
    return "#E0E0E0"

def convert_df_to_excel(df, name):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=True, sheet_name='Timetable')
    output.seek(0)
    b64 = base64.b64encode(output.read()).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{name}.xlsx">📥 Download as Excel</a>'
    return href

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
