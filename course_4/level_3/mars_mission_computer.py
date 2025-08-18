# mars_mission_computer.py
import random
import json
import time
import threading
import multiprocessing
import platform
import signal
import sys
import os
import select
import subprocess
from datetime import datetime
from typing import Dict, Optional

# 전역 종료 이벤트
stop_event = multiprocessing.Event()


def signal_handler(signum, frame):
    stop_event.set()


signal.signal(signal.SIGINT, signal_handler)


class DummySensor:
    """더미 센서: 화성 기지 환경 데이터 시뮬레이션"""

    def __init__(self):
        self.env_values: Dict[str, float] = {
            'mars_base_internal_temperature': 0.0,
            'mars_base_external_temperature': 0.0,
            'mars_base_internal_humidity': 0.0,
            'mars_base_external_illuminance': 0.0,
            'mars_base_internal_co2': 0.0,
            'mars_base_internal_oxygen': 0.0
        }

    def set_env(self) -> None:
        """지정된 범위에서 랜덤 환경값 설정"""
        self.env_values['mars_base_internal_temperature'] = round(random.uniform(18, 30), 2)
        self.env_values['mars_base_external_temperature'] = round(random.uniform(0, 21), 2)
        self.env_values['mars_base_internal_humidity'] = round(random.uniform(50, 60), 2)
        self.env_values['mars_base_external_illuminance'] = round(random.uniform(500, 715), 2)
        self.env_values['mars_base_internal_co2'] = round(random.uniform(0.02, 0.1), 4)
        self.env_values['mars_base_internal_oxygen'] = round(random.uniform(4, 7), 2)

    def get_env(self) -> Dict[str, float]:
        """환경값 반환 및 로그 파일 기록"""
        log_data = {
            'datetime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            **self.env_values
        }
        try:
            log_file_path = os.path.join('result', 'mars_base_env_log.txt')
            with open(log_file_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_data, ensure_ascii=False, indent=2) + '\n')
        except IOError as e:
            print(f'로그 파일 기록 실패: {e}')
        return self.env_values.copy()


