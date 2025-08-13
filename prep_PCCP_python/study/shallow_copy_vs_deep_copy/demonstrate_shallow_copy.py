# ============= 얕은 복사 완벽 이해 예제 =============
# 얕은 복사(copy or slicing): 복사된 “겉 컨테이너” 자체에 대한 구조 변경. 즉, 컨테이너 객체만 새로 할당하고 내부 요소들은 원본과 같은 객체를 참조하므로, 컨테이너의 슬롯을 재할당하는 최상위 레벨 수정은 복사본만 영향을 받지만, 내부 가변 객체를 제자리(in-place)로 변경하면 원본과 복사본 모두에 반영됩니다.
#
# 깊은 복사(deepcopy): 컨테이너와 내부의 모든 가변 객체를 재귀적으로 새로 복제하여 완전히 독립된 메모리 구조를 가지므로, 최상위 레벨 수정이든 내부 객체 수정이든 원본과 복사본이 서로 전혀 영향을 주지 않습니다.

import copy


def demonstrate_shallow_copy():
    """얕은 복사의 모든 방법과 주의사항 시연"""

    print("=== 얕은 복사 (Shallow Copy) 완벽 분석 ===\n")

    # 1차원 리스트의 얕은 복사 (문제없음)
    print("1. 단순 리스트 얕은 복사")
    simple_list = [1, 2, 3, 4, 5]

    # 얕은 복사의 5가지 방법
    copy1 = simple_list[:]  # 방법 1: 슬라이싱
    copy2 = simple_list.copy()  # 방법 2: copy() 메서드
    copy3 = list(simple_list)  # 방법 3: list() 생성자
    copy4 = copy.copy(simple_list)  # 방법 4: copy.copy()
    copy5 = [item for item in simple_list]  # 방법 5: 리스트 컴프리헨션

    print(f"원본: {simple_list}")
    print(f"복사본들이 모두 동일: {copy1 == copy2 == copy3 == copy4 == copy5}")
    print(f"하지만 서로 다른 객체: {id(simple_list) != id(copy1)}")

    # 원본 수정해보기
    simple_list.append(6)
    print(f"원본 수정 후 - 원본: {simple_list}")
    print(f"원본 수정 후 - 복사본: {copy1} (영향 받지 않음)")
    print()

    # 2차원 리스트의 얕은 복사 (문제 발생!)
    print("2. 중첩 리스트 얕은 복사 - 문제점 발견!")
    nested_list = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    shallow_copy = nested_list[:]  # 얕은 복사

    print(f"원본: {nested_list}")
    print(f"얕은 복사본: {shallow_copy}")
    print(f"최상위 리스트 ID 다름: {id(nested_list) != id(shallow_copy)}")
    print(f"내부 리스트 ID 같음: {id(nested_list[0]) == id(shallow_copy)}")
    print()

    # 최상위 레벨 수정 (문제없음)
    print("최상위 레벨 수정:")
    shallow_copy.append([10, 11, 12])
    print(f"복사본에 리스트 추가 후 - 원본: {nested_list}")
    print(f"복사본에 리스트 추가 후 - 복사본: {shallow_copy}")
    print("→ 최상위 레벨은 독립적!")
    print()

    # 내부 객체 수정 (문제 발생!)
    print("⚠️  내부 객체 수정 - 문제 발생!")
    shallow_copy[0][0] = 999  # 첫 번째 내부 리스트의 첫 번째 요소 수정
    print(f"복사본 내부 수정 후 - 원본: {nested_list}")
    print(f"복사본 내부 수정 후 - 복사본: {shallow_copy}")
    print("→ 내부 객체는 공유되므로 둘 다 변경됨!")
    print()

    # 딕셔너리와 세트의 얕은 복사
    print("3. 딕셔너리 얕은 복사")
    nested_dict = {
        'user1': {'name': '김철수', 'scores': [85, 90, 78]},
        'user2': {'name': '박영희', 'scores': [92, 88, 95]}
    }

    dict_shallow = nested_dict.copy()
    print(f"원본 딕셔너리: {nested_dict}")

    # 내부 딕셔너리 수정
    dict_shallow['user1']['scores'] = 100  # 내부 리스트 수정
    print(f"복사본 내부 수정 후 - 원본: {nested_dict}")
    print(f"복사본 내부 수정 후 - 복사본: {dict_shallow}")
    print("→ 딕셔너리도 같은 문제 발생!")


demonstrate_shallow_copy()
