# ============= collections 고급 컨테이너 =============
from collections import defaultdict, Counter, deque, namedtuple, OrderedDict
from typing import List, Dict, Any


def demonstrate_collections_advanced():
    """collections 모듈의 고급 활용법"""

    print("=== defaultdict - 기본값 자동 생성 ===")

    # 예제 1: 그래프 표현
    def build_graph_adjacency_list(edges: List[tuple]) -> defaultdict:
        """간선 리스트로부터 인접 리스트 그래프 생성"""
        graph = defaultdict(list)

        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)  # 무방향 그래프

        return graph

    edges = [(1, 2), (2, 3), (3, 4), (1, 4), (2, 4)]
    graph = build_graph_adjacency_list(edges)

    print("그래프 인접 리스트:")
    for node, neighbors in sorted(graph.items()):
        print(f"  노드 {node}: {neighbors}")

    # 결과: 각 노드의 인접 노드들 출력

    # 예제 2: 단어별 위치 추적
    def find_word_positions(text: str) -> defaultdict:
        """텍스트에서 각 단어의 위치들 추적"""
        word_positions = defaultdict(list)

        words = text.split()
        for i, word in enumerate(words):
            word_positions[word.lower()].append(i)

        return word_positions

    sample_text = "the quick brown fox jumps over the lazy dog the fox"
    positions = find_word_positions(sample_text)

    print(f"\n텍스트: {sample_text}")
    print("단어별 위치:")
    for word, pos_list in sorted(positions.items()):
        print(f"  '{word}': {pos_list}")
    # 결과: 'the': [0, 6, 9], 'fox': [3, 10] 등

    print(f"\n=== Counter - 빈도수 계산의 달인 ===")

    # 예제 3: 문자 빈도 분석
    def analyze_character_frequency(text: str) -> Dict[str, int]:
        """문자 빈도 분석 및 통계"""
        # 알파벳만 추출하고 소문자로 변환
        letters_only = ''.join(c.lower() for c in text if c.isalpha())
        char_count = Counter(letters_only)

        return char_count

    sample_text = "Hello World! This is a test message."
    char_freq = analyze_character_frequency(sample_text)

    print("문자 빈도 분석:")
    # 빈도순 정렬
    for char, count in char_freq.most_common():
        print(f"  '{char}': {count}회")

    # 결과: 가장 빈번한 문자부터 순서대로 출력

    # 예제 4: 리스트 요소 비교
    def compare_lists(list1: List, list2: List) -> Dict[str, Any]:
        """두 리스트의 차이점 분석"""
        counter1 = Counter(list1)
        counter2 = Counter(list2)

        # Counter의 산술 연산 활용
        common = counter1 & counter2  # 교집합
        difference = counter1 - counter2  # 차집합
        union = counter1 | counter2  # 합집합

        return {
            "common": dict(common),
            "only_in_first": dict(difference),
            "only_in_second": dict(counter2 - counter1),
            "union": dict(union)
        }

    list_a = [1, 2, 2, 3, 4, 4, 4]
    list_b = [2, 3, 3, 4, 5, 5]

    comparison = compare_lists(list_a, list_b)
    print(f"\n리스트 A: {list_a}")
    print(f"리스트 B: {list_b}")
    print(f"공통 요소: {comparison['common']}")
    print(f"A에만 있는 요소: {comparison['only_in_first']}")
    print(f"B에만 있는 요소: {comparison['only_in_second']}")
    # 결과: 각 집합의 차이점 명확히 출력

    print(f"\n=== namedtuple - 구조화된 데이터 ===")

    # 예제 5: 좌표 시스템
    Point = namedtuple('Point', ['x', 'y'])
    Rectangle = namedtuple('Rectangle', ['top_left', 'bottom_right'])

    # 점들 생성
    points = [
        Point(0, 0),
        Point(3, 4),
        Point(-2, 1),
        Point(1, -3)
    ]

    # 원점으로부터의 거리 계산
    def distance_from_origin(point: Point) -> float:
        return (point.x ** 2 + point.y ** 2) ** 0.5

    # 거리순 정렬
    sorted_points = sorted(points, key=distance_from_origin)

    print("원점으로부터 거리순 정렬:")
    for point in sorted_points:
        dist = distance_from_origin(point)
        print(f"  {point} → 거리: {dist:.2f}")
    # 결과: Point(x=0, y=0) → 거리: 0.00 등

    # 예제 6: 학생 성적 관리
    Student = namedtuple('Student', ['name', 'grade', 'subjects'])
    Subject = namedtuple('Subject', ['name', 'score'])

    students = [
        Student("Alice", 10, [
            Subject("Math", 95),
            Subject("English", 87),
            Subject("Science", 92)
        ]),
        Student("Bob", 10, [
            Subject("Math", 78),
            Subject("English", 94),
            Subject("Science", 85)
        ])
    ]

    # 평균 점수 계산
    def calculate_average(student: Student) -> float:
        total_score = sum(subject.score for subject in student.subjects)
        return total_score / len(student.subjects)

    print(f"\n학생별 평균 점수:")
    for student in students:
        avg_score = calculate_average(student)
        print(f"  {student.name}: {avg_score:.1f}점")
        for subject in student.subjects:
            print(f"    {subject.name}: {subject.score}점")
    # 결과: 각 학생의 과목별 점수와 평균 출력


demonstrate_collections_advanced()
