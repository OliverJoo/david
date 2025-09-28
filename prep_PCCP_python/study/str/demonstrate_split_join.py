# ============= Split/Join 마스터 클래스 =============
def demonstrate_split_join():
    """split과 join의 고급 활용법과 실전 예제"""

    print("=== Split 기본 및 고급 활용 ===")

    # 1. 기본 split
    sentence = "Python은 강력하고 배우기 쉬운 프로그래밍 언어입니다"
    words = sentence.split()
    print(f"기본 split: {words}")

    # 2. 구분자 지정 split
    csv_data = "이름,나이,직업,연봉"
    fields = csv_data.split(',')
    print(f"CSV split: {fields}")

    # 3. 최대 분할 수 제한
    log_entry = "2024-08-10 15:30:45 INFO Database connection established successfully"
    parts = log_entry.split(' ', 3)  # 최대 3번만 분할
    date, time, level, message = parts
    print(f"로그 파싱: 날짜={date}, 시간={time}, 레벨={level}, 메시지={message}")

    # 4. rsplit (오른쪽부터 분할)
    file_path = "/home/user/documents/project/data/analysis.py"
    directory, filename = file_path.rsplit('/', 1)
    print(f"경로 분리: 디렉토리={directory}, 파일명={filename}")

    # 5. splitlines (줄 단위 분할)
    multi_line = """첫 번째 줄
두 번째 줄
세 번째 줄"""
    lines = multi_line.splitlines()
    print(f"줄 단위 분할: {lines}")

    print(f"\n=== Join 고급 활용 ===")

    # 1. 기본 join
    words_list = ["데이터", "분석", "전문가"]
    sentence = " ".join(words_list)
    print(f"공백으로 결합: {sentence}")

    # 2. 다양한 구분자 join
    numbers = ["1", "2", "3", "4", "5"]
    print(f"쉼표로 결합: {','.join(numbers)}")
    print(f"화살표로 결합: {' → '.join(numbers)}")
    print(f"줄바꿈으로 결합:\n{chr(10).join(numbers)}")

    # 3. 실전 SQL 쿼리 생성
    table_name = "users"
    columns = ["id", "name", "email", "created_at"]
    conditions = ["status = 'active'", "age >= 18", "country = 'KR'"]

    select_query = f"SELECT {', '.join(columns)} FROM {table_name} WHERE {' AND '.join(conditions)}"
    print(f"\n생성된 SQL: {select_query}")

    # 4. 파일 경로 생성 (운영체제 무관)
    import os
    path_parts = ["home", "user", "projects", "python", "data.csv"]
    file_path = os.path.join(*path_parts)  # 운영체제에 맞는 구분자 사용
    print(f"파일 경로: {file_path}")

    # 5. HTML 태그 생성
    def create_html_list(items, list_type="ul"):
        list_items = [f"  <li>{item}</li>" for item in items]
        return f"<{list_type}>\n{chr(10).join(list_items)}\n</{list_type}>"

    skills = ["Python", "데이터분석", "머신러닝", "SQL"]
    html_list = create_html_list(skills)
    print(f"\n생성된 HTML:\n{html_list}")

    # 6. 데이터 검증 및 정제
    def clean_and_validate_data(raw_data):
        """CSV 데이터 정제 및 검증"""
        lines = raw_data.strip().split('\n')
        cleaned_data = []

        for i, line in enumerate(lines):
            fields = [field.strip() for field in line.split(',')]
            if len(fields) != 3:
                print(f"⚠️  {i + 1}번째 줄 오류: 필드 수 부족 ({len(fields)}/3)")
                continue
            cleaned_data.append(fields)

        return cleaned_data

    raw_csv = """홍길동, 30, 개발자
김철수,25,디자이너  
박영희,35
이민수, 28, 분석가"""

    cleaned = clean_and_validate_data(raw_csv)
    print(f"\n정제된 데이터:")
    for row in cleaned:
        print(f"  {' | '.join(row)}")


demonstrate_split_join()
