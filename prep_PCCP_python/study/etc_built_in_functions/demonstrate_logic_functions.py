# ============= any() / all() 함수 =============
def demonstrate_logic_functions():
    """논리 연산 함수 완벽 활용법"""

    print("=== any() 함수 - 하나라도 True이면 True ===")

    # 예제 1: 리스트에서 조건 검사
    numbers = [0, 2, 0, 4, 0]
    has_positive = any(num > 0 for num in numbers)
    print(f"양수가 있나요? {has_positive}")
    # 결과: True (2와 4가 양수이므로)

    # 예제 2: 문자열 검증
    passwords = ["abc", "12345", "password123", ""]
    has_valid_password = any(len(pwd) >= 8 for pwd in passwords)
    print(f"8글자 이상 비밀번호가 있나요? {has_valid_password}")
    # 결과: True ("password123"이 8글자 이상)

    print(f"\n=== all() 함수 - 모두 True여야 True ===")

    # 예제 3: 모든 조건 만족 여부
    scores = [85, 92, 78, 88, 95]
    all_passed = all(score >= 60 for score in scores)
    print(f"모든 학생이 합격했나요? {all_passed}")
    # 결과: True (모든 점수가 60 이상)

    # 예제 4: 입력 데이터 유효성 검사
    user_data = ["John", "25", "john@email.com", "password"]
    all_fields_filled = all(field.strip() for field in user_data)
    print(f"모든 필드가 채워졌나요? {all_fields_filled}")
    # 결과: True (모든 필드에 데이터 존재)

    # 실전 활용: 2D 리스트에서 조건 검사
    matrix = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]

    # 모든 행의 합이 10 이상인가?
    all_rows_sum_valid = all(sum(row) >= 10 for row in matrix)
    print(f"모든 행의 합이 10 이상인가요? {all_rows_sum_valid}")
    # 결과: True (6, 15, 24 모두 10 이상)

    # 어떤 행에든 0이 있는가?
    has_zero = any(0 in row for row in matrix)
    print(f"0이 포함된 행이 있나요? {has_zero}")
    # 결과: False (모든 원소가 양수)


demonstrate_logic_functions()
