#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python sorted() key 매개변수 활용 예시
코딩 테스트에서 자주 사용되는 패턴들을 포함한 완전한 예제
Python 3.12+ 호환
"""

from operator import itemgetter, attrgetter
import functools


def main():
    """메인 함수: 다양한 sorted key 활용법 데모"""

    print("=" * 50)
    print("Python sorted() key 매개변수 활용 예시")
    print("=" * 50)

    # 1. 기본 내장 함수를 key로 사용
    print("\n1. 문자열 길이 기준 정렬 (len 함수)")
    words = ["banana", "pie", "Washington", "book", "a"]
    try:
        sorted_by_length = sorted(words, key=len)  # ['a', 'pie', 'book', 'banana', 'Washington']
        print(f"원본: {words}")
        print(f"길이순: {sorted_by_length}")
    except Exception as e:
        print(f"에러 발생: {e}")

    # 2. 절댓값 기준 정렬
    print("\n2. 절댓값 기준 정렬 (abs 함수)")
    numbers = [-4, -2, 1, 3, -5, 2]
    try:
        sorted_by_abs = sorted(numbers, key=abs)  # [1, -2, 2, 3, -4, -5]
        print(f"원본: {numbers}")
        print(f"절댓값순: {sorted_by_abs}")
    except Exception as e:
        print(f"에러 발생: {e}")

    # 3. 대소문자 구분 없는 문자열 정렬
    print("\n3. 대소문자 구분 없는 정렬 (str.lower)")
    mixed_case = ["Apple", "banana", "Cherry", "date"]
    try:
        sorted_case_insensitive = sorted(mixed_case, key=str.lower)  # ['Apple', 'banana', 'Cherry', 'date']
        print(f"원본: {mixed_case}")
        print(f"대소문자무시: {sorted_case_insensitive}")
    except Exception as e:
        print(f"에러 발생: {e}")

    # 4. lambda 함수를 이용한 튜플 정렬
    print("\n4. 튜플의 특정 인덱스 기준 정렬 (lambda)")
    student_tuples = [('john', 'A', 15), ('jane', 'B', 12), ('dave', 'B', 10)]
    try:
        # 나이(인덱스 2) 기준 정렬
        sorted_by_age = sorted(student_tuples, key=lambda student: student[2])  # [('dave', 'B', 10), ('jane', 'B', 12), ('john', 'A', 15)]
        print(f"원본: {student_tuples}")
        print(f"나이순: {sorted_by_age}")

        # 성적(인덱스 1) 기준 정렬
        sorted_by_grade = sorted(student_tuples, key=lambda student: student[1])  # [('john', 'A', 15), ('jane', 'B', 12), ('dave', 'B', 10)]
        print(f"성적순: {sorted_by_grade}")
    except Exception as e:
        print(f"에러 발생: {e}")

    # 5. 딕셔너리 리스트 정렬
    print("\n5. 딕셔너리 리스트 정렬")
    people = [
        {'name': 'John', 'age': 45, 'score': 85},
        {'name': 'Diane', 'age': 35, 'score': 92},
        {'name': 'Mike', 'age': 25, 'score': 78}
    ]
    try:
        # 나이 기준 정렬
        sorted_by_age_dict = sorted(people, key=lambda x: x['age'])  # [{'name': 'Mike', 'age': 25, 'score': 78}, ...]
        print(f"나이순: {sorted_by_age_dict}")

        # 점수 기준 내림차순 정렬
        sorted_by_score_desc = sorted(people, key=lambda x: x['score'], reverse=True)  # [{'name': 'Diane', 'age': 35, 'score': 92}, ...]
        print(f"점수 내림차순: {sorted_by_score_desc}")
    except Exception as e:
        print(f"에러 발생: {e}")

    # 6. 복합 조건 정렬 (Multiple Criteria)
    print("\n6. 복합 조건 정렬 - 성적(내림차순) → 나이(오름차순)")
    students = [
        ("Alice", "A", 95, 20),
        ("Bob", "B", 87, 19),
        ("Charlie", "A", 92, 21),
        ("Teddy", "A", 92, 22),
        ("David", "C", 88, 18),
        ("Eve", "B", 90, 20)
    ]
    try:
        # 성적 내림차순, 같은 성적이면 나이 오름차순
        sorted_multi = sorted(students, key=lambda x: (-ord(x[1]), x[3]))  # [('Alice', 'A', 95, 20), ('Charlie', 'A', 92, 21), ...]
        print(f"복합정렬: {sorted_multi}")

        # 점수 내림차순, 같은 점수면 이름 오름차순
        # 튜플의 경우, key=lambda x: (-x[2], x) 처럼 x 만 사용시, 앞의 -x[2]로 정렬한 뒤 동일한 값일 경우 튜플 x의 내부 데이타의 순서대로 비교하고 동일하면 다음 데이타를 비교하는 방식으로 최종적으로 전체를 비교하게 될 경우까지 갈 수 도 있다.
        sorted_score_name = sorted(students, key=lambda x: (-x[2], x))  # [('Alice', 'A', 95, 20), ('Charlie', 'A', 92, 21), ...]
        print(f"점수-이름순: {sorted_score_name}")
    except Exception as e:
        print(f"에러 발생: {e}")

    # 7. 사용자 정의 정렬 순서
    print("\n7. 사용자 정의 정렬 순서")
    priority_order = {'urgent': 0, 'high': 1, 'medium': 2, 'low': 3}
    tasks = ['medium', 'urgent', 'low', 'high', 'medium', 'unknown']
    try:
        # 정의된 우선순위대로 정렬, 미정의는 마지막
        sorted_custom = sorted(tasks, key=lambda item: priority_order.get(item, 999))  # ['urgent', 'high', 'medium', 'medium', 'low', 'unknown']
        print(f"원본: {tasks}")
        print(f"우선순위: {sorted_custom}")
    except Exception as e:
        print(f"에러 발생: {e}")

    # 8. operator 모듈을 활용한 정렬
    print("\n8. operator 모듈 활용")
    try:
        # itemgetter를 이용한 튜플 정렬
        sorted_itemgetter = sorted(student_tuples, key=itemgetter(1))  # 성적 기준 정렬
        print(f"itemgetter(성적): {sorted_itemgetter}")

        # 복수 키로 정렬 (성적, 나이 순)
        sorted_multi_item = sorted(student_tuples, key=itemgetter(1, 2))  # [('john', 'A', 15), ('dave', 'B', 10), ('jane', 'B', 12)]
        print(f"itemgetter(성적,나이): {sorted_multi_item}")
    except Exception as e:
        print(f"에러 발생: {e}")

    # 9. 클래스 객체 정렬
    print("\n9. 클래스 객체 정렬")

    class Student:
        def __init__(self, name, grade, age):
            self.name = name
            self.grade = grade
            self.age = age

        def __repr__(self):
            return f"Student('{self.name}', '{self.grade}', {self.age})"

    student_objects = [
        Student('john', 'A', 15),
        Student('jane', 'B', 12),
        Student('dave', 'B', 10)
    ]

    try:
        # 나이 기준 정렬
        sorted_objects = sorted(student_objects, key=lambda s: s.age)  # [Student('dave', 'B', 10), Student('jane', 'B', 12), Student('john', 'A', 15)]
        print(f"객체 나이순: {sorted_objects}")

        # attrgetter 사용
        sorted_attr = sorted(student_objects, key=attrgetter('grade', 'age'))  # 성적, 나이 순
        print(f"attrgetter: {sorted_attr}")
    except Exception as e:
        print(f"에러 발생: {e}")

    # 10. 특수한 정렬 패턴들
    print("\n10. 특수 정렬 패턴")

    # 문자열에서 숫자 추출하여 정렬
    mixed_strings = ["file1.txt", "file10.txt", "file2.txt", "file20.txt"]
    try:
        # 파일명에서 숫자 부분만 추출하여 정렬
        import re
        def extract_number(filename):
            match = re.search(r'(\d+)', filename)
            return int(match.group(1)) if match else 0

        sorted_files = sorted(mixed_strings, key=extract_number)  # ['file1.txt', 'file2.txt', 'file10.txt', 'file20.txt']
        print(f"파일명 숫자순: {sorted_files}")
    except Exception as e:
        print(f"에러 발생: {e}")

    # 좌표 점들을 원점으로부터의 거리순으로 정렬
    points = [(1, 2), (3, 1), (0, 0), (2, 3), (1, 1)]
    try:
        # 유클리드 거리 계산
        sorted_by_distance = sorted(points, key=lambda p: p[0] ** 2 + p[1] ** 2)  # [(0, 0), (1, 1), (1, 2), (3, 1), (2, 3)]
        print(f"원점거리순: {sorted_by_distance}")
    except Exception as e:
        print(f"에러 발생: {e}")


def test_sorting_functions():
    """정렬 함수들의 단위 테스트"""
    print("\n" + "=" * 30)
    print("테스트 실행")
    print("=" * 30)

    # 테스트 케이스들
    test_cases = [
        {
            'name': '길이 정렬 테스트',
            'data': ["hello", "a", "world", "python"],
            'key_func': len,
            'expected': ["a", "hello", "world", "python"]
        },
        {
            'name': '절댓값 정렬 테스트',
            'data': [-3, 1, -1, 2],
            'key_func': abs,
            'expected': [1, -1, 2, -3]
        }
    ]

    for test in test_cases:
        try:
            result = sorted(test['data'], key=test['key_func'])
            status = "✅ PASS" if result == test['expected'] else "❌ FAIL"
            print(f"{status} {test['name']}: {result}")
        except Exception as e:
            print(f"❌ ERROR {test['name']}: {e}")


if __name__ == "__main__":
    try:
        main()
        test_sorting_functions()
        print(f"\n{'=' * 50}")
        print("모든 예시 실행 완료!")
        print("=" * 50)
    except Exception as e:
        print(f"프로그램 실행 중 오류 발생: {e}")
        import traceback

        traceback.print_exc()
