# timetable.py
import sqlite3
import random

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
TIME_SLOTS = [
    "8:30-9:30", "9:30-10:30", "10:45-11:45", "11:45-12:50", "1:45-2:45", "2:45-3:45", "3:45-4:45"
]

class TimetableGenerator:
    def __init__(self):
        self.conn = sqlite3.connect("timetable.db")
        self.cursor = self.conn.cursor()
        self.sections = ["A", "B", "C"]
        self.teachers = {}
        self.subjects = []
        self.timetable = {}

    def fetch_data(self):
        self.cursor.execute("SELECT * FROM teachers")
        for t_id, name, role, max_units in self.cursor.fetchall():
            self.teachers[t_id] = {
                "name": name,
                "role": role,
                "max_units": max_units,
                "units_assigned": 0,
                "schedule": {day: [None]*len(TIME_SLOTS) for day in DAYS}
            }

        self.cursor.execute("SELECT * FROM subjects")
        self.subjects = self.cursor.fetchall()

    def is_teacher_available(self, t_id, day, slot):
        return self.teachers[t_id]["schedule"][day][slot] is None

    def assign_teacher(self, t_id, day, slot, subject, section):
        self.teachers[t_id]["schedule"][day][slot] = f"{subject} ({section})"
        self.teachers[t_id]["units_assigned"] += 2 if "Lab" in subject else 2

    def generate(self, balance_workload=False):
        self.fetch_data()
        self.timetable = {sec: {day: ["" for _ in TIME_SLOTS] for day in DAYS} for sec in self.sections}

        subjects_sorted = self.subjects
        if balance_workload:
            subjects_sorted = sorted(self.subjects, key=lambda s: self.teachers[s[2]]['units_assigned'])

        for course_code, sname, t_id, credit, hr_per_week, sub_type, section_name in subjects_sorted:
            hours_assigned = 0
            attempts = 0
            while hours_assigned < hr_per_week and attempts < 300:
                day = random.choice(DAYS)
                slot = random.randint(0, len(TIME_SLOTS) - (2 if sub_type == "Lab" else 1))

                if sub_type == "Lab":
                    if slot > len(TIME_SLOTS) - 2:
                        attempts += 1
                        continue
                    if self.timetable[section_name][day][slot] == "" and self.timetable[section_name][day][slot+1] == "" and \
                       self.is_teacher_available(t_id, day, slot) and self.is_teacher_available(t_id, day, slot+1):
                        self.timetable[section_name][day][slot] = f"{sname} ({self.teachers[t_id]['name']})"
                        self.timetable[section_name][day][slot+1] = f"{sname} ({self.teachers[t_id]['name']})"
                        self.assign_teacher(t_id, day, slot, sname, section_name)
                        self.assign_teacher(t_id, day, slot+1, sname, section_name)
                        hours_assigned += 1
                else:
                    if self.timetable[section_name][day][slot] == "" and self.is_teacher_available(t_id, day, slot):
                        self.timetable[section_name][day][slot] = f"{sname} ({self.teachers[t_id]['name']})"
                        self.assign_teacher(t_id, day, slot, sname, section_name)
                        hours_assigned += 1
                attempts += 1

    def get_section_timetable(self, section):
        return self.timetable.get(section, {})

    def get_teacher_timetable(self, teacher_id):
        return self.teachers[teacher_id]['schedule'] if teacher_id in self.teachers else {}
