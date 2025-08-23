# ============= SET 정렬 예제 =============
def demonstrate_set_sorting():
    """세트 정렬 (리스트로 변환 후 정렬)"""

    numbers = {64, 34, 25, 12, 22, 11, 90, 34, 12}  # 중복 포함
    print(f"원본 세트 (중복 자동 제거): {numbers}")

    # 세트는 순서가 없으므로 정렬하려면 리스트로 변환
    print("\n=== 세트 정렬 (리스트 변환) ===")

    # 방법 1: sorted() 함수 사용
    sorted_list = sorted(numbers)
    print(f"sorted() 사용: {sorted_list}")

    # 방법 2: 리스트 변환 후 sort()
    number_list = list(numbers)
    number_list.sort()
    print(f"list() + sort() 사용: {number_list}")

    # 정렬된 결과를 다시 세트로 (순서는 보장되지 않음)
    # Python 3.7+ 에서는 딕셔너리가 삽입 순서를 보장하지만, 세트는 여전히 순서 보장 안함
    sorted_set = set(sorted_list)  # 의미 없음 (순서 사라짐)
    print(f"정렬 후 다시 세트로 변환: {sorted_set}")

    # 문자열 세트 정렬
    words = {"python", "java", "javascript", "go", "rust"}
    print(f"\n문자열 세트: {words}")
    print(f"알파벳 순 정렬: {sorted(words)}")
    print(f"길이 순 정렬: {sorted(words, key=len)}")


demonstrate_set_sorting()
