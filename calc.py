import json
from pprint import pprint
from typing import NoReturn, Tuple, List, Dict, Iterable
from constants import StudentKeys, SemesterKeys, JSON
from models import *


class SingleGradeCalculator:
    def __init__(self, data: JSON) -> NoReturn:
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

    @staticmethod
    def get_rank(subjects: Iterable[Subject]) -> float:
        total: int = 0
        units: int = 0
        for subject in subjects:
            if subject.type == SubjectType.RELATIVE:
                total += subject.rank * subject.units
                units += subject.units
        return total / units

    @property
    def subjects(self) -> List[Subject]:
        subjects: List[Subject] = []
        for semester in self._semesters:
            for subject in semester.subjects:
                subjects.append(subject)
        return subjects

    @property
    def korean_subjects(self) -> Tuple[Subject]:
        korean_subjects: List[Subject] = []
        for semester in self._semesters:
            korean_subjects.extend(semester.korean_subjects)
        return tuple(korean_subjects)

    @property
    def math_subjects(self) -> Tuple[Subject]:
        math_subjects: List[Subject] = []
        for semester in self._semesters:
            math_subjects.extend(semester.math_subjects)
        return tuple(math_subjects)

    @property
    def english_subjects(self) -> Tuple[Subject]:
        english_subjects: List[Subject] = []
        for semester in self._semesters:
            english_subjects.extend(semester.english_subjects)
        return tuple(english_subjects)

    @property
    def science_subjects(self) -> Tuple[Subject]:
        science_subjects: List[Subject] = []
        for semester in self._semesters:
            science_subjects.extend(semester.science_subjects)
        return tuple(science_subjects)

    @property
    def sociology_subjects(self) -> Tuple[Subject]:
        sociology_subjects: List[Subject] = []
        for semester in self._semesters:
            sociology_subjects.extend(semester.sociology_subjects)
        return tuple(sociology_subjects)

    @property
    def etc_subjects(self) -> Tuple[Subject]:
        etc_subjects: List[Subject] = []
        for semester in self._semesters:
            etc_subjects.extend(semester.etc_subjects)
        return tuple(etc_subjects)

    @property
    def map(self) -> Dict[str, Dict[str, List[Subject]]]:
        # Use caching.
        data = getattr(self, '__subjects__map__', False)
        if data: return data
        # If not cached.
        data = {}
        for subjectName in SubjectCategory.__members__.values():
            subjectsProperty: property = getattr(self, f'{subjectName.name.lower()}_subjects', None)
            subjects = subjectsProperty.__get__() if isinstance(subjectsProperty, property) else subjectsProperty  # make sure value of the property is stored.
            subjectData = {}
            for subject in subjects:
                try:
                    subjectData[subject.semesterInfo]
                except KeyError:
                    subjectData[subject.semesterInfo] = []
                subjectData[subject.semesterInfo].append(subject)
            data[subjectName.value] = subjectData
        setattr(self, '__subjects_map__', data)
        return data

    def category_grades(self):
        """
        Calculate total subject grade (내신) of certain subject category

        Args:
            category (SubjectCategory): subject's category
        """
        print('> 종합 내신 총점 : {}'.format(self.get_rank(
            self.subjects
        )))
        print('> 국영수사과 총점 : {}'.format(self.get_rank(
            self.korean_subjects +
            self.math_subjects +
            self.english_subjects +
            self.science_subjects +
            self.sociology_subjects
        )))
        print('> 국영수 총점 : {}'.format(self.get_rank(
            self.korean_subjects +
            self.math_subjects +
            self.english_subjects
        )))
        print('> 국영수과 총점 : {}'.format(self.get_rank(
            self.korean_subjects +
            self.math_subjects +
            self.english_subjects +
            self.science_subjects
        )))
        print('> 국영수사 총점 : {}'.format(self.get_rank(
            self.korean_subjects +
            self.math_subjects +
            self.english_subjects +
            self.sociology_subjects
        )))
        print('> 영수과 총점 : {}'.format(self.get_rank(
            self.math_subjects +
            self.english_subjects +
            self.science_subjects
        )))

        for subjectName, subjects in self.map.items():
            print('='*10)
            print(f'[ {subjectName} 영역 ]')
            for semesterInfo, subjects in subjects.items():
                print(f'{semesterInfo}:')
                for subject in subjects:
                    print(subject.pretty())
            print(f'> {subjectName} 영역 내신 총점 : {self.get_rank(subjects)}')
