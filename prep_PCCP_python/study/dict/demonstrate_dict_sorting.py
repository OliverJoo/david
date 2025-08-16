# ============= DICTIONARY 정렬 예제 =============
def demonstrate_dict_sorting():
    """딕셔너리 정렬의 다양한 방법 시연"""

    scores = {
        "김철수": 85,
        "박영희": 92,
        "이민수": 78,
        "정수진": 95,
        "최준호": 88
    }

    print(f"원본 딕셔너리: {scores}")
    print()

    # 키(Key) 기준 정렬
    print("=== 키 기준 정렬 ===")
    sorted_by_key = dict(sorted(scores.items()))  # 키 오름차순
    print(f"키 오름차순: {sorted_by_key}")

    sorted_by_key_desc = dict(sorted(scores.items(), reverse=True))  # 키 내림차순
    print(f"키 내림차순: {sorted_by_key_desc}")
    print()

    # 값(Value) 기준 정렬
    print("=== 값 기준 정렬 ===")
    sorted_by_value = dict(sorted(scores.items(), key=lambda x: x[1]))  # 값 오름차순
    print(f"점수 오름차순: {sorted_by_value}")

    sorted_by_value_desc = dict(sorted(scores.items(), key=lambda x: x[1], reverse=True))  # 값 내림차순
    print(f"점수 내림차순: {sorted_by_value_desc}")
    print()

    # 복잡한 딕셔너리 정렬
    students = {
        "김철수": {"age": 20, "grade": 85, "city": "서울"},
        "박영희": {"age": 19, "grade": 92, "city": "부산"},
        "이민수": {"age": 21, "grade": 78, "city": "대구"},
        "정수진": {"age": 20, "grade": 95, "city": "서울"}
    }

    print("=== 중첩 딕셔너리 정렬 ===")
    print("원본:", students)
    print()

    # 성적 기준 정렬
    by_grade = dict(sorted(students.items(), key=lambda x: x[1]["grade"], reverse=True))
    print("성적 높은 순:", by_grade)

    # 나이 → 성적 순 다중 정렬
    multi_sort = dict(sorted(students.items(), key=lambda x: (x[1]["age"], -x[1]["grade"])))
    print("나이 순, 같으면 성적 높은 순:", multi_sort)


demonstrate_dict_sorting()
