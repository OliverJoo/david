# ============= TUPLE CRUD 연산 예제 =============
class TupleCRUDManager:
    """튜플 CRUD 연산을 관리하는 클래스 (불변성으로 인한 제약 있음)"""

    def __init__(self):
        self.data = ()

    # CREATE: 새로운 튜플 생성
    def create_tuple(self, items) -> tuple:
        """새로운 튜플 생성"""
        self.data = tuple(items)
        return self.data

    def add_item(self, item) -> tuple:
        """아이템 추가 (새로운 튜플 반환)"""
        # 방법 1: + 연산자 사용
        new_tuple_1 = self.data + (item,)

        # 방법 2: unpacking 사용
        new_tuple_2 = (*self.data, item)

        self.data = new_tuple_1  # 실제로는 새로운 객체
        return self.data

    # READ: 데이터 조회
    def read_item(self, index: int):
        """인덱스로 아이템 조회"""
        try:
            return self.data[index]
        except IndexError:
            print(f"인덱스 {index}는 범위를 벗어났습니다.")
            return None

    def read_all(self) -> tuple:
        """모든 아이템 조회"""
        return self.data

    # UPDATE: 데이터 수정 (실제로는 새로운 튜플 생성)
    def update_item(self, index: int, new_value) -> tuple:
        """특정 인덱스의 아이템 '수정' (새로운 튜플 생성)"""
        try:
            if 0 <= index < len(self.data):
                # 리스트로 변환 → 수정 → 다시 튜플로
                temp_list = list(self.data)
                temp_list[index] = new_value
                self.data = tuple(temp_list)
                return self.data
            else:
                print(f"인덱스 {index}는 유효하지 않습니다.")
                return self.data
        except Exception as e:
            print(f"수정 실패: {e}")
            return self.data

    # DELETE: 데이터 삭제 (실제로는 새로운 튜플 생성)
    def delete_item(self, index: int) -> tuple:
        """인덱스로 아이템 '삭제' (새로운 튜플 생성)"""
        try:
            if 0 <= index < len(self.data):
                # 슬라이싱으로 제거
                self.data = self.data[:index] + self.data[index + 1:]
                return self.data
            else:
                print(f"인덱스 {index}는 유효하지 않습니다.")
                return self.data
        except Exception as e:
            print(f"삭제 실패: {e}")
            return self.data


# 사용 예제
print("=== TUPLE CRUD 연산 예제 ===")
tuple_manager = TupleCRUDManager()

# CREATE
coords = (1, 2, 3)
tuple_manager.create_tuple(coords)
print(f"생성된 튜플: {tuple_manager.read_all()}")

# 아이템 추가
tuple_manager.add_item(4)
print(f"추가 후: {tuple_manager.read_all()}")

# READ
print(f"인덱스 1의 값: {tuple_manager.read_item(1)}")

# UPDATE (새로운 튜플 생성)
original_id = id(tuple_manager.data)
tuple_manager.update_item(1, 99)
new_id = id(tuple_manager.data)
print(f"수정 후: {tuple_manager.read_all()}")
print(f"객체 ID 변경됨: {original_id} → {new_id}")

# DELETE (새로운 튜플 생성)
tuple_manager.delete_item(0)
print(f"삭제 후: {tuple_manager.read_all()}")
