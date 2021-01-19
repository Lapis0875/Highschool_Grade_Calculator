import json
from typing import NoReturn, Tuple
from .models import *


class SingleGradeCalculator:
    def __init__(self, filename: str) -> NoReturn:
        with open(f"data/{filename}.json", mode="rt", encoding="utf-8") as f:
            data = json.load(f)

        self.student = Student(data[Keys.STUDENT])

    def parse_data(self, data: JSON) -> Tuple[""]:
        """Parse config data into Calculator"""
        pass

    def category_grade(self, *subjects: Subject):
        """
        Calculate total subject grade (내신) of certain subject category
        :param subjects:
        :return:
        """