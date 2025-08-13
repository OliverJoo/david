from __future__ import annotations
from copy import copy, deepcopy

def demonstrate_shallow_vs_deep_dict():
    # 방어적 설정: 복합 구조(dict of dict/list)
    original = {
        "user": {"name": "Alice", "tags": ["admin", "owner"]},
        "count": 1,  # 불변
    }
    print("initial data:", original)

    shallow = copy(original)   # 최상위 dict만 새로 만듦, 내부는 공유
    deep = deepcopy(original)  # 내부까지 모두 복제

    # 1) 최상위 레벨 수정: 키에 새 값 할당(참조 바꾸기)
    shallow["count"] = 100          # shallow만 영향
    deep["user"] = {"name": "Bob"}  # deep만 영향

    # 2) 내부 객체 수정: 공유되는 내부 구조를 제자리 변경
    # original["user"]와 shallow["user"]는 같은 dict를 가리킴
    original["user"]["tags"].append("core")  # original과 shallow에 반영, deep에는 영향 없음

    # 3) 내부 불변 값 교체 vs 내부 가변 제자리 변경
    # 불변 교체(=참조 교체): 키 값 자체를 새 객체로 바꾸면 각 컨테이너 독립
    shallow["user"]["name"] = "Carol"   # original에도 보입니다(공유되는 내부 dict의 '값'을 교체)
    # 위 줄은 내부 dict의 키 값을 교체이므로 "내부 객체 수정"에 해당합니다.
    # 따라서 original과 shallow 모두에서 name이 "Carol"로 보입니다.

    return original, shallow, deep

original, shallow, deep = demonstrate_shallow_vs_deep_dict()
print("original:", original) # 결과: original: {'user': {'name': 'Carol', 'tags': ['admin', 'owner', 'core']}, 'count': 1}
print("shallow :", shallow) # 결과: shallow : {'user': {'name': 'Carol', 'tags': ['admin', 'owner', 'core']}, 'count': 100}
print("deep    :", deep) # 결과: deep    : {'user': {'name': 'Bob'}, 'count': 1}
