from typing import Union, Any
import os
import json

from models import *
from calc import *


def read_json(path: str) -> JSON:
    if not os.path.isfile(path):
        raise ValueError(f'{path} is not a file!')
    elif os.path.splitext(path)[1] != '.json':
        raise ValueError(f'{path} is not a json file!')
    with open(path, mode='rt', encoding='utf-8') as f:
        return json.load(f)


# Phase
def intro():
    """Intro phase of High school grade calculator"""
    print(
        """
        [ 내신 산출 도구 ]
        ver 2021.01
        @author Minjun Kim (Lapis0875)
        @copyright 2021
        
        내신을 보다 쉽고 편리하게 계산하기 위한 도구입니다.
        """
    )


def read_data() -> Union[SingleGradeCalculator, Tuple[SingleGradeCalculator]]:
    print("="*10)
    print(
        """
        [ 내신 산출 도구 ] [ 성적 입력 ]
        1. 전체 : /data 경로의 모든 파일을 열람합니다.
        2. 선택한 파일들만 열람합니다. , 로 구분해 두개 이상의 파일을 지정할 수 있습니다.
        """
    )
    data_path: str = os.path.join(os.getcwd(), "data")
    answer: str = input("> ")
    if answer == "1":
        data = map(lambda file: read_json(os.path.join(data_path, file)), os.listdir(data_path))

    elif answer == "2":
        print(
            """
            [ 내신 산출 도구 ] [ 성적 입력 ] [ 파일 이름 입력 ]
            열람할 파일을 , 로 구분해 입력해주세요. 띄어쓰기는 사용하지 마세요.
            """
        )
        filenames: List[str, ...] = input('> ').split(',')
        data = map(lambda file: read_json(os.path.join(data_path, file)), filenames)
    else:
        raise ValueError(f'{answer} 은 지원되지 않는 선택지입니다!')
    calcs = tuple(map(lambda datum: SingleGradeCalculator(datum), data))
    if len(calcs) == 1:
        return calcs[0]
    return calcs


def viewer(calc: Union[SingleGradeCalculator, Tuple[SingleGradeCalculator]]):
    if isinstance(calc, tuple):
        # Multiple calcs.
        raise ValueError('WIP - Not implemented.')

    print(
        """
        [ 내신 산출 도구 ] [ 계산 방식 ]
        1. 전체
        2. 전과목
        3. 과목별
        4. 국수영사과
        5. 국수영과
        6. 국수영사
        7. 국수영
        8. 국영사
        9. 수영과
        10. 수과
        """
    )
    choice = input("> ")
    calc.category_grades()


def main():
    """내신 총점을 다양하게 산출합니다."""
    intro()
    calculators: Union[SingleGradeCalculator, Tuple[SingleGradeCalculator]] = read_data()
    print("="*10)
    viewer(calculators)
    

if __name__ == "__main__":
    main()
