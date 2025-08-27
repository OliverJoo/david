def handle_edge_cases():
    """극한 상황에서의 타입 동작"""

    print("=== 극한 상황 테스트 ===")

    # Case 1: middle이 빈 리스트가 되는 경우
    short_tuple = (1, 2)
    a, *middle, b = short_tuple
    print(f"짧은 튜플 {short_tuple}:")
    print(f"  a = {a} (타입: {type(a).__name__})")  # a = 1 (타입: int)
    print(f"  middle = {middle} (타입: {type(middle).__name__})")  # middle = [] (타입: list)
    print(f"  b = {b} (타입: {type(b).__name__})")  # b = 2 (타입: int)

    # Case 2: 모든 요소가 middle로 가는 경우
    single_tuple = (42,)
    *all_middle, = single_tuple  # 마지막 쉼표 주의
    print(f"\n단일 요소 튜플 {single_tuple}:")
    print(f"  all_middle = {all_middle} (타입: {type(all_middle).__name__})")  # all_middle = [42] (타입: list)

    # Case 3: None이 포함된 경우의 타입 유지
    none_tuple = (None, 1, 2, None)
    start, *middle_none, end = none_tuple
    print(f"\nNone 포함 튜플 {none_tuple}:")
    print(f"  start = {start} (타입: {type(start).__name__})")  # start = None (타입: NoneType)
    print(f"  middle_none = {middle_none} (타입: {type(middle_none).__name__})")  # middle_none = [1, 2] (타입: list)
    print(f"  end = {end} (타입: {type(end).__name__})")  # end = None (타입: NoneType)


handle_edge_cases()
