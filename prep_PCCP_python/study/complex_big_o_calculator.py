#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
알고리즘 복잡도 계산 및 분석 클래스
Python 3.12 호환
"""

import time
import tracemalloc
import functools
import inspect
from typing import Callable, Dict, List, Tuple, Any, Optional, Union
from dataclasses import dataclass
from enum import Enum
import math


class ComplexityType(Enum):
    """복잡도 유형 열거형"""
    CONSTANT = "O(1)"
    LOGARITHMIC = "O(log n)"
    LINEAR = "O(n)"
    LINEARITHMIC = "O(n log n)"
    QUADRATIC = "O(n²)"
    CUBIC = "O(n³)"
    EXPONENTIAL = "O(2^n)"
    FACTORIAL = "O(n!)"


@dataclass
class PerformanceResult:
    """성능 측정 결과"""
    input_size: int
    execution_time: float
    memory_usage: int
    function_name: str
    complexity_estimate: Optional[str] = None


class ComplexityCalculator:
    """알고리즘 복잡도 계산 및 분석 클래스"""

    def __init__(self):
        """복잡도 계산기 초기화"""
        self.results: List[PerformanceResult] = []
        self.complexity_patterns = {
            ComplexityType.CONSTANT: lambda n: 1,
            ComplexityType.LOGARITHMIC: lambda n: math.log2(n) if n > 0 else 0,
            ComplexityType.LINEAR: lambda n: n,
            ComplexityType.LINEARITHMIC: lambda n: n * math.log2(n) if n > 0 else 0,
            ComplexityType.QUADRATIC: lambda n: n ** 2,
            ComplexityType.CUBIC: lambda n: n ** 3,
            ComplexityType.EXPONENTIAL: lambda n: 2 ** min(n, 20),  # 제한된 지수
            ComplexityType.FACTORIAL: lambda n: math.factorial(min(n, 10))  # 제한된 팩토리얼
        }

    def measure_performance(
            self,
            func: Callable,
            input_sizes: List[int],
            data_generator: Optional[Callable[[int], Any]] = None
    ) -> List[PerformanceResult]:
        """
        함수의 성능을 다양한 입력 크기에 대해 측정

        Args:
            func: 측정할 함수
            input_sizes: 테스트할 입력 크기들
            data_generator: 입력 데이터 생성 함수

        Returns:
            성능 측정 결과 리스트
        """
        if not callable(func):
            raise ValueError("func는 호출 가능한 객체여야 합니다.")

        if not input_sizes:
            raise ValueError("input_sizes는 비어있을 수 없습니다.")

        results = []

        # 기본 데이터 생성기 (리스트)
        if data_generator is None:
            data_generator = lambda n: list(range(n))

        for size in input_sizes:
            if size < 0:
                print(f"경고: 음수 입력 크기 {size} 건너뛰기")
                continue

            try:
                # 입력 데이터 생성
                test_data = data_generator(size)

                # 메모리 추적 시작
                tracemalloc.start()

                # 시간 측정
                start_time = time.perf_counter()

                # 함수 실행
                if inspect.signature(func).parameters:
                    result = func(test_data)
                else:
                    result = func()

                end_time = time.perf_counter()

                # 메모리 사용량 측정
                current, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()

                # 결과 저장
                perf_result = PerformanceResult(
                    input_size=size,
                    execution_time=end_time - start_time,
                    memory_usage=peak,
                    function_name=func.__name__
                )

                results.append(perf_result)

            except Exception as e:
                print(f"크기 {size}에서 오류 발생: {e}")
                continue

        self.results.extend(results)
        return results

    def estimate_complexity(self, results: List[PerformanceResult]) -> str:
        """
        측정 결과로부터 시간 복잡도 추정

        Args:
            results: 성능 측정 결과

        Returns:
            추정된 복잡도 문자열
        """
        if len(results) < 2:
            return "데이터 부족: 복잡도 추정 불가"

        # 입력 크기와 실행 시간 추출
        sizes = [r.input_size for r in results if r.input_size > 0]
        times = [r.execution_time for r in results if r.input_size > 0]

        if len(sizes) < 2:
            return "유효한 데이터 부족"

        best_fit = None
        best_error = float('inf')

        # 각 복잡도 패턴과 비교
        for complexity_type, pattern_func in self.complexity_patterns.items():
            try:
                # 패턴 값 계산
                pattern_values = [pattern_func(n) for n in sizes]

                # 정규화를 위해 최대값으로 나누기
                if max(pattern_values) > 0 and max(times) > 0:
                    normalized_pattern = [v / max(pattern_values) for v in pattern_values]
                    normalized_times = [t / max(times) for t in times]

                    # 평균 제곱 오차 계산
                    error = sum((p - t) ** 2 for p, t in zip(normalized_pattern, normalized_times)) / len(times)

                    if error < best_error:
                        best_error = error
                        best_fit = complexity_type.value

            except (OverflowError, ValueError, ZeroDivisionError):
                continue

        return best_fit if best_fit else "복잡도 추정 실패"

    def analyze_space_complexity(self, results: List[PerformanceResult]) -> str:
        """
        공간 복잡도 분석

        Args:
            results: 성능 측정 결과

        Returns:
            공간 복잡도 추정 결과
        """
        if len(results) < 2:
            return "데이터 부족: 공간 복잡도 분석 불가"

        # 메모리 사용량 증가율 계산
        memory_ratios = []
        for i in range(1, len(results)):
            if results[i - 1].memory_usage > 0:
                size_ratio = results[i].input_size / results[i - 1].input_size
                memory_ratio = results[i].memory_usage / results[i - 1].memory_usage
                if size_ratio > 0:
                    memory_ratios.append(memory_ratio / size_ratio)

        if not memory_ratios:
            return "메모리 사용량 분석 불가"

        avg_ratio = sum(memory_ratios) / len(memory_ratios)

        # 비율에 따른 복잡도 추정
        if avg_ratio < 1.2:
            return "O(1) - 상수 공간"
        elif avg_ratio < 2.0:
            return "O(log n) - 로그 공간"
        elif avg_ratio < 3.0:
            return "O(n) - 선형 공간"
        else:
            return "O(n²) 이상 - 고차 공간"

    def benchmark_function(
            self,
            func: Callable,
            iterations: int = 100,
            input_size: int = 1000
    ) -> Dict[str, float]:
        """
        함수의 벤치마크 수행

        Args:
            func: 벤치마크할 함수
            iterations: 반복 횟수
            input_size: 입력 크기

        Returns:
            벤치마크 결과
        """
        if iterations <= 0:
            raise ValueError("iterations는 양수여야 합니다.")

        times = []
        test_data = list(range(input_size))

        for _ in range(iterations):
            try:
                start_time = time.perf_counter()
                if inspect.signature(func).parameters:
                    func(test_data)
                else:
                    func()
                end_time = time.perf_counter()
                times.append(end_time - start_time)
            except Exception as e:
                print(f"벤치마크 중 오류: {e}")
                continue

        if not times:
            return {"error": "모든 측정 실패"}

        return {
            "min_time": min(times),
            "max_time": max(times),
            "avg_time": sum(times) / len(times),
            "total_time": sum(times),
            "iterations": len(times)
        }

    def compare_algorithms(
            self,
            algorithms: Dict[str, Callable],
            input_sizes: List[int] = None
    ) -> Dict[str, Any]:
        """
        여러 알고리즘 성능 비교

        Args:
            algorithms: 비교할 알고리즘들 {이름: 함수}
            input_sizes: 테스트할 입력 크기들

        Returns:
            비교 결과
        """
        if not algorithms:
            raise ValueError("비교할 알고리즘이 없습니다.")

        if input_sizes is None:
            input_sizes = [100, 500, 1000, 2000, 5000]

        comparison_results = {}

        for name, func in algorithms.items():
            try:
                print(f"\n{name} 분석 중...")
                results = self.measure_performance(func, input_sizes)
                complexity = self.estimate_complexity(results)

                comparison_results[name] = {
                    "results": results,
                    "estimated_complexity": complexity,
                    "avg_time": sum(r.execution_time for r in results) / len(results) if results else 0,
                    "total_memory": sum(r.memory_usage for r in results) if results else 0
                }

            except Exception as e:
                print(f"{name} 분석 중 오류: {e}")
                comparison_results[name] = {"error": str(e)}

        return comparison_results

    def generate_report(self) -> str:
        """성능 분석 보고서 생성"""
        if not self.results:
            return "분석된 데이터가 없습니다."

        report = ["=== 성능 분석 보고서 ===\n"]

        # 함수별 그룹화
        functions = {}
        for result in self.results:
            if result.function_name not in functions:
                functions[result.function_name] = []
            functions[result.function_name].append(result)

        for func_name, func_results in functions.items():
            report.append(f"📊 함수: {func_name}")
            report.append(f"측정 횟수: {len(func_results)}")

            if func_results:
                times = [r.execution_time for r in func_results]
                memories = [r.memory_usage for r in func_results]

                report.append(f"평균 실행 시간: {sum(times) / len(times):.6f}초")
                report.append(f"최대 실행 시간: {max(times):.6f}초")
                report.append(f"평균 메모리 사용: {sum(memories) / len(memories):,} bytes")

                complexity = self.estimate_complexity(func_results)
                report.append(f"추정 시간 복잡도: {complexity}")

                space_complexity = self.analyze_space_complexity(func_results)
                report.append(f"추정 공간 복잡도: {space_complexity}")

            report.append("")

        return "\n".join(report)

    def clear_results(self) -> None:
        """저장된 결과 초기화"""
        self.results.clear()


# 데코레이터 함수들
def measure_time(calculator: ComplexityCalculator):
    """함수 실행 시간 측정 데코레이터"""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()

            # 입력 크기 추정
            input_size = 0
            if args:
                first_arg = args[0]
                if hasattr(first_arg, '__len__'):
                    input_size = len(first_arg)
                elif isinstance(first_arg, int):
                    input_size = first_arg

            perf_result = PerformanceResult(
                input_size=input_size,
                execution_time=end_time - start_time,
                memory_usage=0,  # 메모리는 별도 측정 필요
                function_name=func.__name__
            )

            calculator.results.append(perf_result)
            return result

        return wrapper

    return decorator


# 예제 사용법 및 테스트
def demo_algorithms():
    """데모용 알고리즘들"""

    def bubble_sort(arr):
        """버블 정렬 - O(n²)"""
        arr = arr.copy()
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr

    def linear_search(arr):
        """선형 탐색 - O(n)"""
        target = len(arr) // 2
        for i, item in enumerate(arr):
            if item == target:
                return i
        return -1

    def binary_search_wrapper(arr):
        """이진 탐색 래퍼 - O(log n)"""
        arr = sorted(arr)
        target = len(arr) // 2

        def binary_search(arr, target, left, right):
            if left > right:
                return -1

            mid = (left + right) // 2
            if arr[mid] == target:
                return mid
            elif arr[mid] > target:
                return binary_search(arr, target, left, mid - 1)
            else:
                return binary_search(arr, target, mid + 1, right)

        return binary_search(arr, target, 0, len(arr) - 1)

    return {
        "bubble_sort": bubble_sort,
        "linear_search": linear_search,
        "binary_search": binary_search_wrapper
    }


if __name__ == "__main__":
    # 복잡도 계산기 사용 예제
    print("=== ComplexityCalculator 사용 예제 ===\n")

    calculator = ComplexityCalculator()

    # 1. 단일 함수 성능 측정
    algorithms = demo_algorithms()

    print("1. 버블 정렬 성능 측정")
    bubble_results = calculator.measure_performance(
        algorithms["bubble_sort"],
        [100, 200, 500, 1000],
        lambda n: list(range(n, 0, -1))  # 역순 데이터
    )

    for result in bubble_results:
        print(f"크기 {result.input_size}: {result.execution_time:.6f}초")

    complexity = calculator.estimate_complexity(bubble_results)
    print(f"추정 복잡도: {complexity}\n")

    # 2. 알고리즘 비교
    print("2. 알고리즘 성능 비교")
    comparison = calculator.compare_algorithms(
        algorithms,
        [100, 300, 500, 800, 1000]
    )

    for name, data in comparison.items():
        if "error" not in data:
            print(f"{name}: {data['estimated_complexity']}")
        else:
            print(f"{name}: 오류 - {data['error']}")

    print("\n3. 종합 보고서")
    print(calculator.generate_report())
