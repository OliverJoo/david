from typing import Any, Union, Optional, Dict, List, Tuple, Set
from collections import defaultdict


class IndexFinder:
    """다양한 자료구조에서 값의 인덱스/위치를 찾는 클래스"""

    def __init__(self):
        """인덱스 파인더 초기화"""
        self.search_methods = ['first', 'all', 'safe']

    def find_in_list(self, data: List[Any], target_value: Any, method: str = 'first') -> Union[int, List[int], None]:
        """리스트에서 값의 인덱스 찾기"""
        try:
            if not isinstance(data, list):
                raise TypeError("데이터가 리스트가 아닙니다.")

            if method == 'first':
                # 첫 번째 발견된 인덱스만 반환[95]
                index = data.index(target_value)
                print(f"리스트에서 '{target_value}' 첫 번째 위치: {index}")
                return index

            elif method == 'all':
                # 모든 발견된 인덱스 반환[27]
                indices = [i for i, value in enumerate(data) if value == target_value]
                print(f"리스트에서 '{target_value}' 모든 위치: {indices}")
                return indices

            elif method == 'safe':
                # 안전한 검색 (없으면 None 반환)
                try:
                    index = data.index(target_value)
                    print(f"리스트에서 '{target_value}' 안전 검색 위치: {index}")
                    return index
                except ValueError:
                    print(f"리스트에서 '{target_value}'를 찾을 수 없습니다.")
                    return None

        except ValueError as e:
            print(f"값 오류: {e}")
            return None
        except Exception as e:
            print(f"리스트 검색 실패: {e}")
            return None

    def find_in_dict_by_value(self, data: Dict[Any, Any], target_value: Any,
                              method: str = 'first') -> Union[Any, List[Any], None]:
        """딕셔너리에서 값으로 키 찾기 (역방향 검색)"""
        try:
            if not isinstance(data, dict):
                raise TypeError("데이터가 딕셔너리가 아닙니다.")

            if method == 'first':
                # 첫 번째 발견된 키만 반환
                for key, value in data.items():
                    if value == target_value:
                        print(f"딕셔너리에서 값 '{target_value}'의 첫 번째 키: '{key}'")
                        return key
                print(f"딕셔너리에서 값 '{target_value}'를 찾을 수 없습니다.")
                return None

            elif method == 'all':
                # 모든 발견된 키 반환
                keys = [key for key, value in data.items() if value == target_value]
                print(f"딕셔너리에서 값 '{target_value}'의 모든 키: {keys}")
                return keys

        except Exception as e:
            print(f"딕셔너리 검색 실패: {e}")
            return None

    def find_in_tuple(self, data: Tuple[Any, ...], target_value: Any,
                      method: str = 'first') -> Union[int, List[int], None]:
        """튜플에서 값의 인덱스 찾기"""
        try:
            if not isinstance(data, tuple):
                raise TypeError("데이터가 튜플이 아닙니다.")

            if method == 'first':
                # 첫 번째 발견된 인덱스만 반환[98]
                index = data.index(target_value)
                print(f"튜플에서 '{target_value}' 첫 번째 위치: {index}")
                return index

            elif method == 'all':
                # 모든 발견된 인덱스 반환
                indices = [i for i, value in enumerate(data) if value == target_value]
                print(f"튜플에서 '{target_value}' 모든 위치: {indices}")
                return indices

        except ValueError as e:
            print(f"튜플에서 '{target_value}'를 찾을 수 없습니다.")
            return None
        except Exception as e:
            print(f"튜플 검색 실패: {e}")
            return None

    def find_in_set(self, data: Set[Any], target_value: Any) -> bool:
        """집합에서 값 존재 여부 확인 (인덱스 개념 없음)"""
        try:
            if not isinstance(data, set):
                raise TypeError("데이터가 집합이 아닙니다.")

            exists = target_value in data
            if exists:
                print(f"집합에서 '{target_value}' 존재함 (순서 없음)")
            else:
                print(f"집합에서 '{target_value}' 존재하지 않음")
            return exists

        except Exception as e:
            print(f"집합 검색 실패: {e}")
            return False

    def find_tuple_in_list(self, data: List[Tuple], target_tuple: Tuple,
                           sub_index: Optional[int] = None) -> Union[int, List[int], None]:
        """튜플을 요소로 가진 리스트에서 튜플 또는 특정 위치 값 검색[91]"""
        try:
            if not isinstance(data, list):
                raise TypeError("데이터가 리스트가 아닙니다.")

            if sub_index is not None:
                # 특정 서브 인덱스의 값으로 검색
                indices = []
                for i, item in enumerate(data):
                    if isinstance(item, tuple) and len(item) > sub_index:
                        if item[sub_index] == target_tuple:
                            indices.append(i)

                if indices:
                    print(f"튜플 리스트에서 [{sub_index}]번째 값이 '{target_tuple}'인 위치: {indices}")
                    return indices[0] if len(indices) == 1 else indices
                else:
                    print(f"튜플 리스트에서 [{sub_index}]번째 값 '{target_tuple}'를 찾을 수 없습니다.")
                    return None
            else:
                # 전체 튜플로 검색
                try:
                    index = data.index(target_tuple)
                    print(f"튜플 리스트에서 튜플 {target_tuple}의 위치: {index}")
                    return index
                except ValueError:
                    print(f"튜플 리스트에서 튜플 {target_tuple}를 찾을 수 없습니다.")
                    return None

        except Exception as e:
            print(f"튜플 리스트 검색 실패: {e}")
            return None


