def str_to_sec(time_str: str) -> int:
    m, s = map(int, time_str.split(':'))
    return m * 60 + s


def sec_to_str(sec):
    m, s = divmod(sec, 60)

    return f'{m:02d}:{s:02d}'


def solution(video_len, pos, op_start, op_end, commands):
    video_len_sec = str_to_sec(video_len)
    pos_sec = str_to_sec(pos)
    op_start_sec = str_to_sec(op_start)
    op_end_sec = str_to_sec(op_end)

    if op_start_sec <= pos_sec <= op_end_sec:
        pos_sec = op_end_sec

    for cmd in commands:
        if cmd == 'next':
            pos_sec = min(pos_sec + 10, video_len_sec)
        elif cmd == 'prev':
            pos_sec = max(0, pos_sec - 10)

        if op_start_sec <= pos_sec <= op_end_sec:
            pos_sec = op_end_sec

    return sec_to_str(pos_sec)


# prev: move backward 10s, min 0s
# next: move forward 10s, min max_playtime
# skipping opening : if op_start ≤ current position ≤ op_end, move op_end

if __name__ == '__main__':
    print(solution("34:33", "13:00", "00:55", "02:55", ["next", "prev"]))
    print()
    print(solution("10:55", "00:05", "00:15", "06:55", ["prev", "next", "next"]))
    print()
    print(solution("07:22", "04:05", "00:15", "04:07", ["next"]))
    print()
    print(solution("07:22", "04:05", "00:15", "04:07", ["prev"]))
