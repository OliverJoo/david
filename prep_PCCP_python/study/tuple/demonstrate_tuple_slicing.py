# ============= TUPLE 슬라이싱 예제 =============
def demonstrate_tuple_slicing():
    """튜플 슬라이싱 시연 (리스트와 동일한 방식)"""

    coordinates = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
    print(f"원본 튜플: {coordinates}")
    print()

    # 기본 슬라이싱 (리스트와 동일)
    print("=== 튜플 슬라이싱 ===")
    print(f"coordinates[2:5] = {coordinates[2:5]}")  # (2, 3, 4)
    print(f"coordinates[:3] = {coordinates[:3]}")  # (0, 1, 2)
    print(f"coordinates[7:] = {coordinates[7:]}")  # (7, 8, 9)
    print(f"coordinates[::-1] = {coordinates[::-1]}")  # 역순
    print(f"coordinates[::2] = {coordinates[::2]}")  # 짝수 인덱스
    print()

    # 튜플 언패킹과 슬라이싱 조합
    print("=== 튜플 언패킹과 슬라이싱 ===")
    a, *middle, b = coordinates  # 첫 번째, 마지막, 나머지
    print(f"첫 번째: {a}, 마지막: {b}, 나머지: {middle}")

    # 중첩 튜플 슬라이싱
    nested = ((1, 2), (3, 4), (5, 6), (7, 8))
    print(f"중첩 튜플: {nested}")
    print(f"nested[1:3] = {nested[1:3]}")  # ((3, 4), (5, 6))
    print(f"nested[0][1] = {nested[1]}")  # 2


demonstrate_tuple_slicing()
