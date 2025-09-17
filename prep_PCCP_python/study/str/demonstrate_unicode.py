# ============= 유니코드 완벽 이해 =============
def demonstrate_unicode():
    """유니코드의 모든 측면과 실전 활용법"""

    print("=== 1. 유니코드 기본 개념 ===")

    # 다양한 언어의 문자열
    korean = "안녕하세요"
    chinese = "你好"
    japanese = "こんにちは"
    arabic = "مرحبا"
    emoji = "👋🌍💻🚀"

    languages = [
        ("한국어", korean),
        ("중국어", chinese),
        ("일본어", japanese),
        ("아랍어", arabic),
        ("이모지", emoji)
    ]

    for lang_name, text in languages:
        print(f"{lang_name:>6}: {text}")
        print(f"        코드포인트: {[ord(char) for char in text]}")
        print(f"        바이트 길이: {len(text.encode('utf-8'))} bytes")
        print(f"        문자 길이: {len(text)} chars")
        print()

    print("=== 2. 유니코드 조작 및 변환 ===")

    # ord()와 chr() 함수
    char = "A"
    print(f"문자 '{char}'의 유니코드 코드포인트: {ord(char)}")
    print(f"코드포인트 65의 문자: '{chr(65)}'")

    # 한글 유니코드 범위 확인
    hangul_start = ord('가')
    hangul_end = ord('힣')
    print(f"한글 유니코드 범위: {hangul_start}~{hangul_end}")

    def is_hangul(char):
        """한글 문자 여부 검사"""
        code = ord(char)
        return 0xAC00 <= code <= 0xD7A3

    test_string = "Hello 안녕 123 🎉"
    hangul_chars = [char for char in test_string if is_hangul(char)]
    print(f"'{test_string}'에서 한글만 추출: {''.join(hangul_chars)}")

    print(f"\n=== 3. 인코딩과 디코딩 ===")

    # 다양한 인코딩 방식
    text = "파이썬으로 데이터 분석하기 🐍📊"

    encodings = ['utf-8', 'utf-16', 'utf-32', 'euc-kr']
    for encoding in encodings:
        try:
            encoded = text.encode(encoding)
            decoded = encoded.decode(encoding)
            print(f"{encoding:>8}: {len(encoded):>3} bytes - {decoded == text}")
        except UnicodeEncodeError:
            print(f"{encoding:>8}: 인코딩 불가")

    # 인코딩 오류 처리
    problematic_text = "특수문자: ñ, ü, ℃, ©, ™"

    print(f"\n=== 4. 인코딩 오류 처리 ===")
    print(f"원본: {problematic_text}")

    error_handlers = ['ignore', 'replace', 'xmlcharrefreplace', 'backslashreplace']

    for handler in error_handlers:
        try:
            encoded = problematic_text.encode('ascii', errors=handler)
            decoded = encoded.decode('ascii', errors=handler)
            print(f"{handler:>18}: '{decoded}'")
        except Exception as e:
            print(f"{handler:>18}: 오류 - {e}")

    print(f"\n=== 5. 실전 활용 예제 ===")

    # 1. 다국어 지원 로그 시스템
    class MultilingualLogger:
        def __init__(self):
            self.messages = {
                'ko': {'success': '성공적으로 완료되었습니다', 'error': '오류가 발생했습니다'},
                'en': {'success': 'Completed successfully', 'error': 'An error occurred'},
                'ja': {'success': '正常に完了しました', 'error': 'エラーが発生しました'},
                'zh': {'success': '成功完成', 'error': '发生错误'}
            }

        def log(self, level, lang='ko'):
            message = self.messages.get(lang, self.messages['en']).get(level, 'Unknown')
            timestamp = "2024-08-10 15:30:45"
            return f"[{timestamp}] {level.upper()}: {message}"

    logger = MultilingualLogger()
    for lang in ['ko', 'en', 'ja', 'zh']:
        print(logger.log('success', lang))

    # 2. 텍스트 정규화 (NFD/NFC)
    import unicodedata

    # 합성 문자 vs 분해 문자
    composed = "é"  # 단일 문자 (é)
    decomposed = "e\u0301"  # e + 결합 액센트

    print(f"\n=== 유니코드 정규화 ===")
    print(f"시각적으로 동일: '{composed}' == '{decomposed}' → {composed == decomposed}")
    print(f"정규화 후 비교: {unicodedata.normalize('NFC', composed) == unicodedata.normalize('NFC', decomposed)}")

    # 3. 문자 분류
    def analyze_text(text):
        """텍스트의 문자 유형 분석"""
        categories = {}
        for char in text:
            category = unicodedata.category(char)
            categories[category] = categories.get(category, 0) + 1
        return categories

    sample_text = "Hello 안녕! 123 @#$ 🎉"
    analysis = analyze_text(sample_text)

    category_names = {
        'Ll': '소문자', 'Lu': '대문자', 'Lo': '기타 문자',
        'Nd': '십진 숫자', 'Po': '기타 구두점', 'Sm': '수학 기호',
        'So': '기타 기호', 'Zs': '공백', 'Ps': '열린 괄호', 'Pe': '닫힌 괄호'
    }

    print(f"\n'{sample_text}' 문자 분석:")
    for category, count in sorted(analysis.items()):
        name = category_names.get(category, category)
        print(f"  {name} ({category}): {count}개")

    # 4. 유니코드 이스케이프 시퀀스 처리
    def unicode_escape_demo():
        """유니코드 이스케이프 시퀀스 예제"""
        escapes = [
            r'\u0041',  # A
            r'\u0048\u0065\u006C\u006C\u006F',  # Hello
            r'\uC548\uB155',  # 안녕
            r'\U0001F600',  # 😀
            r'\U0001F1F0\U0001F1F7'  # 🇰🇷
        ]

        print("\n=== 유니코드 이스케이프 시퀀스 ===")
        for escape in escapes:
            decoded = escape.encode().decode('unicode-escape')
            print(f"{escape:>25} → '{decoded}'")

    unicode_escape_demo()


demonstrate_unicode()
