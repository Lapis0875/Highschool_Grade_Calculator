from __future__ import annotations

import json
import logging
from sys import stdout
from abstracts import JsonObject, ParsableEnum, ComparableEnum
from enum import Enum
from typing import Union, NoReturn, Any, List, Tuple
from extend_builtins import Filter
from constants import *

__all__ = (
    "SubjectType",
    "SubjectCategory",
    "SubjectAchievementLevels",
    "Subject",
    "DetailedSubject",
    "Student",
    "Semester"
)

logger = logging.getLogger("models")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(stream=stdout)
handler.setFormatter(
    logging.Formatter(
        style="{",
        fmt="[{asctime}] [{levelname}] {name}: {message}"
    )
)
logger.addHandler(handler)


class StringComparableEnum(ComparableEnum):
    """
    Enum class supporting Enum-Enum, Enum-String compare.
    """
    def __eq__(self, other: Union[ComparableEnum, Any]) -> bool:
        if isinstance(other, Enum):
            return self.value == other.value
        elif isinstance(other, str):
            return self.value == other
        else:
            TypeError(f'Cannot compare ComparableEnum object with {type(other)} object!')


class SubjectType(ParsableEnum, StringComparableEnum):

    RELATIVE = "상대평가"
    ABSOLUTE = "절대평가"
    PASS_NOT_PASS = "PnP"
    PNP = PASS_NOT_PASS  # Alias for Pass not Pass

    @classmethod
    def parse(cls, value: str) -> SubjectType:
        """
        Parse raw string into SubjectType instance.

        Args:
            value (str): value to parse into SubjectType object.
        """
        return Filter(lambda enum: enum.value == value, cls._member_map_.values()).find_first()


class SubjectCategory(ParsableEnum, StringComparableEnum):
    KOREAN = "국어"
    MATH = "수학"
    ENGLISH = "영어"
    SCIENCE = "과학"
    SOCIOLOGY = "사회(역사/도덕포함)"
    ETC = "기술・가정/제2외국어/한문/교양"

    @classmethod
    def parse(cls, value: str) -> SubjectCategory:
        """
        Parse raw string into SubjectCategory instance.

        Args:
            value (str): value to parse into SubjectCategory object.
        """
        return Filter(lambda enum: enum.value == value, cls._member_map_.values()).find_first()


