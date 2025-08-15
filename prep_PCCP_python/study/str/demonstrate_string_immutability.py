# ============= 문자열 불변성 완벽 이해 =============
def demonstrate_string_immutability():
    """문자열 불변성의 모든 측면을 시연"""

    print("=== 문자열 불변성 증명 ===")

    # 1. 직접 수정 시도 (실패)
    original_string = "Hello"
    print(f"원본 문자열: {original_string}")
    print(f"원본 ID: {id(original_string)}")

    try:
        original_string[0] = 'h'  # TypeError 발생
    except TypeError as e:
        print(f"❌ 직접 수정 시도 실패: {e}")

    # 2. 문자열 "수정"은 실제로 새 객체 생성
    modified_string = original_string.replace('H', 'h')
    print(f"\n'수정'된 문자열: {modified_string}")
    print(f"'수정'된 문자열 ID: {id(modified_string)}")
    print(f"원본은 그대로: {original_string}")
    print(f"서로 다른 객체: {id(original_string) != id(modified_string)}")

    # 3. 문자열 연산도 새 객체 생성
    greeting = "Hello"
    name = "World"
    full_greeting = greeting + " " + name

    print(f"\n=== 문자열 연산과 객체 생성 ===")
    print(f"greeting ID: {id(greeting)}")
    print(f"name ID: {id(name)}")
    print(f"full_greeting ID: {id(full_greeting)}")
    print(f"결과: {full_greeting}")

    # 4. 문자열 리터럴 최적화 (작은 문자열)
    str1 = "python"
    str2 = "python"
    print(f"\n=== 문자열 리터럴 최적화 ===")
    print(f"str1: {str1}, ID: {id(str1)}")
    print(f"str2: {str2}, ID: {id(str2)}")
    print(f"같은 객체 참조: {str1 is str2}")  # True (최적화)

    # 5. 성능 영향 (문자열 반복 연결의 문제)
    import time

    print(f"\n=== 성능 비교: 비효율적 vs 효율적 ===")

    # 비효율적 방법 (O(n²))
    start = time.time()
    result = ""
    for i in range(1000):
        result += str(i) + ","
    inefficient_time = time.time() - start

    # 효율적 방법 (O(n))
    start = time.time()
    parts = []
    for i in range(1000):
        parts.append(str(i))
    result = ",".join(parts)
    efficient_time = time.time() - start

    print(f"비효율적 방법 (문자열 연결): {inefficient_time:.4f}초")
    print(f"효율적 방법 (join 사용): {efficient_time:.4f}초")
    print(f"성능 향상: {inefficient_time / efficient_time:.1f}배")


demonstrate_string_immutability()
