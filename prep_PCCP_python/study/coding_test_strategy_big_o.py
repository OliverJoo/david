#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
코딩테스트 전략 및 문제 해결 가이드 클래스
Python 3.12 호환
"""

import time
import sys
from typing import List, Dict, Tuple, Optional, Callable, Any, Union
from dataclasses import dataclass
from enum import Enum
from abc import ABC, abstractmethod
import heapq
from collections import deque, defaultdict, Counter
import bisect
import itertools


class ProblemType(Enum):
    """문제 유형 열거형"""
    ARRAY = "배열"
    STRING = "문자열"
    LINKED_LIST = "연결리스트"
    STACK_QUEUE = "스택/큐"
    TREE = "트리"
    GRAPH = "그래프"
    DYNAMIC_PROGRAMMING = "동적계획법"
    GREEDY = "그리디"
    BINARY_SEARCH = "이진탐색"
    TWO_POINTERS = "투포인터"
    SLIDING_WINDOW = "슬라이딩윈도우"
    BACKTRACKING = "백트래킹"
    BIT_MANIPULATION = "비트조작"
    MATH = "수학"
    SORTING = "정렬"


@dataclass
class Strategy:
    """전략 정보"""
    name: str
    description: str
    time_complexity: str
    space_complexity: str
    when_to_use: str
    template: str
    example: str


@dataclass
class ProblemAnalysis:
    """문제 분석 결과"""
    problem_type: ProblemType
    difficulty: str
    suggested_approach: str
    time_limit: float
    space_limit: int
    key_insights: List[str]


class CodingTestStrategy:
    """코딩테스트 전략 및 문제 해결 가이드 클래스"""

    def __init__(self):
        """코딩테스트 전략 초기화"""
        self.strategies: Dict[ProblemType, List[Strategy]] = {}
        self.templates: Dict[str, str] = {}
        self.common_mistakes: Dict[ProblemType, List[str]] = {}
        self._initialize_strategies()
        self._initialize_templates()
        self._initialize_common_mistakes()

    def _initialize_strategies(self):
        """전략 초기화"""
        # 배열 전략
        self.strategies[ProblemType.ARRAY] = [
            Strategy(
                name="투포인터",
                description="두 개의 포인터를 사용하여 배열을 순회",
                time_complexity="O(n)",
                space_complexity="O(1)",
                when_to_use="정렬된 배열에서 합/차이 찾기, 회문 검사",
                template="two_pointers",
                example="두 수의 합이 target인 경우 찾기"
            ),
            Strategy(
                name="슬라이딩윈도우",
                description="고정 크기 윈도우를 이동시키며 최적값 찾기",
                time_complexity="O(n)",
                space_complexity="O(1)",
                when_to_use="연속된 부분배열의 최대/최소값",
                template="sliding_window",
                example="크기 k인 부분배열의 최대 합"
            )
        ]

        # 그래프 전략
        self.strategies[ProblemType.GRAPH] = [
            Strategy(
                name="DFS (깊이우선탐색)",
                description="재귀적으로 깊이 탐색",
                time_complexity="O(V + E)",
                space_complexity="O(V)",
                when_to_use="경로 찾기, 연결성 확인, 사이클 탐지",
                template="dfs",
                example="섬의 개수 구하기"
            ),
            Strategy(
                name="BFS (너비우선탐색)",
                description="레벨별로 탐색",
                time_complexity="O(V + E)",
                space_complexity="O(V)",
                when_to_use="최단경로, 레벨별 탐색",
                template="bfs",
                example="미로 최단경로"
            )
        ]

        # DP 전략
        self.strategies[ProblemType.DYNAMIC_PROGRAMMING] = [
            Strategy(
                name="탑다운 DP (메모이제이션)",
                description="재귀 + 메모이제이션",
                time_complexity="O(상태수)",
                space_complexity="O(상태수)",
                when_to_use="자연스러운 재귀 구조, 복잡한 상태 전이",
                template="top_down_dp",
                example="피보나치 수열"
            ),
            Strategy(
                name="바텀업 DP (타뷸레이션)",
                description="반복문으로 작은 문제부터 해결",
                time_complexity="O(상태수)",
                space_complexity="O(상태수)",
                when_to_use="명확한 순서, 공간 최적화 가능",
                template="bottom_up_dp",
                example="계단 오르기"
            )
        ]

    def _initialize_templates(self):
        """코드 템플릿 초기화"""
        self.templates = {
            "two_pointers": '''
def two_pointers_solution(arr, target):
    """투포인터 템플릿"""
    left, right = 0, len(arr) - 1

    while left < right:
        current_sum = arr[left] + arr[right]

        if current_sum == target:
            return [left, right]
        elif current_sum < target:
            left += 1
        else:
            right -= 1

    return [-1, -1]
            ''',

            "sliding_window": '''
def sliding_window_solution(arr, k):
    """슬라이딩윈도우 템플릿"""
    if not arr or k <= 0:
        return 0

    # 초기 윈도우 합 계산
    window_sum = sum(arr[:k])
    max_sum = window_sum

    # 윈도우 슬라이딩
    for i in range(k, len(arr)):
        window_sum = window_sum - arr[i - k] + arr[i]
        max_sum = max(max_sum, window_sum)

    return max_sum
            ''',

            "dfs": '''
def dfs_solution(graph, start, visited=None):
    """DFS 템플릿"""
    if visited is None:
        visited = set()

    visited.add(start)
    result = [start]

    for neighbor in graph.get(start, []):
        if neighbor not in visited:
            result.extend(dfs_solution(graph, neighbor, visited))

    return result
            ''',

            "bfs": '''
def bfs_solution(graph, start):
    """BFS 템플릿"""
    from collections import deque

    visited = set()
    queue = deque([start])
    visited.add(start)
    result = []

    while queue:
        node = queue.popleft()
        result.append(node)

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return result
            ''',

            "top_down_dp": '''
def top_down_dp_solution(n, memo=None):
    """탑다운 DP 템플릿"""
    if memo is None:
        memo = {}

    # 기저 조건
    if n <= 1:
        return n

    # 메모이제이션 확인
    if n in memo:
        return memo[n]

    # 재귀 호출 및 메모이제이션
    memo[n] = top_down_dp_solution(n-1, memo) + top_down_dp_solution(n-2, memo)
    return memo[n]
            ''',

            "bottom_up_dp": '''
def bottom_up_dp_solution(n):
    """바텀업 DP 템플릿"""
    if n <= 1:
        return n

    # DP 테이블 초기화
    dp = [0] * (n + 1)
    dp, dp[1] = 0, 1

    # 바텀업 방식으로 계산
    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]

    return dp[n]
            ''',

            "binary_search": '''
def binary_search_solution(arr, target):
    """이진탐색 템플릿"""
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = left + (right - left) // 2

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1
            '''
        }

    def _initialize_common_mistakes(self):
        """자주 하는 실수들 초기화"""
        self.common_mistakes = {
            ProblemType.ARRAY: [
                "인덱스 범위 초과 (off-by-one error)",
                "빈 배열 처리 안함",
                "정수 오버플로우 고려 안함",
                "투포인터에서 left >= right 조건 실수"
            ],
            ProblemType.STRING: [
                "빈 문자열 처리 안함",
                "대소문자 구분 실수",
                "문자열 불변성 무시",
                "인코딩 문제 (ASCII vs Unicode)"
            ],
            ProblemType.DYNAMIC_PROGRAMMING: [
                "기저 조건 잘못 설정",
                "메모이제이션 빼먹음",
                "상태 정의 모호",
                "점화식 오류"
            ],
            ProblemType.GRAPH: [
                "방문 체크 빼먹음",
                "무방향 그래프를 방향 그래프로 착각",
                "사이클 처리 안함",
                "연결되지 않은 그래프 고려 안함"
            ]
        }

    def analyze_problem(
            self,
            problem_description: str,
            constraints: Dict[str, Any] = None
    ) -> ProblemAnalysis:
        """
        문제 설명을 분석하여 적절한 전략 제안

        Args:
            problem_description: 문제 설명
            constraints: 제약 조건 {"n": 10000, "time": 1.0}

        Returns:
            문제 분석 결과
        """
        if constraints is None:
            constraints = {}

        # 키워드 기반 문제 유형 판단
        problem_type = self._classify_problem_type(problem_description)

        # 난이도 추정
        difficulty = self._estimate_difficulty(problem_description, constraints)

        # 접근 방법 제안
        suggested_approach = self._suggest_approach(problem_type, constraints)

        # 핵심 인사이트 추출
        key_insights = self._extract_insights(problem_description, problem_type)

        return ProblemAnalysis(
            problem_type=problem_type,
            difficulty=difficulty,
            suggested_approach=suggested_approach,
            time_limit=constraints.get("time_limit", 2.0),
            space_limit=constraints.get("space_limit", 256),
            key_insights=key_insights
        )

    def _classify_problem_type(self, description: str) -> ProblemType:
        """문제 설명으로부터 유형 분류"""
        description_lower = description.lower()

        # 키워드 기반 분류
        type_keywords = {
            ProblemType.ARRAY: ["배열", "array", "리스트", "list"],
            ProblemType.STRING: ["문자열", "string", "문자", "char"],
            ProblemType.TREE: ["트리", "tree", "이진트리", "binary tree"],
            ProblemType.GRAPH: ["그래프", "graph", "노드", "node", "간선", "edge"],
            ProblemType.DYNAMIC_PROGRAMMING: ["dp", "동적계획법", "메모이제이션", "최적"],
            ProblemType.GREEDY: ["그리디", "greedy", "탐욕적"],
            ProblemType.BINARY_SEARCH: ["이진탐색", "binary search", "정렬된"],
            ProblemType.TWO_POINTERS: ["두 포인터", "two pointer", "합이"],
            ProblemType.BACKTRACKING: ["백트래킹", "backtrack", "모든 경우"]
        }

        for problem_type, keywords in type_keywords.items():
            if any(keyword in description_lower for keyword in keywords):
                return problem_type

        return ProblemType.ARRAY  # 기본값

    def _estimate_difficulty(self, description: str, constraints: Dict) -> str:
        """난이도 추정"""
        n = constraints.get("n", 1000)

        if n <= 100:
            return "쉬움"
        elif n <= 10000:
            return "보통"
        else:
            return "어려움"

    def _suggest_approach(self, problem_type: ProblemType, constraints: Dict) -> str:
        """접근 방법 제안"""
        n = constraints.get("n", 1000)

        if problem_type == ProblemType.ARRAY:
            if n <= 1000:
                return "브루트포스 또는 투포인터"
            else:
                return "투포인터, 슬라이딩윈도우, 또는 이진탐색"

        elif problem_type == ProblemType.GRAPH:
            if n <= 1000:
                return "DFS 또는 BFS"
            else:
                return "최적화된 그래프 알고리즘 (다익스트라, 플로이드-워셜)"

        elif problem_type == ProblemType.DYNAMIC_PROGRAMMING:
            return "메모이제이션 또는 타뷸레이션"

        return "문제 유형에 맞는 표준 알고리즘"

    def _extract_insights(self, description: str, problem_type: ProblemType) -> List[str]:
        """핵심 인사이트 추출"""
        insights = []

        if "최대" in description or "최소" in description:
            insights.append("최적화 문제: DP, 그리디, 또는 이진탐색 고려")

        if "모든" in description:
            insights.append("완전탐색: 백트래킹 또는 비트마스킹 고려")

        if "순서" in description:
            insights.append("정렬 또는 순서 보존이 중요")

        if problem_type == ProblemType.ARRAY:
            insights.append("배열 인덱스 범위 주의")

        return insights

    def get_strategy(self, problem_type: ProblemType) -> List[Strategy]:
        """문제 유형별 전략 조회"""
        return self.strategies.get(problem_type, [])

    def get_template(self, template_name: str) -> str:
        """템플릿 코드 조회"""
        return self.templates.get(template_name, "템플릿을 찾을 수 없습니다.")

    def get_common_mistakes(self, problem_type: ProblemType) -> List[str]:
        """자주 하는 실수 조회"""
        return self.common_mistakes.get(problem_type, [])

    def solve_step_by_step(self, problem_description: str) -> Dict[str, Any]:
        """단계별 문제 해결 가이드"""

        # 1. 문제 분석
        analysis = self.analyze_problem(problem_description)

        # 2. 전략 선택
        strategies = self.get_strategy(analysis.problem_type)

        # 3. 주의사항
        mistakes = self.get_common_mistakes(analysis.problem_type)

        return {
            "step1_analysis": {
                "problem_type": analysis.problem_type.value,
                "difficulty": analysis.difficulty,
                "approach": analysis.suggested_approach,
                "insights": analysis.key_insights
            },
            "step2_strategies": [
                {
                    "name": s.name,
                    "description": s.description,
                    "complexity": f"시간: {s.time_complexity}, 공간: {s.space_complexity}",
                    "when_to_use": s.when_to_use
                } for s in strategies
            ],
            "step3_template": self.get_template(strategies[0].template) if strategies else "",
            "step4_mistakes": mistakes,
            "step5_tips": self._get_solving_tips(analysis.problem_type)
        }

    def _get_solving_tips(self, problem_type: ProblemType) -> List[str]:
        """문제 해결 팁"""
        tips = {
            ProblemType.ARRAY: [
                "예제를 손으로 직접 시뮬레이션해보기",
                "경계값 (0, 1, n-1, n) 테스트하기",
                "정렬 여부 확인하기",
                "중복 원소 존재 여부 확인하기"
            ],
            ProblemType.DYNAMIC_PROGRAMMING: [
                "작은 예제로 패턴 찾기",
                "상태 정의 명확히 하기",
                "점화식 도출하기",
                "기저 조건 정확히 설정하기"
            ],
            ProblemType.GRAPH: [
                "그래프 표현 방법 결정 (인접리스트 vs 인접행렬)",
                "방향성 여부 확인",
                "가중치 여부 확인",
                "연결성 확인"
            ]
        }

        return tips.get(problem_type, ["문제를 작은 단위로 나누어 생각하기"])

    def practice_problems_generator(self, problem_type: ProblemType) -> List[Dict[str, str]]:
        """연습 문제 추천"""
        problems = {
            ProblemType.ARRAY: [
                {
                    "title": "두 수의 합",
                    "description": "배열에서 합이 target인 두 수의 인덱스 찾기",
                    "level": "쉬움",
                    "algorithm": "투포인터 or 해시맵"
                },
                {
                    "title": "최대 부분 배열 합",
                    "description": "연속된 부분 배열의 최대 합 구하기",
                    "level": "보통",
                    "algorithm": "카데인 알고리즘"
                }
            ],
            ProblemType.DYNAMIC_PROGRAMMING: [
                {
                    "title": "피보나치 수열",
                    "description": "n번째 피보나치 수 구하기",
                    "level": "쉬움",
                    "algorithm": "기본 DP"
                },
                {
                    "title": "계단 오르기",
                    "description": "n개 계단을 오르는 방법의 수",
                    "level": "쉬움",
                    "algorithm": "1차원 DP"
                }
            ]
        }

        return problems.get(problem_type, [])

    def time_complexity_analyzer(self, code: str) -> Dict[str, str]:
        """코드의 시간복잡도 분석 (간단한 휴리스틱)"""

        nested_loops = code.count("for") + code.count("while")
        recursive_calls = code.count("return") if "def" in code else 0

        if "sort" in code.lower():
            return {
                "complexity": "O(n log n)",
                "reason": "정렬 알고리즘 사용"
            }
        elif nested_loops >= 2:
            return {
                "complexity": "O(n²)",
                "reason": "중첩 반복문"
            }
        elif nested_loops == 1:
            return {
                "complexity": "O(n)",
                "reason": "단일 반복문"
            }
        elif recursive_calls > 0:
            return {
                "complexity": "O(2^n) or O(n)",
                "reason": "재귀 호출 (메모이제이션 여부에 따라)"
            }
        else:
            return {
                "complexity": "O(1)",
                "reason": "상수 시간 연산"
            }

    def generate_test_cases(self, problem_type: ProblemType) -> List[Dict[str, Any]]:
        """테스트 케이스 생성"""
        if problem_type == ProblemType.ARRAY:
            return [
                {"input": [], "expected": "빈 배열 처리"},
                {"input": [1], "expected": "단일 원소"},
                {"input": [1, 2, 3], "expected": "일반적인 경우"},
                {"input": [3, 2, 1], "expected": "역순 배열"},
                {"input": [1, 1, 1], "expected": "중복 원소"}
            ]

        return [{"input": "example", "expected": "expected_output"}]


# 데모 함수들
def demo_coding_strategy():
    """코딩테스트 전략 사용 예제"""
    print("=== 코딩테스트 전략 사용 예제 ===\n")

    strategy = CodingTestStrategy()

    # 1. 문제 분석
    problem = "배열에서 합이 target인 두 수의 인덱스를 찾으시오."
    constraints = {"n": 1000, "time_limit": 1.0}

    print("1. 문제 분석")
    analysis = strategy.analyze_problem(problem, constraints)
    print(f"문제 유형: {analysis.problem_type.value}")
    print(f"난이도: {analysis.difficulty}")
    print(f"제안 접근법: {analysis.suggested_approach}")
    print(f"핵심 인사이트: {', '.join(analysis.key_insights)}")
    print()

    # 2. 단계별 해결 가이드
    print("2. 단계별 해결 가이드")
    solution_guide = strategy.solve_step_by_step(problem)

    print("📋 전략:")
    for i, s in enumerate(solution_guide["step2_strategies"], 1):
        print(f"  {i}. {s['name']}: {s['description']}")
        print(f"     복잡도: {s['complexity']}")
        print(f"     사용시기: {s['when_to_use']}")
    print()

    # 3. 템플릿 코드
    print("3. 템플릿 코드")
    template = strategy.get_template("two_pointers")
    print(template)
    print()

    # 4. 주의사항
    print("4. 주의사항")
    mistakes = strategy.get_common_mistakes(ProblemType.ARRAY)
    for mistake in mistakes:
        print(f"  ⚠️ {mistake}")
    print()

    # 5. 연습 문제
    print("5. 추천 연습 문제")
    practice = strategy.practice_problems_generator(ProblemType.ARRAY)
    for prob in practice:
        print(f"  📝 {prob['title']} ({prob['level']})")
        print(f"     {prob['description']}")
        print(f"     알고리즘: {prob['algorithm']}")


if __name__ == "__main__":
    demo_coding_strategy()

    # 추가 사용 예제
    print("\n=== 추가 기능 테스트 ===")

    strategy = CodingTestStrategy()

    # 시간복잡도 분석
    sample_code = """
    for i in range(n):
        for j in range(n):
            if arr[i] + arr[j] == target:
                return [i, j]
    """

    complexity = strategy.time_complexity_analyzer(sample_code)
    print(f"코드 복잡도: {complexity['complexity']} ({complexity['reason']})")

    # 테스트 케이스 생성
    test_cases = strategy.generate_test_cases(ProblemType.ARRAY)
    print("\n테스트 케이스:")
    for tc in test_cases:
        print(f"  입력: {tc['input']} → {tc['expected']}")
