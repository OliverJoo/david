from __future__ import annotations
import copy
import json
import pickle
import time
from typing import Any

def demonstrate_deep_copy():
    """깊은 복사의 모든 방법과 특징 시연 (Python 3.12)"""
    print("=== 깊은 복사 (Deep Copy) 완벽 분석 ===\n")

    # 복잡한 중첩 구조
    complex_data: dict[str, Any] = {
        "students": [
            {"name": "김철수", "scores": [85, 90, 78], "info": {"age": 20, "city": "서울"}},
            {"name": "박영희", "scores": [92, 88, 95], "info": {"age": 19, "city": "부산"}},
        ],
        "metadata": {
            "school": "한국대학교",
            "year": 2024,
            "subjects": ["수학", "영어", "과학"],
        },
    }

    # 경로 상수(실수 방지)
    STUDENTS = "students"
    METADATA = "metadata"
    SUBJECTS = "subjects"
    FIRST = 0
    SCORES = "scores"
    INFO = "info"

    # 1) 방어적 검증: 리스트 → 정수 인덱스 → 딕셔너리 키 순서
    assert isinstance(complex_data, dict)
    assert STUDENTS in complex_data and isinstance(complex_data[STUDENTS], list), "students는 list여야 함"
    assert len(complex_data[STUDENTS]) > FIRST, "students에 최소 1명 이상 필요"
    assert isinstance(complex_data[STUDENTS][FIRST], dict), "첫 번째 학생은 dict여야 함"
    assert SCORES in complex_data[STUDENTS][FIRST] and isinstance(complex_data[STUDENTS][FIRST][SCORES], list), "scores 리스트 필요"
    assert INFO in complex_data[STUDENTS][FIRST] and isinstance(complex_data[STUDENTS][FIRST][INFO], dict), "info dict 필요"
    assert METADATA in complex_data and SUBJECTS in complex_data[METADATA] and isinstance(complex_data[METADATA][SUBJECTS], list), "subjects 리스트 필요"

    # 편의 변수(동일 경로 재사용)
    students = complex_data[STUDENTS]                  # list
    first_student = students[FIRST]                    # dict
    scores = first_student[SCORES]                     # list
    subjects = complex_data[METADATA][SUBJECTS]        # list

    print("1. copy.deepcopy() 사용 (표준 방법)")
    deep_copy_1 = copy.deepcopy(complex_data)

    # 동일/상이 객체 여부 확인: 반드시 같은 경로로 비교
    print(f"원본과 복사본 최상위 객체 다름: {id(complex_data) != id(deep_copy_1)}")  # True
    print(f"내부 리스트도 다른 객체: {id(students) != id(deep_copy_1[STUDENTS])}")  # True
    print(f"더 깊은 내부 dict도 다름: {id(first_student) != id(deep_copy_1[STUDENTS][FIRST])}")  # True
    print(f"가장 깊은 레벨(첫 학생 scores 리스트)도 다름: "
          f"{id(scores) != id(deep_copy_1[STUDENTS][FIRST][SCORES])}")  # True
    print()
    # 예시:
    # 원본과 복사본 최상위 객체 다름: True
    # 내부 리스트도 다른 객체: True
    # 더 깊은 내부 dict도 다름: True
    # 가장 깊은 레벨(첫 학생 scores 리스트)도 다름: True

    print("2. 깊은 복사 확인 - 내부 객체 수정")
    print("수정 전:")
    print(f"원본 첫 번째 학생 점수: {complex_data[STUDENTS][FIRST][SCORES]}")   # -> [85, 90, 78]
    print(f"복사본 첫 번째 학생 점수: {deep_copy_1[STUDENTS][FIRST][SCORES]}")  # -> [85, 90, 78]

    # 복사본의 깊은 내부 수정 (원본 영향 없어야 함)
    deep_copy_1[STUDENTS][FIRST][SCORES][0] = 100
    deep_copy_1[STUDENTS][FIRST][INFO]["age"] = 25
    deep_copy_1[METADATA][SUBJECTS].append("체육")

    print("복사본 수정 후:")
    print(f"원본 첫 번째 학생 점수: {complex_data[STUDENTS][FIRST][SCORES]} (변경 안됨)")   # -> [85, 90, 78]
    print(f"복사본 첫 번째 학생 점수: {deep_copy_1[STUDENTS][FIRST][SCORES]} (변경됨)")      # -> [100, 90, 78]
    print(f"원본 첫 번째 학생 나이: {complex_data[STUDENTS][FIRST][INFO]['age']} (변경 안됨)") # -> 20
    print(f"복사본 첫 번째 학생 나이: {deep_copy_1[STUDENTS][FIRST][INFO]['age']} (변경됨)")    # -> 25
    print("→ 깊은 복사는 완전히 독립적!\n")

    print("3. 다른 깊은 복사 방법들")
    # JSON (직렬화 가능한 기본 타입에 한정)
    try:
        json_deep_copy = json.loads(json.dumps(complex_data))
        assert json_deep_copy[STUDENTS][1][SCORES] == [92, 88, 95]
        print("✅ JSON 방법 성공 (단, datetime/tuple/set/사용자정의 객체 등은 제약)")
    except Exception as e:
        print(f"❌ JSON 방법 실패: {e}")

    # pickle (더 다양한 객체 지원, 보안/환경 주의)
    try:
        pickle_deep_copy = pickle.loads(pickle.dumps(complex_data))
        assert pickle_deep_copy[METADATA]["school"] == "한국대학교"
        print("✅ Pickle 방법 성공 (더 다양한 객체 지원, 환경/보안 주의)")
    except Exception as e:
        print(f"❌ Pickle 방법 실패: {e}")

    # 재귀 수동 깊은 복사 (학습용)
    def manual_deep_copy(obj: Any) -> Any:
        if isinstance(obj, dict):
            return {k: manual_deep_copy(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [manual_deep_copy(x) for x in obj]
        if isinstance(obj, tuple):
            return tuple(manual_deep_copy(x) for x in obj)
        if isinstance(obj, set):
            return {manual_deep_copy(x) for x in obj}
        return obj

    manual_deep_copy_result = manual_deep_copy(complex_data)
    # 분리 여부 확인 (같은 경로로 비교)
    assert manual_deep_copy_result is not complex_data
    assert manual_deep_copy_result[STUDENTS][FIRST] is not complex_data[STUDENTS][FIRST]
    assert manual_deep_copy_result[STUDENTS][FIRST][SCORES] is not complex_data[STUDENTS][FIRST][SCORES]
    print("✅ 수동 깊은 복사 성공 (교육용, 실제로는 copy.deepcopy 권장)\n")

    print("4. 성능 비교 (참고용)")
    large_data = {"data": [[i for i in range(100)] for _ in range(100)]}

    start = time.time()
    for _ in range(10):
        copy.deepcopy(large_data)
    deepcopy_time = time.time() - start

    start = time.time()
    for _ in range(10):
        json.loads(json.dumps(large_data))
    json_time = time.time() - start

    print(f"copy.deepcopy() 시간: {deepcopy_time:.4f}초")
    print(f"JSON 방법 시간: {json_time:.4f}초")
    print("→ JSON이 빠를 수 있으나 타입 제약 큼")

if __name__ == "__main__":
    demonstrate_deep_copy()
# 실행 예시(요약)
# 수정 전:
# 원본 첫 번째 학생 점수: [85, 90, 78]
# 복사본 첫 번째 학생 점수: [85, 90, 78]
# 복사본 수정 후:
# 원본 첫 번째 학생 점수: [85, 90, 78] (변경 안됨)
# 복사본 첫 번째 학생 점수: [100, 90, 78] (변경됨)
# 원본 첫 번째 학생 나이: 20 (변경 안됨)
# 복사본 첫 번째 학생 나이: 25 (변경됨)