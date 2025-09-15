import math

material_dict = {
    '유리': 2.4,
    '알루미늄': 2.7,
    '탄소강': 7.85
}

def sphere_area(): # 여기는 문제 요구사항에 나온거 복붙했었어요 ㅋㅋㅋ
    return round('면적', 3), round('무게', 3) # 이런식?

def main():
    try:
        diameter = float(input('지름을 입력하시오').strip())

        if not isinstance(diameter, int) and diameter <= 0:
            raise ValueError

        material = input('재질 입력').strip()
        if material not in material_dict.keys():
            raise ValueError

        thickness = input('두께를 입력하시오').strip()
        if thickness == '':
            thickness = 1.0

        if not isinstance(thickness, float) and thickness <= 0:
            raise ValueError

        print(diameter, material, thickness)

    except (TypeError, ValueError):
        print(f'Input Value Error.')
    except Exception as e:
        print(f'Unexpected Error: {e}') # -> 익셉션의 프린트문 표기는 {e}는 없애고 제출했던거같아요. 하지만 프로그래밍도중에 무슨 에러가 나오는지 보느라 {e}를 넣어놨었죠.

if __name__ == '__main__':
    main()