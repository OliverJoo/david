# ============= Counter 완벽 마스터 =============
from collections import Counter
import re
from typing import List, Dict, Any


def demonstrate_counter():
    """Counter의 모든 기능과 실전 활용법"""

    print("=== 1. Counter 기본 생성 및 조작 ===")

    # 다양한 방법으로 Counter 생성

    # 방법 1: 리스트에서
    fruits = ['apple', 'banana', 'apple', 'cherry', 'banana', 'apple']
    fruit_counter = Counter(fruits)
    print(f"과일 카운터: {fruit_counter}")

    # 방법 2: 문자열에서
    text = "hello world"
    char_counter = Counter(text)
    print(f"문자 카운터: {char_counter}")

    # 방법 3: 딕셔너리에서
    grades = Counter({'A': 5, 'B': 3, 'C': 2, 'D': 1})
    print(f"성적 분포: {grades}")

    # 방법 4: 키워드 인수
    colors = Counter(red=3, blue=2, green=1)
    print(f"색상 카운터: {colors}")

    print(f"\n=== 2. Counter 주요 메서드 ===")

    # most_common() - 가장 빈번한 요소들
    print(f"가장 많은 과일 TOP 2: {fruit_counter.most_common(2)}")
    print(f"모든 과일 빈도순: {fruit_counter.most_common()}")

    # elements() - 카운트만큼 반복 생성
    print(f"elements() 결과: {list(fruit_counter.elements())}")

    # total() - Python 3.10+에서 추가됨
    try:
        print(f"총 개수: {fruit_counter.total()}")
    except AttributeError:
        print(f"총 개수: {sum(fruit_counter.values())}")

    # 수학적 연산
    counter1 = Counter(['a', 'b', 'c', 'a', 'b'])
    counter2 = Counter(['a', 'b', 'b', 'd'])

    print(f"\ncounter1: {counter1}")
    print(f"counter2: {counter2}")
    print(f"덧셈 (합집합): {counter1 + counter2}")
    print(f"뺄셈 (차집합): {counter1 - counter2}")
    print(f"교집합 (최솟값): {counter1 & counter2}")
    print(f"합집합 (최댓값): {counter1 | counter2}")

    print(f"\n=== 3. 실전 활용 예제 ===")

    # 1. 텍스트 분석 - 단어 빈도
    def analyze_text_frequency(text: str) -> Dict[str, Any]:
        """텍스트의 다양한 빈도 분석"""
        # 전처리
        text = text.lower()
        words = re.findall(r'\b\w+\b', text)  # 단어만 추출

        # 분석
        word_counter = Counter(words)
        char_counter = Counter(text.replace(' ', ''))  # 공백 제외

        return {
            'total_words': len(words),
            'unique_words': len(word_counter),
            'most_common_words': word_counter.most_common(5),
            'word_length_dist': Counter(len(word) for word in words),
            'char_frequency': char_counter.most_common(5)
        }

    sample_text = """
    Python은 강력하고 유연한 프로그래밍 언어입니다. 
    데이터 분석, 웹 개발, 인공지능 등 다양한 분야에서 사용됩니다.
    Python의 간결한 문법과 풍부한 라이브러리는 개발자들에게 인기가 높습니다.
    """

    analysis = analyze_text_frequency(sample_text)
    print("텍스트 분석 결과:")
    for key, value in analysis.items():
        print(f"  {key}: {value}")

    # 2. 로그 분석 시스템
    class LogAnalyzer:
        """로그 파일 분석을 위한 Counter 활용 클래스"""

        def __init__(self):
            self.ip_counter = Counter()
            self.status_counter = Counter()
            self.hour_counter = Counter()
            self.endpoint_counter = Counter()

        def parse_log_entry(self, log_line: str):
            """단일 로그 엔트리 파싱"""
            # 간단한 로그 형식: IP - - [timestamp] "METHOD /path" status size
            pattern = r'(\d+\.\d+\.\d+\.\d+).*\[([^\]]+)\] "(\w+) ([^"]*)" (\d+)'
            match = re.match(pattern, log_line)

            if match:
                ip, timestamp, method, path, status = match.groups()
                hour = timestamp.split()[1].split(':')[0]

                self.ip_counter[ip] += 1
                self.status_counter[status] += 1
                self.hour_counter[hour] += 1
                self.endpoint_counter[f"{method} {path}"] += 1

        def analyze_logs(self, log_lines: List[str]) -> Dict[str, Any]:
            """로그 라인들을 분석하여 통계 반환"""
            for line in log_lines:
                self.parse_log_entry(line)

            return {
                'top_ips': self.ip_counter.most_common(3),
                'status_distribution': dict(self.status_counter),
                'peak_hours': self.hour_counter.most_common(3),
                'top_endpoints': self.endpoint_counter.most_common(3)
            }

    # 샘플 로그 데이터
    sample_logs = [
        '192.168.1.1 - - [10/Oct/2024:13:55:36 +0900] "GET /api/users" 200 1234',
        '192.168.1.2 - - [10/Oct/2024:13:56:42 +0900] "POST /api/login" 200 567',
        '192.168.1.1 - - [10/Oct/2024:14:01:23 +0900] "GET /api/data" 404 89',
        '192.168.1.3 - - [10/Oct/2024:14:05:17 +0900] "GET /api/users" 200 1456',
        '192.168.1.1 - - [10/Oct/2024:15:10:33 +0900] "POST /api/upload" 500 234'
    ]

    analyzer = LogAnalyzer()
    log_stats = analyzer.analyze_logs(sample_logs)

    print(f"\n로그 분석 결과:")
    for category, data in log_stats.items():
        print(f"  {category}: {data}")

    # 3. 실시간 데이터 스트림 분석
    class StreamAnalyzer:
        """실시간 스트림 데이터 분석"""

        def __init__(self, window_size: int = 100):
            self.window_size = window_size
            self.data_buffer = []
            self.current_counter = Counter()

        def add_data(self, item):
            """새 데이터 추가 (슬라이딩 윈도우)"""
            self.data_buffer.append(item)
            self.current_counter[item] += 1

            # 윈도우 크기 초과시 오래된 데이터 제거
            if len(self.data_buffer) > self.window_size:
                removed_item = self.data_buffer.pop(0)
                self.current_counter[removed_item] -= 1
                if self.current_counter[removed_item] == 0:
                    del self.current_counter[removed_item]

        def get_top_items(self, n: int = 5):
            """현재 윈도우에서 상위 N개 아이템"""
            return self.current_counter.most_common(n)

        def get_statistics(self):
            """현재 통계 정보"""
            if not self.current_counter:
                return {"message": "데이터 없음"}

            total = sum(self.current_counter.values())
            most_common = self.current_counter.most_common(1)[0]

            return {
                "total_items": total,
                "unique_items": len(self.current_counter),
                "most_frequent": most_common,
                "entropy": self._calculate_entropy()
            }

        def _calculate_entropy(self) -> float:
            """데이터의 엔트로피 계산 (다양성 측정)"""
            import math
            total = sum(self.current_counter.values())
            if total == 0:
                return 0.0

            entropy = 0
            for count in self.current_counter.values():
                p = count / total
                entropy -= p * math.log2(p)

            return entropy

    # 스트림 분석 예제
    stream = StreamAnalyzer(window_size=10)

    # 시뮬레이션 데이터 추가
    import random
    items = ['A', 'B', 'C', 'D', 'E']

    print(f"\n실시간 스트림 분석:")
    for i in range(20):
        item = random.choices(items, weights=[5, 3, 2, 1, 1])[0]  # 가중 선택
        stream.add_data(item)

        if i % 5 == 4:  # 5개마다 통계 출력
            stats = stream.get_statistics()
            print(f"  {i + 1:2d}개 처리 후: {stats}")


demonstrate_counter()
