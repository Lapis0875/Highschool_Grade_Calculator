from __future__ import annotations
import logging
from sys import stdout
from abc import abstractmethod, ABC
from enum import Enum
from typing import Dict, Union, NoReturn, Any, List
from extend_builtins import compute

__all__ = (
    "JSON",
    "SubjectType",
    "SubjectCategory",
    "SubjectAchievementLevels",
    "Subject",
    "DetailedSubject",
    "Student",
    "Keys"
)

JSON = Dict[str, Union[str, int, float, bytes, list, dict, None]]

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


class JsonObject(ABC):
    @abstractmethod
    def toJson(self) -> JSON:
        """Parse python object(JsojObject's subclasses) into json data"""

    @classmethod
    @abstractmethod
    def fromJson(cls, data: JSON) -> JsonObject:
        """Parse json data into python object"""


class ParsableEnum(Enum, ABC):
    @classmethod
    @abstractmethod
    def parse(cls, value: Any) -> ParsableEnum:
        """
        Parse raw value into ParsableEnum instance.

        Args:
            value (Any): value to parse into ParsableEnum object.
        """
        ...


class SubjectType(ParsableEnum):
    RELATIVE = "상대평가"
    ABSOLUTE = "설대평가"
    PASS_NOT_PASS = "Pnp"
    PNP = PASS_NOT_PASS  # Alias for Pass not Pass

    @classmethod
    def parse(cls, value: str) -> SubjectType:
        """
        Parse raw string into SubjectType instance.

        Args:
            value (str): value to parse into SubjectType object.
        """
        return filter(lambda enum: enum.value == value, cls._member_map_.values()).find_first()


class SubjectCategory(ParsableEnum):
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
        return filter(lambda enum: enum.value == value, cls._member_map_.values()).find_first()


class SubjectAchievementLevels(ParsableEnum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"

    def __eq__(self, other):
        if isinstance(other, SubjectAchievementLevels):
            return self.value == other.value
        elif isinstance(other, str):
            return self.value == other
        else:
            return False

    @classmethod
    def parse(cls, value: str) -> SubjectAchievementLevels:
        """
        Parse raw string into SubjectAchievementLevels instance.

        Args:
            value (str): value to parse into SubjectAchievementLevels object.
        """
        return cls._member_map_[value]


class Subject(JsonObject):
    """Abstract Base Class for common subjects (Relative, Absolute, PnP)"""

    @classmethod
    def fromJson(cls, data: JSON) -> Subject:
        """Parse subject's common attributes from json data and convert to Subject object"""
        # Read raw attributes
        raw_subject_type: str = data["교과유형"]
        raw_category: str = data["교과분류"]
        name: str = data["교과명"]
        units: int = data["단위수"]
        rank: int = data["석차등급"]
        raw_achievement: str = data["성취도"]

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
            achievement
        )

    def __init__(
            self,
            subject_type: SubjectType,  # 교과 유형 (상대평가, 절대평가, PnP)
            category: SubjectCategory,  # 교과 분류 (국어 수학 영어 과학 사회 ...)
            name: str,  # 과목명
            units: int,  # 단위수
            rank: int,  # 석차등급
            achievement: SubjectAchievementLevels  # 교과 성취도
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

    def toJson(self) -> JSON:
        return {
            ""
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


class DetailedSubject(Subject):
    """Abstract Base Class for detailed subjects (Relative, Abolute)"""

    @classmethod
    def fromJson(cls, data: JSON) -> DetailedSubject:
        """Parse subject's common attributes from json data and convert to DetailedSubject object"""
        # Read raw attributes
        raw_subject_type: str = data["교과유형"]
        raw_category: str = data["교과분류"]
        name: str = data["교과명"]
        units: int = data["단위수"]
        rank: int = data["석차등급"]
        raw_achievement: str = data["성취도"]
        score: float = data["원점수"]
        average: float = data["과목평균"]
        standard_deviation: float = data["표준편차"]
        participants: int = data["수강자수"]

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
            participants
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
            participants: int  # 수강자 수
    ) -> NoReturn:
        super(DetailedSubject, self).__init__(
            subject_type,
            category,
            name,
            units,
            rank,
            achievement
        )
        self._score: float = score
        self._average: float = average
        self._standard_deviation: float = standard_deviation
        self._participants: int = participants

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


class Student(JsonObject):
    """JsonObject containing student's information"""

    @classmethod
    def fromJson(cls, data: JSON) -> JsonObject:
        return cls(
            name=data["name"],
            grade=data["grade"]
        )

    def __init__(self, name: str, grade: int):
        self._name: str = name
        self._grade: int = grade

    @property
    def name(self) -> str:
        return self._name

    @property
    def grade(self) -> int:
        return self._grade

    def toJson(self) -> JSON:
        return {"name": self._name, "grade": self._grade}


class Semester(JsonObject):
    """Represents `semester` object in config"""
    @classmethod
    def fromJson(cls, data: JSON) -> JsonObject:
        pass

    def __init__(self, grade: int, semester: int, subjects: List[Union[Subject, DetailedSubject]]):
        self._grade: int = grade
        self._semester: int = semester
        self._subject_list: List[Union[Subject, DetailedSubject]] = subjects

    def toJson(self) -> JSON:
        subject_scores: JSON = {}
        compute(
            lambda subject_json: subject_scores.update(subject_json),
            map(
                lambda subject: subject.toJson(),
                self._subject_list
            )
        )
        return {
            Keys.GRADE: self._grade,
            Keys.SemesterKeys.SEMESTER: self._semester,
            Keys.SemesterKeys.SUBJECT_SCORES: subject_scores
        }


class Keys:
    # Common keys
    GRADE: str = "학년"  # 학생의 학년에 대응하는 키

    # Student Object
    STUDENT: str = "student"  # 학생 오브젝트에 대응하는 키

    class StudentKeys:
        """Key constants of Student object"""
        NAME: str = "이름"  # 학생의 이름에 대응하는 키

    # Semester Array
    SEMESTERS: str = "semesters"  # 학기별 성적 오브젝트의 array 에 대응하는 키

    class SemesterKeys:
        """Key constants of Semester object"""
        SEMESTER: str = "학기"
        SUBJECT_SCORES: str = "교과성적"

    # Subject Object

    class SubjectKeys:
        """Key constants of Subject object"""
        TYPE: str = "교과유형"
        CATEGORY: str = "교과분류"
        NAME: str = "교과명"
        UNITS: str = "단위수"
        RANK: str = "석차등급"
        SCORE: str = "원점수"
        AVERAGE: str = "과목평균"
        STANDARD_DEVIATION: str = "표준편차"
        ACHIEVEMENT_LEVEL: str = "성취도"
        PARTICIPANTS: str = "수강자수"