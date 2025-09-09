import json
import os
import time
import zipfile, zlib
import itertools
import string
from multiprocessing import Pool, cpu_count
import multiprocessing as mp
import re

# Password Rule: 특수 문자없이 숫자와 소문자 알파벳으로 구성된 6자리 문자
# ENCRYPTED_ZIP_FILE = os.path.join('data_source', 'ai_file.zip') # for test
# UNLOCK_ZIP_SUCCESS_FILE = os.path.join('result', 'ai_file_password.txt')  # q1 | # for test
ENCRYPTED_ZIP_FILE = os.path.join('data_source', 'emergency_storage_key.zip')
UNLOCK_ZIP_SUCCESS_FILE = os.path.join('result', 'password.txt')  # q1
CAESAR_PASSWORD_FILE = os.path.join('data_source', 'password.txt')  # q2 | emergency_storage_key.zip 안의 password.txt
CAESAR_PASSWORD_SUCCESS_FILE = os.path.join('result', 'result.txt')
MULTIPROCESSING_NUMB_WORKERS = cpu_count()


# emergency_storage_key.zip 의 암호 해독 코드 작성. 단 암호는 특수 문자없이 숫자와 소문자 알파벳으로 구성된 6자리 문자로 되어 있다.
# 암호를 푸는 과정을 출력하는데 시작 시간과 반복 회수 그리고 진행 시간등을 출력한다.
# 보너스 과제: 암호를 좀 더 빠르게 풀 수 있는 알고리즘을 제시하고 코드로 구현한다.
def unlock_zip(password_list):
    try:
        with zipfile.ZipFile(ENCRYPTED_ZIP_FILE, 'r') as zf:

            file_info = zf.getinfo(zf.namelist()[0])

            for idx, password in enumerate(password_list, 1):
                try:
                    # 1단계: 빠른 검사. 헤더 일부(1)만 읽어 암호가 맞는지 빠르게 확인합니다.
                    with zf.open(file_info, pwd=password.encode()) as fp:
                        first_byte = fp.read(1)
                        full_content = first_byte + fp.read()

                        # 2단계: 정밀 검사 (CRC-32). 1단계를 통과한 후보에 대해서만 실행합니다.
                        # False Positive를 완벽하게 걸러내기 위해 파일 전체를 읽어 무결성을 검증
                        if (zlib.crc32(full_content) & 0xFFFFFFFF) == file_info.CRC:
                            print(f'\n[발견] PID: {os.getpid()} | {idx}번째에서 비밀번호 발견: "{password}"')
                            save_file(password=password)
                            return password
                        else:
                            # 매우 드문 False Positive 케이스 검증
                            print(f'\n[경고] PID: {os.getpid()} | {idx}번째에서 False Positive 발생: "{password}"')
                            continue

                except (RuntimeError, zipfile.BadZipFile, OSError, Exception) as e:
                    # print(f'Wrong Password: {password} | {e}')
                    pass

                if idx % 2_500_000 == 0:
                    print(
                        f'PID={mp.current_process().pid} | 진행상황: {idx:,} / {len(password_list):,} | 방금 확인한 비밀번호:{password}')

    except Exception as e:
        print(f"ZIP 파일 처리 에러: {e}")
        return None
    return None


def save_file(file_path=UNLOCK_ZIP_SUCCESS_FILE, password=''):
    try:
        with open(file_path, 'w') as f:
            f.write(password)
        print(f'[정보] 비밀번호 저장 완료 | 파일 위치: {file_path}')
        return True
    except OSError as e:
        print(f'[에러] 비밀번호 저장 실패: {e}')


def read_file(file_path: str = CAESAR_PASSWORD_FILE):
    try:
        with open(file_path, 'r', encoding='utf-8', newline='') as f:
            return f.readlines()
    except OSError as e:
        print(f'[에러] 비밀번호 읽기 실패: {e}')
        return None


