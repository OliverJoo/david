import os
import re

CAESAR_PASSWORD_SUCCESS_FILE = os.path.join('result', 'result.txt')
CAESAR_PASSWORD_TEXT = 'B ehox Ftkl. 123'


def save_file(file_path=CAESAR_PASSWORD_SUCCESS_FILE, password=''):
    try:
        with open(file_path, 'w') as f:
            f.write(password)
        print(f'[정보] 비밀번호 저장 완료 | 파일 위치: {file_path}')
        return True
    except OSError as e:
        print(f'[에러] 비밀번호 저장 실패: {e}')


def caesar_cipher_decode():
    try:
        target_text = str(CAESAR_PASSWORD_TEXT).lower().split()
        final_list = []
        character_numbers = 26
        print("\\n--- 과제 풀이한 형식으로 복호화 ---")
        for idx in range(1, character_numbers + 1):
            text_combination = []
            for text in target_text:
                text = re.sub(r'[^a-z]', '', text)
                # print(''.join([chr((ord(char) - ord('a') + idx) % 26 + ord('a')) for char in text]))
                text_combination.append(
                    ''.join([chr((ord(char) - ord('a') + idx) % character_numbers + ord('a')) for char in text])
                )

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


def caesar_cipher_decode_lower_only():
    try:
        target_text = CAESAR_PASSWORD_TEXT.lower()
        final_list = []
        character_numbers = 26
        print("\\n--- 영문 소문자만 복호화 ---")

        # print(list(target_text))
        for idx in range(1, character_numbers + 1):
            decrypted_chars = []
            for char in target_text:
                if 'a' <= char <= 'z':
                    shifted_char = chr((ord(char) - ord('a') + idx) % character_numbers + ord('a'))
                    decrypted_chars.append(shifted_char)
                else:
                    decrypted_chars.append(char)

            decrypted_text = ''.join(decrypted_chars)
            final_list.append(decrypted_text)
            print(f'{idx}th 자릿수 해독 결과: {final_list[idx - 1]}')

        result = True
        while result:
            try:
                input_text = int(input('\\n저장하고 싶은 자릿수의 숫자를 입력하세요(범위 1~26): '))
                store_text = final_list[int(input_text) - 1]

                print(f'\\n[결과] 암호 해독 저장 텍스트: {store_text}')
                save_file(file_path=CAESAR_PASSWORD_SUCCESS_FILE, password=store_text)

                result = False
            except (ValueError, IndexError):
                print(f'[오류] 잘못 입력 하셨습니다.')
                continue

    except Exception as e:
        print(f'[에러] caesar_cipher_decode_lower_only: {e}')


def caesar_cipher_decode_all_letters():
    try:
        target_text = CAESAR_PASSWORD_TEXT
        final_list = []
        character_numbers = 26
        print("\\n--- 모든 영문자 복호화 ---")
        for idx in range(1, character_numbers + 1):
            decrypted_chars = []
            for char in target_text:
                if 'a' <= char <= 'z':
                    shifted_char = chr((ord(char) - ord('a') + idx) % character_numbers + ord('a'))
                    decrypted_chars.append(shifted_char)
                elif 'A' <= char <= 'Z':
                    shifted_char = chr((ord(char) - ord('A') + idx) % character_numbers + ord('A'))
                    decrypted_chars.append(shifted_char)
                else:
                    decrypted_chars.append(char)

            decrypted_text = ''.join(decrypted_chars)
            final_list.append(decrypted_text)
            print(f'{idx}th 자릿수 해독 결과: {final_list[idx - 1]}')

        result = True
        while result:
            try:
                input_text = int(input('\\n저장하고 싶은 자릿수의 숫자를 입력하세요(범위 1~26): '))
                store_text = final_list[int(input_text) - 1]

                print(f'\\n[결과] 암호 해독 저장 텍스트: {store_text}')
                save_file(file_path=CAESAR_PASSWORD_SUCCESS_FILE, password=store_text)

                result = False
            except (ValueError, IndexError):
                print(f'[오류] 잘못 입력 하셨습니다.')
                continue

    except Exception as e:
        print(f'[에러] caesar_cipher_decode_all_letters: {e}')


if __name__ == '__main__':
    try:
        # caesar_cipher_decode()
        caesar_cipher_decode_lower_only()
        # caesar_cipher_decode_all_letters()
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
