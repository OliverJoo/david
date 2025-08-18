#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python operator 모듈 완벽 활용 가이드
Python 3.12 호환
"""

import operator
from typing import List, Dict, Any, Callable, Optional, Union, Tuple
from functools import reduce, partial
from dataclasses import dataclass
from enum import Enum
import time


class OperatorCategory(Enum):
    """연산자 카테고리 열거형"""
    ARITHMETIC = "산술 연산자"
    COMPARISON = "비교 연산자"
    LOGICAL = "논리 연산자"
    BITWISE = "비트 연산자"
    SEQUENCE = "시퀀스 연산자"
    ATTRIBUTE = "속성 연산자"
    ITEM = "아이템 연산자"


@dataclass
class OperatorInfo:
    """연산자 정보"""
    name: str
    function: Callable
    description: str
    example: str
    category: OperatorCategory


class OperatorModule:
    """Python operator 모듈 완벽 활용 클래스"""

    def __init__(self):
        """operator 모듈 데모 클래스 초기화"""
        self.operators = self._initialize_operators()
        self.performance_results = {}

    def _initialize_operators(self) -> Dict[OperatorCategory, List[OperatorInfo]]:
        """모든 연산자 정보 초기화"""
        return {
            OperatorCategory.ARITHMETIC: [
                OperatorInfo("add", operator.add, "덧셈", "add(3, 4) = 7", OperatorCategory.ARITHMETIC),
                OperatorInfo("sub", operator.sub, "뺄셈", "sub(10, 3) = 7", OperatorCategory.ARITHMETIC),
                OperatorInfo("mul", operator.mul, "곱셈", "mul(5, 6) = 30", OperatorCategory.ARITHMETIC),
                OperatorInfo("truediv", operator.truediv, "나눗셈", "truediv(15, 3) = 5.0", OperatorCategory.ARITHMETIC),
                OperatorInfo("floordiv", operator.floordiv, "정수 나눗셈", "floordiv(17, 3) = 5",
                             OperatorCategory.ARITHMETIC),
                OperatorInfo("mod", operator.mod, "나머지", "mod(17, 3) = 2", OperatorCategory.ARITHMETIC),
                OperatorInfo("pow", operator.pow, "거듭제곱", "pow(2, 3) = 8", OperatorCategory.ARITHMETIC),
                OperatorInfo("neg", operator.neg, "음수 변환", "neg(5) = -5", OperatorCategory.ARITHMETIC),
                OperatorInfo("pos", operator.pos, "양수 변환", "pos(-5) = -5", OperatorCategory.ARITHMETIC),
                OperatorInfo("abs", operator.abs, "절댓값", "abs(-5) = 5", OperatorCategory.ARITHMETIC),
            ],

            OperatorCategory.COMPARISON: [
                OperatorInfo("eq", operator.eq, "같음", "eq(5, 5) = True", OperatorCategory.COMPARISON),
                OperatorInfo("ne", operator.ne, "같지 않음", "ne(5, 3) = True", OperatorCategory.COMPARISON),
                OperatorInfo("lt", operator.lt, "작음", "lt(3, 5) = True", OperatorCategory.COMPARISON),
                OperatorInfo("le", operator.le, "작거나 같음", "le(3, 3) = True", OperatorCategory.COMPARISON),
                OperatorInfo("gt", operator.gt, "큼", "gt(5, 3) = True", OperatorCategory.COMPARISON),
                OperatorInfo("ge", operator.ge, "크거나 같음", "ge(5, 5) = True", OperatorCategory.COMPARISON),
            ],

            OperatorCategory.LOGICAL: [
                OperatorInfo("and_", operator.and_, "논리곱", "and_(True, False) = False", OperatorCategory.LOGICAL),
                OperatorInfo("or_", operator.or_, "논리합", "or_(True, False) = True", OperatorCategory.LOGICAL),
                OperatorInfo("not_", operator.not_, "논리부정", "not_(True) = False", OperatorCategory.LOGICAL),
            ],

            OperatorCategory.BITWISE: [
                OperatorInfo("lshift", operator.lshift, "왼쪽 시프트", "lshift(4, 2) = 16", OperatorCategory.BITWISE),
                OperatorInfo("rshift", operator.rshift, "오른쪽 시프트", "rshift(16, 2) = 4", OperatorCategory.BITWISE),
                OperatorInfo("xor", operator.xor, "배타적 OR", "xor(5, 3) = 6", OperatorCategory.BITWISE),
                OperatorInfo("invert", operator.invert, "비트 반전", "invert(5) = -6", OperatorCategory.BITWISE),
            ],

            OperatorCategory.SEQUENCE: [
                OperatorInfo("concat", operator.concat, "연결", "concat([1,2], [3,4]) = [1,2,3,4]",
                             OperatorCategory.SEQUENCE),
                OperatorInfo("contains", operator.contains, "포함 여부", "contains([1,2,3], 2) = True",
                             OperatorCategory.SEQUENCE),
                OperatorInfo("countOf", operator.countOf, "개수 세기", "countOf([1,2,2,3], 2) = 2",
                             OperatorCategory.SEQUENCE),
                OperatorInfo("indexOf", operator.indexOf, "인덱스 찾기", "indexOf([1,2,3], 2) = 1",
                             OperatorCategory.SEQUENCE),
            ],

            OperatorCategory.ITEM: [
                OperatorInfo("getitem", operator.getitem, "아이템 가져오기", "getitem([1,2,3], 1) = 2", OperatorCategory.ITEM),
                OperatorInfo("setitem", operator.setitem, "아이템 설정", "setitem(d, 'key', 'value')",
                             OperatorCategory.ITEM),
                OperatorInfo("delitem", operator.delitem, "아이템 삭제", "delitem(d, 'key')", OperatorCategory.ITEM),
            ],

            OperatorCategory.ATTRIBUTE: [
                OperatorInfo("attrgetter", operator.attrgetter, "속성 가져오기", "attrgetter('name')(obj)",
                             OperatorCategory.ATTRIBUTE),
                OperatorInfo("methodcaller", operator.methodcaller, "메서드 호출", "methodcaller('upper')('hello')",
                             OperatorCategory.ATTRIBUTE),
            ]
        }


def demonstrate_operator_module():
    """Python operator 모듈의 완벽한 활용 시연"""

    print("=== Python operator 모듈 완벽 활용 가이드 ===\n")

    # 1. 기본 산술 연산자
    print("1. 🔢 산술 연산자")
    numbers = [10, 5, 3, 2]

    # 일반적인 방법 vs operator 모듈
    print("일반 방법:", sum(numbers))
    print("operator 방법:", reduce(operator.add, numbers))

    # 곱셈으로 팩토리얼 계산
    factorial_5 = reduce(operator.mul, range(1, 6))
    print(f"5! = {factorial_5}")  # 출력: 5! = 120

    # 연산자를 변수로 저장
    operations = {
        '더하기': operator.add,
        '빼기': operator.sub,
        '곱하기': operator.mul,
        '나누기': operator.truediv
    }

    a, b = 15, 3
    for name, op in operations.items():
        result = op(a, b)
        print(f"{a} {name} {b} = {result}")
    print()

    # 2. 비교 연산자 활용
    print("2. ⚖️ 비교 연산자")
    students = [
        {'name': '김철수', 'score': 85},
        {'name': '박영희', 'score': 92},
        {'name': '이민수', 'score': 78},
        {'name': '정수진', 'score': 95}
    ]

    # operator.itemgetter를 이용한 정렬
    sorted_by_score = sorted(students, key=operator.itemgetter('score'), reverse=True)
    print("성적순 정렬:")
    for student in sorted_by_score:
        print(f"  {student['name']}: {student['score']}점")

    # 다중 키 정렬
    students_extended = [
        {'name': '김철수', 'age': 20, 'score': 85},
        {'name': '박영희', 'age': 19, 'score': 92},
        {'name': '이민수', 'age': 20, 'score': 85},
        {'name': '정수진', 'age': 19, 'score': 95}
    ]

    # 나이 → 성적 순으로 정렬
    multi_sorted = sorted(students_extended, key=operator.itemgetter('age', 'score'))
    print("\n나이순, 같으면 성적순:")
    for student in multi_sorted:
        print(f"  {student['name']}: {student['age']}세, {student['score']}점")
    print()

    # 3. 함수형 프로그래밍 패턴
    print("3. 🔧 함수형 프로그래밍 패턴")

    # map과 operator 조합
    numbers = [1, 2, 3, 4, 5]

    # 각 숫자를 제곱
    squares = list(map(operator.pow, numbers, [2] * len(numbers)))
    print(f"제곱: {squares}")  # 출력: 제곱: [1, 4, 9, 16, 25]

    # 부분 적용 (partial) 활용
    square = partial(operator.pow, exp=2)  # 잘못된 사용법 수정

    # 올바른 방법:
    def square_func(x):
        return operator.pow(x, 2)

    squares_partial = list(map(square_func, numbers))
    print(f"부분 적용 제곱: {squares_partial}")

    # filter와 operator 조합
    data = [1, -2, 3, -4, 5, -6]
    positives = list(filter(partial(operator.lt, 0), data))  # 0보다 큰 수
    print(f"양수만: {positives}")  # 출력: 양수만: [1, 3, 5]
    print()

    # 4. 속성 접근자 활용
    print("4. 🎯 속성 접근자 활용")

    @dataclass
    class Person:
        name: str
        age: int
        city: str

        def greet(self):
            return f"안녕하세요, {self.name}입니다."

    people = [
        Person("김철수", 25, "서울"),
        Person("박영희", 30, "부산"),
        Person("이민수", 22, "대구")
    ]

    # attrgetter로 속성 추출
    get_name = operator.attrgetter('name')
    get_age = operator.attrgetter('age')

    names = list(map(get_name, people))
    ages = list(map(get_age, people))

    print(f"이름들: {names}")  # 출력: 이름들: ['김철수', '박영희', '이민수']
    print(f"나이들: {ages}")  # 출력: 나이들: [25, 30, 22]

    # 나이순 정렬
    sorted_by_age = sorted(people, key=operator.attrgetter('age'))
    print("나이순 정렬:")
    for person in sorted_by_age:
        print(f"  {person.name}: {person.age}세")

    # methodcaller로 메서드 호출
    greet_method = operator.methodcaller('greet')
    greetings = list(map(greet_method, people))

    print("인사말:")
    for greeting in greetings:
        print(f"  {greeting}")
    print()

    # 5. 시퀀스 연산자 활용
    print("5. 📜 시퀀스 연산자 활용")

    lists = [[1, 2], [3, 4], [5, 6]]

    # concat으로 리스트 연결
    flattened = reduce(operator.concat, lists)
    print(f"평면화: {flattened}")  # 출력: 평면화: [1, 2, 3, 4, 5, 6]

    # contains로 포함 여부 확인
    test_list = [1, 2, 3, 4, 5]
    contains_3 = operator.contains(test_list, 3)
    print(f"3이 포함되어 있나? {contains_3}")  # 출력: 3이 포함되어 있나? True

    # countOf로 개수 세기
    count_list = [1, 2, 2, 3, 2, 4]
    count_2 = operator.countOf(count_list, 2)
    print(f"2의 개수: {count_2}")  # 출력: 2의 개수: 3

    # indexOf로 인덱스 찾기
    try:
        index_3 = operator.indexOf(test_list, 3)
        print(f"3의 인덱스: {index_3}")  # 출력: 3의 인덱스: 2
    except ValueError:
        print("찾는 값이 없습니다.")
    print()

    # 6. 비트 연산자 활용
    print("6. 🔀 비트 연산자 활용")

    # 플래그 관리 예제
    class Permission:
        READ = 1  # 001
        WRITE = 2  # 010
        EXECUTE = 4  # 100

    # 권한 설정
    user_permission = Permission.READ
    print(f"초기 권한: {user_permission:03b}")

    # 쓰기 권한 추가
    user_permission = operator.or_(user_permission, Permission.WRITE)
    print(f"쓰기 추가 후: {user_permission:03b}")

    # 실행 권한 추가
    user_permission = operator.or_(user_permission, Permission.EXECUTE)
    print(f"실행 추가 후: {user_permission:03b}")

    # 권한 확인
    has_read = operator.and_(user_permission, Permission.READ) != 0
    has_write = operator.and_(user_permission, Permission.WRITE) != 0
    has_execute = operator.and_(user_permission, Permission.EXECUTE) != 0

    print(f"읽기 권한: {has_read}, 쓰기 권한: {has_write}, 실행 권한: {has_execute}")

    # 권한 제거 (XOR 활용)
    user_permission = operator.xor(user_permission, Permission.WRITE)
    print(f"쓰기 권한 제거 후: {user_permission:03b}")
    print()

    # 7. 실전 활용 예제: 데이터 처리 파이프라인
    print("7. 🚀 실전 활용: 데이터 처리 파이프라인")

    sales_data = [
        {'product': 'laptop', 'price': 1200, 'quantity': 3, 'region': 'north'},
        {'product': 'mouse', 'price': 25, 'quantity': 50, 'region': 'south'},
        {'product': 'keyboard', 'price': 80, 'quantity': 20, 'region': 'north'},
        {'product': 'monitor', 'price': 300, 'quantity': 8, 'region': 'east'},
        {'product': 'laptop', 'price': 1200, 'quantity': 2, 'region': 'south'}
    ]

    # 총액 계산 함수
    def calculate_total(item):
        return operator.mul(item['price'], item['quantity'])

    # 각 아이템의 총액 계산
    totals = list(map(calculate_total, sales_data))
    print(f"각 항목 총액: {totals}")

    # 전체 매출 합계
    total_sales = reduce(operator.add, totals)
    print(f"전체 매출: ${total_sales:,}")

    # 지역별 매출 (groupby 대신 딕셔너리 활용)
    regional_sales = {}
    for item in sales_data:
        region = item['region']
        total = calculate_total(item)
        regional_sales[region] = operator.add(regional_sales.get(region, 0), total)

    print("지역별 매출:")
    for region, sales in sorted(regional_sales.items(), key=operator.itemgetter(1), reverse=True):
        print(f"  {region}: ${sales:,}")

    # 고가 상품 필터링 (가격 100 이상)
    expensive_items = list(filter(lambda x: operator.ge(x['price'], 100), sales_data))
    print(f"\n고가 상품 수: {len(expensive_items)}")

    # 최고가 상품 찾기
    most_expensive = max(sales_data, key=operator.itemgetter('price'))
    print(f"최고가 상품: {most_expensive['product']} (${most_expensive['price']})")


def demonstrate_advanced_patterns():
    """고급 패턴 시연"""

    print("\n=== 고급 활용 패턴 ===\n")

    # 1. 함수 컴포지션
    print("1. 🔗 함수 컴포지션")

    def compose(*functions):
        """함수들을 조합하는 컴포지션 함수"""
        return reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)

    # 데이터 변환 파이프라인
    data = [1, 2, 3, 4, 5]

    # 제곱 → 2배 → 10 더하기
    transform = compose(
        partial(operator.add, 10),  # 10 더하기
        partial(operator.mul, 2),  # 2배
        lambda x: operator.pow(x, 2)  # 제곱
    )

    transformed = list(map(transform, data))
    print(f"변환 결과: {transformed}")  # 출력: 변환 결과: [12, 18, 28, 42, 60]
    print()

    # 2. 조건부 연산자 체이닝
    print("2. ⛓️ 조건부 연산자 체이닝")

    def conditional_operator(condition, true_op, false_op, *args):
        """조건에 따라 다른 연산자 적용"""
        return true_op(*args) if condition else false_op(*args)

    numbers = [1, -2, 3, -4, 5]

    # 음수면 절댓값, 양수면 제곱
    processed = []
    for num in numbers:
        result = conditional_operator(
            operator.lt(num, 0),  # 조건: 0보다 작은가
            operator.abs,  # True일 때: 절댓값
            lambda x: operator.pow(x, 2),  # False일 때: 제곱
            num
        )
        processed.append(result)

    print(f"조건부 처리 결과: {processed}")  # 출력: 조건부 처리 결과: [1, 2, 9, 4, 25]
    print()

    # 3. 성능 최적화 패턴
    print("3. ⚡ 성능 최적화 패턴")

    # 큰 데이터셋으로 성능 비교
    large_data = list(range(1000000))

    # 방법 1: 람다 함수
    start_time = time.time()
    sum1 = reduce(lambda x, y: x + y, large_data)
    lambda_time = time.time() - start_time

    # 방법 2: operator 함수
    start_time = time.time()
    sum2 = reduce(operator.add, large_data)
    operator_time = time.time() - start_time

    print(f"람다 함수 시간: {lambda_time:.4f}초")
    print(f"operator 시간: {operator_time:.4f}초")
    print(f"성능 향상: {lambda_time / operator_time:.2f}배")
    print(f"결과 동일: {sum1 == sum2}")


def demonstrate_error_handling():
    """에러 처리 패턴"""

    print("\n=== 안전한 operator 사용 패턴 ===\n")

    def safe_operation(operation, *args, default=None):
        """안전한 연산 수행"""
        try:
            return operation(*args)
        except (TypeError, ValueError, ZeroDivisionError) as e:
            print(f"⚠️ 연산 오류: {e}")
            return default

    # 안전한 나눗셈
    test_cases = [
        (10, 2),  # 정상
        (10, 0),  # 0으로 나누기
        ("10", 2),  # 타입 오류
    ]

    print("안전한 나눗셈 테스트:")
    for a, b in test_cases:
        result = safe_operation(operator.truediv, a, b, default="오류")
        print(f"  {a} ÷ {b} = {result}")


if __name__ == "__main__":
    # 메인 시연 실행
    demonstrate_operator_module()
    demonstrate_advanced_patterns()
    demonstrate_error_handling()

    print("\n🎉 operator 모듈 완벽 활용 가이드 완료!")
