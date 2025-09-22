import random
import json
from datetime import datetime


class DummySensor:
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': 0.0,
            'mars_base_external_temperature': 0.0,
            'mars_base_internal_humidity': 0.0,
            'mars_base_external_illuminance': 0.0,
            'mars_base_internal_co2': 0.0,
            'mars_base_internal_oxygen': 0.0
        }

        # 단위 정보를 별도로 관리
        self.units = {
            'mars_base_internal_temperature': '°C',
            'mars_base_external_temperature': '°C',
            'mars_base_internal_humidity': '%',
            'mars_base_external_illuminance': 'W/m²',
            'mars_base_internal_co2': '%',
            'mars_base_internal_oxygen': '%'
        }

        # 한국어 필드명 매핑
        self.field_names_kr = {
            'mars_base_internal_temperature': '화성 기지 내부 온도',
            'mars_base_external_temperature': '화성 기지 외부 온도',
            'mars_base_internal_humidity': '화성 기지 내부 습도',
            'mars_base_external_illuminance': '화성 기지 외부 광량',
            'mars_base_internal_co2': '화성 기지 내부 이산화탄소 농도',
            'mars_base_internal_oxygen': '화성 기지 내부 산소 농도'
        }

    def set_env(self):
        """환경값을 지정된 범위 내에서 랜덤하게 설정"""
        try:
            self.env_values['mars_base_internal_temperature'] = round(random.uniform(18, 30), 2)
            self.env_values['mars_base_external_temperature'] = round(random.uniform(0, 21), 2)
            self.env_values['mars_base_internal_humidity'] = round(random.uniform(50, 60), 2)
            self.env_values['mars_base_external_illuminance'] = round(random.uniform(500, 715), 2)
            self.env_values['mars_base_internal_co2'] = round(random.uniform(0.02, 0.1), 4)
            self.env_values['mars_base_internal_oxygen'] = round(random.uniform(4, 7), 2)
        except Exception as e:
            print(f'환경값 설정 중 오류 발생: {e}')

    def get_env(self):
        """순수 숫자 데이터만 반환 (계산용)"""
        return self.env_values.copy()

    def get_env_with_units(self):
        """값과 단위를 함께 문자열로 반환 (표시용)"""
        try:
            result = {}
            for key, value in self.env_values.items():
                unit = self.units.get(key, '')
                result[key] = f'{value} {unit}'
            return result
        except Exception as e:
            print(f'단위 포함 환경값 조회 중 오류 발생: {e}')
            return {}

    def get_env_formatted(self):
        """한국어 필드명과 단위를 함께 표시 (사용자 친화적)"""
        try:
            result = {}
            for key, value in self.env_values.items():
                kr_name = self.field_names_kr.get(key, key)
                unit = self.units.get(key, '')
                result[kr_name] = f'{value} {unit}'
            return result
        except Exception as e:
            print(f'포맷된 환경값 조회 중 오류 발생: {e}')
            return {}

    def display_env(self):
        """환경 정보를 보기 좋게 출력"""
        print('=== 화성 기지 환경 정보 ===')
        for key, value in self.env_values.items():
            kr_name = self.field_names_kr.get(key, key)
            unit = self.units.get(key, '')
            print(f'{kr_name}: {value} {unit}')
        print('-' * 40)


# 테스트 코드
if __name__ == '__main__':
    ds = DummySensor()
    ds.set_env()

    print('1. 순수 숫자 데이터 (계산용):')
    print(json.dumps(ds.get_env(), indent=2))

    print('\n2. 단위 포함 데이터 (JSON):')
    print(json.dumps(ds.get_env_with_units(), indent=2, ensure_ascii=False))

    print('\n3. 한국어 + 단위:')
    print(json.dumps(ds.get_env_formatted(), indent=2, ensure_ascii=False))

    print('\n4. 포맷된 출력:')
    ds.display_env()
