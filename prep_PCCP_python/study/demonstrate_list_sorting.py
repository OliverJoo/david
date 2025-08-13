# ============= LIST 정렬 예제 =============
def demonstrate_list_sorting():
    """리스트 정렬의 다양한 방법 시연"""

    # 숫자 정렬
    numbers = [64, 34, 25, 12, 22, 11, 90]
    print(f"원본 숫자 리스트: {numbers}")

    # 방법 1: sort() - 원본 리스트 자체를 정렬 (in-place)
    numbers_copy1 = numbers.copy()
    numbers_copy1.sort()
    print(f"sort() 사용 (오름차순): {numbers_copy1}")

    numbers_copy2 = numbers.copy()
    numbers_copy2.sort(reverse=True)
    print(f"sort(reverse=True) 사용 (내림차순): {numbers_copy2}")

    # 방법 2: sorted() - 새로운 정렬된 리스트 반환
    sorted_asc = sorted(numbers)
    sorted_desc = sorted(numbers, reverse=True)
    print(f"sorted() 사용 (오름차순): {sorted_asc}")
    print(f"sorted(reverse=True) 사용 (내림차순): {sorted_desc}")
    print(f"원본은 변경되지 않음: {numbers}")
    print()

    # 문자열 정렬
    words = ["python", "java", "javascript", "c++", "go", "rust"]
    print(f"원본 문자열 리스트: {words}")

    # 알파벳 순 정렬
    print(f"알파벳 순: {sorted(words)}")

    # 길이 순 정렬 (key 매개변수 활용)
    print(f"길이 순: {sorted(words, key=len)}")

    # 대소문자 구분 없이 정렬
    mixed_case = ["Python", "java", "JavaScript", "C++", "Go", "rust"]
    print(f"대소문자 구분 없이: {sorted(mixed_case, key=str.lower)}")
    print()

    # 복잡한 객체 정렬
    students = [
        {"name": "김철수", "age": 20, "grade": 85},
        {"name": "박영희", "age": 19, "grade": 92},
        {"name": "이민수", "age": 21, "grade": 78},
        {"name": "정수진", "age": 20, "grade": 95}
    ]

    print("=== 학생 데이터 정렬 ===")
    print("원본:", students)
    print()

    # 나이 순 정렬
    by_age = sorted(students, key=lambda x: x["age"])
    print("나이 순:", by_age)

    # 성적 순 정렬 (내림차순)
    by_grade = sorted(students, key=lambda x: x["grade"], reverse=True)
    print("성적 순 (높은 순):", by_grade)

    # 다중 조건 정렬 (나이 → 성적 순)
    multi_sort = sorted(students, key=lambda x: (x["age"], -x["grade"]))
    print("나이 순, 같으면 성적 높은 순:", multi_sort)


demonstrate_list_sorting()
