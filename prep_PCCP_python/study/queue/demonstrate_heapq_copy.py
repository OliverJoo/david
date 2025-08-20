"""
heapq 복사(얕은 vs 깊은) 데모
Python 3.12  기준
"""
from __future__ import annotations

import copy
import heapq
from typing import List, Tuple


def demonstrate_heapq_copy() -> None:
    """Heapq(리스트) 복사 특성을 시각적으로 보여준다."""
    print("\n=== Heapq 복사 특성 ===")

    # 1) 원본 힙 생성 ─ 튜플 (우선순위, 작업목록) 구조
    original_heap: List[Tuple[int, List[str]]] = [
        (1, ["task_a"]),
        (3, ["task_b"]),
        (2, ["task_c"]),
    ]
    heapq.heapify(original_heap)          # O(n)
    print(f"원본 힙        : {original_heap}")

    # 2) 얕은·깊은 복사
    shallow_heap = copy.copy(original_heap)
    deep_heap = copy.deepcopy(original_heap)
    print(f"얕은 복사      : {shallow_heap}")
    print(f"깊은 복사      : {deep_heap}")

    # 3) 객체 ID 비교
    print("\n[ID 비교] 최상위 리스트는 모두 다르다")
    print(
        f" original vs shallow : {id(original_heap) != id(shallow_heap)}\n"
        f" original vs deep    : {id(original_heap) != id(deep_heap)}"
    )

    print("\n[ID 비교] 내부 리스트(shared vs isolated)")
    print(
        f" original_heap[0][1] id : {id(original_heap[1])}\n"
        f" shallow_heap[1]  id : {id(shallow_heap[1])}  <- 공유\n"
        f" deep_heap[1]     id : {id(deep_heap[1])}     <- 독립"
    )

    # 4) 내부 객체 수정 — shallow 는 영향, deep 은 무영향
    print("\n[수정 테스트] original 내부 리스트에 'extra' 추가")
    original_heap[1].append("extra")
    print(f"원본   : {original_heap}")
    print(f"얕은복사: {shallow_heap}  ← 영향 받음")
    print(f"깊은복사: {deep_heap}     ← 영향 없음")

    # 5) 힙 연산이 각 사본에 독립적으로 작동하는지 확인
    heapq.heappush(original_heap, (0, ["urgent"]))     # 우선순위 0
    heapq.heappush(shallow_heap,  (4, ["low"]))        # 우선순위 4
    print("\n[heappush 이후]")
    print(f"original heappush(0) : {original_heap}")
    print(f"shallow  heappush(4) : {shallow_heap}")
    print(f"deep     변화 없음   : {deep_heap}")

    # 6) pop 으로 힙 성질 유지 확인
    print(f"\noriginal heappop → {heapq.heappop(original_heap)}")
    print(f"original 상태     : {original_heap}")


# --------- 간단 테스트 루틴 ---------
if __name__ == "__main__":
    try:
        demonstrate_heapq_copy()
        print("\n✅ 모든 데모가 정상 종료되었습니다.")
    except Exception as exc:              # 최후 방어
        print(f"❌ 데모 중 예외 발생: {exc}")
