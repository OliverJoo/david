# ============= 우선순위 큐 튜플 형태 완벽 분석 및 구현 =============

from queue import PriorityQueue, Empty
from dataclasses import dataclass, field
from typing import Any, Tuple, Union
import heapq
import threading
import time


# 다양한 데이터 타입 정의
@dataclass
class Task:
    """작업을 나타내는 클래스"""
    name: str
    duration: int

    def __str__(self):
        return f"Task({self.name}, {self.duration}s)"


@dataclass(order=True)
class ComparableTask:
    """비교 가능한 작업 클래스"""
    priority: int
    task: Task = field(compare=False)  # 비교에서 제외

    def __str__(self):
        return f"ComparableTask(priority={self.priority}, task={self.task})"


def demonstrate_priority_queue_formats():
    """우선순위 큐의 다양한 튜플 형태 시연"""
    print("=== 우선순위 큐 튜플 형태 완벽 분석 ===\n")

    # 1. (숫자, 문자열) - 기본 형태
    print("1. (숫자, 문자열) 형태")
    pq1 = PriorityQueue()

    # 우선순위와 작업명
    tasks = [(3, "낮은 우선순위"), (1, "높은 우선순위"), (2, "중간 우선순위")]

    for priority, task in tasks:
        pq1.put((priority, task))
        print(f"추가: ({priority}, '{task}')")

    print("처리 순서:")
    while not pq1.empty():
        priority, task = pq1.get()
        print(f"  처리됨: ({priority}, '{task}')")
    print()

    # 2. (문자열, 숫자) 형태
    print("2. (문자열, 숫자) 형태")
    pq2 = PriorityQueue()

    # 문자열이 먼저 오는 경우 - 사전순으로 정렬됨
    data = [("urgent", 100), ("normal", 50), ("low", 10)]

    for category, value in data:
        pq2.put((category, value))
        print(f"추가: ('{category}', {value})")

    print("처리 순서 (사전순):")
    while not pq2.empty():
        category, value = pq2.get()
        print(f"  처리됨: ('{category}', {value})")
    print()

    # 3. (숫자, 숫자) 형태
    print("3. (숫자, 숫자) 형태")
    pq3 = PriorityQueue()

    # (우선순위, 데이터값) 형태
    numbers = [(2, 200), (1, 100), (3, 300)]

    for priority, data in numbers:
        pq3.put((priority, data))
        print(f"추가: ({priority}, {data})")

    print("처리 순서:")
    while not pq3.empty():
        priority, data = pq3.get()
        print(f"  처리됨: ({priority}, {data})")
    print()

    # 4. (문자열, 문자열) 형태
    print("4. (문자열, 문자열) 형태")
    pq4 = PriorityQueue()

    # 모두 문자열인 경우
    items = [("medium", "작업B"), ("high", "작업A"), ("low", "작업C")]

    for priority, task in items:
        pq4.put((priority, task))
        print(f"추가: ('{priority}', '{task}')")

    print("처리 순서 (사전순):")
    while not pq4.empty():
        priority, task = pq4.get()
        print(f"  처리됨: ('{priority}', '{task}')")
    print()


def demonstrate_tuple_comparison_rules():
    """Python 튜플 비교 규칙 상세 설명"""
    print("=== Python 튜플 비교 규칙 상세 분석 ===\n")

    # 1. 기본 비교 규칙
    print("1. 튜플 비교는 첫 번째 요소부터 순차적으로 진행")
    comparisons = [
        ((1, "B"), (2, "A")),  # 첫 번째 요소로 결정
        ((1, "B"), (1, "A")),  # 두 번째 요소로 결정
        ((1, 2, "C"), (1, 3, "A")),  # 두 번째 요소로 결정
    ]

    for t1, t2 in comparisons:
        result = t1 < t2
        print(f"  {t1} < {t2} = {result}")
    print()

    # 2. 동일 우선순위에서의 동작
    print("2. 동일 우선순위에서의 정렬")
    pq = PriorityQueue()

    # 같은 우선순위(1)로 여러 작업 추가
    same_priority_tasks = [
        (1, "작업Z"),
        (1, "작업A"),
        (1, "작업M"),
    ]

    for priority, task in same_priority_tasks:
        pq.put((priority, task))
        print(f"추가: ({priority}, '{task}')")

    print("처리 순서 (두 번째 요소의 사전순):")
    while not pq.empty():
        priority, task = pq.get()
        print(f"  처리됨: ({priority}, '{task}')")
    print()


