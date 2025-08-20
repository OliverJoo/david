# ============= QUEUE 완벽 구현 및 시연 =============

from collections import deque
from queue import Queue, LifoQueue, PriorityQueue, Empty, Full
from typing import List, Any, Optional, Union, Generic, TypeVar
import threading
import time
import heapq
from dataclasses import dataclass
from enum import Enum

T = TypeVar('T')


class QueueType(Enum):
    """큐 타입 열거형"""
    DEQUE = "deque"
    THREAD_SAFE = "thread_safe"
    PRIORITY = "priority"
    LIFO = "lifo"


@dataclass
class QueueBenchmark:
    """큐 성능 벤치마크 결과"""
    queue_type: str
    enqueue_time: float
    dequeue_time: float
    memory_usage: int


class SafeQueue(Generic[T]):
    """방어적 프로그래밍이 적용된 안전한 큐 래퍼"""

    def __init__(self, queue_type: QueueType = QueueType.DEQUE, maxsize: int = 0):
        self.queue_type = queue_type
        self.maxsize = maxsize
        self._queue = self._create_queue()
        self._lock = threading.RLock()  # 스레드 안전성을 위한 락

    def _create_queue(self) -> Union[deque, Queue, LifoQueue, PriorityQueue]:
        """큐 타입에 따른 큐 객체 생성"""
        if self.queue_type == QueueType.DEQUE:
            return deque(maxlen=self.maxsize if self.maxsize > 0 else None)
        elif self.queue_type == QueueType.THREAD_SAFE:
            return Queue(maxsize=self.maxsize)
        elif self.queue_type == QueueType.PRIORITY:
            return PriorityQueue(maxsize=self.maxsize)
        elif self.queue_type == QueueType.LIFO:
            return LifoQueue(maxsize=self.maxsize)
        else:
            raise ValueError(f"지원하지 않는 큐 타입: {self.queue_type}")

    def enqueue(self, item: T, priority: int = 0, timeout: Optional[float] = None) -> bool:
        """큐에 아이템 추가"""
        try:
            if self.queue_type == QueueType.DEQUE:
                if self.maxsize > 0 and len(self._queue) >= self.maxsize:
                    return False  # 큐가 가득 참
                self._queue.append(item)
                return True

            elif self.queue_type == QueueType.PRIORITY:
                # 우선순위 큐의 경우 (priority, item) 튜플로 저장
                self._queue.put((priority, item), timeout=timeout)
                return True

            else:  # THREAD_SAFE, LIFO
                self._queue.put(item, timeout=timeout)
                return True

        except Full:
            return False
        except Exception as e:
            print(f"큐 추가 실패: {e}")
            return False

    def dequeue(self, timeout: Optional[float] = None) -> Optional[T]:
        """큐에서 아이템 제거 및 반환"""
        try:
            if self.queue_type == QueueType.DEQUE:
                if not self._queue:
                    return None
                return self._queue.popleft()

            elif self.queue_type == QueueType.PRIORITY:
                priority, item = self._queue.get(timeout=timeout)
                return item

            else:  # THREAD_SAFE, LIFO
                return self._queue.get(timeout=timeout)

        except Empty:
            return None
        except Exception as e:
            print(f"큐 제거 실패: {e}")
            return None

    def peek(self) -> Optional[T]:
        """큐의 첫 번째 아이템 확인 (제거하지 않음)"""
        try:
            if self.queue_type == QueueType.DEQUE:
                return self._queue[0] if self._queue else None
            else:
                # Thread-safe 큐들은 peek을 직접 지원하지 않음
                return None
        except (IndexError, Exception):
            return None

    def size(self) -> int:
        """큐 크기 반환"""
        if self.queue_type == QueueType.DEQUE:
            return len(self._queue)
        else:
            return self._queue.qsize()

    def is_empty(self) -> bool:
        """큐가 비어있는지 확인"""
        return self.size() == 0

    def is_full(self) -> bool:
        """큐가 가득 찼는지 확인"""
        if self.maxsize <= 0:
            return False
        return self.size() >= self.maxsize

    def clear(self) -> None:
        """큐 비우기"""
        if self.queue_type == QueueType.DEQUE:
            self._queue.clear()
        else:
            # Thread-safe 큐들은 clear 메서드가 없으므로 모든 아이템 제거
            while not self.is_empty():
                try:
                    self.dequeue(timeout=0.1)
                except:
                    break


