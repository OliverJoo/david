# ============= SET CRUD 연산 예제 =============
class SetCRUDManager:
    """세트 CRUD 연산을 안전하게 관리하는 클래스"""

    def __init__(self):
        self.data: set = set()

    # CREATE: 세트 생성/요소 추가
    def create_set(self, items) -> set:
        """새로운 세트 생성"""
        self.data = set(items)  # 자동으로 중복 제거
        return self.data

    def add_item(self, item) -> bool:
        """요소 추가"""
        try:
            # 방법 1: add() 메서드 (단일 요소)
            initial_size = len(self.data)
            self.data.add(item)
            return len(self.data) > initial_size  # 실제 추가되었는지 확인
        except Exception as e:
            print(f"추가 실패: {e}")
            return False

    def add_multiple(self, items) -> bool:
        """여러 요소 한번에 추가"""
        try:
            # 방법 2: update() 메서드 (여러 요소)
            self.data.update(items)
            return True
        except Exception as e:
            print(f"다중 추가 실패: {e}")
            return False

    # READ: 데이터 조회
    def contains(self, item) -> bool:
        """요소 존재 여부 확인"""
        return item in self.data

    def read_all(self) -> set:
        """모든 요소 조회"""
        return self.data.copy()

    def get_size(self) -> int:
        """세트 크기 조회"""
        return len(self.data)

    def is_empty(self) -> bool:
        """빈 세트인지 확인"""
        return len(self.data) == 0

    # UPDATE: 세트는 일반적으로 수정 개념이 없음 (삭제 후 추가)
    def replace_item(self, old_item, new_item) -> bool:
        """요소 교체 (삭제 후 추가)"""
        if old_item in self.data:
            self.data.remove(old_item)
            self.data.add(new_item)
            return True
        return False

    # DELETE: 데이터 삭제
    def delete_item(self, item) -> bool:
        """요소 삭제"""
        try:
            # 방법 1: remove() 메서드 (없으면 KeyError)
            self.data.remove(item)
            return True
        except KeyError:
            print(f"요소 '{item}'을 찾을 수 없습니다.")
            return False

    def delete_item_safe(self, item) -> bool:
        """안전하게 요소 삭제"""
        # 방법 2: discard() 메서드 (없어도 오류 없음)
        initial_size = len(self.data)
        self.data.discard(item)
        return len(self.data) < initial_size

    def pop_random(self):
        """임의의 요소 삭제 및 반환"""
        try:
            return self.data.pop()
        except KeyError:
            print("세트가 비어있습니다.")
            return None

    def clear_all(self):
        """모든 요소 삭제"""
        self.data.clear()

    # 집합 연산 메서드들
    def union_with(self, other_set) -> set:
        """합집합"""
        return self.data.union(other_set)

    def intersection_with(self, other_set) -> set:
        """교집합"""
        return self.data.intersection(other_set)

    def difference_with(self, other_set) -> set:
        """차집합"""
        return self.data.difference(other_set)


# 사용 예제
print("=== SET CRUD 연산 예제 ===")
set_manager = SetCRUDManager()

# CREATE
fruits = ["apple", "banana", "orange", "apple", "grape"]  # 중복 포함
set_manager.create_set(fruits)
print(f"생성된 세트 (중복 자동 제거): {set_manager.read_all()}")

# 요소 추가
print(f"'kiwi' 추가 성공: {set_manager.add_item('kiwi')}")
print(f"'apple' 추가 시도 (이미 존재): {set_manager.add_item('apple')}")
set_manager.add_multiple(['mango', 'peach'])
print(f"추가 후: {set_manager.read_all()}")

# READ
print(f"'banana' 존재: {set_manager.contains('banana')}")
print(f"'cherry' 존재: {set_manager.contains('cherry')}")
print(f"세트 크기: {set_manager.get_size()}")

# UPDATE (교체)
set_manager.replace_item('banana', 'cherry')
print(f"'banana'를 'cherry'로 교체 후: {set_manager.read_all()}")

# DELETE
print(f"'apple' 삭제 성공: {set_manager.delete_item('apple')}")
print(f"'watermelon' 안전 삭제: {set_manager.delete_item_safe('watermelon')}")
print(f"삭제 후: {set_manager.read_all()}")

# 집합 연산
other_fruits = {'cherry', 'lemon', 'apple'}
print(f"다른 세트: {other_fruits}")
print(f"합집합: {set_manager.union_with(other_fruits)}")
print(f"교집합: {set_manager.intersection_with(other_fruits)}")
print(f"차집합: {set_manager.difference_with(other_fruits)}")
