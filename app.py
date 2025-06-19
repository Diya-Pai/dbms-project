# app.py
import streamlit as st
import pandas as pd
from timetable import TimetableGenerator, DAYS, TIME_SLOTS
from io import BytesIO
import base64
from fpdf import FPDF
import tempfile

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
    daily_track = {day: 0 for day in DAYS}
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
gen.generate(force_fill_days=True)

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

def convert_df_to_excel(df, name):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=True, sheet_name='Timetable')
    output.seek(0)
    b64 = base64.b64encode(output.read()).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{name}.xlsx">📥 Download as Excel</a>'
    return href

def convert_df_to_pdf(df, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    col_width = 30
    row_height = 10

    pdf.cell(200, 10, txt=filename, ln=True, align='C')
    pdf.ln(5)

    pdf.set_fill_color(220, 220, 220)
    pdf.set_text_color(0)
    pdf.set_font("Arial", 'B', size=9)
    pdf.cell(30, row_height, "", border=1)
    for col in df.columns:
        pdf.cell(col_width, row_height, col, border=1)
    pdf.ln(row_height)

    pdf.set_font("Arial", size=8)
    for idx, row in df.iterrows():
        pdf.cell(30, row_height, idx, border=1)
        for item in row:
            clean_text = str(item).replace('<div style=', '').split('>')[-1].replace('</div>', '')
            pdf.cell(col_width, row_height, clean_text, border=1)
        pdf.ln(row_height)

    tmpfile = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(tmpfile.name)
    with open(tmpfile.name, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    href = f'<a href="data:application/pdf;base64,{b64}" download="{filename}.pdf">📄 Download as PDF</a>'
    return href

if view_mode == "Section Timetable":
    tt = gen.get_section_tt(selected_section)
    df = display_timetable(tt, f"Section {selected_section}")
    st.markdown(convert_df_to_excel(df, f"Section_{selected_section}_Timetable"), unsafe_allow_html=True)
    st.markdown(convert_df_to_pdf(df, f"Section_{selected_section}_Timetable"), unsafe_allow_html=True)

elif view_mode == "Faculty Timetable":
    teacher_names = [(tid, f.name) for tid, f in gen.faculties.items()]
    selected = st.selectbox("Select Faculty", options=teacher_names, format_func=lambda x: x[1])
    if selected:
        tid, tname = selected
        tt = gen.get_faculty_tt(tid)
        df = display_timetable(tt, f"Timetable for {tname}")
        st.markdown(convert_df_to_excel(df, f"Timetable_{tname.replace(' ', '_')}"), unsafe_allow_html=True)
        st.markdown(convert_df_to_pdf(df, f"Timetable_{tname.replace(' ', '_')}"), unsafe_allow_html=True)
