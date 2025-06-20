# dbms-project
This is a DBMS-based Timetable Management System built with Python, SQLite, and Streamlit. It automatically generates weekly timetables for multiple sections based on teacher workload, subject hours, and lab constraints.


Features
Auto-generates timetables based on subject requirements and teacher limits
Separate views for section-wise and teacher-wise timetables
Weekly workload chart for each teacher
Uses SQLite as the backend database
User-friendly interface built with Streamlit

Project Structure
├── app.py                    # Streamlit web app
├── timetable.py             # Core timetable generation logic
├── create_timetable_db.py   # Script to create & populate the SQLite DB
├── timetable.db             # (Auto-generated) SQLite database
└── README.md

How It Works
Subjects are assigned based on hr_per_week and teacher availability.
Labs require 2 consecutive slots and consume 4 units (1 hour = 2 units).
Teachers have a max_units limit per week.
The generator tries random valid placements within constraints and prints alerts if subjects can’t be fully scheduled.
