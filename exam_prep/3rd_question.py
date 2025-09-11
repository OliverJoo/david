import json
import pprint
from datetime import datetime

LOG_FILE = 'data_source/mission_computer_main.log'


def process_log_file(file_path=LOG_FILE, encoding='utf-8'):
    try:
        with open(file_path, 'r', encoding=encoding) as file:
            return file.readlines()
    except FileNotFoundError:
        print(f'Error: {file_path} not found')
        return []
    except UnicodeDecodeError as e:
        print(f'파일 인코딩 관련 에러: {e}')
        return []
    except Exception as e:
        print(f'Unexpected error: {e}')
        return []


# class ProcessingError(Exception):
#     def __init__(self, message: str, stage: str, details: Optional[dict] = None):
#         super().__init__(message)
#         self.stage = stage
#         self.details = details or {}


def main():
    try:
        log_origin = process_log_file()
        print(f'=== log original DataSet Structure ===')
        print(f'{log_origin}\n\n')

        # log_list = [logs.strip('\n').split(',', 2) for logs in log_origin[1:]]

        log_list = []
        for logs in log_origin[1:]:
            log_data = logs.strip().strip('\n').split(',', 2)
            if len(log_data) == 3:
                time_stamp, log_level, message = log_data
                try:
                    # datetime.fromisoformat(time_stamp.strip())
                    # NOTI: datetime.strptime Exception
                    if datetime.strptime(time_stamp.strip(), '%Y-%m-%d %H:%M:%S'):
                        log_list.append((time_stamp.strip(), message.strip()))
                    else:
                        raise (TypeError, ValueError)
                except (TypeError, ValueError) as e:
                    print(f'====== datetime type error ======')
        # print(f'\n\n=== Log - Tuple List(1) ===') # no
        # print(*log_list, sep='\n')
        # print(f'\n\n=== Log - Tuple List(2) ===') # no
        # print('\n'.join(str(item) for item in log_list))
        print(f'\n\n=== Log - log_list:01 (original) ===')
        print(f'{log_list}')
        print(f'\n\n=== Log - log_list:02 (formatted_log_list) ===')
        formatted_log_list  = "[\n" + "\n".join(f"  {item}{',' if i < len(log_list) - 1 else ''}" for i, item in enumerate(log_list) ) + "\n]"
        print(formatted_log_list)
        print(f'\n\n=== Log - log_list:03 (pprint.pprint) ===')
        log_list_pprint = pprint.pformat(log_list, width=120)
        print(log_list_pprint)

        print(f'\n\n=== Log - reversed list:01 (original) ===')
        reversed_list = sorted(log_list, key=lambda x: x[0], reverse=True)
        print(reversed_list)
        print(f'\n\n=== Log - reversed list:02 (formatted_reversed_log_list) ===')
        formatted_reversed_log_list = "[\n" + "\n".join(
            f"  {item}{',' if i < len(reversed_list) - 1 else ''}" for i, item in enumerate(reversed_list)) + "\n]"
        print(formatted_reversed_log_list)
        print(f'\n\n=== Log - reversed list:03 (pprint.pprint) ===')
        formatted_reversed_log_list_pprint = pprint.pformat(reversed_list, width=120)
        print(formatted_reversed_log_list_pprint)

        print(f'\n\n=== dictionary type:01 (original) ===') # 1st try
        dict_result = dict(reversed_list)
        print(dict_result)
        print(f'\n\n=== dictionary type:02 (formatted_log_dict) ===')  # 2nd try
        formatted_dict_result = "{\n" + "\n".join(f"  '{k}': '{v}'{',' if i < len(dict_result) - 1 else ''}"
            for i, (k, v) in enumerate(dict_result.items())) + "\n}"
        print(formatted_dict_result)
        print(f'\n\n=== dictionary type:03 (pprint.pprint) ===')
        dict_result_pprint = pprint.pformat(dict_result,  width=120)
        print(dict_result_pprint)
        print(f'\n\n=== dictionary type:04 (json.dumps) ===')
        dict_result_json_dumps = json.dumps(dict_result, ensure_ascii=False, indent=2)
        print(dict_result_json_dumps)


    except Exception as e:
        print(f'Unexpected Exception: {e}')


if __name__ == '__main__':
    main()
