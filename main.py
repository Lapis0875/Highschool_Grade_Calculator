from .models import *
from .calc import *


def main():
    """내신 총점을 다양하게 산출합니다."""
    print(
        """
        [ 내신 산출 도구 ]
        ver 2021.01
        @author Minjun Kim (Lapis0875)
        @copyright 2021
        
        내신을 보다 쉽고 편리하게 계산하기 위한 도구입니다.
        """
    )
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
