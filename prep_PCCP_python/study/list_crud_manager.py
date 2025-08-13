# ============= LIST CRUD 연산 예제 =============
import copy
from typing import List, Any


class ListCRUDManager:
    """리스트 CRUD 연산을 안전하게 관리하는 클래스"""

    def __init__(self):
        self.data: List[Any] = []

    # CREATE: 데이터 생성/추가
    def create_list(self, items: List[Any]) -> List[Any]:
        """새로운 리스트 생성"""
        self.data = items.copy()  # 방어적 복사
        return self.data

    def add_item(self, item: Any, index: int = None) -> bool:
        """아이템 추가 (끝에 추가 또는 특정 위치에 삽입)"""
        try:
            if index is None:
                self.data.append(item)  # 방법 1: 끝에 추가
            else:
                self.data.insert(index, item)  # 방법 2: 특정 위치에 삽입
            return True
        except (IndexError, TypeError) as e:
            print(f"추가 실패: {e}")
            return False

    # READ: 데이터 조회
    def read_item(self, index: int) -> Any:
        """인덱스로 아이템 조회"""
        try:
            return self.data[index]
        except IndexError:
            print(f"인덱스 {index}는 범위를 벗어났습니다.")
            return None

    def read_all(self) -> List[Any]:
        """모든 아이템 조회"""
        return self.data.copy()  # 방어적 복사로 원본 보호

    # UPDATE: 데이터 수정
    def update_item(self, index: int, new_value: Any) -> bool:
        """특정 인덱스의 아이템 수정"""
        try:
            if 0 <= index < len(self.data):
                self.data[index] = new_value
                return True
            else:
                print(f"인덱스 {index}는 유효하지 않습니다.")
                return False
        except TypeError as e:
            print(f"수정 실패: {e}")
            return False

    # DELETE: 데이터 삭제
    def delete_item(self, index: int = None, value: Any = None) -> Any:
        """인덱스 또는 값으로 아이템 삭제"""
        try:
            if index is not None:
                return self.data.pop(index)  # 방법 1: 인덱스로 삭제
            elif value is not None:
                self.data.remove(value)  # 방법 2: 값으로 삭제
                return value
            else:
                return self.data.pop()  # 마지막 요소 삭제
        except (IndexError, ValueError) as e:
            print(f"삭제 실패: {e}")
            return None


# 사용 예제
print("=== LIST CRUD 연산 예제 ===")
manager = ListCRUDManager()

# CREATE
numbers = [1, 2, 3, 4, 5]
manager.create_list(numbers)
print(f"생성된 리스트: {manager.read_all()}")

# 아이템 추가
manager.add_item(6)  # 끝에 추가
manager.add_item(0, 0)  # 맨 앞에 삽입
print(f"추가 후: {manager.read_all()}")

# READ
print(f"인덱스 2의 값: {manager.read_item(2)}")
print(f"전체 리스트: {manager.read_all()}")

# UPDATE
manager.update_item(1, 99)
print(f"수정 후: {manager.read_all()}")

# DELETE
deleted = manager.delete_item(0)  # 인덱스로 삭제
print(f"삭제된 값: {deleted}, 삭제 후: {manager.read_all()}")

manager.delete_item(value=99)  # 값으로 삭제
print(f"값 삭제 후: {manager.read_all()}")
