from typing import ClassVar, Final

__all__ = (
    "StudentKeys",
    "SemesterKeys",
    "SubjectKeys"
)

ClassConstantString = Final[ClassVar[str]]


class StudentKeys:
    """Key constants of Student object"""
    key: ClassConstantString = "students"   # key of student object
    # Student object
    NAME: ClassConstantString = "이름"
    GRADE: ClassConstantString = "학년"


class SemesterKeys:
    """Key constants of Semester object"""
    key: ClassConstantString = "semesters"  # key of semesters array object
    # Semester object
    GRADE: ClassConstantString = "학년"                # key of grade
    SEMESTER: ClassConstantString = "학기",            # key of semester
    SUBJECT_SCORES: ClassConstantString = "교과성적"    # key of subjects array object


class SubjectKeys:
    """Key constants of Subject object"""
    TYPE: ClassConstantString = "교과유형"
    CATEGORY: ClassConstantString = "교과분류"
    NAME: ClassConstantString = "교과명"
    UNITS: ClassConstantString = "단위수"
    RANK: ClassConstantString = "석차등급"
    SCORE: ClassConstantString = "원점수"
    AVERAGE: ClassConstantString = "과목평균"
    STANDARD_DEVIATION: ClassConstantString = "표준편차"
    ACHIEVEMENT_LEVEL: ClassConstantString = "성취도"
    PARTICIPANTS: ClassConstantString = "수강자수"
