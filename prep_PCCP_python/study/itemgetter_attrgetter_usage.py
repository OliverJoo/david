# 1) itemgetter란? 기본 형식
from operator import itemgetter

key_func = itemgetter(1)  # 두 번째 요소 반환
key_func_multi = itemgetter(1, 3)  # 두 번째와 네 번째 요소를 (튜플)로 반환
print(f'1. itemgetter(1)은 시퀀스의 두 번째 요소를, itemgetter(1,3)은 두 요소를 튜플로 반환 -> '
      f'{key_func(["x", 10, "y", 20])}, {key_func_multi(["x", 10, "y", 20])}')

# 2) 단일 인덱스 예시 - 튜플 리스트 정렬(성적 기준)
student_tuples = [
    ('Alice', 85, 'A'),
    ('Bob', 70, 'C'),
    ('Charlie', 92, 'A+'),
    ('Daisy', 78, 'B'),
]

sorted_by_score = sorted(student_tuples, key=itemgetter(1))
print(f'2-1. 튜플의 1번 인덱스(성적) 기준 오름차순 정렬 -> {sorted_by_score}')

# 2) 단일 인덱스 예시 - 리스트(내부 리스트) 정렬
records = [
    ['kr', 'Seoul', 9765],
    ['jp', 'Tokyo', 13960],
    ['us', 'NYC', 8468],
]

sorted_by_pop = sorted(records, key=itemgetter(2), reverse=True)
print(f'2-2. 내부 리스트의 2번 인덱스(인구) 기준 내림차순 정렬 -> {sorted_by_pop}')

# 3) 다중 인덱스 예시(복합 키) - 성적 오름, 이름 오름
student_tuples2 = [
    ('Alice', 85),
    ('Bob', 85),
    ('Charlie', 92),
    ('Daisy', 78),
]

sorted_by_score_then_name = sorted(student_tuples2, key=itemgetter(1, 0))
print(f'3-1. 1순위 성적, 동점 시 0번(이름)으로 정렬 -> {sorted_by_score_then_name}')

# 3) 다중 인덱스 예시 - 날짜/시간 정렬
rows = [
    ('2025-08-10', '13:40', 'A'),
    ('2025-08-10', '09:15', 'B'),
    ('2025-07-30', '22:00', 'C'),
]

rows_sorted = sorted(rows, key=itemgetter(0, 1))
print(f'3-2. 날짜(0번) 우선, 같은 날짜면 시간(1번)으로 정렬 -> {rows_sorted}')

# 4) min/max에도 활용
data = [
    ('AAPL', 185.2),
    ('GOOGL', 132.6),
    ('NVDA', 127.4),
]

min_price = min(data, key=itemgetter(1))
max_price = max(data, key=itemgetter(1))
print(f'4-1. 1번 인덱스(가격) 최솟값 종목 -> {min_price}')
print(f'4-2. 1번 인덱스(가격) 최댓값 종목 -> {max_price}')

# 5) 딕셔너리 리스트 정렬 - 키 기준 정렬
students = [
    {'name': 'Alice', 'score': 85, 'grade': 'A'},
    {'name': 'Bob', 'score': 70, 'grade': 'C'},
    {'name': 'Charlie', 'score': 92, 'grade': 'A+'},
]

sorted_by_score_dict = sorted(students, key=itemgetter('score'))
sorted_by_grade_then_name = sorted(students, key=itemgetter('grade', 'name'))

print(f"5-1. 딕셔너리의 'score' 키 기준 정렬 -> {sorted_by_score_dict}")
print(f"5-2. (버그) 'grade' 우선, 동률이면 'name' 정렬 -> {sorted_by_grade_then_name}")

students = [
    {'name': 'Alice', 'score': 85, 'grade': 'A'},
    {'name': 'Bob', 'score': 70, 'grade': 'C'},
    {'name': 'Charlie', 'score': 92, 'grade': 'A+'},
    {'name': 'Daisy', 'score': 88, 'grade': 'A-'},
    {'name': 'Evan', 'score': 81, 'grade': 'B+'},
]

# 1) 등급 우선순위 매핑 정의 (원하는 정책대로 수정 가능)
grade_rank = {
    'A+': 12, 'A': 11, 'A-': 10,
    'B+': 9,  'B': 8,  'B-': 7,
    'C+': 6,  'C': 5,  'C-': 4,
    'D+': 3,  'D': 2,  'D-': 1,
    'F': 0,
}

