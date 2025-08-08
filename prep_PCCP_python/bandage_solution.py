def solution(bandage, health, attacks):
    answer = health
    max_len = len(attacks) - 1
    attack_finish_time = attacks[max_len][0]
    bandage_time, recovery, additional_recovery = bandage
    accumulated_cnt = 0
    attack_dict = {attack[0]: attack[1] for attack in attacks}

    for idx in range(1, attack_finish_time + 1):
        if idx in attack_dict:
            answer -= attack_dict.get(idx)
            accumulated_cnt = 0
            print(f'1 attack info : {idx} | bandage_time:{bandage_time} |  attack: {attack_dict.get(idx)} | answer:{answer}')

            if answer <= 0:
                return -1
        else:
            answer += recovery
            accumulated_cnt += 1
            if accumulated_cnt == bandage_time:
                answer += additional_recovery
                accumulated_cnt = 0

            print(f'2 attack info : {idx} | bandage_time:{bandage_time} |  attack: {attack_dict.get(idx)} | answer:{answer}')

            if answer >= health:
                answer = health


        print(f'final attack info : {idx} | bandage_time:{bandage_time} |  attack: {attack_dict.get(idx)} | answer:{answer}')
    return -1 if answer <= 0 else answer


if __name__ == '__main__':
    print(solution([5, 1, 5], 30, [[2, 10], [9, 15], [10, 5], [11, 5]]))
    print()
    print(solution([3, 2, 7], 20, [[1, 15], [5, 16], [8, 6]]))
    print()
    print(solution([4, 2, 7], 20, [[1, 15], [5, 16], [8, 6]]))
    print()
    print(solution([1, 1, 1], 5, [[1, 2], [3, 2]]))
