def solution(my_string, queries):
    my_string = list(my_string)

    for query in queries:
        my_string[query[0]: query[1] + 1] = my_string[query[0]: query[1] + 1][::-1]
        print(''.join(my_string))

    return ''.join(my_string)


if __name__ == '__main__':
    print(solution("rermgorpsam", [[2, 3], [0, 7], [5, 9], [6, 10]]))
