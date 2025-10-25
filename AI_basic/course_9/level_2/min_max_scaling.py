import csv
import random


def load_data_from_files(data_file, attributes_file):
    try:
        with open(attributes_file, 'r', encoding='utf-8') as f:
            attributes = [line.strip() for line in f if line.strip()]

        data_rows = []
        with open(data_file, 'r', encoding='utf-8') as f:
            csv_reader = csv.reader(f)
            for row in csv_reader:
                if len(row) != len(attributes):
                    continue

                row_dict = {}
                for i, attr in enumerate(attributes):
                    if attr == 'Sex':
                        row_dict[attr] = row[i]
                    else:
                        row_dict[attr] = float(row[i])
                data_rows.append(row_dict)

        return data_rows
    except FileNotFoundError as e:
        print(f'파일을 찾을 수 없습니다: {e}')
        return []
    except Exception as e:
        print(f'데이터 로딩 중 오류 발생: {e}')
        return []


def manual_min_max_scaling(data_rows, exclude_columns=None):
    if not data_rows:
        return []

    if exclude_columns is None:
        exclude_columns = []

    numeric_columns = [
        col for col in data_rows[0].keys()
        if col not in exclude_columns and isinstance(data_rows[0][col], (int, float))
    ]

    min_max_dict = {}
    for col in numeric_columns:
        values = [row[col] for row in data_rows]
        min_val = min(values)
        max_val = max(values)
        min_max_dict[col] = {'min': min_val, 'max': max_val}

    scaled_data = []
    for row in data_rows:
        new_row = {}
        for col, value in row.items():
            if col in numeric_columns:
                min_val = min_max_dict[col]['min']
                max_val = min_max_dict[col]['max']

                if max_val == min_val:
                    new_row[col] = 0.0
                else:
                    new_row[col] = (value - min_val) / (max_val - min_val)
            else:
                new_row[col] = value
        scaled_data.append(new_row)

    return scaled_data


class MinMaxScaler:

    def __init__(self):
        self.min_values = {}
        self.max_values = {}
        self.numeric_columns = []

    def fit(self, data_rows, exclude_columns=None):
        if not data_rows:
            return self

        if exclude_columns is None:
            exclude_columns = []

        self.numeric_columns = [
            col for col in data_rows[0].keys()
            if col not in exclude_columns and isinstance(data_rows[0][col], (int, float))
        ]

        for col in self.numeric_columns:
            values = [row[col] for row in data_rows]
            self.min_values[col] = min(values)
            self.max_values[col] = max(values)

        return self

    def transform(self, data_rows):
        if not self.min_values:
            raise ValueError('fit() 메서드를 먼저 호출해야 합니다.')

        scaled_data = []
        for row in data_rows:
            new_row = {}
            for col, value in row.items():
                if col in self.numeric_columns:
                    min_val = self.min_values[col]
                    max_val = self.max_values[col]

                    if max_val == min_val:
                        new_row[col] = 0.0
                    else:
                        new_row[col] = (value - min_val) / (max_val - min_val)
                else:
                    new_row[col] = value
            scaled_data.append(new_row)

        return scaled_data

    def fit_transform(self, data_rows, exclude_columns=None):
        self.fit(data_rows, exclude_columns)
        return self.transform(data_rows)


def main():
    print('\n[단계 1] 데이터 로딩')
    data = load_data_from_files('abalone.txt', 'abalone_attributes.txt')
    print(f'총 {len(data)}개의 데이터 로드 완료')
    # print(f'첫 번째 데이터 샘플: {data[0]}')

    print('\n[단계 2] Sex 컬럼 분리')
    labels = [row['Sex'] for row in data]

    data_without_sex = []
    for row in data:
        new_row = {k: v for k, v in row.items() if k != 'Sex'}
        data_without_sex.append(new_row)

    print(f'레이블 개수: {len(labels)}')
    print(f'레이블 분포: M={labels.count("M")}, F={labels.count("F")}, I={labels.count("I")}')
    print(f'Sex 제거 후 첫 번째 데이터: {data_without_sex[0]}')

    print('\n[단계 3] 원본 데이터 통계 (스케일링 전)')
    print(f'{"컬럼명":<20} {"최소값":>12} {"최대값":>12} {"범위":>12}')
    print('-' * 80)
    for col in data_without_sex[0].keys():
        values = [row[col] for row in data_without_sex]
        min_val = min(values)
        max_val = max(values)
        print(f'{col:<20} {min_val:>12.4f} {max_val:>12.4f} {max_val - min_val:>12.4f}')

    print('\n[단계 4] 방법 1 - 수식 직접 구현')
    scaled_manual = manual_min_max_scaling(data_without_sex)
    print('스케일링 완료')
    print(f'첫 번째 스케일링된 데이터: {scaled_manual[0]}')

    print('\n[단계 5] 방법 2 - MinMaxScaler 클래스 사용')
    scaler = MinMaxScaler()
    scaled_class = scaler.fit_transform(data_without_sex)
    print('스케일링 완료')
    print(f'첫 번째 스케일링된 데이터: {scaled_class[0]}')

    print('\n[단계 6] 스케일링 후 데이터 통계')
    print(f'{"컬럼명":<20} {"최소값":>12} {"최대값":>12}')
    print('-' * 80)
    for col in scaled_manual[0].keys():
        values = [row[col] for row in scaled_manual]
        min_val = min(values)
        max_val = max(values)
        print(f'{col:<20} {min_val:>12.6f} {max_val:>12.6f}')

    print('\n[단계 7] 두 방법의 결과 비교')
    is_same = True
    for i in range(len(scaled_manual)):
        for col in scaled_manual[i].keys():
            diff = abs(scaled_manual[i][col] - scaled_class[i][col])
            if diff > 1e-10:
                is_same = False
                break
        if not is_same:
            break

    print(f'두 방법의 결과 일치 여부: {is_same}')
    print('\n요구사항 1 완료\n')

    return scaled_manual, labels


if __name__ == '__main__':
    main()