# 사용 예시 및 결과
finder = IndexFinder()

print("=== 리스트에서 인덱스 찾기 ===")
test_list = [10, 20, 30, 20, 40, 20]
finder.find_in_list(test_list, 20, 'first')  # 리스트에서 '20' 첫 번째 위치: 1
finder.find_in_list(test_list, 20, 'all')  # 리스트에서 '20' 모든 위치: [1, 3, 5]
finder.find_in_list(test_list, 999, 'safe')  # 리스트에서 '999'를 찾을 수 없습니다.

print("\n=== 딕셔너리에서 키 찾기 (역방향) ===")
test_dict = {"name": "홍길동", "age": 25, "city": "서울", "nickname": "홍길동"}
finder.find_in_dict_by_value(test_dict, "홍길동", 'first')  # 딕셔너리에서 값 '홍길동'의 첫 번째 키: 'name'
finder.find_in_dict_by_value(test_dict, "홍길동", 'all')  # 딕셔너리에서 값 '홍길동'의 모든 키: ['name', 'nickname']

print("\n=== 튜플에서 인덱스 찾기 ===")
test_tuple = ("Python", "Java", "C++", "Java", "Go")
finder.find_in_tuple(test_tuple, "Java", 'first')  # 튜플에서 'Java' 첫 번째 위치: 1
finder.find_in_tuple(test_tuple, "Java", 'all')  # 튜플에서 'Java' 모든 위치: [1, 3]

print("\n=== 집합에서 존재 여부 확인 ===")
test_set = {100, 200, 300, 400}
finder.find_in_set(test_set, 200)  # 집합에서 '200' 존재함 (순서 없음)
finder.find_in_set(test_set, 999)  # 집합에서 '999' 존재하지 않음

print("\n=== 튜플 리스트에서 검색 ===")
tuple_list = [("apple", 5), ("banana", 7), ("cherry", 3), ("apple", 10)]
finder.find_tuple_in_list(tuple_list, ("banana", 7))  # 튜플 리스트에서 튜플 ('banana', 7)의 위치: 1
finder.find_tuple_in_list(tuple_list, "apple", 0)  # 튜플 리스트에서 [0]번째 값이 'apple'인 위치: [0, 3]
finder.find_tuple_in_list(tuple_list, 7, 1)  # 튜플 리스트에서 [1]번째 값이 '7'인 위치: 1
