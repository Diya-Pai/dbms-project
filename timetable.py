import sqlite3
import random
from collections import defaultdict

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
TIME_SLOTS = ["8:30-9:30", "9:30-10:30", "10:45-11:45", "11:45-12:50", "1:45-2:45", "2:45-3:45", "3:45-4:45"]

class TimetableGenerator:
    def __init__(self):
        self.conn = sqlite3.connect("timetable.db")
        self.cursor = self.conn.cursor()

        self.teachers = {}  # t_id -> {name, role, max_units, assigned}
        self.subjects = defaultdict(list)  # section -> list of (subj)
        self.teacher_timetable = defaultdict(lambda: {day: ["None"] * 7 for day in DAYS})
        self.section_timetable = defaultdict(lambda: {day: ["None"] * 7 for day in DAYS})
        self.assigned_hours = defaultdict(int)

        self.load_data()

    def load_data(self):
        for row in self.cursor.execute("SELECT * FROM teachers"):
            t_id, name, role, maxu = row
            self.teachers[t_id] = {"name": name, "role": role, "max_units": maxu, "assigned": 0}

        for row in self.cursor.execute("SELECT * FROM subjects"):
            code, sname, credit, hrs, stype, section = row
            self.subjects[section].append({
                "code": code, "name": sname, "hrs": hrs,
                "type": stype, "teacher": None
            })

    def find_available_teacher(self, hrs_needed):
        candidates = sorted(
            [(tid, data) for tid, data in self.teachers.items() if tid != "T999" and data["assigned"] + hrs_needed <= data["max_units"]],
            key=lambda x: x[1]["assigned"]
        )
        return candidates[0][0] if candidates else None

    def assign_teacher_to_subjects(self):
        for section, subs in self.subjects.items():
            for subj in subs:
                hrs = subj["hrs"]
                teacher = self.find_available_teacher(hrs)
                if teacher:
                    subj["teacher"] = teacher
                    self.teachers[teacher]["assigned"] += hrs

    def slot_available(self, timetable, day, slot):
        return timetable[day][slot] == "None"

    def assign_to_slot(self, section, teacher, day, slot, name):
        self.section_timetable[section][day][slot] = name
        self.teacher_timetable[teacher][day][slot] = name
        self.assigned_hours[(section, day, slot)] = 1

    def generate(self):
        self.assign_teacher_to_subjects()

        for section, subs in self.subjects.items():
            for subj in subs:
                hrs = subj["hrs"]
                name = f"{subj['name']} ({section})"
                teacher = subj["teacher"]

                if subj["type"] == "lab":
                    placed = False
                    for day in DAYS:
                        for i in range(len(TIME_SLOTS) - 1):
                            if all([
                                self.slot_available(self.section_timetable[section], day, i),
                                self.slot_available(self.section_timetable[section], day, i+1),
                                self.slot_available(self.teacher_timetable[teacher], day, i),
                                self.slot_available(self.teacher_timetable[teacher], day, i+1)
                            ]):
                                self.assign_to_slot(section, teacher, day, i, name)
                                self.assign_to_slot(section, teacher, day, i+1, name)
                                placed = True
                                break
                        if placed:
                            break
                else:
                    hours_placed = 0
                    for day in DAYS:
                        for i in range(len(TIME_SLOTS)):
                            if hours_placed >= hrs:
                                break
                            if self.slot_available(self.section_timetable[section], day, i) and self.slot_available(self.teacher_timetable[teacher], day, i):
                                self.assign_to_slot(section, teacher, day, i, name)
                                hours_placed += 1

    def get_section_timetable(self, section):
        return self.section_timetable[section]

    def get_teacher_timetable(self, t_id):
        return self.teacher_timetable[t_id]

    def get_teacher_workload(self):
        return {
            tid: (data["name"], data["assigned"], data["max_units"])
            for tid, data in self.teachers.items()
        }
