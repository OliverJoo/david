from collections import namedtuple

# Point namedtuple 정의
Point = namedtuple('Point', 'x y', defaults=[0, 0])  # Python 3.7+에서 기본값 지원

# 1. _make() - 기존 시퀀스로부터 생성
coordinates = [3, 4]
point1 = Point._make(coordinates)
print(f"_make() 결과: {point1}")  # _make() 결과: Point(x=3, y=4)

# 2. _asdict() - 딕셔너리로 변환
point_dict = point1._asdict()
print(f"_asdict() 결과: {point_dict}")  # _asdict() 결과: {'x': 3, 'y': 4}

# 3. _replace() - 일부 필드만 변경한 새 인스턴스 생성
point2 = point1._replace(x=10)
print(f"_replace() 결과: {point2}")  # _replace() 결과: Point(x=10, y=4)

# 4. _fields - 필드명 튜플 반환
print(f"_fields: {Point._fields}")  # _fields: ('x', 'y')

# 5. _field_defaults - 기본값 딕셔너리 반환 (Python 3.7+)
print(f"_field_defaults: {Point._field_defaults}")  # _field_defaults: {'x': 0, 'y': 0}
