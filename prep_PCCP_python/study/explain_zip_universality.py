def explain_zip_universality():
    """zip(*)이 모든 자료구조에서 동작하는 이유 설명"""

    print("=" * 60)
    print("zip(*data)의 범용성 분석")
    print("=" * 60)

    # 세 가지 자료구조
    tuple_of_tuples = ((1, 2, 3), (4, 5, 6), (7, 8, 9))
    list_of_tuples = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]
    list_of_lists = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

    print("1. 내부 동작 원리:")
    print("   zip(*data)는 data의 각 요소를 언패킹하여 전달")
    print("   - tuple_of_tuples -> zip((1,2,3), (4,5,6), (7,8,9))")
    print("   - list_of_tuples  -> zip([1,2,3], [4,5,6], [7,8,9])")
    print("   - list_of_lists   -> zip([1,2,3], [4,5,6], [7,8,9])")

    print("\n2. zip() 함수의 다형성(Polymorphism):")
    for i, data in enumerate([tuple_of_tuples, list_of_tuples, list_of_lists], 1):
        result = list(zip(*data))
        print(f"   {i}번째 구조: {result}")  # 모두 동일한 결과

    print("\n3. 이터러블 프로토콜:")
    print("   - zip()은 이터러블 객체라면 타입에 관계없이 처리")
    print("   - tuple, list 모두 이터러블 프로토콜을 구현")
    print("   - 따라서 외부 컨테이너 타입과 무관하게 동작")


explain_zip_universality()
