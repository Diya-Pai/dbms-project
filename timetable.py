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
        self.lab_assigned = {}  # Track labs already assigned per section

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
        self.teachers[t_id]["units_assigned"] += 2 if "Lab" in subject else 1

    def generate(self, force_fill_days=False):
        self.fetch_data()
        self.timetable = {sec: {day: ["" for _ in TIME_SLOTS] for day in DAYS} for sec in self.sections}
        self.lab_assigned = {sec: set() for sec in self.sections}

        for section in self.sections:
            for course_code, sname, t_id, credit, hr_per_week, sub_type, section_name in self.subjects:
                if section_name.upper() != section:
                    continue  # Only process subjects for this section

                teacher = self.teachers[t_id]
                hours_assigned = 0
                attempts = 0

                # --- If this is a lab and already assigned for this section, skip completely ---
                if sub_type == "Lab":
                    lab_key = f"{sname}_{section}"
                    if lab_key in self.lab_assigned[section]:
                        continue  # Already assigned this lab once for this section

                while hours_assigned < hr_per_week and attempts < 1000:
                    # Sort teachers by current load — helps balance teacher hours
                    available_teachers = sorted(self.teachers.items(), key=lambda item: item[1]['units_assigned'])
                    t_id = available_teachers[0][0]  # Pick the teacher with fewest units
                    teacher = self.teachers[t_id]

                    day = random.choice(DAYS)
                    slot = random.randint(0, len(TIME_SLOTS) - (2 if sub_type == "Lab" else 1))
                    units_to_assign = 2 if "Lab" in sub_type else 1

                    if teacher["units_assigned"] + units_to_assign > teacher["max_units"]:
                        attempts += 1
                        continue

                    if sub_type == "Lab":
                        if slot > len(TIME_SLOTS) - 2:
                            attempts += 1
                            continue
                        if self.timetable[section][day][slot] == "" and self.timetable[section][day][slot+1] == "" \
                           and self.is_teacher_available(t_id, day, slot) and self.is_teacher_available(t_id, day, slot+1):
                            self.timetable[section][day][slot] = f"{sname} ({teacher['name']})"
                            self.timetable[section][day][slot+1] = f"{sname} ({teacher['name']})"
                            self.assign_teacher(t_id, day, slot, sname, section)
                            self.assign_teacher(t_id, day, slot+1, sname, section)
                            hours_assigned += 2
                            self.lab_assigned[section].add(lab_key)  # Mark this lab as assigned for this section
                            break  # Lab done — no more assignments for this lab+section
                    else:
                        if self.timetable[section][day][slot] == "" and self.is_teacher_available(t_id, day, slot):
                            self.timetable[section][day][slot] = f"{sname} ({teacher['name']})"
                            self.assign_teacher(t_id, day, slot, sname, section)
                            hours_assigned += 1

                    attempts += 1

    def get_section_timetable(self, section):
        return self.timetable.get(section, {})

    def get_teacher_timetable(self, teacher_id):
        return self.teachers[teacher_id]['schedule'] if teacher_id in self.teachers else {}
