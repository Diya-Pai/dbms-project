# timetable.py
import random
from collections import defaultdict

# Constants
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
TIME_SLOTS = ["9-10", "10-11", "11-12", "12-1", "2-3", "3-4"]

# Role-based max units per week
ROLE_UNITS = {
    "HOD": 8,
    "Cluster Head": 12,
    "Associate Professor": 16,
    "Assistant Professor": 24
}

UNIT_VALUE = {
    "Theory": 2,
    "Lab": 2
}

class Faculty:
    def __init__(self, tid, name, role):
        self.tid = tid
        self.name = name
        self.role = role
        self.max_units = ROLE_UNITS[role]
        self.subjects = []
        self.schedule = defaultdict(lambda: [None]*len(TIME_SLOTS))
        self.units_allocated = 0

    def can_teach(self, units):
        return self.units_allocated + units <= self.max_units

class Subject:
    def __init__(self, code, name, type, hrs_per_week, section):
        self.code = code
        self.name = name
        self.type = type
        self.hrs_per_week = hrs_per_week
        self.section = section

class TimetableGenerator:
    def __init__(self):
        self.faculties = {}
        self.subjects = []
        self.sections = {"A": {}, "B": {}, "C": {}}
        self.generated_tt = defaultdict(lambda: defaultdict(lambda: [None]*len(TIME_SLOTS)))

    def add_faculty(self, tid, name, role):
        self.faculties[tid] = Faculty(tid, name, role)

    def assign_subject(self, code, name, type, hrs_per_week, section, teacher_id):
        subject = Subject(code, name, type, hrs_per_week, section)
        self.subjects.append(subject)
        self.faculties[teacher_id].subjects.append(subject)

    def generate(self):
        for subject in self.subjects:
            tid = self.get_teacher_for_subject(subject)
            faculty = self.faculties[tid]
            units = UNIT_VALUE[subject.type] * subject.hrs_per_week
            count = subject.hrs_per_week
            for day in DAYS:
                for i, slot in enumerate(TIME_SLOTS):
                    if count <= 0:
                        break
                    if self.generated_tt[subject.section][day][i] is None:
                        if faculty.schedule[day][i] is None and self.can_schedule(faculty, day, i, subject.type):
                            self.generated_tt[subject.section][day][i] = (subject.name, faculty.name)
                            faculty.schedule[day][i] = subject.name
                            faculty.units_allocated += UNIT_VALUE[subject.type]
                            count -= 1

    def get_teacher_for_subject(self, subject):
        for tid, faculty in self.faculties.items():
            if subject in faculty.subjects:
                return tid
        return None

    def can_schedule(self, faculty, day, i, type):
        if type == "Theory":
            if i > 0 and faculty.schedule[day][i-1] is not None:
                return False
            if i < len(TIME_SLOTS)-1 and faculty.schedule[day][i+1] is not None:
                return False
        return True

    def get_section_tt(self, section):
        return self.generated_tt[section]

    def get_faculty_tt(self, tid):
        return self.faculties[tid].schedule
