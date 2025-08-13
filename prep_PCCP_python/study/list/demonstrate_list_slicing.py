# ============= LIST 슬라이싱 예제 =============
def demonstrate_list_slicing():
    """리스트 슬라이싱의 다양한 방법 시연"""

    data = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    print(f"원본 리스트: {data}")
    print()

    # 기본 슬라이싱
    print("=== 기본 슬라이싱 ===")
    print(f"data[2:5] = {data[2:5]}")  # 인덱스 2부터 4까지
    print(f"data[:3] = {data[:3]}")  # 처음부터 인덱스 2까지
    print(f"data[7:] = {data[7:]}")  # 인덱스 7부터 끝까지
    print(f"data[:] = {data[:]}")  # 전체 복사
    print()

    # 음수 인덱스 활용
    print("=== 음수 인덱스 슬라이싱 ===")
    print(f"data[-3:] = {data[-3:]}")  # 뒤에서 3개
    print(f"data[:-2] = {data[:-2]}")  # 뒤에서 2개 제외하고 모두
    print(f"data[-5:-2] = {data[-5:-2]}")  # 뒤에서 5번째부터 3번째까지
    print()

    # 스텝(간격) 활용
    print("=== 스텝 활용 슬라이싱 ===")
    print(f"data[::2] = {data[::2]}")  # 2칸씩 건너뛰며 모든 요소
    print(f"data[1::2] = {data[1::2]}")  # 1번부터 2칸씩 건너뛰기
    print(f"data[::-1] = {data[::-1]}")  # 역순 정렬
    print(f"data[8:2:-1] = {data[8:2:-1]}")  # 8부터 3까지 역순
    print()

    # 슬라이싱으로 수정
    print("=== 슬라이싱을 이용한 수정 ===")
    temp_data = data.copy()
    temp_data[2:5] = [20, 30, 40]  # 범위 교체
    print(f"data[2:5] = [20, 30, 40] 후: {temp_data}")

    temp_data = data.copy()
    temp_data[::2] = [0, 20, 40, 60, 80]  # 짝수 인덱스 모두 교체
    print(f"data[::2] = [0, 20, 40, 60, 80] 후: {temp_data}")


demonstrate_list_slicing()
