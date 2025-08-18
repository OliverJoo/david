# ============= bisect 모듈 완벽 활용 =============
import bisect
from typing import List


def demonstrate_bisect_module():
    """bisect 모듈의 모든 기능과 실전 활용"""

    print("=== bisect_left vs bisect_right 차이점 ===")

    # 예제 1: 중복 값이 있는 정렬된 리스트
    scores = [60, 70, 80, 80, 80, 90, 95]
    target_score = 80

    left_pos = bisect.bisect_left(scores, target_score)
    right_pos = bisect.bisect_right(scores, target_score)

    print(f"점수 리스트: {scores}")
    print(f"찾는 점수: {target_score}")
    print(f"bisect_left 결과: {left_pos} (첫 번째 80의 위치)")
    print(f"bisect_right 결과: {right_pos} (마지막 80의 다음 위치)")

    # 결과: left_pos = 2, right_pos = 5

    # 예제 2: 범위 내 개수 구하기
    def count_in_range(arr: List[int], left_val: int, right_val: int) -> int:
        """특정 범위에 속하는 원소의 개수 반환"""
        left_idx = bisect.bisect_left(arr, left_val)
        right_idx = bisect.bisect_right(arr, right_val)
        return right_idx - left_idx

    data = [1, 2, 3, 3, 3, 4, 4, 5, 6, 7, 8]
    range_count = count_in_range(data, 3, 5)
    print(f"\n데이터: {data}")
    print(f"3~5 범위의 원소 개수: {range_count}")
    # 결과: 5개 (3이 3개, 4가 2개)

    print(f"\n=== insort - 정렬 상태 유지하며 삽입 ===")

    # 예제 3: 실시간 순위 시스템
    class RankingSystem:
        def __init__(self):
            self.rankings = []  # 점수를 내림차순으로 유지

        def add_score(self, score: int):
            """점수를 추가하고 순위 유지"""
            # 내림차순 유지를 위해 음수로 변환하여 삽입
            bisect.insort_left(self.rankings, -score)

        def get_rankings(self) -> List[int]:
            """현재 순위 반환 (내림차순)"""
            return [-score for score in self.rankings]

        def get_rank(self, score: int) -> int:
            """특정 점수의 순위 반환 (1등부터)"""
            pos = bisect.bisect_left(self.rankings, -score)
            return pos + 1

    # 실시간 순위 테스트
    ranking = RankingSystem()
    scores_to_add = [85, 92, 78, 88, 95, 82]

    print("점수 추가 과정:")
    for score in scores_to_add:
        ranking.add_score(score)
        current_rankings = ranking.get_rankings()
        user_rank = ranking.get_rank(score)
        print(f"  {score}점 추가 → 순위: {current_rankings}, {score}점의 순위: {user_rank}등")
    # 결과: 각 점수 추가시마다 정렬된 순위 출력

    print(f"\n=== 실전 활용: 이진 탐색 구현 ===")

    # 예제 4: 커스텀 이진 탐색
    def binary_search_index(arr: List[int], target: int) -> int:
        """이진 탐색으로 정확한 인덱스 찾기 (없으면 -1)"""
        pos = bisect.bisect_left(arr, target)
        if pos < len(arr) and arr[pos] == target:
            return pos
        return -1

    def binary_search_range(arr: List[int], target: int) -> tuple:
        """target이 나타나는 첫 번째와 마지막 인덱스 반환"""
        left = bisect.bisect_left(arr, target)
        right = bisect.bisect_right(arr, target)

        if left == right:  # target이 존재하지 않음
            return (-1, -1)
        return (left, right - 1)

    # 테스트
    test_array = [1, 3, 3, 3, 5, 7, 7, 9]

    # 3의 위치 찾기
    first_3_index = binary_search_index(test_array, 3)
    range_3 = binary_search_range(test_array, 3)

    print(f"배열: {test_array}")
    print(f"3의 첫 번째 위치: {first_3_index}")
    print(f"3의 범위: {range_3}")

    # 결과: 첫 번째 위치 = 1, 범위 = (1, 3)

    # 예제 5: 좌표 압축 (Coordinate Compression)
    def coordinate_compression(coords: List[int]) -> dict:
        """좌표 압축을 통한 인덱스 매핑"""
        # 중복 제거하고 정렬
        unique_coords = sorted(set(coords))

        # 원본 좌표 -> 압축된 인덱스 매핑
        coord_to_index = {}
        for coord in coords:
            compressed_index = bisect.bisect_left(unique_coords, coord)
            coord_to_index[coord] = compressed_index

        return coord_to_index, unique_coords

    # 큰 좌표값들을 작은 인덱스로 압축
    large_coords = [1000000, 500, 1000000, 2000000, 500, 750000]
    mapping, unique_sorted = coordinate_compression(large_coords)

    print(f"\n원본 좌표: {large_coords}")
    print(f"압축된 좌표: {unique_sorted}")
    print(f"매핑: {mapping}")
    # 결과: 큰 수들이 0, 1, 2, 3 같은 작은 인덱스로 압축됨


demonstrate_bisect_module()
