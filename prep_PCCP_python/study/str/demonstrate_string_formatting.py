# ============= 문자열 포맷팅 완전 정복 =============
def demonstrate_string_formatting():
    """모든 문자열 포맷팅 방법과 고급 활용법"""

    # 테스트 데이터
    name = "김데이터"
    age = 28
    salary = 75000000
    accuracy = 0.9547

    print("=== 1. f-string (Python 3.6+) - 가장 현대적이고 빠름 ===")

    # 기본 사용법
    print(f"이름: {name}, 나이: {age}살")

    # 수식 계산
    print(f"10년 후 나이: {age + 10}살")

    # 메서드 호출
    print(f"이름 길이: {len(name)}글자")

    # 포맷팅 옵션
    print(f"연봉: {salary:,}원")  # 천단위 콤마
    print(f"정확도: {accuracy:.2%}")  # 백분율 (소수점 2자리)
    print(f"정확도: {accuracy:.4f}")  # 소수점 4자리

    # 정렬과 패딩
    print(f"'{name:>10}'")  # 우측 정렬 (10칸)
    print(f"'{name:<10}'")  # 좌측 정렬 (10칸)
    print(f"'{name:^10}'")  # 중앙 정렬 (10칸)
    print(f"'{name:*^12}'")  # 중앙 정렬 + * 패딩

    print(f"\n=== 2. .format() 메서드 - 이전 버전 호환성 ===")

    # 위치 인수
    print("이름: {}, 나이: {}살".format(name, age))

    # 인덱스 지정
    print("나이: {1}살, 이름: {0}".format(name, age))

    # 키워드 인수
    print("이름: {name}, 연봉: {salary:,}원".format(name=name, salary=salary))

    # 딕셔너리 언패킹
    person = {"name": name, "age": age, "salary": salary}
    print("이름: {name}, 나이: {age}살, 연봉: {salary:,}원".format(**person))

    print(f"\n=== 3. % 포맷팅 - 레거시 (비추천) ===")
    print("이름: %s, 나이: %d살, 정확도: %.2f%%" % (name, age, accuracy * 100))

    print(f"\n=== 4. 실전 활용 예제 ===")

    # 1. 테이블 형태 출력
    def print_table(data, headers):
        # 각 열의 최대 길이 계산
        col_widths = [max(len(str(row[i])) for row in [headers] + data) for i in range(len(headers))]

        # 헤더 출력
        header_line = " | ".join(f"{headers[i]:<{col_widths[i]}}" for i in range(len(headers)))
        print(header_line)
        print("-" * len(header_line))

        # 데이터 출력
        for row in data:
            data_line = " | ".join(f"{str(row[i]):<{col_widths[i]}}" for i in range(len(row)))
            print(data_line)

    employees = [
        ["김철수", 30, 5500000],
        ["박영희", 28, 6200000],
        ["이민수", 35, 7800000]
    ]

    print("직원 테이블:")
    print_table(employees, ["이름", "나이", "월급"])

    # 2. 진행률 표시
    def show_progress(current, total, bar_length=20):
        progress = current / total
        filled_length = int(bar_length * progress)
        bar = '█' * filled_length + '░' * (bar_length - filled_length)
        percent = progress * 100
        return f"진행률: [{bar}] {percent:5.1f}% ({current}/{total})"

    print(f"\n진행률 예제:")
    for i in [25, 50, 75, 100]:
        print(show_progress(i, 100))

    # 3. 로그 메시지 포맷팅
    import datetime

    def log_message(level, message, **kwargs):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        base_msg = f"[{timestamp}] {level:>5} - {message}"

        if kwargs:
            details = " | ".join(f"{k}={v}" for k, v in kwargs.items())
            return f"{base_msg} ({details})"
        return base_msg

    print(f"\n로그 메시지 예제:")
    print(log_message("INFO", "데이터베이스 연결 성공"))
    print(log_message("ERROR", "파일 읽기 실패", file="data.csv", size="1.2MB"))
    print(log_message("DEBUG", "API 호출 완료", endpoint="/api/users", duration="245ms"))

    # 4. 금액 포맷팅 (한국어)
    def format_korean_currency(amount):
        units = ["", "만", "억", "조"]
        result = []

        for i, unit in enumerate(units):
            if amount == 0:
                break
            current = amount % 10000
            if current > 0:
                result.append(f"{current:,}{unit}")
            amount //= 10000

        return "".join(reversed(result)) + "원" if result else "0원"

    print(f"\n한국어 금액 포맷팅:")
    amounts = [1500, 15000, 1500000, 15000000, 150000000000]
    for amount in amounts:
        print(f"{amount:>12,} → {format_korean_currency(amount)}")


demonstrate_string_formatting()
