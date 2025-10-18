# n 개의 퍼즐 제한 시간 내에 풀기
# 난이도 diff / 퍼즐소요시간 time_cur / 이전 퍼즐 소요시간 time_prev / 숙련도 level
# process
# diff <= level, time_cur 시간 소요
# diff > level, (diff - level) * (time_cur + time_prev) + time_cur

# 제한시간 내의 모든 퍼즐 해결하기 위한 level 의 최소값 구하기.
