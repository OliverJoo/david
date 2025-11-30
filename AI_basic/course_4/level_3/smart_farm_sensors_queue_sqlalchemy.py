import threading
import time
import random
from datetime import datetime, timedelta
from queue import Queue, Empty
from typing import Dict, List, Tuple
from contextlib import contextmanager

from sqlalchemy import func
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from database import db_config, ParmData

import platform
from matplotlib import font_manager, rc

# ====== 전역 상수 ======
SENSOR_COUNT = 5
SENSOR_INTERVAL = 10  # 센서 데이터 생성 주기 (초)
QUEUE_CHECK_INTERVAL = 1  # Queue 확인 주기 (초)
QUEUE_MAX_SIZE = 50  # Queue 최대 크기 (메모리 제한)

# ====== 전역 Queue (FIFO) ======
sensor_queue = Queue(maxsize=QUEUE_MAX_SIZE)


def configure_korean_font():
    '''
    OS별 Matplotlib 한글 폰트 설정

    이유:
    Matplotlib 기본 폰트(DejaVu Sans)는 한글을 지원하지 않아 깨짐 현상 발생.
    OS를 감지하여 시스템 기본 한글 폰트로 교체함.
    '''
    system_name = platform.system()

    try:
        if system_name == 'Windows':
            # 윈도우 기본 한글 폰트
            rc('font', family='Malgun Gothic')
        elif system_name == 'Darwin':
            # 맥OS 기본 한글 폰트
            rc('font', family='AppleGothic')
        else:
            # 리눅스 (Docker 등)
            # 주의: apt-get install fonts-nanum 등으로 설치되어 있어야 함
            rc('font', family='NanumGothic')

        # 한글 폰트 사용 시 마이너스(-) 기호가 깨지는 문제 해결
        rc('axes', unicode_minus=False)
        print(f'[System] 한글 폰트 설정 완료 ({system_name})')

    except Exception as e:
        print(f'[Warning] 폰트 설정 실패: {e}')
        print('그래프의 한글이 깨질 수 있습니다.')


class FarmSensor:

    def __init__(self, sensor_name: str):
        self.sensor_name = sensor_name
        self.temperature = 0
        self.illuminance = 0
        self.humidity = 0

    def set_data(self) -> None:
        self.temperature = random.randint(20, 30)
        self.illuminance = random.randint(5000, 10000)
        self.humidity = random.randint(40, 70)

    def get_data(self) -> Tuple[int, int, int]:
        return (self.temperature, self.illuminance, self.humidity)


@contextmanager
def get_db_session():
    session = db_config.get_session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()


def insert_sensor_data(sensor_name: str, input_time: datetime,
                       temperature: int, illuminance: int,
                       humidity: int) -> int | None:
    try:
        with get_db_session() as session:
            sensor_data = ParmData(
                sensor_name=sensor_name,
                input_time=input_time,
                temperature=temperature,
                illuminance=illuminance,
                humidity=humidity
            )
            session.add(sensor_data)
            session.flush()
            data_id = sensor_data.data_id

            return data_id

    except Exception as e:
        print(f'DB 삽입 오류 ({sensor_name}): {e}')
        return None


def get_sensor_data(sensor_name: str | None = None,
                    start_time: datetime | None = None,
                    end_time: datetime | None = None) -> List[ParmData]:
    try:
        with get_db_session() as session:
            query = session.query(ParmData)

            if sensor_name:
                query = query.filter(ParmData.sensor_name == sensor_name)
            if start_time:
                query = query.filter(ParmData.input_time >= start_time)
            if end_time:
                query = query.filter(ParmData.input_time <= end_time)

            results = query.order_by(ParmData.input_time.asc()).all()

            for result in results:
                session.expunge(result)

            return results

    except Exception as e:
        print(f'데이터 조회 오류: {e}')
        return []


def get_hourly_average_temperature() -> Dict[str, Dict[datetime, float]]:
    try:
        with get_db_session() as session:
            # MariaDB의 DATE_FORMAT 함수로 시간별 그룹화
            query = session.query(
                ParmData.sensor_name,
                func.date_format(
                    ParmData.input_time,
                    '%Y-%m-%d %H:00:00'
                ).label('hour'),
                func.avg(ParmData.temperature).label('avg_temp')
            ).group_by(
                ParmData.sensor_name,
                func.date_format(ParmData.input_time, '%Y-%m-%d %H:00:00')
            ).order_by(
                ParmData.sensor_name,
                'hour'
            )

            results = query.all()

            data_dict = {}
            for sensor_name, hour_str, avg_temp in results:
                if sensor_name not in data_dict:
                    data_dict[sensor_name] = {}

                hour_dt = datetime.strptime(hour_str, '%Y-%m-%d %H:%M:%S')
                data_dict[sensor_name][hour_dt] = float(avg_temp)

            return data_dict

    except Exception as e:
        print(f'시간별 평균 조회 오류: {e}')
        return {}


