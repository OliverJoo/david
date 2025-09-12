from typing import List, Tuple, Union
import copy


class DataStructureManager:
    """다양한 자료구조의 요소별 합산 및 추가 관리 클래스"""

    @staticmethod
    def calculate_element_wise_sum_zip(data: Union[tuple, list]) -> Union[tuple, list]:
        """zip()을 이용한 요소별 합산 계산"""
        try:
            # 입력 데이터 유효성 검사
            if not data or len(data) == 0:
                raise ValueError("데이터가 비어있습니다")

            # 모든 하위 요소의 길이가 동일한지 확인
            first_length = len(data[0])
            if not all(len(item) == first_length for item in data):
                raise ValueError("모든 하위 요소의 길이가 동일해야 합니다")

            # zip(*data)로 전치 후 각 위치별 합산
            sums = tuple(sum(column) for column in zip(*data))

            return sums

        except Exception as e:
            print(f"요소별 합산 실패: {e}")
            return None

    @staticmethod
    def add_sum_to_tuple_of_tuples(data_tuple: tuple) -> tuple:
        """튜플의 튜플에 합산 결과 추가"""
        try:
            # 요소별 합산 계산
            element_sum = DataStructureManager.calculate_element_wise_sum_zip(data_tuple)
            if element_sum is None:
                return data_tuple

            # 기존 튜플에 새 튜플 추가 (불변 객체이므로 새로운 튜플 생성)
            result = data_tuple + (element_sum,)

            print(f"원본: {data_tuple}")
            print(f"합산 결과: {element_sum}")  # 합산 결과: (16, 20, 27)
            print(f"최종: {result}")

            return result

        except Exception as e:
            print(f"튜플 추가 실패: {e}")
            return data_tuple

    @staticmethod
    def add_sum_to_tuple_list(tuple_list: list) -> list:
        """리스트의 튜플에 합산 결과 추가"""
        try:
            # 요소별 합산 계산
            element_sum = DataStructureManager.calculate_element_wise_sum_zip(tuple_list)
            if element_sum is None:
                return tuple_list

            # 리스트는 가변 객체이므로 직접 추가 가능
            result = copy.deepcopy(tuple_list)  # 원본 보호
            result.append(element_sum)

            print(f"원본: {tuple_list}")
            print(f"합산 결과: {element_sum}")  # 합산 결과: (16, 20, 27)
            print(f"최종: {result}")

            return result

        except Exception as e:
            print(f"튜플 리스트 추가 실패: {e}")
            return tuple_list

    @staticmethod
    def add_sum_to_list_of_lists(data_list: list) -> list:
        """리스트의 리스트에 합산 결과 추가"""
        try:
            # 요소별 합산 계산
            element_sum = DataStructureManager.calculate_element_wise_sum_zip(data_list)
            if element_sum is None:
                return data_list

            # 튜플을 리스트로 변환하여 추가
            sum_as_list = list(element_sum)

            result = copy.deepcopy(data_list)  # 원본 보호
            result.append(sum_as_list)

            print(f"원본: {data_list}")
            print(f"합산 결과: {sum_as_list}")  # 합산 결과: [16, 20, 27]
            print(f"최종: {result}")

            return result

        except Exception as e:
            print(f"리스트 추가 실패: {e}")
            return data_list


# 사용 예시
def demonstrate_zip_method():
    """zip() 방식 시연"""
    print("=" * 60)
    print("방법 1: zip()과 sum()을 활용한 요소별 합산")
    print("=" * 60)

    # 원본 데이터
    data_tuple = ((1, 2, 3), (3, 4, 7), (5, 6, 8), (7, 8, 9))
    tuple_list = ([1, 2, 3], [3, 4, 7], [5, 6, 8], [7, 8, 9])
    data_list = [[1, 2, 3], [3, 4, 7], [5, 6, 8], [7, 8, 9]]

    # 각 자료구조별 처리
    print("\n1. 튜플의 튜플 처리:")
    result1 = DataStructureManager.add_sum_to_tuple_of_tuples(data_tuple)

    print("\n2. 리스트의 튜플 처리:")
    result2 = DataStructureManager.add_sum_to_tuple_list(tuple_list)

    print("\n3. 리스트의 리스트 처리:")
    result3 = DataStructureManager.add_sum_to_list_of_lists(data_list)

    return result1, result2, result3


# 실행
demonstrate_zip_method()
