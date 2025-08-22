def custom_heappush_visualization(heap, item):
    """heappush 과정을 단계별로 시각화"""
    print(f"\n=== {item} 삽입 과정 ===")
    heap_copy = heap[:]
    print(f"0. 원본: {heap_copy}")
    heap_copy.append(item)
    print(f"1. 끝에 추가: {heap_copy}")

    # Sift-up 과정 시뮬레이션
    pos = len(heap_copy) - 1
    step = 2

    while pos > 0:
        parent_pos = (pos - 1) // 2
        if heap_copy[pos] >= heap_copy[parent_pos]:
            break

        print(f"{step}. 위치 {pos}({heap_copy[pos]})와 부모 {parent_pos}({heap_copy[parent_pos]}) 교환")
        heap_copy[pos], heap_copy[parent_pos] = heap_copy[parent_pos], heap_copy[pos]
        print(f"   결과: {heap_copy}")
        pos = parent_pos
        step += 1

    return heap_copy


# 예제 실행
heap = [3, 8, 4, 10, 12, 7, 9]
result = custom_heappush_visualization(heap, 1)