def plot_temperature_graph(save_path: str = 'temperature_graph.png') -> None:
    configure_korean_font()  # 한글 폰트 설정 호출

    # 데이터 조회
    data_dict = get_hourly_average_temperature()

    if not data_dict:
        print('그래프 생성 실패: 데이터가 없습니다')
        return

    plt.figure(figsize=(14, 7))

    for sensor_name, hour_temps in data_dict.items():
        hours = sorted(hour_temps.keys())
        temps = [hour_temps[h] for h in hours]

        plt.plot(hours, temps, marker='o', label=sensor_name, linewidth=2)

    plt.title('센서별 시간별 평균 온도', fontsize=16, fontweight='bold')
    plt.xlabel('시간 (시)', fontsize=12)
    plt.ylabel('평균 온도 (°C)', fontsize=12)
    plt.legend(loc='best', fontsize=10)
    plt.grid(True, alpha=0.3)

    ax = plt.gca()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
    plt.xticks(rotation=45, ha='right')

    plt.ylim(19, 31)

    plt.tight_layout()

    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    print(f'그래프 저장 완료: {save_path}')

    plt.show()

    plt.close()


def sensor_producer(sensor: FarmSensor) -> None:
    try:
        while True:
            sensor.set_data()
            temp, light, humi = sensor.get_data()
            timestamp = datetime.now()

            timestamp_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')
            print(f'{timestamp_str} {sensor.sensor_name} -- '
                  f'temp {temp:02d}, light {light:04d}, humi {humi:02d}')

            # Queue에 데이터 추가 (FIFO)
            sensor_data = {
                'sensor_name': sensor.sensor_name,
                'input_time': timestamp,
                'temperature': temp,
                'illuminance': light,
                'humidity': humi
            }

            try:
                # Queue가 가득 차면 최대 5초 대기
                sensor_queue.put(sensor_data, block=True, timeout=5)
                print(f'  → Queue 저장 완료 (크기: {sensor_queue.qsize()})')
            except Exception as e:
                print(f'  → Queue 저장 실패: {e}')

            time.sleep(SENSOR_INTERVAL)

    except KeyboardInterrupt:
        pass
    finally:
        db_config.remove_session()


def db_consumer() -> None:
    try:
        while True:
            try:
                # Queue에서 데이터 가져오기 (타임아웃 1초)
                sensor_data = sensor_queue.get(block=True, timeout=QUEUE_CHECK_INTERVAL)

                # DB에 저장
                data_id = insert_sensor_data(
                    sensor_name=sensor_data['sensor_name'],
                    input_time=sensor_data['input_time'],
                    temperature=sensor_data['temperature'],
                    illuminance=sensor_data['illuminance'],
                    humidity=sensor_data['humidity']
                )

                if data_id:
                    print(f'[DB Writer] {sensor_data["sensor_name"]} 데이터 '
                          f'DB 저장 완료 (ID: {data_id}, Queue 남은 개수: {sensor_queue.qsize()})')
                else:
                    print(f'[DB Writer] {sensor_data["sensor_name"]} DB 저장 실패')

                sensor_queue.task_done()

            except Empty:
                pass

    except KeyboardInterrupt:
        pass
    finally:
        print('\n[DB Writer] 남은 Queue 데이터 처리 중...')
        while not sensor_queue.empty():
            try:
                sensor_data = sensor_queue.get_nowait()
                insert_sensor_data(
                    sensor_name=sensor_data['sensor_name'],
                    input_time=sensor_data['input_time'],
                    temperature=sensor_data['temperature'],
                    illuminance=sensor_data['illuminance'],
                    humidity=sensor_data['humidity']
                )
                sensor_queue.task_done()
            except Empty:
                break

        print('[DB Writer] Queue 처리 완료')
        db_config.remove_session()


def main() -> None:
    print('=== 스마트 팜 센서 모니터링 시스템 (Queue + SQLAlchemy) ===')

    try:
        db_config.create_tables()
    except Exception as e:
        print(f'테이블 생성 실패: {e}')
        return

    sensors = [FarmSensor(f'Farm-{i}') for i in range(1, SENSOR_COUNT + 1)]

    producer_threads = []
    for sensor in sensors:
        thread = threading.Thread(
            target=sensor_producer,
            args=(sensor,),
            name=f'Producer-{sensor.sensor_name}',
            daemon=True
        )
        producer_threads.append(thread)

    consumer_thread = threading.Thread(
        target=db_consumer,
        name='Consumer-DBWriter',
        daemon=True
    )
    for thread in producer_threads:
        thread.start()

    consumer_thread.start()

    print(f'모니터링 시작 (센서: {SENSOR_COUNT}개, Queue 크기: {QUEUE_MAX_SIZE})')
    print('Ctrl+C로 종료\n')

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print('\n\n모니터링 종료 요청')

        print('Queue 처리 대기 중...')
        sensor_queue.join()

        print('그래프 생성 중...')
        plot_temperature_graph()

    finally:
        db_config.dispose_engine()
        print('프로그램 종료')


if __name__ == '__main__':
    main()