class SubjectAchievementLevels(ParsableEnum, StringComparableEnum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    PASS = "Pass"
    P = PASS
    NotPass = "Not Pass"
    NP = NotPass

    @classmethod
    def parse(cls, value: str) -> SubjectAchievementLevels:
        """
        Parse raw string into SubjectAchievementLevels instance.

        Args:
            value (str): value to parse into SubjectAchievementLevels object.
        """
        return cls.__members__[value]


class Subject(JsonObject):
    """Abstract Base Class for common subjects (Relative, Absolute, PnP)"""

    @classmethod
    def fromJson(cls, data: JSON, grade: int, semester: int) -> Subject:
        """Parse subject's common attributes from json data and convert to Subject object"""
        # Read raw attributes
        raw_subject_type: str = data[SubjectKeys.TYPE]
        raw_category: str = data[SubjectKeys.CATEGORY]
        name: str = data[SubjectKeys.NAME]
        units: int = data[SubjectKeys.UNITS]
        rank: int = data[SubjectKeys.RANK]
        raw_achievement: str = data[SubjectKeys.ACHIEVEMENT_LEVEL]

        # Parse raw attributes into Enum classes
        subject_type: SubjectType = SubjectType.parse(raw_subject_type)
        category: SubjectCategory = SubjectCategory.parse(raw_category)
        achievement: SubjectAchievementLevels = SubjectAchievementLevels.parse(raw_achievement)
        return cls(
            subject_type,
            category,
            name,
            units,
            rank,
            achievement,
            grade,
            semester
        )

    def __init__(
            self,
            subject_type: SubjectType,  # 교과 유형 (상대평가, 절대평가, PnP)
            category: SubjectCategory,  # 교과 분류 (국어 수학 영어 과학 사회 ...)
            name: str,  # 과목명
            units: int,  # 단위수
            rank: int,  # 석차등급
            achievement: SubjectAchievementLevels,  # 교과 성취도
            # Information injected during json parse.
            grade: int,
            semester: int
    ) -> NoReturn:
        """
        Initialize Subject object

        Args:
            data (JSON): json data to parse as Subject.
        """
        self._subject_type: SubjectType = subject_type
        self._category: SubjectCategory = category
        self._name: str = name
        self._units: int = units
        self._rank: int = rank
        self._achievement: SubjectAchievementLevels = achievement

        # Information injected during json parse.
        self._grade: int = grade    # 학년
        self._semester: int = semester  # 학기

    def toJson(self) -> JSON:
        return {
            SubjectKeys.TYPE: self._subject_type.value,
            SubjectKeys.CATEGORY: self._category.value,
            SubjectKeys.NAME: self._name,
            SubjectKeys.UNITS: self._units,
            SubjectKeys.RANK: self._rank,
            SubjectKeys.ACHIEVEMENT_LEVEL: self._achievement.value
        }

    # Common properties

    @property
    def type(self) -> SubjectType:
        """
        Subject's type (유형).

        상대평가 -> SubjectType.RELATIVE
        절대평가 -> SubjectType.ABSOLUTE
        PnP (Pass or Not Pass) -> SubjectType.PNP
        """
        return self._subject_type

    @property
    def category(self) -> SubjectCategory:
        """
        Subject's category (교과).

        Example:
            문학: (국어) -> 국어

        국어 -> SubjectCategory.KOREAN
        수학 -> SubjectCategory.MATH
        영어 -> SubjectCategory.ENGLISH
        과학 -> SubjectCategory.SCIENCE
        사회(역사/도덕포함) -> SubjectCategory.SOCIOLOGY
        기술・가정/제2외국어/한문/교양 -> SubjectCategory.ETC
        """
        return self._category

    @property
    def name(self) -> str:
        """
        Subject's name (과목).

        Example:
            문학: (국어) -> 문학
        """
        return self._name

    @property
    def units(self) -> int:
        """Subject's units (단위수)."""
        return self._units

    @property
    def rank(self) -> int:
        """Subject's rank (석차등급)."""
        return self._rank

    @property
    def achievement(self) -> SubjectAchievementLevels:
        """Subject's standard deviation (성취도)."""
        return self._achievement

    # Information injected during json parse.
    @property
    def semesterInfo(self) -> str:
        """Subject's grade (학년)."""
        return f'{self._grade}학년 {self._semester}학기'

    def pretty(self) -> str:
        return f"""
        과목명 : {self.name}
        과목 유형 : {self.type}
        단위수 : {self.units}
        석차등급 : {self.rank}
        성취도 : {self.achievement.value}
        """

    def __repr__(self) -> str:
        return f"Subject<category={self.category},name={self.name},semesterInfo={self.semesterInfo},units={self.units},rank={self.rank}>"


class DetailedSubject(Subject):
    """Abstract Base Class for detailed subjects (Relative, Absolute)"""

    @classmethod
    def fromJson(cls, data: JSON, grade: int, semester: int) -> DetailedSubject:
        """Parse subject's common attributes from json data and convert to DetailedSubject object"""
        # Read raw attributes
        raw_subject_type: str = data[SubjectKeys.TYPE]
        raw_category: str = data[SubjectKeys.CATEGORY]
        name: str = data[SubjectKeys.NAME]
        units: int = data[SubjectKeys.UNITS]
        rank: int = data[SubjectKeys.RANK]
        raw_achievement: str = data[SubjectKeys.ACHIEVEMENT_LEVEL]
        score: float = data[SubjectKeys.SCORE]
        average: float = data[SubjectKeys.AVERAGE]
        standard_deviation: float = data[SubjectKeys.STANDARD_DEVIATION]
        participants: int = data[SubjectKeys.PARTICIPANTS]

        # Parse raw attributes into Enum classes
        subject_type: SubjectType = SubjectType.parse(raw_subject_type)
        category: SubjectCategory = SubjectCategory.parse(raw_category)
        achievement: SubjectAchievementLevels = SubjectAchievementLevels.parse(raw_achievement)

        return cls(
            subject_type,
            category,
            name,
            units,
            rank,
            achievement,
            score,
            average,
            standard_deviation,
            participants,
            grade,
            semester
        )

    def __init__(
            self,
            # 공통 항목
            subject_type: SubjectType,  # 교과 유형 (상대평가, 절대평가, PnP)
            category: SubjectCategory,  # 교과 분류 (국어 수학 영어 과학 사회 ...)
            name: str,  # 과목명
            units: int,  # 단위수
            rank: int,  # 석차등급
            achievement: SubjectAchievementLevels,  # 교과 성취도
            # 세부 항목
            score: float,  # 원점수
            average: float,  # 과목평균
            standard_deviation: float,  # 표준편차
            participants: int,  # 수강자 수
            # Information injected during json parse.
            grade: int,
            semester: int
    ) -> NoReturn:
        super(DetailedSubject, self).__init__(
            subject_type,
            category,
            name,
            units,
            rank,
            achievement,
            grade,
            semester
        )
        self._score: float = score
        self._average: float = average
        self._standard_deviation: float = standard_deviation
        self._participants: int = participants

    def toJson(self) -> JSON:
        data = super(DetailedSubject, self).toJson()
        data.update(
            {
                SubjectKeys.SCORE: self._score,
                SubjectKeys.AVERAGE: self._average,
                SubjectKeys.STANDARD_DEVIATION: self._standard_deviation,
                SubjectKeys.PARTICIPANTS: self._participants
            }
        )
        return data

    # Only Relative & Absolute subjects

    @property
    def score(self) -> float:
        """Subject's score (원점수)."""
        return self._score

    @property
    def average(self) -> float:
        """Subject's average (과목평균)."""
        return self._average

    @property
    def standard_deviation(self) -> float:
        """Subject's standard deviation (표준편차)."""
        return self._standard_deviation

    @property
    def participants(self) -> int:
        """Subject's participants (수강자수)."""
        return self._participants

    students = listeners = participants  # Alias

    def pretty(self) -> str:
        return f"""
        과목명 : {self.name}
        과목 유형 : {self.type}
        단위수 : {self.units}
        석차등급 : {self.rank}
        원점수 : {self.score}
        과목평균 : {self.average}
        표준편차 : {self.standard_deviation}
        수강자 수 : {self.participants}
        성취도 : {self.achievement.value}
        """


class Student(JsonObject):
    """JsonObject containing student's information"""

    @classmethod
    def fromJson(cls, data: JSON) -> Student:
        return cls(
            name=data[StudentKeys.NAME],
            grade=data[StudentKeys.GRADE]
        )

    def __init__(self, name: str, grade: int) -> None:
        self._name: str = name
        self._grade: int = grade

    def toJson(self) -> JSON:
        return {StudentKeys.NAME: self._name, StudentKeys.GRADE: self._grade}

    @property
    def name(self) -> str:
        return self._name

    @property
    def grade(self) -> int:
        return self._grade


class Semester(JsonObject):
    """Represents `semester` object in config"""
    @classmethod
    def fromJson(cls, data: JSON) -> Semester:
        grade: int = data[SemesterKeys.GRADE]
        semester: int = data[SemesterKeys.SEMESTER]

        raw_subjects: List[JSON] = data[SemesterKeys.SUBJECT_SCORES]
        subjects: List[Union[SubjectKeys, DetailedSubject]] = [
            DetailedSubject.fromJson(subject, grade, semester)
            if SubjectKeys.SCORE in subject
            else Subject.fromJson(subject, grade, semester)
            for subject in raw_subjects
        ]
        return cls(
            grade,
            semester,
            subjects
        )

    def __init__(self, grade: int, semester: int, subjects: List[Union[SubjectKeys, DetailedSubject]]) -> None:
        self._grade: int = grade
        self._semester: int = semester
        self._subject_list: List[Union[SubjectKeys, DetailedSubject]] = subjects

    @property
    def subjects(self) -> Tuple[Union[SubjectKeys, DetailedSubject]]:
        return tuple(self._subject_list)

    def filter_category(self, category: SubjectCategory) -> Tuple[Subject, ...]:
        return tuple(filter(
            lambda s: s.category == category,
            self._subject_list
        ))

    @property
    def korean_subjects(self) -> Tuple[Subject, ...]:
        return self.filter_category(SubjectCategory.KOREAN)

    @property
    def math_subjects(self) -> Tuple[Subject, ...]:
        return self.filter_category(SubjectCategory.MATH)

    @property
    def english_subjects(self) -> Tuple[Subject, ...]:
        return self.filter_category(SubjectCategory.ENGLISH)

    @property
    def science_subjects(self) -> Tuple[Subject, ...]:
        return self.filter_category(SubjectCategory.SCIENCE)

    @property
    def sociology_subjects(self) -> Tuple[Subject, ...]:
        return self.filter_category(SubjectCategory.SOCIOLOGY)

    @property
    def etc_subjects(self) -> Tuple[Subject, ...]:
        return self.filter_category(SubjectCategory.ETC)

    def toJson(self) -> JSON:
        subject_scores: JSON = {}
        for subjectJson in map(lambda s: s.toJson(), self._subject_list):
            subject_scores.update(subjectJson)
        logger.debug(
            json.dumps(subject_scores)
        )
        return {
            SemesterKeys.GRADE: self._grade,
            SemesterKeys.SEMESTER: self._semester,
            SemesterKeys.SUBJECT_SCORES: subject_scores
        }
