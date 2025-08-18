#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python functools 모듈 완벽 활용 가이드 (수정 버전)
Python 3.12 호환 - 오류 수정됨
"""

import functools
import time
import operator
import threading
from typing import List, Dict, Any, Callable, Optional, Union, TypeVar, Generic
from dataclasses import dataclass, field
from enum import Enum
from abc import ABC, abstractmethod
import sys
import weakref

# 타입 힌트용 제네릭 타입
T = TypeVar('T')
R = TypeVar('R')


class OptimizationType(Enum):
    """최적화 타입 열거형"""
    CACHING = "캐싱"
    PARTIAL_APPLICATION = "부분 적용"
    MEMOIZATION = "메모이제이션"
    DISPATCH = "디스패치"
    COMPOSITION = "함수 합성"


@dataclass
class PerformanceMetric:
    """성능 측정 결과"""
    function_name: str
    execution_time: float
    memory_usage: int
    cache_hits: int = 0
    cache_misses: int = 0
    optimization_type: OptimizationType = OptimizationType.CACHING


def demonstrate_functools_module():
    """Python functools 모듈의 완벽한 활용 시연"""

    print("=== Python functools 모듈 완벽 활용 가이드 ===\n")

    # 1. functools.partial - 부분 함수 적용
    print("1. 🔧 functools.partial - 부분 함수 적용")

    def multiply(x, y, z=1):
        """세 수를 곱하는 함수"""
        return x * y * z

    # 일부 인수를 고정한 새로운 함수들 생성
    double = functools.partial(multiply, 2)  # x를 2로 고정
    triple = functools.partial(multiply, 3)  # x를 3로 고정
    square = functools.partial(multiply, z=1)  # z를 1로 고정 (기본값과 동일)

    print(f"원본 함수: multiply(5, 6, 2) = {multiply(5, 6, 2)}")  # 출력: 60
    print(f"double(10, 1) = {double(10, 1)}")  # 출력: 20
    print(f"triple(4, 1) = {triple(4, 1)}")  # 출력: 12

    # 실전 활용: 설정값이 고정된 로깅 함수
    def log_message(level, module, message):
        return f"[{level}] {module}: {message}"

    error_logger = functools.partial(log_message, "ERROR")
    info_logger = functools.partial(log_message, "INFO")
    db_error_logger = functools.partial(error_logger, "DATABASE")

    print(f"에러 로그: {db_error_logger('연결 실패')}")  # 출력: [ERROR] DATABASE: 연결 실패
    print(f"정보 로그: {info_logger('API', '서버 시작됨')}")  # 출력: [INFO] API: 서버 시작됨
    print()

    # 2. functools.reduce - 누적 연산
    print("2. 📊 functools.reduce - 누적 연산")

    numbers = [1, 2, 3, 4, 5]

    # 기본적인 reduce 사용
    sum_result = functools.reduce(operator.add, numbers)
    product_result = functools.reduce(operator.mul, numbers)
    max_result = functools.reduce(max, numbers)

    print(f"숫자 리스트: {numbers}")
    print(f"합계: {sum_result}")  # 출력: 15
    print(f"곱셈: {product_result}")  # 출력: 120
    print(f"최댓값: {max_result}")  # 출력: 5

    # 초기값과 함께 사용
    sum_with_initial = functools.reduce(operator.add, numbers, 100)
    print(f"초기값 100과 함께 합계: {sum_with_initial}")  # 출력: 115

    # 복잡한 데이터 구조 처리
    students = [
        {'name': '김철수', 'score': 85},
        {'name': '박영희', 'score': 92},
        {'name': '이민수', 'score': 78}
    ]

    def combine_scores(acc, student):
        acc['total_score'] += student['score']
        acc['count'] += 1
        acc['names'].append(student['name'])
        return acc

    initial_acc = {'total_score': 0, 'count': 0, 'names': []}
    result = functools.reduce(combine_scores, students, initial_acc)
    average_score = result['total_score'] / result['count']

    print(f"전체 학생: {', '.join(result['names'])}")  # 출력: 김철수, 박영희, 이민수
    print(f"평균 점수: {average_score:.1f}점")  # 출력: 85.0점
    print()

    # 3. functools.lru_cache - LRU 캐싱
    print("3. 🚀 functools.lru_cache - LRU 캐싱")

    # 피보나치 수열로 성능 비교
    def fibonacci_naive(n):
        """캐시 없는 피보나치 (느림)"""
        if n < 2:
            return n
        return fibonacci_naive(n - 1) + fibonacci_naive(n - 2)

    @functools.lru_cache(maxsize=128)
    def fibonacci_cached(n):
        """LRU 캐시 적용 피보나치 (빠름)"""
        if n < 2:
            return n
        return fibonacci_cached(n - 1) + fibonacci_cached(n - 2)

    # 성능 측정
    test_n = 30

    start_time = time.time()
    result_naive = fibonacci_naive(test_n)
    naive_time = time.time() - start_time

    start_time = time.time()
    result_cached = fibonacci_cached(test_n)
    cached_time = time.time() - start_time

    print(f"fibonacci({test_n}) 결과: {result_naive}")  # 출력: 832040
    print(f"캐시 없음: {naive_time:.4f}초")
    print(f"LRU 캐시: {cached_time:.4f}초")
    print(f"성능 향상: {naive_time / cached_time:.0f}배 빨라짐")

    # 캐시 통계 확인
    cache_info = fibonacci_cached.cache_info()
    print(f"캐시 통계: {cache_info}")

    # 캐시 지우기
    fibonacci_cached.cache_clear()
    print("캐시 초기화 완료")
    print()

    # 4. functools.cache - 무제한 캐싱 (Python 3.9+)
    print("4. ♾️ functools.cache - 무제한 캐싱")

    @functools.cache
    def expensive_computation(n):
        """비용이 많이 드는 계산 시뮬레이션"""
        time.sleep(0.01)  # 0.01초 지연으로 비용이 많이 드는 작업 시뮬레이션
        return n ** 3 + n ** 2 + n + 1

    # 첫 번째 호출 (실제 계산)
    start_time = time.time()
    result1 = expensive_computation(10)
    first_call_time = time.time() - start_time

    # 두 번째 호출 (캐시에서 반환)
    start_time = time.time()
    result2 = expensive_computation(10)
    second_call_time = time.time() - start_time

    print(f"첫 번째 호출: {result1}, 시간: {first_call_time:.4f}초")  # 출력: 1111
    print(f"두 번째 호출: {result2}, 시간: {second_call_time:.4f}초")
    print(f"캐시 효과: {first_call_time / second_call_time:.0f}배 빨라짐")
    print()

    # 5. functools.wraps - 데코레이터 메타데이터 보존
    print("5. 🏷️ functools.wraps - 데코레이터 메타데이터 보존")

    def timer_decorator(func):
        """실행 시간을 측정하는 데코레이터"""

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            print(f"  → {func.__name__} 실행 시간: {end_time - start_time:.4f}초")
            return result

        return wrapper

    def debug_decorator(func):
        """디버깅 정보를 출력하는 데코레이터 (wraps 없음)"""

        def wrapper(*args, **kwargs):
            print(f"  → 호출: {func.__name__}({args}, {kwargs})")
            return func(*args, **kwargs)

        return wrapper

    @timer_decorator
    def calculate_square(n):
        """숫자의 제곱을 계산합니다."""
        time.sleep(0.001)  # 짧은 지연
        return n ** 2

    @debug_decorator
    def calculate_cube(n):
        """숫자의 세제곱을 계산합니다."""
        return n ** 3

    # 함수 메타데이터 확인
    print("wraps 사용한 함수:")
    print(f"  함수명: {calculate_square.__name__}")
    print(f"  독스트링: {calculate_square.__doc__}")

    print("wraps 사용하지 않은 함수:")
    print(f"  함수명: {calculate_cube.__name__}")
    print(f"  독스트링: {calculate_cube.__doc__}")

    # 함수 실행
    result1 = calculate_square(5)
    result2 = calculate_cube(3)
    print(f"제곱 결과: {result1}, 세제곱 결과: {result2}")  # 출력: 25, 27
    print()

    # 6. functools.singledispatch - 단일 디스패치
    print("6. 🎯 functools.singledispatch - 단일 디스패치")

    @functools.singledispatch
    def process_data(data):
        """기본 데이터 처리 함수"""
        return f"처리할 수 없는 타입: {type(data)}"

    @process_data.register
    def _(data: str):
        """문자열 처리"""
        return f"문자열 처리: '{data}' (길이: {len(data)})"

    @process_data.register
    def _(data: list):
        """리스트 처리"""
        return f"리스트 처리: {len(data)}개 항목, 합계: {sum(data) if all(isinstance(x, (int, float)) for x in data) else 'N/A'}"

    @process_data.register
    def _(data: dict):
        """딕셔너리 처리"""
        return f"딕셔너리 처리: {len(data)}개 키, 키 목록: {list(data.keys())}"

    @process_data.register
    def _(data: int):
        """정수 처리"""
        return f"정수 처리: {data} ({'짝수' if data % 2 == 0 else '홀수'})"

    # 다양한 타입으로 테스트
    test_cases = [
        "Hello World",
        [1, 2, 3, 4, 5],
        {"name": "김철수", "age": 25, "city": "서울"},
        42,
        3.14,  # float는 등록되지 않음
    ]

    for data in test_cases:
        result = process_data(data)
        print(f"입력: {data} → {result}")
    print()

    # 7. functools.cached_property - 프로퍼티 캐싱
    print("7. 🏠 functools.cached_property - 프로퍼티 캐싱")

    class DataProcessor:
        """데이터 처리 클래스 (비용이 많이 드는 계산 포함)"""

        def __init__(self, data):
            self.data = data

        @functools.cached_property
        def expensive_calculation(self):
            """비용이 많이 드는 계산 (한 번만 실행됨)"""
            print("  → 비용이 많이 드는 계산 실행 중...")
            time.sleep(0.01)  # 시뮬레이션
            return sum(x ** 2 for x in self.data)

        @property
        def normal_calculation(self):
            """일반 프로퍼티 (매번 실행됨)"""
            print("  → 일반 계산 실행 중...")
            return sum(x for x in self.data)

    processor = DataProcessor([1, 2, 3, 4, 5])

    print("첫 번째 expensive_calculation 호출:")
    result1 = processor.expensive_calculation

    print("두 번째 expensive_calculation 호출:")
    result2 = processor.expensive_calculation

    print("첫 번째 normal_calculation 호출:")
    result3 = processor.normal_calculation

    print("두 번째 normal_calculation 호출:")
    result4 = processor.normal_calculation

    print(f"캐시된 결과: {result1}, 일반 결과: {result3}")  # 출력: 55, 15
    print()

    # 8. functools.total_ordering - 비교 연산자 자동 생성
    print("8. ⚖️ functools.total_ordering - 비교 연산자 자동 생성")

    @functools.total_ordering
    class Student:
        """학생 클래스 (성적 기준 비교)"""

        def __init__(self, name: str, score: int):
            self.name = name
            self.score = score

        def __eq__(self, other):
            if not isinstance(other, Student):
                return NotImplemented
            return self.score == other.score

        def __lt__(self, other):
            if not isinstance(other, Student):
                return NotImplemented
            return self.score < other.score

        def __repr__(self):
            return f"Student('{self.name}', {self.score})"

    # 학생 객체 생성
    students = [
        Student("김철수", 85),
        Student("박영희", 92),
        Student("이민수", 78),
        Student("정수진", 95)
    ]

    # 정렬 (total_ordering으로 모든 비교 연산자 사용 가능)
    sorted_students = sorted(students)
    print("성적순 정렬 (오름차순):")
    for student in sorted_students:
        print(f"  {student}")

    # 다양한 비교 연산자 테스트
    s1, s2 = students[0], students[1]
    print(f"\n비교 연산자 테스트:")
    print(f"{s1.name} == {s2.name}: {s1 == s2}")  # 출력: False
    print(f"{s1.name} < {s2.name}: {s1 < s2}")  # 출력: True
    print(f"{s1.name} > {s2.name}: {s1 > s2}")  # 출력: False
    print(f"{s1.name} <= {s2.name}: {s1 <= s2}")  # 출력: True
    print(f"{s1.name} >= {s2.name}: {s1 >= s2}")  # 출력: False
    print()


def demonstrate_advanced_functools_patterns():
    """고급 functools 패턴 시연 (수정 버전)"""

    print("=== 고급 functools 활용 패턴 ===\n")

    # 1. 함수 합성 패턴
    print("1. 🔗 함수 합성 패턴")

    def compose(*functions):
        """여러 함수를 합성하는 함수"""
        return functools.reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)

    # 개별 함수들
    def add_ten(x):
        return x + 10

    def multiply_by_two(x):
        return x * 2

    def square(x):
        return x ** 2

    # 함수 합성
    composed_function = compose(square, multiply_by_two, add_ten)

    result = composed_function(5)  # ((5 + 10) * 2) ** 2 = (15 * 2) ** 2 = 30 ** 2 = 900
    print(f"합성 함수 결과: compose(square, multiply_by_two, add_ten)(5) = {result}")  # 출력: 900

    # 데이터 파이프라인 예제
    def clean_text(text):
        return text.strip().lower()

    def remove_punctuation(text):
        import string
        return text.translate(str.maketrans('', '', string.punctuation))

    def count_words(text):
        return len(text.split())

    text_processor = compose(count_words, remove_punctuation, clean_text)

    sample_text = "  Hello, World! This is a Test.  "
    word_count = text_processor(sample_text)
    print(f"텍스트 처리 파이프라인: '{sample_text}' → {word_count}개 단어")  # 출력: 5개 단어
    print()

    # 2. 메모이제이션 패턴 고도화
    print("2. 🧠 고급 메모이제이션 패턴")

    class SmartCache:
        """스마트 캐시 데코레이터"""

        def __init__(self, maxsize=128, ttl=60):
            self.maxsize = maxsize
            self.ttl = ttl  # Time To Live (초)
            self.cache = {}
            self.timestamps = {}

        def __call__(self, func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                # 캐시 키 생성
                key = str(args) + str(sorted(kwargs.items()))
                current_time = time.time()

                # TTL 확인
                if key in self.cache:
                    if current_time - self.timestamps[key] < self.ttl:
                        return self.cache[key]
                    else:
                        # TTL 만료, 캐시에서 제거
                        del self.cache[key]
                        del self.timestamps[key]

                # 새로운 결과 계산
                result = func(*args, **kwargs)

                # 캐시 크기 제한 확인
                if len(self.cache) >= self.maxsize:
                    # 가장 오래된 항목 제거 (LRU 방식)
                    oldest_key = min(self.timestamps.keys(), key=self.timestamps.get)
                    del self.cache[oldest_key]
                    del self.timestamps[oldest_key]

                # 캐시에 저장
                self.cache[key] = result
                self.timestamps[key] = current_time

                return result

            wrapper.cache_info = lambda: {
                'cache_size': len(self.cache),
                'maxsize': self.maxsize,
                'ttl': self.ttl
            }
            wrapper.cache_clear = lambda: (self.cache.clear(), self.timestamps.clear())

            return wrapper

    @SmartCache(maxsize=5, ttl=2)  # 2초 TTL
    def fetch_data(user_id):
        """데이터베이스에서 사용자 데이터를 가져오는 시뮬레이션"""
        print(f"  → 데이터베이스에서 사용자 {user_id} 데이터 조회 중...")
        time.sleep(0.01)  # DB 조회 시뮬레이션
        return {"user_id": user_id, "name": f"User{user_id}", "timestamp": time.time()}

    # 스마트 캐시 테스트
    print("첫 번째 호출 (DB 조회):")
    result1 = fetch_data(123)

    print("두 번째 호출 (캐시 사용):")
    result2 = fetch_data(123)

    print("2.1초 후 호출 (TTL 만료, 다시 DB 조회):")
    time.sleep(2.1)
    result3 = fetch_data(123)

    cache_info = fetch_data.cache_info()
    print(f"캐시 정보: {cache_info}")
    print()

    # 3. 함수형 프로그래밍 패턴 (수정된 버전)
    print("3. 🎭 함수형 프로그래밍 패턴")

    # Currying 패턴
    def curry(func):
        """함수를 커링하는 데코레이터"""

        @functools.wraps(func)
        def curried(*args, **kwargs):
            if len(args) + len(kwargs) >= func.__code__.co_argcount:
                return func(*args, **kwargs)
            return functools.partial(curried, *args, **kwargs)

        return curried

    @curry
    def add_three_numbers(a, b, c):
        """세 수를 더하는 함수"""
        return a + b + c

    # 커링 사용 예제
    add_5 = add_three_numbers(5)
    add_5_and_3 = add_5(3)
    final_result = add_5_and_3(2)

    print(f"커링 결과: add_three_numbers(5)(3)(2) = {final_result}")  # 출력: 10

    # 부분 적용을 이용한 설정 패턴 (수정된 버전)
    def create_api_client(base_url, endpoint, method='GET', timeout=30, retries=3):
        """API 클라이언트 시뮬레이션 (인수 순서 수정)"""
        return {
            'url': f"{base_url}/{endpoint}",
            'method': method,
            'timeout': timeout,
            'retries': retries
        }

    # 특정 API를 위한 클라이언트 팩토리 (수정된 버전)
    production_api = functools.partial(
        create_api_client,
        "https://api.production.com",
        timeout=30,
        retries=3
    )

    dev_api = functools.partial(
        create_api_client,
        "https://api.dev.com",
        timeout=5,
        retries=1
    )

    # 사용 예제 (수정된 버전)
    prod_user_client = production_api("users", method="GET")
    dev_data_client = dev_api("data", method="POST")

    print(f"운영 API 클라이언트: {prod_user_client}")
    print(f"개발 API 클라이언트: {dev_data_client}")


def demonstrate_performance_optimization():
    """성능 최적화 사례 시연"""

    print("\n=== functools 성능 최적화 사례 ===\n")

    # 1. 비용이 많이 드는 연산 최적화
    print("1. 💰 비용이 많이 드는 연산 최적화")

    def factorial_naive(n):
        """일반적인 팩토리얼 (재귀)"""
        if n <= 1:
            return 1
        return n * factorial_naive(n - 1)

    @functools.lru_cache(maxsize=None)
    def factorial_cached(n):
        """캐시된 팩토리얼"""
        if n <= 1:
            return 1
        return n * factorial_cached(n - 1)

    # 성능 비교
    test_values = [10, 15, 20]

    for n in test_values:
        # 일반 버전
        start = time.time()
        result_naive = factorial_naive(n)
        naive_time = time.time() - start

        # 캐시 버전 (첫 번째 호출)
        start = time.time()
        result_cached = factorial_cached(n)
        cached_time = time.time() - start

        # 캐시 버전 (두 번째 호출)
        start = time.time()
        result_cached_2nd = factorial_cached(n)
        cached_2nd_time = time.time() - start

        print(f"factorial({n}):")
        print(f"  일반: {naive_time:.6f}초")
        print(f"  캐시 (첫 호출): {cached_time:.6f}초")
        print(f"  캐시 (재호출): {cached_2nd_time:.6f}초")
        if cached_2nd_time > 0:
            print(f"  성능 향상: {naive_time / cached_2nd_time:.0f}배")
        else:
            print(f"  성능 향상: 매우 큼 (거의 즉시 반환)")

    print(f"캐시 통계: {factorial_cached.cache_info()}")
    print()

    # 2. 대용량 데이터 처리 최적화
    print("2. 📈 대용량 데이터 처리 최적화")

    # 큰 데이터셋 생성
    large_dataset = list(range(100000))  # 1백만 → 10만으로 수정 (실행 시간 단축)

    # reduce vs 내장 함수 성능 비교
    print("대용량 데이터 (100,000개 요소) 처리:")

    # sum() 내장 함수
    start = time.time()
    result_builtin = sum(large_dataset)
    builtin_time = time.time() - start

    # functools.reduce
    start = time.time()
    result_reduce = functools.reduce(operator.add, large_dataset)
    reduce_time = time.time() - start

    print(f"  내장 sum(): {builtin_time:.4f}초")
    print(f"  functools.reduce(): {reduce_time:.4f}초")
    print(f"  결과 동일: {result_builtin == result_reduce}")
    if builtin_time > 0:
        print(f"  성능 차이: {reduce_time / builtin_time:.2f}배")
    else:
        print(f"  성능 차이: 측정하기 어려울 정도로 빠름")


if __name__ == "__main__":
    # 메인 시연 실행
    demonstrate_functools_module()
    demonstrate_advanced_functools_patterns()
    demonstrate_performance_optimization()

    print("\n🎉 functools 모듈 완벽 활용 가이드 완료!")
