class AdvancedStructureAnalysis:
    """고급 자료구조 분석 클래스"""

    @staticmethod
    def demonstrate_duck_typing():
        """Duck Typing이 적용되는 실제 사례"""

        print("\n" + "=" * 60)
        print("Duck Typing: '오리처럼 걷고 꽥꽥거리면 오리다'")
        print("=" * 60)

        # 이터러블이면 모두 동일하게 처리됨
        data_structures = {
            'tuple_of_tuples': ((1, 2), (3, 4), (5, 6)),
            'list_of_tuples': [(1, 2), (3, 4), (5, 6)],
            'list_of_lists': [[1, 2], [3, 4], [5, 6]],
            'mixed_structure': ([1, 2], (3, 4), [5, 6])  # 혼합도 가능!
        }

        universal_function = lambda data: tuple(sum(col) for col in zip(*data))

        for name, structure in data_structures.items():
            result = universal_function(structure)
            print(f"{name:20}: {structure} -> {result}")
            # 모든 결과: (9, 12) - 동일함!

        print("\n✅ 핵심: zip(*)은 이터러블이기만 하면 타입 무관하게 처리")

    @staticmethod
    def analyze_performance_by_structure():
        """자료구조별 성능 차이 분석"""

        print("\n" + "=" * 60)
        print("자료구조별 성능 분석 (10,000회 실행)")
        print("=" * 60)

        import timeit

        # 동일한 데이터, 다른 구조
        size = 1000
        tuple_data = tuple(tuple(range(i, i + 3)) for i in range(size))
        list_data = [list(range(i, i + 3)) for i in range(size)]
        mixed_data = [tuple(range(i, i + 3)) for i in range(size)]

        structures = {
            'tuple_of_tuples': tuple_data,
            'list_of_lists': list_data,
            'list_of_tuples': mixed_data
        }

        calc_func = lambda data: tuple(sum(col) for col in zip(*data))

        for name, data in structures.items():
            time_taken = timeit.timeit(lambda: calc_func(data), number=10000)
            print(f"{name:20}: {time_taken:.6f}초")

        print("\n📊 결론: 튜플이 리스트보다 약간 빠름 (불변성의 이점)")


# 실행
AdvancedStructureAnalysis.demonstrate_duck_typing()
AdvancedStructureAnalysis.analyze_performance_by_structure()
