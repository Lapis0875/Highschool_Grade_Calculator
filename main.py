from typing import Union
import os

from models import *
from calc import *


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


def read_data() -> Union[SingleGradeCalculator]:
    print("="*10)
    print(
        """
        [ 내신 산출 도구 ] [ 성적 입력 ]
        1. 전체 : /data 경로의 모든 파일을 열람합니다.
        2. 선택한 파일들만 열람합니다. , 로 구분해 두개 이상의 파일을 지정할 수 있습니다.
        """
    )
    data_root: str = os.path.join(os.getcwd(), "data")
    answer: str = input("> ")
    if answer == "1":
        os.f
    elif answer == "2":
        print(
            """
            [ 내신 산출 도구 ] [ 성적 입력 ] [ 파일 이름 입력 ]
            
            """
        )
        filenames: str = input('>')

    



def main():
    """내신 총점을 다양하게 산출합니다."""
    intro()
    calculator = read_data()
    print("="*10)
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
    input("")


if __name__ == "__main__":
    main()
