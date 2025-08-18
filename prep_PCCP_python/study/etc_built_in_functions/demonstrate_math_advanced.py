#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python math 모듈 고급 활용 가이드 (튜플 오류 수정 버전)
Python 3.12 호환 - 튜플 포맷 오류 수정됨
"""

import math
import cmath  # 복소수 수학
import statistics
from typing import List, Tuple, Union, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import time
import random


class MathCategory(Enum):
    """수학 함수 카테고리 열거형"""
    TRIGONOMETRIC = "삼각함수"
    LOGARITHMIC = "로그함수"
    EXPONENTIAL = "지수함수"
    HYPERBOLIC = "쌍곡함수"
    SPECIAL = "특수함수"
    STATISTICAL = "통계함수"
    CONSTANTS = "수학상수"
    CONVERSION = "변환함수"


@dataclass
class MathResult:
    """수학 계산 결과"""
    function_name: str
    input_value: Union[float, int, complex]
    result: Union[float, int, complex]
    category: MathCategory
    execution_time: float = 0.0


class MathUtils:
    """수학 유틸리티 클래스"""

    # 수학 상수들
    CONSTANTS = {
        'π (pi)': math.pi,
        'e (자연상수)': math.e,
        'τ (tau)': math.tau,
        '황금비': (1 + math.sqrt(5)) / 2,
        '오일러 상수': 0.5772156649015329,
        '∞ (무한대)': math.inf,
        'NaN': math.nan
    }

    @staticmethod
    def safe_divide(a: float, b: float) -> float:
        """안전한 나눗셈 (0으로 나누기 방지)"""
        if b == 0:
            return math.inf if a > 0 else -math.inf if a < 0 else math.nan
        return a / b

    @staticmethod
    def is_safe_number(value: float) -> bool:
        """안전한 숫자인지 확인"""
        return math.isfinite(value) and not math.isnan(value)


def demonstrate_math_advanced():
    """Python math 모듈의 고급 활용 시연"""

    print("=== Python math 모듈 고급 활용 가이드 ===\n")

    # 1. 수학 상수들
    print("1. 📐 수학 상수들")
    for name, value in MathUtils.CONSTANTS.items():
        if math.isfinite(value):
            print(f"{name}: {value:.10f}")
        else:
            print(f"{name}: {value}")

    # 실전 활용: 원의 넓이와 둘레
    radius = 5.5
    area = math.pi * radius ** 2
    circumference = 2 * math.pi * radius
    print(f"\n반지름 {radius}인 원:")
    print(f"  넓이: {area:.2f}")  # 출력: 95.03
    print(f"  둘레: {circumference:.2f}")  # 출력: 34.56
    print()

    # 2. 삼각함수 (각도 & 라디안)
    print("2. 📏 삼각함수 활용")

    # 각도를 라디안으로 변환
    angles_deg = [0, 30, 45, 60, 90, 180, 270, 360]
    print("각도(도) → 라디안 → sin, cos, tan")

    for angle_deg in angles_deg:
        angle_rad = math.radians(angle_deg)
        sin_val = math.sin(angle_rad)
        cos_val = math.cos(angle_rad)

        # tan(90°)는 무한대이므로 안전 처리
        try:
            tan_val = math.tan(angle_rad)
            tan_str = f"{tan_val:.4f}" if abs(tan_val) < 1000 else "∞"
        except:
            tan_str = "∞"

        print(f"{angle_deg:3d}° → {angle_rad:6.3f}rad → sin:{sin_val:7.4f}, cos:{cos_val:7.4f}, tan:{tan_str:>8s}")

    # 역삼각함수
    print("\n역삼각함수:")
    test_values = [0, 0.5, 0.707, 0.866, 1.0]
    for val in test_values:
        asin_deg = math.degrees(math.asin(val))
        acos_deg = math.degrees(math.acos(val))
        atan_deg = math.degrees(math.atan(val))
        print(
            f"arcsin({val:.3f}) = {asin_deg:5.1f}°, arccos({val:.3f}) = {acos_deg:5.1f}°, arctan({val:.3f}) = {atan_deg:5.1f}°")
    print()

    # 3. 로그와 지수함수
    print("3. 📈 로그와 지수함수")

    # 다양한 밑의 로그
    numbers = [1, 2, 10, 100, 1000]
    print("숫자  → log₂    log₁₀   ln(자연로그)")
    for num in numbers:
        log2_val = math.log2(num)
        log10_val = math.log10(num)
        ln_val = math.log(num)
        print(f"{num:4d} → {log2_val:7.3f} {log10_val:7.3f} {ln_val:11.3f}")

    # 지수함수
    print("\n지수함수:")
    exp_values = [0, 1, 2, 3, -1, -2]
    for x in exp_values:
        exp_val = math.exp(x)  # e^x
        exp2_val = math.pow(2, x)  # 2^x
        exp10_val = math.pow(10, x)  # 10^x
        print(f"x={x:2d} → e^x:{exp_val:8.3f}, 2^x:{exp2_val:8.3f}, 10^x:{exp10_val:8.3f}")
    print()

    # 4. 제곱근과 거듭제곱
    print("4. √ 제곱근과 거듭제곱")

    roots_numbers = [4, 8, 16, 27, 64, 125]
    print("숫자 → √    ∛(세제곱근) n^(1/5)")
    for num in roots_numbers:
        sqrt_val = math.sqrt(num)  # 제곱근
        cbrt_val = math.pow(num, 1 / 3)  # 세제곱근
        fifth_root = math.pow(num, 1 / 5)  # 5제곱근
        print(f"{num:3d} → {sqrt_val:6.3f} {cbrt_val:11.3f} {fifth_root:9.3f}")

    # 복잡한 거듭제곱
    print("\n복잡한 거듭제곱:")
    base_exp_pairs = [(2, 10), (3, 4), (5, 3), (10, 2)]
    for base, exp in base_exp_pairs:
        result = math.pow(base, exp)
        print(f"{base}^{exp} = {result:.0f}")  # 출력: 1024, 81, 125, 100
    print()

    # 5. 쌍곡함수 (Hyperbolic functions)
    print("5. 📊 쌍곡함수")

    hyp_values = [0, 0.5, 1, 1.5, 2]
    print("x    → sinh(x)  cosh(x)  tanh(x)")
    for x in hyp_values:
        sinh_val = math.sinh(x)
        cosh_val = math.cosh(x)
        tanh_val = math.tanh(x)
        print(f"{x:.1f} → {sinh_val:7.3f} {cosh_val:7.3f} {tanh_val:7.3f}")

    # 쌍곡함수 항등식 확인
    x = 1.5
    identity_check = math.cosh(x) ** 2 - math.sinh(x) ** 2
    print(f"\n쌍곡함수 항등식 확인: cosh²({x}) - sinh²({x}) = {identity_check:.10f} (≈ 1)")
    print()

    # 6. 특수 함수들
    print("6. ⭐ 특수 함수들")

    # 팩토리얼
    factorial_nums = [0, 1, 5, 10, 15]
    print("팩토리얼:")
    for n in factorial_nums:
        fact = math.factorial(n)
        print(f"{n}! = {fact:,}")  # 출력: 1, 1, 120, 3628800, 1307674368000

    # 조합과 순열
    print("\n조합 C(n,k):")
    combinations = [(10, 3), (5, 2), (8, 4)]
    for n, k in combinations:
        comb = math.comb(n, k)
        perm = math.perm(n, k)
        print(f"C({n},{k}) = {comb}, P({n},{k}) = {perm}")  # 출력: 120&720, 10&20, 70&1680

    # 최대공약수
    print("\n최대공약수 (GCD):")
    gcd_pairs = [(48, 18), (100, 25), (17, 13)]
    for a, b in gcd_pairs:
        gcd = math.gcd(a, b)
        lcm = abs(a * b) // gcd  # 최소공배수
        print(f"gcd({a}, {b}) = {gcd}, lcm({a}, {b}) = {lcm}")  # 출력: 6&144, 25&100, 1&221
    print()

    # 7. 수치 처리 함수들
    print("7. 🔢 수치 처리 함수들")

    # 반올림과 절사
    float_numbers = [3.14159, -2.71828, 5.999, -0.001, 12.5]
    print("숫자     → floor   ceil    trunc   round")
    for num in float_numbers:
        floor_val = math.floor(num)
        ceil_val = math.ceil(num)
        trunc_val = math.trunc(num)
        round_val = round(num)
        print(f"{num:8.5f} → {floor_val:5d} {ceil_val:6d} {trunc_val:7d} {round_val:7d}")

    # 절댓값과 부호
    print("\n절댓값과 부호:")
    signed_numbers = [-5, 3.14, -0.001, 0, -100]
    for num in signed_numbers:
        abs_val = abs(num)
        sign = math.copysign(1, num)  # 부호만 추출
        print(f"abs({num:6.3f}) = {abs_val:6.3f}, sign = {sign:4.0f}")
    print()

    # 8. 거리와 벡터 연산
    print("8. 📐 거리와 벡터 연산")

    # 2D 벡터들
    vectors_2d = [
        ((0, 0), (3, 4)),
        ((1, 1), (4, 5)),
        ((-2, -1), (1, 3))
    ]

    print("2D 벡터 거리:")
    for (x1, y1), (x2, y2) in vectors_2d:
        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        # 또는 math.hypot 사용
        distance_hypot = math.hypot(x2 - x1, y2 - y1)
        print(f"({x1},{y1}) → ({x2},{y2}): 거리 = {distance:.3f} (hypot: {distance_hypot:.3f})")

    # 3D 벡터 거리
    print("\n3D 벡터 거리:")
    vectors_3d = [
        ((0, 0, 0), (1, 1, 1)),
        ((2, 3, 1), (5, 7, 4))
    ]

    for (x1, y1, z1), (x2, y2, z2) in vectors_3d:
        distance_3d = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)
        print(f"({x1},{y1},{z1}) → ({x2},{y2},{z2}): 거리 = {distance_3d:.3f}")
    print()

    # 9. 복소수 수학 (cmath)
    print("9. 🌀 복소수 수학")

    # 복소수들
    complex_numbers = [1 + 2j, 3 - 4j, -2 + 5j, 0 + 1j]

    print("복소수    → 절댓값  각도(도)  지수형")
    for c in complex_numbers:
        magnitude = abs(c)
        phase_rad = cmath.phase(c)
        phase_deg = math.degrees(phase_rad)
        exponential = cmath.exp(cmath.log(c))
        print(f"{c:>8} → {magnitude:7.3f} {phase_deg:8.1f}° {exponential.real:6.3f}+{exponential.imag:5.3f}j")

    # 복소수 연산
    print("\n복소수 연산:")
    c1, c2 = 3 + 4j, 1 - 2j
    operations = {
        '덧셈': c1 + c2,
        '곱셈': c1 * c2,
        '나눗셈': c1 / c2,
        '거듭제곱': c1 ** 2,
        '제곱근': cmath.sqrt(c1)
    }

    for op_name, result in operations.items():
        print(f"{op_name}: {result:.3f}")
    print()


def demonstrate_practical_applications():
    """실전 수학 응용 예제"""

    print("=== 실전 수학 응용 예제 ===\n")

    # 1. 물리학 응용: 포물선 운동
    print("1. 🚀 물리학: 포물선 운동")

    def projectile_motion(v0: float, angle_deg: float, g: float = 9.81):
        """포물선 운동 계산"""
        angle_rad = math.radians(angle_deg)

        # 최대 높이
        max_height = (v0 * math.sin(angle_rad)) ** 2 / (2 * g)

        # 비행 시간
        flight_time = 2 * v0 * math.sin(angle_rad) / g

        # 최대 사거리
        max_range = v0 ** 2 * math.sin(2 * angle_rad) / g

        return max_height, flight_time, max_range

    # 다양한 각도로 발사
    initial_velocity = 50  # m/s
    angles = [15, 30, 45, 60, 75]

    print(f"초기 속도 {initial_velocity} m/s로 발사:")
    print("각도  → 최대높이  비행시간  최대사거리")
    for angle in angles:
        height, time, range_val = projectile_motion(initial_velocity, angle)
        print(f"{angle:2d}° → {height:7.1f}m {time:7.1f}s {range_val:9.1f}m")
    print()

    # 2. 금융 수학: 복리 계산 (수정된 버전)
    print("2. 💰 금융 수학: 복리 계산")

    def compound_interest(principal: float, rate: float, times: int, years: float) -> float:
        """복리 계산 - 최종 금액만 반환 (수정됨)"""
        amount = principal * (1 + rate / times) ** (times * years)
        return amount  # 튜플이 아닌 float 반환

    def continuous_compound(principal: float, rate: float, years: float) -> float:
        """연속 복리 계산 - float 반환"""
        amount = principal * math.exp(rate * years)
        return amount

    # 투자 시나리오
    principal = 1000000  # 100만원
    annual_rate = 0.05  # 5%
    years = [1, 5, 10, 20, 30]

    print(f"원금 {principal:,}원, 연 {annual_rate * 100}% 이율:")
    print("기간 → 연복리        월복리        연속복리")

    for year in years:
        annual = compound_interest(principal, annual_rate, 1, year)
        monthly = compound_interest(principal, annual_rate, 12, year)
        continuous = continuous_compound(principal, annual_rate, year)

        # 수정된 포맷: 이제 float 값이므로 정상 작동
        print(f"{year:2d}년 → {annual:10,.0f}원 {monthly:10,.0f}원 {continuous:12,.0f}원")
    print()

    # 3. 통계학: 정규분포 근사
    print("3. 📊 통계학: 표준정규분포 근사")

    def standard_normal_pdf(x: float) -> float:
        """표준정규분포 확률밀도함수"""
        return (1 / math.sqrt(2 * math.pi)) * math.exp(-0.5 * x ** 2)

    def standard_normal_cdf_approx(x: float) -> float:
        """표준정규분포 누적분포함수 근사"""
        # 간단한 근사식 사용
        if x >= 0:
            return 0.5 + 0.5 * math.sqrt(1 - math.exp(-2 * x ** 2 / math.pi))
        else:
            return 1 - standard_normal_cdf_approx(-x)

    z_values = [-3, -2, -1, 0, 1, 2, 3]
    print("Z값 → PDF      CDF(근사)")
    for z in z_values:
        pdf_val = standard_normal_pdf(z)
        cdf_val = standard_normal_cdf_approx(z)
        print(f"{z:2d}  → {pdf_val:.4f}  {cdf_val:.4f}")
    print()

    # 4. 컴퓨터 그래픽스: 회전 변환
    print("4. 🎮 컴퓨터 그래픽스: 2D 회전 변환")

    def rotate_point(x: float, y: float, angle_deg: float, cx: float = 0, cy: float = 0):
        """점을 중심점 기준으로 회전"""
        angle_rad = math.radians(angle_deg)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)

        # 중심점으로 이동
        x_translated = x - cx
        y_translated = y - cy

        # 회전
        x_rotated = x_translated * cos_a - y_translated * sin_a
        y_rotated = x_translated * sin_a + y_translated * cos_a

        # 원래 위치로 이동
        x_final = x_rotated + cx
        y_final = y_rotated + cy

        return x_final, y_final

    # 정사각형의 꼭짓점들을 원점 기준으로 회전
    square_points = [(1, 1), (-1, 1), (-1, -1), (1, -1)]
    rotation_angles = [0, 45, 90, 180]

    print("정사각형 회전 (원점 기준):")
    for angle in rotation_angles:
        print(f"{angle:3d}° 회전:")
        for i, (x, y) in enumerate(square_points):
            x_rot, y_rot = rotate_point(x, y, angle)
            print(f"  점{i + 1}: ({x:2.0f}, {y:2.0f}) → ({x_rot:6.2f}, {y_rot:6.2f})")
        print()


def demonstrate_numerical_methods():
    """수치해석 방법 시연"""

    print("=== 수치해석 방법 시연 ===\n")

    # 1. 뉴턴-랩슨 방법으로 제곱근 구하기
    print("1. 🔍 뉴턴-랩슨 방법: 제곱근 계산")

    def newton_sqrt(n: float, precision: float = 1e-10) -> Tuple[float, int]:
        """뉴턴-랩슨 방법으로 제곱근 계산"""
        if n < 0:
            raise ValueError("음수의 제곱근은 계산할 수 없습니다.")

        if n == 0:
            return 0.0, 0

        x = n / 2  # 초기 추정값
        iterations = 0

        while True:
            root = 0.5 * (x + n / x)
            iterations += 1

            if abs(root - x) < precision:
                return root, iterations

            x = root

    # 다양한 수의 제곱근 계산
    test_numbers = [2, 10, 50, 100, 1000]
    print("숫자 → 뉴턴방법      내장함수      반복횟수  오차")

    for num in test_numbers:
        newton_result, iterations = newton_sqrt(num)
        builtin_result = math.sqrt(num)
        error = abs(newton_result - builtin_result)

        print(f"{num:4d} → {newton_result:11.8f} {builtin_result:11.8f} {iterations:7d}  {error:.2e}")
    print()

    # 2. 몬테카를로 방법으로 π 추정
    print("2. 🎯 몬테카를로 방법: π 추정")

    def estimate_pi_monte_carlo(num_points: int) -> Tuple[float, float]:
        """몬테카를로 방법으로 π 추정"""
        inside_circle = 0

        for _ in range(num_points):
            x = random.uniform(-1, 1)
            y = random.uniform(-1, 1)

            if x * x + y * y <= 1:
                inside_circle += 1

        pi_estimate = 4 * inside_circle / num_points
        error = abs(pi_estimate - math.pi)

        return pi_estimate, error

    # 다양한 표본 크기로 π 추정
    sample_sizes = [1000, 10000, 100000, 1000000]
    print("표본수    → π 추정값    오차      정확도")

    for size in sample_sizes:
        pi_est, error = estimate_pi_monte_carlo(size)
        accuracy = (1 - error / math.pi) * 100
        print(f"{size:8,} → {pi_est:.6f}  {error:.6f}  {accuracy:6.2f}%")
    print()

    # 3. 적분 계산: 사다리꼴 공식
    print("3. ∫ 수치적분: 사다리꼴 공식")

    def trapezoidal_integration(func: Callable[[float], float],
                                a: float, b: float, n: int) -> float:
        """사다리꼴 공식으로 정적분 계산"""
        h = (b - a) / n
        result = 0.5 * (func(a) + func(b))

        for i in range(1, n):
            x = a + i * h
            result += func(x)

        return result * h

    # 여러 함수의 적분 계산
    functions = [
        (lambda x: x ** 2, 0, 1, 1 / 3, "x²"),
        (lambda x: math.sin(x), 0, math.pi, 2, "sin(x)"),
        (lambda x: math.exp(-x ** 2), -2, 2, math.sqrt(math.pi), "e^(-x²)")
    ]

    print("함수    구간     → 수치해      해석해      오차")
    subdivisions = 1000

    for func, a, b, analytical, name in functions:
        numerical = trapezoidal_integration(func, a, b, subdivisions)
        error = abs(numerical - analytical)
        print(f"{name:6s} [{a:2.0f},{b:2.0f}] → {numerical:9.6f}  {analytical:9.6f}  {error:.2e}")


if __name__ == "__main__":
    # 메인 시연 실행
    demonstrate_math_advanced()
    demonstrate_practical_applications()
    demonstrate_numerical_methods()

    print("\n🎉 math 모듈 고급 활용 가이드 완료!")