# 2) 등급 우선, 이름 보조 정렬
#   - grade는 매핑 점수 내림차순
#   - name은 오름차순
sorted_by_grade_then_name = sorted(students, key=lambda x: (-grade_rank.get(x['grade'], -1), x['name']))
print(f"5-2. (수정) 등급 우선순위 매핑을 적용하여 정렬 -> {sorted_by_grade_then_name}")

# 6) groupby와 함께 쓰기 (정렬 후 그룹핑)
from itertools import groupby

rows2 = [
    ('Alice', 'A'),
    ('Bob', 'C'),
    ('Charlie', 'A+'),
    ('Daisy', 'B'),
    ('Aaron', 'A'),
]

grade_rank = {
    'A+': 0, 'A': 1, 'A-': 2,
    'B+': 3, 'B': 4, 'B-': 5,
    'C+': 6, 'C': 7, 'C-': 8,
    'D+': 9, 'D': 10, 'D-': 11,
    'F': 12,
}

# 2) 랭크를 사용해 정렬: 1순위 학점 랭크, 2순위 이름(가독성과 안정성)
rows2_sorted = sorted(rows2, key=lambda x: (grade_rank.get(x[1], 9999), x))

# 3) groupby도 같은 키(학점)로 묶기
grouped = []
for grade, group in groupby(rows2_sorted, key=itemgetter(1)):
    names = [name for name, _ in group]
    grouped.append((grade, names))

print('6. 간단설명: 학점 서열(랭크) 기준으로 정렬 후 groupby 적용 ->', grouped)

# 7) 복합 키 + 정렬 방향 혼합(점수 내림, 이름 오름) - lambda 혼용
students2 = [
    ('Charlie', 92),
    ('Alice', 92),
    ('Daisy', 78),
    ('Bob', 85),
]

sorted_mixed = sorted(students2, key=lambda x: (-x[1], x))
print(f'7. 점수는 내림차순(-score), 이름은 오름차순으로 정렬 -> {sorted_mixed}')

# 8) itemgetter vs attrgetter
from operator import attrgetter
from collections import namedtuple

User = namedtuple('User', 'name age')
users = [User('Alice', 30), User('Bob', 25), User('Charlie', 35)]

sorted_by_age_attr = sorted(users, key=attrgetter('age'))  # 속성 접근
print(f"8-1. attrgetter로 속성('age') 기준 정렬 -> {sorted_by_age_attr}")

# 같은 자료를 인덱스로 접근 가능하다면 itemgetter(1)도 가능
users_as_tuples = [('Alice', 30), ('Bob', 25), ('Charlie', 35)]
print(f"8-2. itemgetter(1)로 튜플의 나이 기준 정렬 -> {sorted(users_as_tuples, key=itemgetter(1))}")

# 9) 실전 패턴 요약 예시 모음
data2 = [(3, 'c'), (1, 'a'), (2, 'b')]
print(f'9-1. 첫 요소(0번) 기준 오름차순 정렬 -> {sorted(data2, key=itemgetter(0))}')

# 다중 기준
data3 = [
    ('kr', 'Seoul', 1),
    ('kr', 'Busan', 2),
    ('jp', 'Tokyo', 1),
]
print(f'9-2. 국가(0번) -> 순번(2번) 복합 키 정렬 -> {sorted(data3, key=itemgetter(0, 2))}')

# 딕셔너리 리스트
dlist = [{'k': 2, 'v': 10}, {'k': 1, 'v': 20}, {'k': 2, 'v': 5}]
print(f"9-3. 'k' 오름 -> 'v' 오름 복합 키 정렬 -> {sorted(dlist, key=itemgetter('k', 'v'))}")

# 10) 질문에 나온 코드 해설 예시
student_tuples3 = [
    ('Alice', 85, 'A'),
    ('Bob', 70, 'C'),
    ('Charlie', 92, 'A+'),
    ('Daisy', 78, 'B'),
]

sorted_itemgetter = sorted(student_tuples3, key=itemgetter(1))
sorted_itemgetter2 = sorted(student_tuples3, key=lambda x: -x[1])
print(f'10-1. 두 번째 요소(성적) 기준 오름차순, 동점은 안정 정렬로 입력 순서 유지 -> {sorted_itemgetter}')
print(f'10-2. 두 번째 요소(성적) 기준 내림차순, 동점은 안정 정렬로 입력 순서 유지 -> {sorted_itemgetter2}')
