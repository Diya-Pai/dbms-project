# timetable.py
import sqlite3
import random
from collections import defaultdict

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
TIME_SLOTS = ["8:30-9:30", "9:30-10:30", "10:45-11:45", "11:45-12:50", "1:45-2:45", "2:45-3:45", "3:45-4:45"]

class TimetableGenerator:
    def __init__(self):
        self.sections = ["A", "B", "C"]
        self.subjects = []
        self.teachers = {}
        self.section_timetables = {sec: {day: [None]*7 for day in DAYS} for sec in self.sections}
        self.load_data()

    def load_data(self):
        conn = sqlite3.connect("timetable.db")
        cursor = conn.cursor()

        cursor.execute("SELECT t_id, name, role, max_units FROM teachers")
        for tid, name, role, max_units in cursor.fetchall():
            self.teachers[tid] = {
                'name': name,
                'max_units': max_units,
                'assigned_units': 0,
                'schedule': {day: [None]*7 for day in DAYS}
            }

        cursor.execute("SELECT course_code, sname, credit, hr_per_week, type, section_name FROM subjects")
        self.subjects = cursor.fetchall()

        conn.close()

   def can_assign(self, teacher_id, day, slot, is_lab):
    teacher = self.teachers[teacher_id]
    schedule = teacher['schedule'][day]

    if schedule[slot] is not None:
        return False
    if is_lab and (slot >= len(TIME_SLOTS) - 1 or schedule[slot + 1]):
        return False

    # avoid isolated slots
    neighbors = []
    if slot > 0:
        neighbors.append(schedule[slot - 1])
    if slot < len(TIME_SLOTS) - 1:
        neighbors.append(schedule[slot + 1])
    if all(n is None for n in neighbors):
        return False  # don't allow lonely slot unless necessary

    return True


    def assign_class(self, section, subject, teacher_id, sessions_needed):
        is_lab = subject[4] == "lab"
        for i in range(sessions_needed):
            valid_slots = [(day, slot) for day in DAYS for slot in range(len(TIME_SLOTS) - (1 if is_lab else 0))]
            random.shuffle(valid_slots)
            for day, slot in valid_slots:
                if self.section_timetables[section][day][slot] is None and \
                   (not is_lab or self.section_timetables[section][day][slot + 1] is None) and \
                   self.can_assign(teacher_id, day, slot, is_lab):

                    label = f"{subject[1]} ({self.teachers[teacher_id]['name']})"
                    self.section_timetables[section][day][slot] = label
                    self.teachers[teacher_id]['schedule'][day][slot] = f"{subject[1]} ({section})"
                    if is_lab:
                        self.section_timetables[section][day][slot + 1] = label
                        self.teachers[teacher_id]['schedule'][day][slot + 1] = f"{subject[1]} ({section})"
                    self.teachers[teacher_id]['assigned_units'] += (2 if is_lab else 1)
                    break

    def generate(self, balance_workload=False, avoid_back_to_back=False, allow_subject_split=False):
        random.shuffle(self.subjects)
        subject_groups = defaultdict(list)
        for s in self.subjects:
            subject_groups[s[1]].append(s)

        teacher_pool = list(self.teachers.keys())
        ti = 0
        for subj_list in subject_groups.values():
            for subject in subj_list:
                assigned = False
                retries = 0
                while not assigned and retries < len(teacher_pool):
                    teacher_id = teacher_pool[ti % len(teacher_pool)]
                    teacher = self.teachers[teacher_id]
                    needed_units = (2 if subject[4] == 'lab' else 1) * subject[3]
                    if teacher['assigned_units'] + needed_units <= teacher['max_units']:
                        self.assign_class(subject[5], subject, teacher_id, subject[3])
                        assigned = True
                    ti += 1
                    retries += 1

    def get_section_timetable(self, section):
        return self.section_timetables[section]

    def get_teacher_timetable(self, teacher_id):
        return self.teachers[teacher_id]['schedule']
