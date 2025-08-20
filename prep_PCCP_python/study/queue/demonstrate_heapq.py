# ============= Heapq 완벽 마스터 =============
import heapq
import copy
from typing import List, Tuple, Any
import random
import time


def demonstrate_heapq():
    """Heapq의 모든 기능과 고급 활용법"""

    print("=== 1. 기본 Heap 연산 ===")

    # 기본 힙 생성 및 조작
    heap = []
    data = [64, 34, 25, 12, 22, 11, 90]

    print(f"원본 데이터: {data}")

    # heapify: 기존 리스트를 힙으로 변환 (O(n))
    heap_copy = data.copy()
    heapq.heapify(heap_copy)
    print(f"heapify 후: {heap_copy}")

    # heappush: 힙에 요소 추가 (O(log n))
    for item in data:
        heapq.heappush(heap, item)
    print(f"push 후 힙: {heap}")

    # heappop: 최솟값 제거 및 반환 (O(log n))
    print(f"최솟값들을 순서대로 제거:")
    result = []
    while heap:
        min_val = heapq.heappop(heap)
        result.append(min_val)
        print(f"  제거: {min_val}, 남은 힙: {heap}")
    print(f"정렬된 결과: {result}")

    print(f"\n=== 2. 고급 Heap 연산 ===")

    # heappushpop: push 후 즉시 pop (O(log n))
    heap = [1, 3, 5, 7, 9]
    heapq.heapify(heap)
    print(f"원본 힙: {heap}")

    result = heapq.heappushpop(heap, 4)
    print(f"4를 push한 후 pop: {result}, 힙: {heap}")

    # heapreplace: pop 후 push (O(log n))
    result = heapq.heapreplace(heap, 2)
    print(f"pop 후 2를 push: {result}, 힙: {heap}")

    # nlargest, nsmallest: 상위/하위 n개 (O(n log k))
    data = [64, 34, 25, 12, 22, 11, 90, 88, 76, 50]
    print(f"\n데이터: {data}")
    print(f"상위 3개: {heapq.nlargest(3, data)}")
    print(f"하위 3개: {heapq.nsmallest(3, data)}")

    # Key 함수 사용
    students = [
        {"name": "김철수", "grade": 85},
        {"name": "박영희", "grade": 92},
        {"name": "이민수", "grade": 78},
        {"name": "정수진", "grade": 95}
    ]

    top_students = heapq.nlargest(2, students, key=lambda x: x["grade"])
    print(f"성적 상위 2명: {top_students}")

    print(f"\n=== 3. 최대 힙 구현 (음수 활용) ===")

    class MaxHeap:
        """최대 힙 클래스 (heapq는 최소 힙만 지원)"""

        def __init__(self):
            self._heap = []

        def push(self, item):
            """최대값 우선으로 요소 추가"""
            heapq.heappush(self._heap, -item)

        def pop(self):
            """최댓값 제거 및 반환"""
            if self._heap:
                return -heapq.heappop(self._heap)
            raise IndexError("pop from empty heap")

        def peek(self):
            """최댓값 확인 (제거하지 않음)"""
            if self._heap:
                return -self._heap[0]
            return None

        def __len__(self):
            return len(self._heap)

        def __bool__(self):
            return bool(self._heap)

        def __repr__(self):
            # 실제 값들을 정렬된 순서로 표시
            items = [-x for x in self._heap]
            return f"MaxHeap({sorted(items, reverse=True)})"

    # 최대 힙 테스트
    max_heap = MaxHeap()
    data = [3, 1, 4, 1, 5, 9, 2, 6]

    print(f"데이터 추가: {data}")
    for item in data:
        max_heap.push(item)

    print(f"최대 힙: {max_heap}")
    print(f"최댓값들을 순서대로 제거:")

    while max_heap:
        max_val = max_heap.pop()
        print(f"  제거: {max_val}, 남은 크기: {len(max_heap)}")

    print(f"\n=== 4. 우선순위 큐 실전 활용 ===")

    # 1. 작업 스케줄러
    class Task:
        def __init__(self, priority: int, name: str, duration: float):
            self.priority = priority
            self.name = name
            self.duration = duration
            self.created_time = time.time()

        def __lt__(self, other):
            # 우선순위가 낮은 숫자일수록 높은 우선순위
            return self.priority < other.priority

        def __repr__(self):
            return f"Task('{self.name}', priority={self.priority})"

    class TaskScheduler:
        def __init__(self):
            self._tasks = []
            self._completed = []

        def add_task(self, priority: int, name: str, duration: float = 1.0):
            """작업 추가"""
            task = Task(priority, name, duration)
            heapq.heappush(self._tasks, task)
            print(f"📝 작업 추가: {task}")

        def execute_next_task(self):
            """우선순위가 가장 높은 작업 실행"""
            if self._tasks:
                task = heapq.heappop(self._tasks)
                print(f"⚙️  실행 중: {task}")
                time.sleep(0.1)  # 작업 시뮬레이션
                self._completed.append(task)
                print(f"✅ 완료: {task}")
                return task
            else:
                print("📭 대기 중인 작업이 없습니다")
                return None

        def execute_all_tasks(self):
            """모든 작업 실행"""
            print(f"🚀 {len(self._tasks)}개 작업 실행 시작")
            while self._tasks:
                self.execute_next_task()
            print(f"🎉 모든 작업 완료!")

        def get_pending_tasks(self):
            """대기 중인 작업 목록"""
            return sorted(self._tasks)

    # 작업 스케줄러 테스트
    scheduler = TaskScheduler()

    # 작업 추가 (우선순위: 숫자가 작을수록 높은 우선순위)
    scheduler.add_task(3, "이메일 전송", 0.5)
    scheduler.add_task(1, "데이터베이스 백업", 3.0)
    scheduler.add_task(2, "보고서 생성", 1.5)
    scheduler.add_task(1, "시스템 점검", 2.0)
    scheduler.add_task(4, "로그 정리", 0.3)

    print(f"\n대기 중인 작업: {scheduler.get_pending_tasks()}")
    scheduler.execute_all_tasks()

    # 2. 다익스트라 알고리즘 (최단 경로)
    def dijkstra(graph: dict, start: str) -> dict:
        """다익스트라 알고리즘으로 최단 경로 찾기"""
        # 거리 초기화
        distances = {node: float('infinity') for node in graph}
        distances[start] = 0

        # 우선순위 큐: (거리, 노드)
        pq = [(0, start)]
        visited = set()

        while pq:
            current_distance, current_node = heapq.heappop(pq)

            if current_node in visited:
                continue

            visited.add(current_node)

            # 인접 노드 확인
            for neighbor, weight in graph[current_node].items():
                distance = current_distance + weight

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(pq, (distance, neighbor))

        return distances

    # 그래프 예제 (노드: {인접노드: 가중치})
    graph = {
        'A': {'B': 4, 'C': 2},
        'B': {'C': 1, 'D': 5},
        'C': {'D': 8, 'E': 10},
        'D': {'E': 2},
        'E': {}
    }

    print(f"\n=== 다익스트라 알고리즘 ===")
    print(f"그래프: {graph}")

    shortest_distances = dijkstra(graph, 'A')
    print(f"A에서 각 노드까지의 최단 거리:")
    for node, distance in sorted(shortest_distances.items()):
        print(f"  A → {node}: {distance}")

    # 3. 병합 정렬된 리스트들
    def merge_sorted_lists(lists: List[List[int]]) -> List[int]:
        """여러 정렬된 리스트를 병합"""
        result = []
        heap = []

        # 각 리스트의 첫 번째 요소를 힙에 추가
        for i, lst in enumerate(lists):
            if lst:  # 비어있지 않은 리스트만
                heapq.heappush(heap, (lst[0], i, 0))  # (값, 리스트_인덱스, 요소_인덱스)

        while heap:
            value, list_idx, element_idx = heapq.heappop(heap)
            result.append(value)

            # 다음 요소가 있으면 힙에 추가
            if element_idx + 1 < len(lists[list_idx]):
                next_value = lists[list_idx][element_idx + 1]
                heapq.heappush(heap, (next_value, list_idx, element_idx + 1))

        return result

    # 병합 정렬 테스트
    sorted_lists = [
        [1, 4, 7, 10],
        [2, 5, 8],
        [3, 6, 9, 11, 12]
    ]

    print(f"\n=== 정렬된 리스트 병합 ===")
    print(f"입력 리스트들: {sorted_lists}")

    merged = merge_sorted_lists(sorted_lists)
    print(f"병합된 결과: {merged}")


demonstrate_heapq()
