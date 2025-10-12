def solution(i, j, k):
    return sum([1 if str(k) in str(num) else 0 for num in range(i, j+1)])



if __name__ == '__main__':
    print(solution(1, 13, 1))
    print(solution(10, 50, 5))