def demonstrate_unpacking_types():
    """튜플 언패킹 시 데이터 타입 변화 시연"""

    # 테스트용 다양한 튜플들
    coordinates = (10, 20, 30, 40, 50)
    mixed_data = ("start", 1, 2, 3, 4, "end")
    nested_data = ((1, 2), "middle1", "middle2", "middle3", (5, 6))

    print("=== 기본 언패킹 타입 확인 ===")

    # 첫 번째 예시: 숫자 튜플
    a, *middle, b = coordinates
    print(f"원본 튜플: {coordinates}")
    print(f"a = {a}, 타입: {type(a)}")  # a = 10, 타입: <class 'int'>
    print(f"middle = {middle}, 타입: {type(middle)}")  # middle = [20, 30, 40], 타입: <class 'list'>
    print(f"b = {b}, 타입: {type(b)}")  # b = 50, 타입: <class 'int'>

    print("\n=== 혼합 타입 언패킹 ===")

    # 두 번째 예시: 혼합 타입 튜플
    first, *center, last = mixed_data
    print(f"원본 튜플: {mixed_data}")
    print(f"first = {first}, 타입: {type(first)}")  # first = start, 타입: <class 'str'>
    print(f"center = {center}, 타입: {type(center)}")  # center = [1, 2, 3, 4], 타입: <class 'list'>
    print(f"last = {last}, 타입: {type(last)}")  # last = end, 타입: <class 'str'>

    print("\n=== 중첩 데이터 언패킹 ===")

    # 세 번째 예시: 중첩된 튜플
    start, *mid_section, end = nested_data
    print(f"원본 튜플: {nested_data}")
    print(f"start = {start}, 타입: {type(start)}")  # start = (1, 2), 타입: <class 'tuple'>
    print(
        f"mid_section = {mid_section}, 타입: {type(mid_section)}")  # mid_section = ['middle1', 'middle2', 'middle3'], 타입: <class 'list'>
    print(f"end = {end}, 타입: {type(end)}")  # end = (5, 6), 타입: <class 'tuple'>

# 타입 변환 규칙
# * 없는 변수: 원본 튜플 요소의 타입 그대로 유지
# * 있는 변수: 항상 리스트(list)로 변환
# 빈 수집: *middle이 0개 요소를 받으면 빈 리스트 []
# 타입 혼재: 수집된 요소들의 타입이 다양해도 모두 리스트에 담김

# 실행
demonstrate_unpacking_types()
