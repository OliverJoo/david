# ============= enumerate() / zip() 고급 패턴 =============
def demonstrate_iteration_functions():
    """반복 함수의 고급 활용법"""

    print("=== enumerate() 고급 활용 ===")

    # 예제 1: 조건부 인덱스 추출
    words = ["apple", "banana", "cherry", "date"]
    long_word_indices = [i for i, word in enumerate(words) if len(word) > 5]
    print(f"5글자 초과 단어의 인덱스: {long_word_indices}")
    # 결과: [1, 2] (banana, cherry)

    # 예제 2: 시작 인덱스 변경
    items = ["first", "second", "third"]
    for rank, item in enumerate(items, start=1):
        print(f"{rank}등: {item}")
    # 결과: 1등: first, 2등: second, 3등: third

    print(f"\n=== zip() 고급 활용 ===")

    # 예제 3: 여러 리스트 동시 처리
    names = ["Alice", "Bob", "Charlie"]
    ages = [25, 30, 35]
    cities = ["Seoul", "Busan", "Daegu"]

    profiles = list(zip(names, ages, cities))
    print("사용자 프로필:")
    for name, age, city in profiles:
        print(f"  {name} ({age}세) - {city}")
    # 결과: Alice (25세) - Seoul, Bob (30세) - Busan, Charlie (35세) - Daegu

    # 예제 4: 딕셔너리 생성
    keys = ["name", "age", "score"]
    values = ["John", 28, 95]
    user_dict = dict(zip(keys, values))
    print(f"생성된 딕셔너리: {user_dict}")
    # 결과: {'name': 'John', 'age': 28, 'score': 95}

    # 예제 5: 행렬 전치 (transpose)
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    transposed = list(zip(*matrix))  # * 언패킹 활용
    print(f"원본 행렬: {matrix}")
    print(f"전치 행렬: {transposed}")
    # 결과: [(1, 4, 7), (2, 5, 8), (3, 6, 9)]

    # 실전 활용: 두 리스트 비교
    list1 = [1, 2, 3, 4, 5]
    list2 = [1, 2, 4, 4, 6]

    differences = [(i, a, b) for i, (a, b) in enumerate(zip(list1, list2)) if a != b]
    print(f"서로 다른 위치와 값: {differences}")
    # 결과: [(2, 3, 4), (4, 5, 6)]


demonstrate_iteration_functions()
