class UnpackingAnalyzer:
    """언패킹 패턴별 타입 분석 클래스"""

    def __init__(self, data: tuple):
        self.data = data
        self.results = []

    def analyze_pattern(self, pattern_name: str, unpacking_vars: tuple):
        """언패킹 패턴 분석 및 결과 저장"""
        result = {
            'pattern': pattern_name,
            'variables': [],
            'original_data': self.data
        }

        for var_name, var_value in unpacking_vars:
            result['variables'].append({
                'name': var_name,
                'value': var_value,
                'type': type(var_value).__name__,
                'is_list': isinstance(var_value, list)
            })

        self.results.append(result)
        return result

    def display_analysis(self):
        """분석 결과 출력"""
        print("=" * 60)
        print("튜플 언패킹 타입 분석 결과")
        print("=" * 60)

        for result in self.results:
            print(f"\n패턴: {result['pattern']}")
            print(f"원본: {result['original_data']}")
            print("-" * 40)

            for var in result['variables']:
                list_indicator = " ← 🟨 리스트 타입!" if var['is_list'] else ""
                print(f"  {var['name']:8} = {var['value']} (타입: {var['type']}){list_indicator}")


# 사용 예시 및 다양한 패턴 테스트
def comprehensive_unpacking_test():
    """포괄적인 언패킹 테스트"""

    # 테스트 데이터
    test_data = (100, 200, 300, 400, 500, 600)
    analyzer = UnpackingAnalyzer(test_data)

    # 패턴 1: a, *middle, b
    a, *middle, b = test_data
    analyzer.analyze_pattern(
        "a, *middle, b",
        [('a', a), ('middle', middle), ('b', b)]
    )

    # 패턴 2: *head, tail
    *head, tail = test_data
    analyzer.analyze_pattern(
        "*head, tail",
        [('head', head), ('tail', tail)]
    )

    # 패턴 3: first, *rest
    first, *rest = test_data
    analyzer.analyze_pattern(
        "first, *rest",
        [('first', first), ('rest', rest)]
    )

    # 패턴 4: x, y, *others, z
    x, y, *others, z = test_data
    analyzer.analyze_pattern(
        "x, y, *others, z",
        [('x', x), ('y', y), ('others', others), ('z', z)]
    )

    # 결과 출력
    analyzer.display_analysis()

    # 핵심 규칙 요약
    print("\n" + "=" * 60)
    print("🔑 핵심 규칙 요약")
    print("=" * 60)
    print("1. *가 붙은 변수는 항상 리스트(list) 타입이 됩니다")
    print("2. *가 없는 변수들은 원본 요소의 타입을 그대로 유지합니다")
    print("3. *변수는 0개 이상의 요소를 수집할 수 있습니다")
    print("4. *변수가 수집하는 요소들의 타입이 달라도 모두 리스트에 담깁니다")


# 실행
comprehensive_unpacking_test()
