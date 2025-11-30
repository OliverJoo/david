import threading
import time
import random
from datetime import datetime


class FarmSensor:

    def __init__(self, sensor_name):
        self.sensor_name = sensor_name
        self.temperature = 0
        self.illuminance = 0
        self.humidity = 0

    def set_data(self):
        self.temperature = random.randint(20, 30)
        self.illuminance = random.randint(5000, 10000)
        self.humidity = random.randint(40, 70)

    def get_data(self):
        return (self.temperature, self.illuminance, self.humidity)


def sensor_worker(sensor):
    try:
        while True:
            sensor.set_data()
            temp, light, humi = sensor.get_data()
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f'{timestamp} {sensor.sensor_name} -- temp {temp:02d}, '
                  f'light {light:04d}, humi {humi:02d}')
            time.sleep(10)
    except KeyboardInterrupt:
        pass


def main():
    sensors = [FarmSensor(f'Farm-{i}') for i in range(1, 6)]

    threads = []
    for sensor in sensors:
        thread = threading.Thread(target=sensor_worker, args=(sensor,))
        thread.daemon = True
        threads.append(thread)

    for thread in threads:
        thread.start()

    print('스마트 팜 센서 모니터링 시작 (Ctrl+C로 종료)')

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print('\n모니터링 종료')


if __name__ == '__main__':
    main()