class MissionComputer:
    """미션 컴퓨터: 센서 데이터 수집 및 관리"""

    def __init__(self):
        self.env_values: Dict[str, float] = {
            'mars_base_internal_temperature': 0.0,
            'mars_base_external_temperature': 0.0,
            'mars_base_internal_humidity': 0.0,
            'mars_base_external_illuminance': 0.0,
            'mars_base_internal_co2': 0.0,
            'mars_base_internal_oxygen': 0.0
        }
        self.ds = DummySensor()
        self.data_history = []
        self.last_average_time = time.time() - 300

    def get_sensor_data(self):
        """센서 데이터를 5초마다 수집하여 JSON으로 출력"""
        print('=== 센서 데이터 수집 시작 ===')
        print('종료하려면 q를 입력하세요.')

        while True:
            try:
                self.ds.set_env()
                self.env_values = self.ds.get_env()
                self.data_history.append(self.env_values.copy())

                print('=== 화성 기지 환경 정보 ===')
                print(json.dumps(self.env_values, indent=2, ensure_ascii=False))
                print(f'업데이트 시간: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

                # 5분(300초)마다 평균 계산
                now = time.time()

                if now - self.last_average_time >= 300:
                    self._calculate_5min_average()
                    self.last_average_time = now

                print('-' * 50)

                # 5초 대기하며 q 입력 감지
                start_time = time.time()
                while time.time() - start_time < 5:
                    ready, _, _ = select.select([sys.stdin], [], [], 0.1)
                    if ready:
                        user_input = sys.stdin.readline().strip().lower()
                        if user_input == 'q':
                            print('System stopped....')
                            return

            except Exception as e:
                print(f'센서 데이터 수집 중 오류: {e}')
                time.sleep(5)

    def _calculate_5min_average(self):
        """5분 평균값 계산 및 출력"""
        if not self.data_history:
            return

        avg_data = {}
        for key in self.env_values.keys():
            values = [data[key] for data in self.data_history if key in data]
            if values:
                avg_data[f'{key}_5min_avg'] = round(sum(values) / len(values), 2)

        print('\n=== 5분 평균 환경 정보 ===')
        print(json.dumps(avg_data, indent=2, ensure_ascii=False))
        print(f'평균 계산 시간: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        print('-' * 50)

        self.data_history = []
        self.data_history = self.data_history[-50:]

    def get_mission_computer_info(self) -> Dict:
        """시스템 정보 수집 및 JSON 출력"""
        try:
            info = {
                'operating_system': platform.system(),
                'os_version': platform.version(),
                'cpu_type': platform.processor(),
                'cpu_cores': self._get_cpu_cores(),
                'memory_total_gb': self._get_memory_info()
            }

            settings = self._load_settings()
            if settings:
                info = self._filter_info_by_settings(info, settings)

            print('=== 미션 컴퓨터 시스템 정보 ===')
            print(json.dumps(info, indent=2, ensure_ascii=False))
            print('-' * 50)
            return info

        except Exception as e:
            print(f'시스템 정보 수집 중 오류: {e}')
            return {}

    def get_mission_computer_load(self) -> Dict:
        """실시간 부하 정보 수집 및 JSON 출력"""
        try:
            load_info = {
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'cpu_usage_percent': self._get_cpu_usage(),
                'memory_usage_percent': self._get_memory_usage()
            }

            print('=== 미션 컴퓨터 부하 정보 ===')
            print(json.dumps(load_info, indent=2, ensure_ascii=False))
            print('-' * 50)
            return load_info

        except Exception as e:
            print(f'시스템 부하 정보 수집 중 오류: {e}')
            return {}

    def _get_cpu_cores(self):
        """CPU 코어 수 반환"""
        try:
            return os.cpu_count() or 'N/A'
        except Exception:
            return 'N/A'

    def _get_memory_info(self):
        """총 메모리 크기 반환 (GB 단위)"""
        try:
            system = platform.system()
            if system == 'Linux':
                with open('/proc/meminfo', 'r') as f:
                    for line in f:
                        if line.startswith('MemTotal:'):
                            mem_kb = int(line.split()[1])
                            return round(mem_kb / (1024 ** 2), 2)
            elif system == 'Darwin':
                result = subprocess.check_output(['sysctl', 'hw.memsize'], text=True)
                mem_bytes = int(result.split(':')[1].strip())
                return round(mem_bytes / (1024 ** 3), 2)
        except Exception as e:
            print(f'메모리 정보 수집 오류: {e}')
        return 'N/A'

    def _get_memory_usage(self):
        """메모리 사용률 반환 (%)"""
        try:
            system = platform.system()
            if system == 'Linux':
                with open('/proc/meminfo', 'r') as f:
                    mem_info = {}
                    for line in f:
                        parts = line.split(':')
                        if len(parts) == 2:
                            key = parts[0].strip()
                            value = int(parts[1].strip().split())
                            mem_info[key] = value

                total = mem_info.get('MemTotal', 0)
                available = mem_info.get('MemAvailable', 0)
                if total > 0:
                    used_percent = round((total - available) / total * 100, 1)
                    return used_percent

            elif system == 'Darwin':
                result = subprocess.check_output(['vm_stat'], text=True)
                pages = {}
                page_size = 4096  # macOS 기본: 4KB

                for line in result.splitlines():
                    if ':' in line:
                        parts = line.split(':')
                        if len(parts) >= 2:
                            key = parts[0].strip().strip('"')
                            value_str = parts[1].strip().rstrip('.')
                            try:
                                pages[key] = int(value_str)
                            except ValueError:
                                continue

                # free_pages = pages.get('Pages free', 0)
                # inactive_pages = pages.get('Pages inactive', 0)
                # active_pages = pages.get('Pages active', 0)
                # wired_pages = pages.get('Pages wired down', 0)
                # total_pages = free_pages + inactive_pages + active_pages + wired_pages

                free = pages.get('Pages free', 0)
                active = pages.get('Pages active', 0)
                inactive = pages.get('Pages inactive', 0)
                speculative = pages.get('Pages speculative', 0)
                wired = pages.get('Pages wired down', 0)
                purgeable = pages.get('Pages purgeable', 0)
                file_backed = pages.get('File-backed pages', 0)
                compressed = pages.get('Pages occupied by compressor', 0)
                total_pages = (free + active + inactive + speculative + wired) * page_size

                # print(f'memory total info: free_pages: {free_pages} | inactive_pages: {inactive_pages} | active_pages: {active_pages} | wired_pages: {wired_pages} | total_pages: {total_pages}\npages:{pages}')

                if total_pages > 0:
                    # used_pages = active_pages + wired_pages
                    used_pages = (active + wired + compressed) * page_size
                    # print(f'memory check : {used_pages} / {total_pages} = {round(used_pages / total_pages * 100, 1)}')
                    return round(used_pages / total_pages * 100, 1)

        except Exception as e:
            print(f'메모리 사용률 수집 오류: {e}')
        return 'N/A'

    def _get_cpu_usage(self):
        """CPU 사용률 반환 (%)"""
        try:
            system = platform.system()
            if system == 'Linux':
                with open('/proc/stat', 'r') as f:
                    cpu_line = f.readline()
                    cpu_times1 = list(map(int, cpu_line.split()[1:]))

                time.sleep(0.1)

                with open('/proc/stat', 'r') as f:
                    cpu_line = f.readline()
                    cpu_times2 = list(map(int, cpu_line.split()[1:]))

                idle1, idle2 = cpu_times1[3], cpu_times2[2]
                total1, total2 = sum(cpu_times1), sum(cpu_times2)

                idle_delta = idle2 - idle1
                total_delta = total2 - total1

                if total_delta > 0:
                    cpu_usage = round((1 - idle_delta / total_delta) * 100, 1)
                    return cpu_usage

            elif system == 'Darwin':
                result = subprocess.check_output(['top', '-l', '1', '-n', '0'], text=True)

                for line in result.splitlines():
                    if 'CPU usage' in line:
                        cpu_part = line.split('CPU usage:')[1].strip()
                        segments = [seg.strip() for seg in cpu_part.split(',')]

                        user_pct = 0
                        sys_pct = 0

                        for segment in segments:
                            if '%' in segment and 'user' in segment:
                                user_pct = float(segment.split('%')[0].strip())
                            elif '%' in segment and 'sys' in segment:
                                sys_pct = float(segment.split('%')[0].strip())

                        return round(user_pct + sys_pct, 1)

        except Exception as e:
            print(f'CPU 사용률 수집 오류: {e}')
        return 'N/A'

    def _load_settings(self):
        """setting.txt 파일 로드"""
        setting_file_path = os.path.join('result', 'setting.txt')

        try:
            if not os.path.exists(setting_file_path):
                self._create_default_settings()

            with open(setting_file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f'설정 파일 로드 실패: {e}')
            return None

    def _create_default_settings(self):
        """기본 setting.txt 파일 생성"""
        setting_file_path = os.path.join('result', 'setting.txt')

        default_settings = {
            'system_info': {
                'show_os': True,
                'show_cpu': True,
                'show_memory': True
            }
        }
        try:
            with open(setting_file_path, 'w', encoding='utf-8') as f:
                json.dump(default_settings, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f'설정 파일 생성 실패: {e}')

    def _filter_info_by_settings(self, info, settings):
        """설정에 따른 정보 필터링"""
        try:
            filtered = {}
            sys_settings = settings.get('system_info', {})

            if sys_settings.get('show_os', True):
                filtered['operating_system'] = info.get('operating_system')
                filtered['os_version'] = info.get('os_version')
            if sys_settings.get('show_cpu', True):
                filtered['cpu_type'] = info.get('cpu_type')
                filtered['cpu_cores'] = info.get('cpu_cores')
            if sys_settings.get('show_memory', True):
                filtered['memory_total_gb'] = info.get('memory_total_gb')

            return filtered if filtered else info
        except Exception:
            return info


# 멀티프로세스용 전역 함수들
def process_info_worker(stop_evt):
    """시스템 정보 수집 프로세스 (runComputer1)"""
    computer = MissionComputer()
    while not stop_evt.is_set():
        print('\n[PROCESS-INFO] 시스템 정보 업데이트')
        computer.get_mission_computer_info()
        for _ in range(200):  # 20초
            if stop_evt.is_set():
                return
            time.sleep(0.1)


def process_load_worker(stop_evt):
    """부하 정보 수집 프로세스 (runComputer2)"""
    computer = MissionComputer()
    while not stop_evt.is_set():
        print('\n[PROCESS-LOAD] 부하 정보 업데이트')
        computer.get_mission_computer_load()
        for _ in range(200):  # 20초
            if stop_evt.is_set():
                return
            time.sleep(0.1)


def process_sensor_worker(stop_evt):
    """센서 데이터 수집 프로세스 (runComputer3)"""
    computer = MissionComputer()
    while not stop_evt.is_set():
        computer.ds.set_env()
        computer.env_values = computer.ds.get_env()
        print('\n[PROCESS-SENSOR] 센서 데이터 업데이트')
        print(json.dumps(computer.env_values, indent=2, ensure_ascii=False))
        for _ in range(50):  # 5초
            if stop_evt.is_set():
                return
            time.sleep(0.1)


def run_multithreaded():
    """멀티스레드 모드 실행"""
    print('=== 멀티스레드 모드 ===')
    print('종료하려면 q를 입력하세요.')

    stop_evt = threading.Event()

    def info_thread():
        computer = MissionComputer()
        while not stop_evt.is_set():
            print('\n[THREAD-INFO] 시스템 정보 업데이트')
            computer.get_mission_computer_info()
            for _ in range(200):  # 20초
                if stop_evt.is_set():
                    return
                time.sleep(0.1)

    def load_thread():
        computer = MissionComputer()
        while not stop_evt.is_set():
            print('\n[THREAD-LOAD] 부하 정보 업데이트')
            computer.get_mission_computer_load()
            for _ in range(200):  # 20초
                if stop_evt.is_set():
                    return
                time.sleep(0.1)

    def sensor_thread():
        computer = MissionComputer()
        while not stop_evt.is_set():
            computer.ds.set_env()
            computer.env_values = computer.ds.get_env()
            print('\n[THREAD-SENSOR] 센서 데이터 업데이트')
            print(json.dumps(computer.env_values, indent=2, ensure_ascii=False))
            for _ in range(50):  # 5초
                if stop_evt.is_set():
                    return
                time.sleep(0.1)

    threads = [
        threading.Thread(target=info_thread, daemon=True),
        threading.Thread(target=load_thread, daemon=True),
        threading.Thread(target=sensor_thread, daemon=True)
    ]

    for thread in threads:
        thread.start()

    try:
        while True:
            ready, _, _ = select.select([sys.stdin], [], [], 0.1)
            if ready:
                user_input = sys.stdin.readline().strip().lower()
                if user_input == 'q':
                    print('System stopped....')
                    break
    except KeyboardInterrupt:
        pass
    finally:
        stop_evt.set()
        for thread in threads:
            thread.join(timeout=1)
        print('[THREAD] 멀티스레드 종료 완료')


def run_multiprocessing():
    """멀티프로세스 모드 실행"""
    print('=== 멀티프로세스 모드 ===')
    print('종료하려면 q를 입력하세요.')

    manager = multiprocessing.Manager()
    stop_evt = manager.Event()

    processes = [
        multiprocessing.Process(target=process_info_worker, args=(stop_evt,), name='runComputer1'),
        multiprocessing.Process(target=process_load_worker, args=(stop_evt,), name='runComputer2'),
        multiprocessing.Process(target=process_sensor_worker, args=(stop_evt,), name='runComputer3')
    ]

    for process in processes:
        process.start()
        print(f'{process.name} 시작됨 (PID: {process.pid})')

    try:
        while True:
            ready, _, _ = select.select([sys.stdin], [], [], 0.1)
            if ready:
                user_input = sys.stdin.readline().strip().lower()
                if user_input == 'q':
                    print('System stopped....')
                    stop_evt.set()
                    break
    except KeyboardInterrupt:
        stop_evt.set()
    finally:
        for process in processes:
            process.join(timeout=2)
            if process.is_alive():
                process.terminate()
                process.join()
        print('[PROCESS] 멀티프로세스 종료 완료')


if __name__ == '__main__':
    print('=== 화성 미션 컴퓨터 시뮬레이션 ===')

    # 문제 1: DummySensor 테스트
    print('\n1. DummySensor 테스트')
    ds = DummySensor()
    ds.set_env()
    sensor_data = ds.get_env()
    print('DummySensor 테스트 완료:')
    print(json.dumps(sensor_data, indent=2, ensure_ascii=False))

    # 문제 3: 시스템 정보 테스트
    print('\n3. 시스템 정보 및 부하 테스트')
    runComputer = MissionComputer()
    runComputer.get_mission_computer_info()
    runComputer.get_mission_computer_load()

    print('\n실행 모드 선택:')
    print('1: 기본 모드 (센서 데이터 수집)')
    print('2: 멀티스레드 모드 (q 종료 가능)')
    print('3: 멀티프로세스 모드 (q 종료 가능)')

    try:
        choice = input('모드 선택 (1-3): ').strip()

        if choice == '1':
            # 문제 2: RunComputer 인스턴스의 get_sensor_data() 호출
            RunComputer = MissionComputer()
            RunComputer.get_sensor_data()
        elif choice == '2':
            run_multithreaded()
        elif choice == '3':
            run_multiprocessing()
        else:
            print('잘못된 선택입니다.')

    except KeyboardInterrupt:
        print('\n프로그램이 종료되었습니다.')
    except Exception as e:
        print(f'실행 중 오류: {e}')