def demonstrate_queue() -> None:
    """큐의 다양한 구현 방식과 사용법 시연"""
    print("=== Python Queue 구현 및 활용 완벽 가이드 ===\n")

    # 1. 기본 FIFO 큐 (deque 기반)
    print("1. 기본 FIFO 큐 (collections.deque)")
    fifo_queue = SafeQueue[int](QueueType.DEQUE)

    # 데이터 추가
    for i in range(1, 6):
        success = fifo_queue.enqueue(i)
        print(f"큐에 {i} 추가: {'성공' if success else '실패'}")

    print(f"큐 크기: {fifo_queue.size()}")
    print(f"첫 번째 요소 확인: {fifo_queue.peek()}")

    # 데이터 제거
    print("큐에서 데이터 제거:")
    while not fifo_queue.is_empty():
        item = fifo_queue.dequeue()
        print(f"제거된 요소: {item}, 남은 크기: {fifo_queue.size()}")

    print()

    # 2. 스레드 안전 큐
    print("2. 스레드 안전 큐 (queue.Queue)")
    thread_safe_queue = SafeQueue[str](QueueType.THREAD_SAFE, maxsize=3)

    # 생산자-소비자 패턴 시연
    def producer(queue: SafeQueue[str], items: List[str]) -> None:
        """생산자 함수"""
        for item in items:
            success = queue.enqueue(item, timeout=1.0)
            print(f"생산자: {item} {'추가됨' if success else '추가 실패'}")
            time.sleep(0.1)

    def consumer(queue: SafeQueue[str], name: str) -> None:
        """소비자 함수"""
        while True:
            item = queue.dequeue(timeout=2.0)
            if item is None:
                break
            print(f"소비자 {name}: {item} 처리됨")
            time.sleep(0.2)

    # 스레드 생성 및 실행
    producer_thread = threading.Thread(
        target=producer,
        args=(thread_safe_queue, ["작업1", "작업2", "작업3", "작업4", "작업5"])
    )
    consumer_thread = threading.Thread(
        target=consumer,
        args=(thread_safe_queue, "A")
    )

    producer_thread.start()
    consumer_thread.start()

    producer_thread.join()
    consumer_thread.join()

    print()

    # 3. 우선순위 큐
    print("3. 우선순위 큐 (queue.PriorityQueue)")
    priority_queue = SafeQueue[str](QueueType.PRIORITY)

    # 우선순위와 함께 데이터 추가 (낮은 숫자가 높은 우선순위)
    tasks = [("긴급 작업", 1), ("일반 작업", 5), ("중요 작업", 2), ("저우선순위", 10)]

    for task, priority in tasks:
        success = priority_queue.enqueue(task, priority=priority)
        print(f"우선순위 {priority}로 '{task}' 추가: {'성공' if success else '실패'}")

    print("\n우선순위 순으로 처리:")
    while not priority_queue.is_empty():
        task = priority_queue.dequeue()
        print(f"처리 중: {task}")

    print()

    # 4. LIFO 큐 (스택)
    print("4. LIFO 큐 - 스택 (queue.LifoQueue)")
    stack_queue = SafeQueue[int](QueueType.LIFO)

    # 데이터 푸시
    for i in range(1, 6):
        stack_queue.enqueue(i)
        print(f"스택에 {i} 푸시")

    # 데이터 팝
    print("\n스택에서 데이터 팝:")
    while not stack_queue.is_empty():
        item = stack_queue.dequeue()
        print(f"팝된 요소: {item}")

    print()

    # 5. 성능 비교
    print("5. 성능 비교")
    benchmark_queues = [
        (SafeQueue[int](QueueType.DEQUE), "collections.deque"),
        (SafeQueue[int](QueueType.THREAD_SAFE), "queue.Queue"),
    ]

    test_size = 10000
    results = []

    for queue, name in benchmark_queues:
        # 삽입 성능 측정
        start_time = time.time()
        for i in range(test_size):
            queue.enqueue(i)
        enqueue_time = time.time() - start_time

        # 제거 성능 측정
        start_time = time.time()
        while not queue.is_empty():
            queue.dequeue()
        dequeue_time = time.time() - start_time

        results.append(QueueBenchmark(name, enqueue_time, dequeue_time, 0))
        print(f"{name}: 삽입 {enqueue_time:.4f}초, 제거 {dequeue_time:.4f}초")

    # 결과: collections.deque가 일반적으로 더 빠름