def demonstrate_complex_tuple_structures():
    """복잡한 튜플 구조 시연"""
    print("=== 복잡한 튜플 구조 및 고급 활용 ===\n")

    # 1. 3요소 튜플 (우선순위, 시간, 작업)
    print("1. 3요소 튜플: (우선순위, 삽입순서, 작업)")
    pq = PriorityQueue()

    # 우선순위가 같을 때 삽입 순서 보장
    counter = 0
    tasks_with_timestamp = [
        (1, "중요 작업 1"),
        (2, "일반 작업 1"),
        (1, "중요 작업 2"),  # 같은 우선순위
        (1, "중요 작업 3"),  # 같은 우선순위
    ]

    for priority, task in tasks_with_timestamp:
        pq.put((priority, counter, task))
        print(f"추가: ({priority}, {counter}, '{task}')")
        counter += 1

    print("처리 순서 (우선순위 → 삽입순서):")
    while not pq.empty():
        priority, order, task = pq.get()
        print(f"  처리됨: ({priority}, {order}, '{task}')")
    print()

    # 2. 객체를 포함한 튜플
    print("2. 객체를 포함한 튜플")
    pq_obj = PriorityQueue()

    # ComparableTask 사용 (dataclass의 order=True 활용)
    comparable_tasks = [
        ComparableTask(3, Task("데이터 백업", 30)),
        ComparableTask(1, Task("시스템 점검", 60)),
        ComparableTask(2, Task("로그 분석", 15)),
    ]

    for task in comparable_tasks:
        pq_obj.put(task)
        print(f"추가: {task}")

    print("처리 순서:")
    while not pq_obj.empty():
        task = pq_obj.get()
        print(f"  처리됨: {task}")
    print()


def demonstrate_edge_cases_and_errors():
    """엣지 케이스와 오류 상황 시연"""
    print("=== 엣지 케이스 및 오류 상황 분석 ===\n")

    # 1. 비교 불가능한 타입 조합
    print("1. 비교 불가능한 타입 조합")
    pq = PriorityQueue()

    try:
        # 숫자와 문자열을 직접 비교하는 경우 (Python 3에서 오류)
        pq.put((1, "문자열"))
        pq.put(("문자열", 1))  # 이것이 문제가 됨
        # 출력: TypeError 발생 예상
    except Exception as e:
        print(f"  오류 발생: {type(e).__name__}: {e}")

    # 2. 해결 방법: 모든 요소를 같은 타입으로 맞추기
    print("\n2. 해결 방법: 타입 통일")
    pq_safe = PriorityQueue()

    # 모든 우선순위를 숫자로 통일
    mixed_data = [
        (1, "높은 우선순위"),
        (2, "중간 우선순위"),
        (3, "낮은 우선순위"),
    ]

    for priority, task in mixed_data:
        pq_safe.put((priority, task))
        print(f"  안전하게 추가: ({priority}, '{task}')")

    # 3. 비교 불가능한 객체 처리
    print("\n3. 비교 불가능한 객체 처리 방법")
    pq_wrapper = PriorityQueue()

    # 일반 Task 객체 (비교 불가능)
    regular_tasks = [
        Task("파일 압축", 20),
        Task("메일 전송", 5),
        Task("보고서 생성", 45),
    ]

    # wrapper 클래스 사용 또는 튜플로 감싸기
    for i, task in enumerate(regular_tasks):
        # 우선순위와 카운터를 사용하여 객체 비교 문제 해결
        pq_wrapper.put((task.duration, i, task))  # 지속시간을 우선순위로 사용
        print(f"  추가: ({task.duration}, {i}, {task})")

    print("처리 순서 (지속시간 기준):")
    while not pq_wrapper.empty():
        duration, order, task = pq_wrapper.get()
        print(f"  처리됨: {task}")


def demonstrate_performance_comparison():
    """다양한 우선순위 큐 구현의 성능 비교"""
    print("\n=== 성능 비교: 다양한 튜플 형태 ===\n")

    import time

    test_size = 10000

    # 1. (int, str) 형태
    start_time = time.time()
    pq1 = PriorityQueue()
    for i in range(test_size):
        pq1.put((i % 100, f"task_{i}"))

    while not pq1.empty():
        pq1.get()

    time1 = time.time() - start_time
    print(f"1. (int, str) 형태: {time1:.4f}초")

    # 2. (str, int) 형태
    start_time = time.time()
    pq2 = PriorityQueue()
    for i in range(test_size):
        pq2.put((f"priority_{i % 100:03d}", i))

    while not pq2.empty():
        pq2.get()

    time2 = time.time() - start_time
    print(f"2. (str, int) 형태: {time2:.4f}초")

    # 3. (int, int, str) 형태
    start_time = time.time()
    pq3 = PriorityQueue()
    for i in range(test_size):
        pq3.put((i % 100, i, f"task_{i}"))

    while not pq3.empty():
        pq3.get()

    time3 = time.time() - start_time
    print(f"3. (int, int, str) 형태: {time3:.4f}초")

    print(f"\n성능 차이:")
    print(f"  문자열 비교는 숫자 비교보다 약 {time2 / time1:.1f}배 느림")
    print(f"  복잡한 튜플은 단순한 튜플보다 약 {time3 / time1:.1f}배 느림")


# 실행 및 테스트 코드
def main():
    """메인 실행 함수"""
    demonstrate_priority_queue_formats()
    demonstrate_tuple_comparison_rules()
    demonstrate_complex_tuple_structures()
    demonstrate_edge_cases_and_errors()
    demonstrate_performance_comparison()


if __name__ == "__main__":
    main()

# 출력 예상 결과:
# 1. (숫자, 문자열): 숫자 우선순위 → 문자열 사전순
# 2. (문자열, 숫자): 문자열 사전순 우선
# 3. (숫자, 숫자): 첫 번째 숫자 → 두 번째 숫자 순
# 4. (문자열, 문자열): 모두 사전순으로 비교
