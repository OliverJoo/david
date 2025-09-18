def solution(array):
    answer = [i for i, num in enumerate(array) if num == 2]

    print([num for num in range(0, len(array), 2)])

    return array[answer[0]: answer[-1] + 1] if len(answer) > 0 else [-1]


if __name__ == '__main__':
    print(solution([1, 2, 1, 4, 5, 2, 9]))
    print(solution([1, 2, 1]))
    print(solution([1, 1, 1]))
