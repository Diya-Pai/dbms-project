import sqlite3
import random
from collections import defaultdict

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
TIME_SLOTS = [
    "8:30-9:30", "9:30-10:30", "10:45-11:45", "11:45-12:50",
    "1:45-2:45", "2:45-3:45", "3:45-4:45"
]

class TimetableGenerator:
    def __init__(self):
        self.teachers = {}
        self.subjects = []
        self.section_timetable = defaultdict(lambda: {day: [None]*7 for day in DAYS})
        self.teacher_timetable = defaultdict(lambda: {day: [None]*7 for day in DAYS})
        self.load_data()

    def load_data(self):
        conn = sqlite3.connect("timetable.db")
        c = conn.cursor()

        for row in c.execute("SELECT * FROM teachers"):
            t_id, name, role, max_units = row
            self.teachers[t_id] = {
                "name": name,
                "role": role,
                "max_units": max_units,
                "assigned_units": 0
            }

        for row in c.execute("SELECT course_code, sname, credit, hr_per_week, type, section_name FROM subjects"):
            code, sname, credit, hrs, stype, section = row
            self.subjects.append({
                "course_code": code,
                "sname": sname,
                "credit": credit,
                "hr_per_week": hrs,
                "type": stype,
                "section": section
            })

        conn.close()

    def is_available(self, ttable, tid, day, slot):
        return ttable[tid][day][slot] is None

    def assign(self, ttable, tid, day, slot, entry):
        ttable[tid][day][slot] = entry

    def generate(self):
        for subj in self.subjects:
            options = list(self.teachers.keys())
            random.shuffle(options)

            for tid in options:
                teacher = self.teachers[tid]
                if teacher['assigned_units'] + subj['hr_per_week'] <= teacher['max_units']:
                    slots_assigned = 0
                    while slots_assigned < subj['hr_per_week']:
                        day = random.choice(DAYS)
                        if subj['type'] == 'lab':
                            for i in range(len(TIME_SLOTS)-1):
                                if self.is_available(self.section_timetable, subj['section'], day, i) and \
                                   self.is_available(self.section_timetable, subj['section'], day, i+1) and \
                                   self.is_available(self.teacher_timetable, tid, day, i) and \
                                   self.is_available(self.teacher_timetable, tid, day, i+1):

                                    label = f"{subj['sname']} Lab ({subj['section']})"
                                    self.assign(self.section_timetable, subj['section'], day, i, label)
                                    self.assign(self.section_timetable, subj['section'], day, i+1, label)

                                    self.assign(self.teacher_timetable, tid, day, i, label)
                                    self.assign(self.teacher_timetable, tid, day, i+1, label)
                                    teacher['assigned_units'] += 2
                                    slots_assigned += 2
                                    break
                        else:
                            slot = random.randint(0, 6)
                            if self.is_available(self.section_timetable, subj['section'], day, slot) and \
                               self.is_available(self.teacher_timetable, tid, day, slot):

                                label = f"{subj['sname']} ({subj['section']})"
                                self.assign(self.section_timetable, subj['section'], day, slot, label)
                                self.assign(self.teacher_timetable, tid, day, slot, label)
                                teacher['assigned_units'] += 1
                                slots_assigned += 1
                    break

    def get_section_timetable(self, section):
        return self.section_timetable[section]

    def get_teacher_timetable(self, tid):
        return self.teacher_timetable[tid]

    def get_teacher_workload(self):
        return {tid: (info['name'], info['assigned_units'], info['max_units']) for tid, info in self.teachers.items()}
