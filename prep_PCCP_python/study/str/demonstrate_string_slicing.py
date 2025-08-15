# ============= 문자열 슬라이싱 마스터 =============
def demonstrate_string_slicing():
    """문자열 슬라이싱의 모든 기법과 실전 활용"""

    text = "파이썬 프로그래밍은 재미있고 강력합니다!"
    english = "Python Programming is Fun and Powerful!"

    print("=== 기본 슬라이싱 ===")
    print(f"원본: {text}")
    print(f"text[3:6]: '{text[3:6]}'")  # "프로그"
    print(f"text[:5]: '{text[:5]}'")  # "파이썬 프"
    print(f"text[7:]: '{text[7:]}'")  # "밍은 재미있고 강력합니다!"
    print(f"text[:]: '{text[:]}'")  # 전체 복사

    print(f"\n=== 음수 인덱스 활용 ===")
    print(f"text[-5:]: '{text[-5:]}'")  # "합니다!"
    print(f"text[:-3]: '{text[:-3]}'")  # 끝 3글자 제외
    print(f"text[-10:-5]: '{text[-10:-5]}'")  # "고 강력"

    print(f"\n=== 스텝(간격) 활용 ===")
    print(f"text[::2]: '{text[::2]}'")  # 2칸씩 건너뛰기
    print(f"text[1::3]: '{text[1::3]}'")  # 1번부터 3칸씩
    print(f"text[::-1]: '{text[::-1]}'")  # 역순
    print(f"english[::2]: '{english[::2]}'")  # 영어도 동일하게 적용

    print(f"\n=== 실전 활용 예제 ===")

    # 1. 파일 확장자 추출
    filename = "data_analysis_report.xlsx"
    name, ext = filename.rsplit('.', 1)
    print(f"파일명: {name}, 확장자: {ext}")

    # 2. URL에서 도메인 추출
    url = "https://www.example.com/api/v1/users"
    protocol = url[:url.find('://')]
    domain_start = url.find('://') + 3
    domain_end = url.find('/', domain_start)
    domain = url[domain_start:domain_end]
    print(f"프로토콜: {protocol}, 도메인: {domain}")

    # 3. 문자열에서 숫자만 추출
    mixed_text = "가격은 1,250,000원이고 할인율은 15%입니다."
    numbers = ''.join([char for char in mixed_text if char.isdigit()])
    print(f"추출된 숫자: {numbers}")

    # 4. 문자열 마스킹 (개인정보 보호)
    email = "hong.gildong@company.com"
    at_index = email.find('@')
    masked_email = email[:2] + '*' * (at_index - 2) + email[at_index:]
    print(f"마스킹된 이메일: {masked_email}")

    # 5. 문자열 회문(palindrome) 검사
    def is_palindrome(s):
        clean_s = ''.join(s.split()).lower()
        return clean_s == clean_s[::-1]

    test_strings = ["레이더", "파이썬", "A man a plan a canal Panama"]
    for s in test_strings:
        print(f"'{s}' 회문 여부: {is_palindrome(s)}")


demonstrate_string_slicing()
