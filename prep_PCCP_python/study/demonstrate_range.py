# ============= Range 완벽 마스터 =============
import sys
import copy


def demonstrate_range():
    """Range의 모든 특징과 활용법"""

    print("=== 1. Range 기본 생성 및 특성 ===")

    # 다양한 Range 생성 방법
    range_examples = {
        "range(5)": list(range(5)),
        "range(2, 8)": list(range(2, 8)),
        "range(1, 10, 2)": list(range(1, 10, 2)),
        "range(10, 0, -1)": list(range(10, 0, -1)),
        "range(-5, 5)": list(range(-5, 5))
    }

    for desc, values in range_examples.items():
        print(f"{desc:>15}: {values}")

    # 메모리 효율성 비교
    print(f"\n=== 2. 메모리 효율성 비교 ===")

    # Range vs List 메모리 사용량
    large_range = range(1000000)
    large_list = list(range(1000000))

    print(f"range(1000000) 메모리: {sys.getsizeof(large_range):,} bytes")
    print(f"list(range(1000000)) 메모리: {sys.getsizeof(large_list):,} bytes")
    print(f"메모리 차이: {sys.getsizeof(large_list) / sys.getsizeof(large_range):.1f}배")

    # Range 객체의 특성
    print(f"\n=== 3. Range 객체 특성 ===")
    r = range(5, 20, 3)
    print(f"Range 객체: {r}")
    print(f"Start: {r.start}, Stop: {r.stop}, Step: {r.step}")
    print(f"길이: {len(r)}")
    print(f"인덱싱: r[2] = {r[2]}")
    print(f"슬라이싱: r[1:3] = {r[1:3]}")
    print(f"멤버십 테스트: 11 in r = {11 in r}")
    print(f"역순: reversed(r) = {list(reversed(r))}")

    # Range 실전 활용
    print(f"\n=== 4. Range 실전 활용 예제 ===")

    # 1. 구구단 출력
    def print_multiplication_table(n):
        """구구단 출력"""
        for i in range(1, 10):
            print(f"{n} x {i} = {n * i}")

    print("3단:")
    print_multiplication_table(3)

    # 2. 피보나치 수열 (Range 인덱스 활용)
    def fibonacci_with_range(n):
        """Range를 활용한 피보나치 수열"""
        if n <= 0:
            return []
        elif n == 1:
            return [0]
        elif n == 2:
            return [0, 1]

        fib = [0, 1]
        for i in range(2, n):
            fib.append(fib[i - 1] + fib[i - 2])
        return fib

    print(f"\n피보나치 수열 (10개): {fibonacci_with_range(10)}")

    # 3. 배치 처리
    def process_in_batches(data, batch_size):
        """데이터를 배치 단위로 처리"""
        batches = []
        for i in range(0, len(data), batch_size):
            batch = data[i:i + batch_size]
            batches.append(batch)
        return batches

    sample_data = list(range(25))
    batches = process_in_batches(sample_data, 7)
    print(f"\n배치 처리 (크기 7):")
    for i, batch in enumerate(batches):
        print(f"  배치 {i + 1}: {batch}")

    # 4. 좌표 생성 (2D Grid)
    def generate_2d_coordinates(width, height):
        """2D 좌표 생성"""
        coordinates = []
        for x in range(width):
            for y in range(height):
                coordinates.append((x, y))
        return coordinates

    coords = generate_2d_coordinates(4, 3)
    print(f"\n4x3 그리드 좌표: {coords}")


# Range 복사 특성 (불변 객체)
def demonstrate_range_copy():
    """Range 객체의 복사 특성"""

    print(f"\n=== Range 복사 특성 (불변 객체) ===")

    original_range = range(10)

    # Range는 불변 객체이므로 얕은/깊은 복사 구분 무의미
    shallow_copy = copy.copy(original_range)
    deep_copy = copy.deepcopy(original_range)

    print(f"원본 Range: {original_range}")
    print(f"얕은 복사: {shallow_copy}")
    print(f"깊은 복사: {deep_copy}")
    print(f"모든 ID 동일: {id(original_range) == id(shallow_copy) == id(deep_copy)}")
    print(f"Range는 불변이므로 참조 공유해도 안전함")

    # Range 연산의 불변성
    r1 = range(5)
    r2 = range(5, 10)

    # Range 객체는 연산을 지원하지 않음 (불변이므로)
    try:
        result = r1 + r2  # 이건 불가능
    except TypeError as e:
        print(f"Range 연결 불가: {e}")

    # 대신 리스트로 변환 후 연산
    combined = list(r1) + list(r2)
    print(f"리스트 변환 후 연결: {combined}")


demonstrate_range()
demonstrate_range_copy()
