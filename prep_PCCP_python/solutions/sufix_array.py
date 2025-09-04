def solution(my_string):
    len_str = len(my_string)
    return sorted([my_string[len_str - num -1 :len_str] for num in range(0, len_str)])


if __name__ == '__main__':
    print(solution("programmers"))
    print(solution("banana"))