def unlock_process():
    chars = string.ascii_lowercase + string.digits
    password_product = [''.join(combo) for combo in itertools.product(chars, repeat=5)]

    total = len(chars) ** 6
    start_ts = time.time()
    start_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_ts))
    print(f"\n[시작] {start_str} | 총 시도 예상: {total:,}개")
    accumulated_cnt = 0

    for idx, first_char in enumerate(chars, 1):
        password_list = list(map(str.__add__, itertools.repeat(first_char), password_product))

        base_chunk_size = len(password_list) // MULTIPROCESSING_NUMB_WORKERS
        remainder = len(password_list) % MULTIPROCESSING_NUMB_WORKERS
        accumulated_cnt += base_chunk_size + remainder

        worker_payloads = []
        start_idx = 0
        for worker_idx in range(MULTIPROCESSING_NUMB_WORKERS):
            chunk_size = base_chunk_size + (1 if worker_idx < remainder else 0)
            chunk = password_list[start_idx:start_idx + chunk_size]
            if chunk:
                worker_payloads.append(chunk)
            start_idx += chunk_size

        print(f'[진행] {idx}회 프로세스 시작 | 배치 크기: {base_chunk_size} | 잔여 갯수: {remainder} | 작업 수: {len(worker_payloads)}\n')

        try:
            with mp.Pool(processes=len(worker_payloads)) as pool:
                # password_result = pool.map(unlock_zip, worker_payloads)
                # password_result = [pool.apply_async(unlock_zip, (item,)) for item in worker_payloads]
                for result in pool.imap_unordered(unlock_zip, worker_payloads, chunksize=1):
                    if result:  # 비밀번호 발견
                        print(f"비밀번호 발견: {result}")
                        pool.terminate()  # 다른 워커들 즉시 종료
                        pool.join()
                        elapsed = time.time() - start_ts
                        print(
                            f"\n[작업 완료] {idx:,}회차 | 진행률: {idx / len(chars):.2%} | 총 소요 시간: {elapsed:.1f}s({elapsed / 60:.1f}분) | {accumulated_cnt / elapsed:,.0f}회/s")
                        return result

        except Exception as e:
            print(f'Unexpected Exception: {e}')

        elapsed = time.time() - start_ts
        print(
            f"\n[진행] {idx:,}회 완료(총 {len(chars)}회) | 진행률: {idx / len(chars):.2%} | 총 소요 시간: {elapsed:.1f}s({elapsed / 60:.1f}분) | {accumulated_cnt / elapsed:,.0f}회/s\n")

    return None


# caesar_cipher_decode() 함수는 풀어야 하는 문자열을 파라메터로 추가한다. 이때 파라메터의 이름은 target_text으로 한다.
# caesar_cipher_decode() 에서 자리수에 따라 암호표가 바뀌게 한다. 자리수는 알파벳 수만큼 반복한다.
# 자리수에 따라서 해독된 결과를 출력한다.
# 몇 번째 자리수로 암호가 해독되는지 찾아낸다. 눈으로 식별이 가능하면 해당 번호를 입력하면 그 결과를 result.txt로 저장을 한다.
# 보너스 과제: 텍스트 사전을 만들고 사전에 있는 단어와 일치하는 키워드가 암호속에서 발견될 경우 반복을 멈출 수 있게 작성
def caesar_cipher_decode():
    try:
        target_text = read_file(CAESAR_PASSWORD_FILE)
        text_list = str(target_text).lower().split()
    except FileNotFoundError as e:
        print(f'File Not Found: {e}')
    except ValueError as e:
        print(f'File Verification Error: {e}')

    try:
        final_list = []
        character_numbers = 26
        for idx in range(1, character_numbers + 1):
            text_combination = []
            for text in text_list:
                text = re.sub(r'[^a-z]', '', text)
                # print(''.join([chr((ord(char) - ord('a') + idx) % 26 + ord('a')) for char in text]))
                text_combination.append(
                    ''.join([chr((ord(char) - ord('a') + idx) % character_numbers + ord('a')) for char in text]))

            final_list.append(' '.join(text_combination))
            print(f'{idx}th 자릿수 해독 결과: {final_list[idx - 1]}')

        result = True
        while result:
            try:
                input_text = int(input('\n저장하고 싶은 자릿수의 숫자를 입력하세요(범위 1~26): '))
                store_text = final_list[int(input_text) - 1]

                print(f'\n[결과] 암호 해독 저장 텍스트: {store_text}')
                save_file(file_path=CAESAR_PASSWORD_SUCCESS_FILE, password=store_text)

                result = False
            except Exception as e:
                print(f'[오류] 잘못 입력 하셨습니다.')
                continue


    except re.error as e:
        print(f'RE Expression Error: {e}')
    except (ValueError, OverflowError) as e:
        print(f'Character Translation Error: {e}')
    except IOError as e:
        print(f'I/O Error: e')


if __name__ == '__main__':
    try:

        # 문제 1
        mp.set_start_method("spawn", force=True)
        print(f'success: {unlock_process()}')

        # 문제 2
        caesar_cipher_decode()
    except Exception as e:
        print(f'Unexpected Exception: {e}')

# 제약사항
#
# python에서 기본 제공되는 명령어 이외의 별도의 라이브러리나 패키지를 사용해서는 안된다.
# 단, zip 파일을 다루는 부분은 외부 라이브러리 사용 가능하다.
# 반복 할 때마다 결과를 눈으로 확인 할 수 있어야 한다.
# 경고 메시지 없이 모든 코드는 실행 되어야 한다.
# 파일을 다루는 부분은 모두 예외처리가 되어 있어야 한다.
# 암호가 확인 되었을 때 최종 암호가 result.txt로 저장되어야 한다.
