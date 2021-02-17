import json
from typing import NoReturn, Tuple, List
from constants import StudentKeys, SemesterKeys
from extend_builtins import Compute
from models import *
from models import Student


class SingleGradeCalculator:
    def __init__(self, filename: str) -> NoReturn:
        with open(f"data/{filename}.json", mode="rt", encoding="utf-8") as f:
            data = json.load(f)

        student, semesters = self.parse_data(data)
        self._student: Student = student
        self._semesters: List[Semester] = semesters

    @staticmethod
    def parse_data(data: JSON) -> Tuple[Student, List[Semester]]:
        """Parse config data into Calculator"""
        raw_student: JSON = data[StudentKeys.key]
        student: Student = Student.fromJson(raw_student)
        raw_semesters: List[JSON] = data[SemesterKeys.key]
        semesters: List[Semester] = [Semester.fromJson(semester) for semester in raw_semesters]
        return student, semesters

    @property
    def korean_subjects(self) -> List[Subject]:
        korean_subjects: List[Subject] = []
        Compute(
            korean_subjects.extend,
            (semester.korean_subjects for semester in self._semesters)
        ).run()
        return korean_subjects

    @property
    def math_subjects(self) -> List[Subject]:
        math_subjects: List[Subject] = []
        Compute(
            math_subjects.extend,
            (semester.math_subjects for semester in self._semesters)
        ).run()
        return math_subjects

    @property
    def english_subjects(self) -> List[Subject]:
        english_subjects: List[Subject] = []
        Compute(
            english_subjects.extend,
            (semester.english_subjects for semester in self._semesters)
        ).run()
        return english_subjects

    @property
    def science_subjects(self) -> List[Subject]:
        science_subjects: List[Subject] = []
        Compute(
            science_subjects.extend,
            (semester.science_subjects for semester in self._semesters)
        ).run()
        return science_subjects

    @property
    def sociology_subjects(self) -> List[Subject]:
        sociology_subjects: List[Subject] = []
        Compute(
            sociology_subjects.extend,
            (semester.sociology_subjects for semester in self._semesters)
        ).run()
        return sociology_subjects

    @property
    def etc_subjects(self) -> List[Subject]:
        etc_subjects: List[Subject] = []
        Compute(
            etc_subjects.extend,
            (semester.etc_subjects for semester in self._semesters)
        ).run()
        return etc_subjects

    def category_grade(self, category: SubjectCategory):
        """
        Calculate total subject grade (내신) of certain subject category

        Args:
            category (SubjectCategory): subject's category
        """