def demonstrate_custom_queue() -> None:
    """커스텀 큐 구현 예제"""
    print("\n=== 커스텀 원형 큐 구현 ===")

    class CircularQueue(Generic[T]):
        """고정 크기 원형 큐 구현"""

        def __init__(self, capacity: int):
            if capacity <= 0:
                raise ValueError("용량은 0보다 커야 합니다")
            self._capacity = capacity
            self._queue: List[Optional[T]] = [None] * capacity
            self._front = 0
            self._rear = 0
            self._size = 0

        def enqueue(self, item: T) -> bool:
            """큐에 아이템 추가"""
            if self.is_full():
                return False

            self._queue[self._rear] = item
            self._rear = (self._rear + 1) % self._capacity
            self._size += 1
            return True

        def dequeue(self) -> Optional[T]:
            """큐에서 아이템 제거"""
            if self.is_empty():
                return None

            item = self._queue[self._front]
            self._queue[self._front] = None  # 메모리 해제
            self._front = (self._front + 1) % self._capacity
            self._size -= 1
            return item

        def peek(self) -> Optional[T]:
            """첫 번째 아이템 확인"""
            return self._queue[self._front] if not self.is_empty() else None

        def is_empty(self) -> bool:
            return self._size == 0

        def is_full(self) -> bool:
            return self._size == self._capacity

        def size(self) -> int:
            return self._size

        def capacity(self) -> int:
            return self._capacity

        def __str__(self) -> str:
            if self.is_empty():
                return "[]"

            items = []
            current = self._front
            for _ in range(self._size):
                items.append(str(self._queue[current]))
                current = (current + 1) % self._capacity

            return f"[{', '.join(items)}]"

    # 원형 큐 사용 예제
    circular_queue = CircularQueue[str](5)

    # 데이터 추가
    items = ["A", "B", "C", "D", "E"]
    for item in items:
        success = circular_queue.enqueue(item)
        print(f"'{item}' 추가 {'성공' if success else '실패'}: {circular_queue}")

    # 가득 찬 상태에서 추가 시도
    success = circular_queue.enqueue("F")
    print(f"'F' 추가 {'성공' if success else '실패'} (큐 가득 찬 상태): {circular_queue}")

    # 일부 데이터 제거 후 다시 추가
    for _ in range(2):
        item = circular_queue.dequeue()
        print(f"'{item}' 제거: {circular_queue}")

    # 새 데이터 추가 (원형 큐의 특성 확인)
    for item in ["F", "G"]:
        success = circular_queue.enqueue(item)
        print(f"'{item}' 추가 {'성공' if success else '실패'}: {circular_queue}")


# 테스트 코드
def test_queue_operations() -> None:
    """큐 연산 테스트"""
    print("\n=== 큐 테스트 수행 ===")

    # 기본 기능 테스트
    test_queue = SafeQueue[int](QueueType.DEQUE)

    # 빈 큐 테스트
    assert test_queue.is_empty() == True
    assert test_queue.size() == 0
    assert test_queue.dequeue() is None
    assert test_queue.peek() is None

    # 데이터 추가 테스트
    for i in range(5):
        assert test_queue.enqueue(i) == True

    assert test_queue.size() == 5
    assert test_queue.is_empty() == False
    assert test_queue.peek() == 0

    # 데이터 제거 테스트
    for expected in range(5):
        actual = test_queue.dequeue()
        assert actual == expected, f"예상: {expected}, 실제: {actual}"

    assert test_queue.is_empty() == True

    print("✅ 모든 테스트 통과!")


if __name__ == "__main__":
    # 전체 시연 실행
    demonstrate_queue()
    demonstrate_custom_queue()
    test_queue_operations()
