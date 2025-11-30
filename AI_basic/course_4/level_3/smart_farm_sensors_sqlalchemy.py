import threading
import time
import random
from datetime import datetime
from contextlib import contextmanager

from database import db_config, ParmData


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

    def get_data(self) -> tuple[int, int, int]:
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
            # ORM 모델 인스턴스 생성
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


def sensor_worker(sensor: FarmSensor) -> None:
    try:
        while True:
            # 센서 데이터 생성
            sensor.set_data()
            temp, light, humi = sensor.get_data()
            timestamp = datetime.now()

            # 화면 출력
            timestamp_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')
            print(f'{timestamp_str} {sensor.sensor_name} -- '
                  f'temp {temp:02d}, light {light:04d}, humi {humi:02d}')

            # DB 저장
            data_id = insert_sensor_data(
                sensor_name=sensor.sensor_name,
                input_time=timestamp,
                temperature=temp,
                illuminance=light,
                humidity=humi
            )

            if data_id:
                print(f'  → DB 저장 완료 (ID: {data_id})')
            else:
                print(f'  → DB 저장 실패')

            time.sleep(10)

    except KeyboardInterrupt:
        pass
    finally:
        db_config.remove_session()


def main() -> None:
    print('=== 스마트 팜 센서 모니터링 시스템 (SQLAlchemy) ===')

    # 1. 데이터베이스 테이블 생성
    try:
        db_config.create_tables()
    except Exception as e:
        print(f'테이블 생성 실패: {e}')
        return

    sensors = [FarmSensor(f'Farm-{i}') for i in range(1, 6)]

    threads = []
    for sensor in sensors:
        thread = threading.Thread(
            target=sensor_worker,
            args=(sensor,),
            name=f'Thread-{sensor.sensor_name}'  # 디버깅용 스레드 이름
        )
        thread.daemon = True
        threads.append(thread)

    for thread in threads:
        thread.start()

    print('모니터링 시작 (Ctrl+C로 종료)\n')

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print('\n\n모니터링 종료')
    finally:
        db_config.dispose_engine()


if __name__ == '__main__':
    main()