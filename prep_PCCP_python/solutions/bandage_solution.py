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


# 붕대감기 - 상태 관리 시뮬레이션
def bandage_healing_solution(bandage, health, attacks):
    """
    입력:
    - bandage: [시전시간, 초당회복량, 추가회복량]
    - health: 최대 체력
    - attacks: [[공격시간, 피해량], ...] 형태의 공격 패턴
    """
    t, x, y = bandage
    max_health = health
    attack_dict = {time: damage for time, damage in attacks}
    print(f'attack_dict: {attack_dict}')
    continuous_time = 0
    current_time = 1

    while current_time <= attacks[-1][0]:
        if current_time in attack_dict:
            # 공격받음 - 상태 초기화
            health -= attack_dict[current_time]
            continuous_time = 0

            if health <= 0:
                return -1
        else:
            # 치료 - 연속 성공 체크
            health += x
            continuous_time += 1

            if continuous_time == t:
                health += y
                continuous_time = 0

            health = min(health, max_health)

        current_time += 1

    return health


def solution_optimized(bandage, health, attacks):
    """
    최적화된 해법: 공격 간격을 계산하여 효율적으로 처리
    - 시간복잡도: O(공격 횟수)
    - 공간복잡도: O(1)
    """
    cast_time, heal_per_sec, bonus_heal = bandage
    max_health = health
    current_health = health
    prev_attack_time = 0

    for attack_time, damage in attacks:
        # 이전 공격부터 현재 공격까지의 회복 시간 계산
        recovery_time = attack_time - prev_attack_time - 1

        if recovery_time > 0:
            # 기본 회복량 계산
            basic_recovery = recovery_time * heal_per_sec

            # 연속 성공 보너스 계산
            bonus_count = recovery_time // cast_time
            bonus_recovery = bonus_count * bonus_heal

            # 총 회복량 적용
            current_health = min(max_health, current_health + basic_recovery + bonus_recovery)

        # 공격 피해 적용
        current_health -= damage

        # 사망 체크 (조기 종료로 성능 향상)
        if current_health <= 0:
            return -1

        # 다음 반복을 위한 시간 업데이트
        prev_attack_time = attack_time

    return current_health


if __name__ == '__main__':
    print(bandage_healing_solution([5, 1, 5], 30, [[2, 10], [9, 15], [10, 5], [11, 5]]))
    print()
    print(bandage_healing_solution([3, 2, 7], 20, [[1, 15], [5, 16], [8, 6]]))
    print()
    print(bandage_healing_solution([4, 2, 7], 20, [[1, 15], [5, 16], [8, 6]]))
    print()
    print(bandage_healing_solution([1, 1, 1], 5, [[1, 2], [3, 2]]))
