def solution(my_string):
    answer = []
    str_dict = {1 : 'w', -1 : 's', 10 : 'd', -10 : 'a'}
    len_str = len(my_string)

    for num in range(1, len_str):
        print(my_string[num]-my_string[num-1])
        answer.append(str_dict[my_string[num]-my_string[num-1]])

    # w = +1
    # s = -1
    # d = +10
    # a = -10

    # wsdawsdassw
    # [+1, -1, +10, -10, +1, -1, +10, -10, -1, -1, +1]

    # [0,   1,   0,  10,  0,  1,   0,  10,  0, -1, -2, -1]
    #       w    s    d    a  w     s   d    a   s   s  w
    # [0,   1,   2,   3,  4,  5,   6,   7,  8,  9, 10, 11]
    return ''.join(answer)


if __name__ == '__main__':
    print(solution([0, 1, 0, 10, 0, 1, 0, 10, 0, -1, -2, -1]))
