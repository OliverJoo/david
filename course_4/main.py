import json
import sys

LOG_FILE = 'data_source/mission_computer_main.log'
JSON_FILE = 'result/mission_computer_main.json'
MARKDOWN_FILE = 'result/log_analysis.md'
DANGER_FILE = 'result/danger_logs.txt'


def process_log_file(file_path, encoding='utf-8') -> tuple:
    log_list = []

    print(f'\n---- 전체 내용 출력({sys._getframe().f_code.co_name}) ----')
    try:
        with open(file_path, 'r', encoding=encoding) as file:
            lines = file.readlines()
            # for idx, line in enumerate(lines):
            for line in lines[1:]:
                print(line.strip())
                # if idx == 0:
                #     continue
                parts = line.strip().split(',', 2)
                if len(parts) == 3:
                    log_list.append(parts)
    except FileNotFoundError:
        print(f'Error: {file_path} not found')
        return [], [], {}
    except UnicodeDecodeError:
        print(f'Error: File Decoding({encoding}) Error occurs')
        return [], [], {}
    except Exception as e:
        print(f'Unexpected error: {e}')
        return [], [], {}

    reverse_logs_list = sorted(log_list, key=lambda x: x[0], reverse=True)
    print(f'\n---- 시간 역순으로 정렬된 리스트 출력({sys._getframe().f_code.co_name}) ----')
    # print(reverse_logs_list)
    for reverse_log in reverse_logs_list:
        print(reverse_log)

    log_dict = {log[0]: {'event': log[1], 'message': log[2]} for log in reverse_logs_list}
    print(f'\n---- Dict 객체({sys._getframe().f_code.co_name}) ----')
    print(log_dict)

    try:
        with open(JSON_FILE, 'w', encoding=encoding) as json_file:
            json.dump(log_dict, json_file, ensure_ascii=False, indent=2)
        print(f'JSON 저장 완료: {JSON_FILE}')
    except FileNotFoundError as e:
        print(f'파일 또는 경로 에러: {e}')
    except UnicodeEncodeError:
        print(f'파일 저장 중 인코딩 에러 발생({encoding})')
    except TypeError as e:
        print(f'JSON 직렬화 에러: {e}')   # log_dict의 value가 인코딩 불가 객체일때
    except Exception as e:
        print(f'Unexpected JSON Error: {e}')

    return log_list, reverse_logs_list, log_dict


def make_markdown_report(file_path, encoding='utf-8'):
    try:
        with open(file_path, 'r', encoding=encoding) as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f'Error: {file_path} not found')
        return
    except UnicodeDecodeError:
        print(f'Error: File Decoding({encoding}) Error occurs')
        return
    except Exception as e:
        print(f'Unexpected Error: {e}')
        return

    events = []
    danger_events = []
    mission_completed_ts = None
    unstable_ts = []
    exploded_ts = []

    try:
        for line in lines[1:]:  # ignore header
            parts = line.strip().split(',', 2)
            if len(parts) != 3:
                continue
            ts, event, message = parts
            events.append({'timestamp': ts, 'event': event, 'message': message})

            if 'Mission completed successfully' in message:
                mission_completed_ts = ts
            if 'Oxygen tank unstable' in message:
                unstable_ts.append(ts)
                danger_events.append(f'{ts} - {message}')
            if 'Oxygen tank explosion' in message:
                exploded_ts.append(ts)
                danger_events.append(f'{ts} - {message}')

            if mission_completed_ts and unstable_ts and exploded_ts:
                summary = (
                    f'로켓 임무는 {mission_completed_ts} 에 성공적으로 종료. '
                    f'하지만 임무 종료 후 {', '.join(unstable_ts)} 산소 탱크의 불안정과 '
                    f'{', '.join(exploded_ts)} 산소탱크 폭발사고 발생'
                    '정확한 원인 분석을 위한 추가 조사 필요'
                )
            else:
                summary = '로그상 정상적 임무 수행이거나, 사고 관련 정보가 없음.'

            with open(MARKDOWN_FILE, 'w', encoding=encoding) as file:
                file.write('# 사고 원인 분석 보고서\n\n')
                file.write('## 요약\n')
                file.write(summary + '\n\n')
                file.write('## 위험 이벤트 타임라인\n')
                for event in danger_events:
                    file.write(f'- {event}\n')
                file.write('\n---\n')
    except FileNotFoundError as e:
        print(f'파일 또는 경로 에러: {e}')
        return
    except UnicodeDecodeError:
        print(f'Error: File Decoding({encoding}) Error occurs')
        return
    except Exception as e:
        print(f'보고서 저장 오류: {e}')
        return
    print(f'Markdown 사고 보고서 파일({MARKDOWN_FILE}) 저장 완료')


def advanced_functions(log_dict, encoding='utf-8'):
    print(f'\n=== 시간 역순 로그 목록({sys._getframe().f_code.co_name}) ===')
    for ts, data in log_dict.items():
        print([ts, data['event'], data['message']])

    danger_keywords = ['폭발', '누출', '고온', 'Oxygen', 'explosion', 'leak', 'high temperature']
    danger_logs = []
    for ts, data in log_dict.items():
        msg = data['message']
        if any(kw.lower() in msg.lower() for kw in danger_keywords):
            danger_logs.append(f"{ts} - {msg}")
    try:
        with open(DANGER_FILE, 'w', encoding=encoding) as f:
            for line in danger_logs:
                f.write(line + '\n')
        print(f'\n위험 로그가 {DANGER_FILE}에 저장되었습니다.')
    except FileNotFoundError as e:
        print(f'파일 또는 경로 에러: {e}')
    except Exception as e:
        print(f'Unexpected Error: {e}')

    try:
        with open(JSON_FILE, 'r', encoding=encoding) as f:
            json_dict = json.load(f)
    except FileNotFoundError:
        print(f'Error: {JSON_FILE} not found')
        return
    except json.JSONDecodeError:
        print(f'Error: JSON 파일 형식이 올바르지 않습니다.')
        return
    except Exception as e:
        print(f'Unexpected Error: {e}')
        return

    search_term = input('\n검색할 메시지 문자열 입력: ').strip()
    print(f'\n[검색 결과: {search_term}]')
    found = False
    for val in json_dict.values():
        if search_term.lower() in val['message'].lower():
            print(f"{val['event']} | {val['message']}")
            found = True
    if not found:
        print('해당 문자열이 포함된 로그가 없습니다.')


if __name__ == '__main__':
    # 1. 로그 파일 분석 및 변환
    logs, reverse_logs, log_dict = process_log_file(LOG_FILE)

    # 2. 사고 분석 보고서 생성
    if logs:
        make_markdown_report(LOG_FILE)

    # 3. 고급 기능(보너스)
    # if logs and reverse_logs and log_dict:
    if logs and log_dict:
        advanced_functions(log_dict)
