# timetable.py
import random
from collections import defaultdict

# Constants
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
TIME_SLOTS = [
    "8:30-9:30", "9:30-10:30", "10:45-11:45", "11:45-12:50",
    "1:45-2:45", "2:45-3:45", "3:45-4:45"
]  # Skipping short break and lunch

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
            count = subject.hrs_per_week

            if subject.type == "Lab":
                self.assign_lab(subject, faculty)
                continue

            for day in DAYS:
                for i, slot in enumerate(TIME_SLOTS):
                    if count <= 0:
                        break
                    if self.generated_tt[subject.section][day][i] is None:
                        if faculty.schedule[day][i] is None and self.can_schedule(faculty, day, i):
                            self.generated_tt[subject.section][day][i] = f"{subject.name} ({faculty.name})"
                            faculty.schedule[day][i] = f"{subject.name} ({subject.section})"
                            faculty.units_allocated += UNIT_VALUE[subject.type]
                            count -= 1

    def assign_lab(self, subject, faculty):
        for day in DAYS:
            for i in range(len(TIME_SLOTS) - 1):
                if (self.generated_tt[subject.section][day][i] is None and
                    self.generated_tt[subject.section][day][i+1] is None and
                    faculty.schedule[day][i] is None and
                    faculty.schedule[day][i+1] is None):

                    self.generated_tt[subject.section][day][i] = f"{subject.name} ({faculty.name})"
                    self.generated_tt[subject.section][day][i+1] = f"{subject.name} ({faculty.name})"
                    faculty.schedule[day][i] = f"{subject.name} ({subject.section})"
                    faculty.schedule[day][i+1] = f"{subject.name} ({subject.section})"
                    faculty.units_allocated += UNIT_VALUE[subject.type] * 1
                    return

    def get_teacher_for_subject(self, subject):
        for tid, faculty in self.faculties.items():
            if subject in faculty.subjects:
                return tid
        return None

    def can_schedule(self, faculty, day, i):
        if i > 0 and faculty.schedule[day][i-1] is not None:
            return False
        if i < len(TIME_SLOTS)-1 and faculty.schedule[day][i+1] is not None:
            return False
        return True

    def get_section_tt(self, section):
        return self.generated_tt[section]

    def get_faculty_tt(self, tid):
        return self.faculties[tid].schedule

# Export constants for app.py
__all__ = ["TimetableGenerator", "DAYS", "TIME_SLOTS"]

