from __future__ import annotations
from copy import copy, deepcopy

def demonstrate_shallow_vs_deep_list():
    # 원본: 내부에 가변(list)과 불변(int)이 섞인 구조
    original = [[1, 2], [3, 4], 5]
    print("initial data:", original)

    # 얕은/깊은 복사
    shallow = copy(original)
    deep = deepcopy(original)

    # 안전하게 인덱싱할 수 있도록 길이 확인
    def safe_set(lst, idx, value):
        # 필요한 경우 None으로 패딩하여 인덱스 확보
        if idx >= len(lst):
            lst.extend([None] * (idx - len(lst) + 1))
        lst[idx] = value

    # 1) 최상위 레벨 수정: 슬롯 교체(슬라이스/append가 아님)
    # shallow[0]은 반드시 존재하도록 방어
    safe_set(shallow, 0, ["X", "Y"])   # shallow만 영향
    safe_set(deep, 1, ["A", "B"])      # deep만 영향

    # 2) 내부 객체 수정: 공유된 내부 리스트 제자리 변경
    # original과 shallow는 original[1] 같은 내부 리스트를 공유
    if len(original) > 1 and isinstance(original[1], list):
        original[1].append(99)          # original과 shallow 모두에 반영, deep은 영향 없음

    # 3) 불변 객체 교체(참조 교체 = 최상위 레벨 수정)
    # 인덱스 2가 없다면 패딩하여 안전하게 할당
    safe_set(shallow, 2, 500)           # shallow만 영향
    safe_set(deep, 2, 900)              # deep만 영향

    return original, shallow, deep

# 실행 및 결과 출력
original, shallow, deep = demonstrate_shallow_vs_deep_list()
print("original:", original) # 결과: original: [[1, 2], [3, 4, 99], 5]
print("shallow :", shallow) # 결과: shallow : [['X', 'Y'], [3, 4, 99], 500]
print("deep    :", deep) # 결과: deep    : [[1, 2], ['A', 'B'], 900]