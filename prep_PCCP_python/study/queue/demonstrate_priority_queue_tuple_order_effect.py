#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
우선순위 큐 튜플 순서 영향 분석
Python 3.12 호환
"""

from queue import PriorityQueue


def demonstrate_priority_queue_tuple_order_effect():
    """튜플 순서가 우선순위 큐에 미치는 영향 시연"""

    print("=== 우선순위 큐 튜플 순서 영향 분석 ===\n")

    # 원본 데이터
    tasks = [("긴급 작업", 1), ("일반 작업", 5), ("중요 작업", 2), ("저우선순위", 10)]
    print(f"원본 데이터: {tasks}")
    print("형태: (문자열, 숫자)\n")

    # 시나리오 1: (문자열, 숫자) 형태로 그대로 저장
    print("🔍 시나리오 1: (문자열, 숫자) 형태로 저장")
    pq1 = PriorityQueue()

    for task_name, priority in tasks:
        pq1.put((task_name, priority))
        print(f"저장: ('{task_name}', {priority})")

    print("\n처리 순서:")
    result1 = []
    while not pq1.empty():
        task_name, priority = pq1.get()
        result1.append(task_name)
        print(f"  {task_name}")

    print("→ 문자열 사전순으로 정렬됨\n")

    # 시나리오 2: (숫자, 문자열) 형태로 변환해서 저장
    print("🎯 시나리오 2: (숫자, 문자열) 형태로 저장")
    pq2 = PriorityQueue()

    for task_name, priority in tasks:
        pq2.put((priority, task_name))  # 순서 바꿈!
        print(f"저장: ({priority}, '{task_name}')")

    print("\n처리 순서:")
    result2 = []
    while not pq2.empty():
        priority, task_name = pq2.get()
        result2.append(task_name)
        print(f"  {task_name}")

    print("→ 숫자(우선순위) 기준으로 정렬됨")
    print("→ 이것이 당신의 실제 결과와 일치!\n")

    # 결과 비교
    print("📊 결과 비교:")
    print(f"시나리오 1 (문자열 우선): {result1}")
    print(f"시나리오 2 (숫자 우선):   {result2}")
    print("\n실제 출력된 순서:", ["긴급 작업", "중요 작업", "일반 작업", "저우선순위"])
    print("→ 시나리오 2와 일치! 당신의 코드는 (priority, task) 형태로 저장했습니다.")


def demonstrate_tuple_comparison():
    """Python 튜플 비교 규칙 설명"""

    print("\n=== Python 튜플 비교 규칙 ===\n")

    # 기본 비교 규칙
    print("Python은 튜플을 첫 번째 요소부터 순차적으로 비교합니다:")

    comparisons = [
        (("긴급 작업", 1), ("일반 작업", 5)),
        (("긴급 작업", 10), ("일반 작업", 1)),  # 첫 번째가 결정적
        ((1, "일반 작업"), (2, "긴급 작업")),  # 숫자가 우선
        ((1, "Z작업"), (1, "A작업")),  # 같으면 두 번째로
    ]

    for t1, t2 in comparisons:
        result = t1 < t2
        print(f"{t1} < {t2} = {result}")

        # 설명
        if isinstance(t1[0], str) and isinstance(t2, str):
            print(f"  → 첫 번째 문자열: '{t1}' vs '{t2}'")
        elif isinstance(t1, int) and isinstance(t2, int):
            print(f"  → 첫 번째 숫자: {t1} vs {t2}")


def create_correct_priority_queue():
    """올바른 우선순위 큐 사용법"""

    print("\n=== 올바른 우선순위 큐 사용법 ===\n")

    tasks = [("긴급 작업", 1), ("일반 작업", 5), ("중요 작업", 2), ("저우선순위", 10)]

    # 숫자 우선순위를 원하는 경우
    print("숫자 우선순위를 원하는 경우:")
    pq = PriorityQueue()

    for task_name, priority in tasks:
        pq.put((priority, task_name))  # (우선순위, 작업명) 순서
        print(f"추가: 우선순위 {priority} - {task_name}")

    print("\n처리 순서 (낮은 숫자 = 높은 우선순위):")
    while not pq.empty():
        priority, task_name = pq.get()
        print(f"  {task_name} (우선순위: {priority})")


def simple_priority_queue_example():
    """간단한 우선순위 큐 예제"""

    print("\n=== 간단한 사용 예제 ===\n")

    pq = PriorityQueue()

    # 데이터 추가 (priority, data) 형태
    pq.put((3, "낮은 우선순위 작업"))
    pq.put((1, "높은 우선순위 작업"))
    pq.put((2, "중간 우선순위 작업"))

    print("우선순위 큐에 추가:")
    print("  (3, '낮은 우선순위 작업')")
    print("  (1, '높은 우선순위 작업')")
    print("  (2, '중간 우선순위 작업')")

    print("\n처리 순서:")
    while not pq.empty():
        priority, task = pq.get()
        print(f"  우선순위 {priority}: {task}")

    # 출력:
    # 우선순위 1: 높은 우선순위 작업
    # 우선순위 2: 중간 우선순위 작업
    # 우선순위 3: 낮은 우선순위 작업


if __name__ == "__main__":
    demonstrate_priority_queue_tuple_order_effect()
    demonstrate_tuple_comparison()
    create_correct_priority_queue()
    simple_priority_queue_example()
