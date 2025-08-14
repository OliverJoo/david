# ============= Deque 완벽 마스터 =============
from collections import deque
from typing import List, Optional, Any
import time


def demonstrate_deque():
    """Deque의 모든 기능과 고급 활용법"""

    print("=== 1. Deque 기본 연산 - 양끝 삽입/삭제 ===")

    # 기본 deque 생성 및 조작
    dq = deque([1, 2, 3, 4, 5])
    print(f"초기 deque: {dq}")

    # 양끝 추가
    dq.appendleft(0)  # 왼쪽에 추가
    dq.append(6)  # 오른쪽에 추가
    print(f"양끝 추가 후: {dq}")

    # 양끝 제거
    left = dq.popleft()  # 왼쪽에서 제거
    right = dq.pop()  # 오른쪽에서 제거
    print(f"제거된 값: 왼쪽={left}, 오른쪽={right}")
    print(f"제거 후: {dq}")

    # 회전 (rotate)
    dq.rotate(2)  # 오른쪽으로 2칸 회전
    print(f"오른쪽 2칸 회전: {dq}")

    dq.rotate(-3)  # 왼쪽으로 3칸 회전
    print(f"왼쪽 3칸 회전: {dq}")

    # 확장 (extend)
    dq.extend([7, 8])  # 오른쪽 확장
    dq.extendleft([0, -1])  # 왼쪽 확장 (역순으로 추가됨 주의!)
    print(f"확장 후: {dq}")

    # 최대 길이 설정
    limited_dq = deque([1, 2, 3], maxlen=5)
    limited_dq.extend([4, 5, 6, 7])  # 길이 초과시 왼쪽부터 제거
    print(f"최대길이 5로 제한된 deque: {limited_dq}")

    print(f"\n=== 2. 성능 비교: List vs Deque ===")

    def performance_test():
        """List와 Deque의 성능 차이 측정"""
        n = 10000

        # List 왼쪽 삽입 성능
        start = time.time()
        lst = []
        for i in range(n):
            lst.insert(0, i)  # O(n) 연산
        list_time = time.time() - start

        # Deque 왼쪽 삽입 성능
        start = time.time()
        dq = deque()
        for i in range(n):
            dq.appendleft(i)  # O(1) 연산
        deque_time = time.time() - start

        print(f"왼쪽 삽입 {n}회:")
        print(f"  List: {list_time:.4f}초")
        print(f"  Deque: {deque_time:.4f}초")
        print(f"  성능차이: {list_time / deque_time:.1f}배")

    performance_test()

    print(f"\n=== 3. 슬라이딩 윈도우 최댓값 - 고전적 문제 ===")

    def sliding_window_maximum(nums: List[int], k: int) -> List[int]:
        """
            슬라이딩 윈도우에서 최댓값을 구하는 효율적 알고리즘

            시간복잡도: O(n) - 각 원소는 최대 한 번씩만 deque에 들어가고 나감
            공간복잡도: O(k) - deque의 최대 크기는 k개

            Args:
                nums: 입력 배열
                k: 윈도우 크기

            Returns:
                각 윈도우의 최댓값들을 담은 리스트
            """
        if not nums or k == 0:
            return []

        if k == 1:
            return nums.copy()  # 윈도우가 1이면 원본 배열과 동일

        result = []
        # 인덱스를 저장하는 deque (값이 감소하는 순서로 유지)
        dq = deque()
        print(f"입력 배열: {nums}, 윈도우 크기: {k}")
        print("-" * 50)

        for i, num in enumerate(nums):
            print(f"단계 {i + 1}: 인덱스 {i}, 값 {num} 처리")

            # 1단계: 윈도우 범위를 벗어난 인덱스 제거
            while dq and dq[0] <= i - k:
                removed_idx = dq.popleft()
                print(f"  범위 벗어난 인덱스 {removed_idx} 제거")

            # 2단계: 현재 값보다 작은 값들의 인덱스 제거
            # 이들은 현재 값이 윈도우에 있는 동안 절대 최댓값이 될 수 없음
            # num 이 dq에 있는 값보다 클 경우, dq의 값을 삭제 and 작을 경우 삭제 안하고 dq에 추가
            while dq and nums[dq[-1]] < num:
                removed_idx = dq.pop()
                print(f"  현재 값({num})보다 작은 값의 인덱스 {removed_idx} 제거 (값: {nums[removed_idx]})")

            # 3단계: 현재 인덱스 추가
            dq.append(i)
            print(f"  현재 인덱스 {i} 추가")
            print(f"  현재 deque 상태: {list(dq)} (값: {[nums[idx] for idx in dq]})")

            # 4단계: 윈도우가 완성되면 최댓값 추가
            if i >= k - 1:
                max_value = nums[dq[0]]  # deque의 첫 번째가 항상 최댓값
                result.append(max_value)
                current_window = nums[i - k + 1:i + 1]
                print(f"  윈도우 완성: {current_window}, 최댓값: {max_value}")

        print(f"\n최종 결과: {result}")
        return result

    # 테스트 케이스
    test_cases = [
        ([1, 3, -1, -3, 5, 3, 6, 7], 3),
        ([1, -1, -3, 5, 3, 6, 7], 4),
        ([9, 11], 2),
        ([4, -2, -3, 5, -1, 8], 2)
    ]

    for nums, k in test_cases:
        result = sliding_window_maximum(nums, k)
        print(f"배열: {nums}, 윈도우크기: {k}")
        print(f"슬라이딩 윈도우 최댓값: {result}")
        print()

    print(f"=== 4. 실전 활용 예제 ===")

    # 1. 웹 브라우저 히스토리
    class BrowserHistory:
        """Deque를 사용한 웹 브라우저 히스토리 구현"""

        def __init__(self, max_history: int = 50):
            self.history = deque(maxlen=max_history)
            self.current_index = -1

        def visit(self, url: str):
            """새 페이지 방문"""
            # 현재 위치 이후의 히스토리 제거
            while len(self.history) > self.current_index + 1:
                self.history.pop()

            self.history.append(url)
            self.current_index = len(self.history) - 1
            return f"방문: {url}"

        def back(self) -> Optional[str]:
            """이전 페이지로"""
            if self.current_index > 0:
                self.current_index -= 1
                return self.history[self.current_index]
            return None

        def forward(self) -> Optional[str]:
            """다음 페이지로"""
            if self.current_index < len(self.history) - 1:
                self.current_index += 1
                return self.history[self.current_index]
            return None

        def current(self) -> Optional[str]:
            """현재 페이지"""
            if 0 <= self.current_index < len(self.history):
                return self.history[self.current_index]
            return None

        def get_history(self) -> List[str]:
            """전체 히스토리"""
            return list(self.history)

    # 브라우저 히스토리 테스트
    browser = BrowserHistory(max_history=5)

    actions = [
        ("visit", "https://google.com"),
        ("visit", "https://python.org"),
        ("visit", "https://github.com"),
        ("back", None),
        ("back", None),
        ("visit", "https://stackoverflow.com"),
        ("forward", None)
    ]

    print("브라우저 히스토리 시뮬레이션:")
    for action, url in actions:
        if action == "visit":
            result = browser.visit(url)
        elif action == "back":
            result = browser.back()
            result = f"뒤로가기: {result}" if result else "뒤로갈 수 없음"
        elif action == "forward":
            result = browser.forward()
            result = f"앞으로가기: {result}" if result else "앞으로갈 수 없음"

        print(f"  {result}")
        print(f"    현재: {browser.current()}")
        print(f"    히스토리: {browser.get_history()}")
        print()

    # 2. 실시간 데이터 스트림 처리
    class StreamProcessor:
        """실시간 스트림 데이터 처리를 위한 Deque 활용"""

        def __init__(self, window_size: int):
            self.window_size = window_size
            self.data_window = deque(maxlen=window_size)
            self.sum_value = 0

        def add_value(self, value: float) -> dict[str, float]:
            """새 값 추가 및 통계 계산"""
            # 윈도우가 가득 찬 경우 제거될 값 추적
            if len(self.data_window) == self.window_size:
                removed_value = self.data_window[0]
                self.sum_value -= removed_value

            # 새 값 추가
            self.data_window.append(value)
            self.sum_value += value

            # 통계 계산
            count = len(self.data_window)
            average = self.sum_value / count if count > 0 else 0
            minimum = min(self.data_window) if self.data_window else 0
            maximum = max(self.data_window) if self.data_window else 0

            return {
                "count": count,
                "sum": self.sum_value,
                "average": average,
                "min": minimum,
                "max": maximum,
                "window": list(self.data_window)
            }

    # 스트림 처리 예제
    processor = StreamProcessor(window_size=5)

    print("실시간 데이터 스트림 처리:")
    sample_data = [10, 15, 8, 22, 5, 18, 12, 25, 7, 20]

    for i, value in enumerate(sample_data):
        stats = processor.add_value(value)
        print(f"  값 {value} 추가 → 평균: {stats['average']:.1f}, "
              f"범위: [{stats['min']}-{stats['max']}], "
              f"윈도우: {stats['window']}")


demonstrate_deque()
