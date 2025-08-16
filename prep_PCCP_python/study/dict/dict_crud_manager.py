# ============= DICTIONARY CRUD 연산 예제 =============
class DictCRUDManager:
    """딕셔너리 CRUD 연산을 안전하게 관리하는 클래스"""

    def __init__(self):
        self.data: dict = {}

    # CREATE: 딕셔너리 생성/키-값 추가
    def create_dict(self, items: dict) -> dict:
        """새로운 딕셔너리 생성"""
        self.data = items.copy()  # 방어적 복사
        return self.data

    def add_item(self, key, value) -> bool:
        """키-값 쌍 추가"""
        try:
            # 방법 1: 대괄호 표기법
            self.data[key] = value
            return True
        except Exception as e:
            print(f"추가 실패: {e}")
            return False

    def add_multiple(self, items: dict) -> bool:
        """여러 키-값 쌍 한번에 추가"""
        try:
            # 방법 2: update() 메서드
            self.data.update(items)
            return True
        except Exception as e:
            print(f"다중 추가 실패: {e}")
            return False

    # READ: 데이터 조회
    def read_item(self, key, default=None):
        """키로 값 조회"""
        # 방법 1: get() 메서드 (안전함, 기본값 설정 가능)
        return self.data.get(key, default)

    def read_item_direct(self, key):
        """키로 직접 값 조회 (KeyError 발생 가능)"""
        try:
            # 방법 2: 대괄호 표기법 (KeyError 발생 가능)
            return self.data[key]
        except KeyError:
            print(f"키 '{key}'를 찾을 수 없습니다.")
            return None

    def read_all(self) -> dict:
        """모든 아이템 조회"""
        return self.data.copy()

    def get_keys(self) -> list:
        """모든 키 조회"""
        return list(self.data.keys())

    def get_values(self) -> list:
        """모든 값 조회"""
        return list(self.data.values())

    def get_items(self) -> list:
        """모든 키-값 쌍 조회"""
        return list(self.data.items())

    # UPDATE: 데이터 수정
    def update_item(self, key, new_value) -> bool:
        """기존 키의 값 수정"""
        if key in self.data:
            self.data[key] = new_value
            return True
        else:
            print(f"키 '{key}'가 존재하지 않습니다.")
            return False

    # DELETE: 데이터 삭제
    def delete_item(self, key):
        """키로 아이템 삭제"""
        try:
            # 방법 1: pop() 메서드 (삭제된 값 반환)
            return self.data.pop(key)
        except KeyError:
            print(f"키 '{key}'를 찾을 수 없습니다.")
            return None

    def delete_item_safe(self, key, default=None):
        """키로 안전하게 아이템 삭제"""
        # 방법 2: pop() with default
        return self.data.pop(key, default)

    def clear_all(self):
        """모든 아이템 삭제"""
        self.data.clear()


# 사용 예제
print("=== DICTIONARY CRUD 연산 예제 ===")
dict_manager = DictCRUDManager()

# CREATE
student_info = {"name": "김철수", "age": 20, "grade": 85}
dict_manager.create_dict(student_info)
print(f"생성된 딕셔너리: {dict_manager.read_all()}")

# 아이템 추가
dict_manager.add_item("city", "서울")
dict_manager.add_multiple({"major": "컴퓨터공학", "year": 2})
print(f"추가 후: {dict_manager.read_all()}")

# READ
print(f"이름: {dict_manager.read_item('name')}")
print(f"존재하지 않는 키: {dict_manager.read_item('height', '정보없음')}")
print(f"모든 키: {dict_manager.get_keys()}")
print(f"모든 값: {dict_manager.get_values()}")

# UPDATE
dict_manager.update_item("age", 21)
print(f"나이 수정 후: {dict_manager.read_all()}")

# DELETE
deleted_grade = dict_manager.delete_item("grade")
print(f"삭제된 성적: {deleted_grade}")
print(f"삭제 후: {dict_manager.read_all()}")
