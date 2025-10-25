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
    except Exception as e:
        print(f'데이터 로딩 중 오류 발생: {e}')
        return []


def separate_data_and_labels(data_rows):
    labels = [row['Sex'] for row in data_rows]
    data = []
    for row in data_rows:
        new_row = {k: v for k, v in row.items() if k != 'Sex'}
        data.append(new_row)

    return data, labels


def split_by_class(data, labels):
    class_data = {}
    for i, (row, label) in enumerate(zip(data, labels)):
        if label not in class_data:
            class_data[label] = []
        class_data[label].append((row, i))

    return class_data


# ==================== Random Over Sampling ====================
def random_over_sampling(data, labels):
    class_data = split_by_class(data, labels)

    class_counts = {label: len(samples) for label, samples in class_data.items()}
    max_count = max(class_counts.values())

    print(f'원본 클래스 분포: {class_counts}')
    print(f'목표 샘플 수 (최대값): {max_count}')

    resampled_data = []
    resampled_labels = []

    for label, samples in class_data.items():
        for row, original_idx in samples:
            resampled_data.append(row)
            resampled_labels.append(label)

        current_count = len(samples)
        samples_needed = max_count - current_count

        if samples_needed > 0:
            additional_samples = random.choices(samples, k=samples_needed)
            for row, original_idx in additional_samples:
                resampled_data.append(row)
                resampled_labels.append(label)

    return resampled_data, resampled_labels


# ==================== Random Under Sampling ====================
def random_under_sampling(data, labels):
    class_data = split_by_class(data, labels)

    class_counts = {label: len(samples) for label, samples in class_data.items()}
    min_count = min(class_counts.values())

    print(f'원본 클래스 분포: {class_counts}')
    print(f'목표 샘플 수 (최소값): {min_count}')

    resampled_data = []
    resampled_labels = []

    for label, samples in class_data.items():
        selected_samples = random.sample(samples, min_count)

        for row, original_idx in selected_samples:
            resampled_data.append(row)
            resampled_labels.append(label)

    return resampled_data, resampled_labels


def print_class_distribution(labels, title):
    class_counts = {}
    for label in labels:
        class_counts[label] = class_counts.get(label, 0) + 1

    print(f'\n{title}')
    print('-' * 40)
    total = len(labels)
    for label in sorted(class_counts.keys()):
        count = class_counts[label]
        percentage = (count / total) * 100
        print(f'{label}: {count:>5}개 ({percentage:>5.2f}%)')
    print(f'{"총계"}: {total:>5}개')


def main():
    print('요구사항 2: 데이터 전처리 Sampling')
    print('=' * 80)

    print('\n[단계 1] 데이터 로딩')
    raw_data = load_data_from_files('abalone.txt', 'abalone_attributes.txt')
    print(f'총 {len(raw_data)}개의 데이터 로드 완료')

    print('\n[단계 2] 데이터와 레이블 분리')
    data, labels = separate_data_and_labels(raw_data)
    print(f'데이터: {len(data)}개')
    print(f'레이블: {len(labels)}개')
    print_class_distribution(labels, '원본 클래스 분포')

    print('\n' + '=' * 80)
    print('[단계 3] Random Over Sampling 수행')
    print('=' * 80)
    oversampled_data, oversampled_labels = random_over_sampling(data, labels)
    print(f'\nOver Sampling 후 총 샘플 수: {len(oversampled_data)}')
    print_class_distribution(oversampled_labels, 'Over Sampling 후 클래스 분포')

    print('\n첫 3개 Over Sampled 데이터:')
    for i in range(min(3, len(oversampled_data))):
        print(f'{i + 1}. Label={oversampled_labels[i]}, Data={oversampled_data[i]}')

    print('\n' + '=' * 80)
    print('[단계 4] Random Under Sampling 수행')
    print('=' * 80)
    undersampled_data, undersampled_labels = random_under_sampling(data, labels)
    print(f'\nUnder Sampling 후 총 샘플 수: {len(undersampled_data)}')
    print_class_distribution(undersampled_labels, 'Under Sampling 후 클래스 분포')

    print('\n첫 3개 Under Sampled 데이터:')
    for i in range(min(3, len(undersampled_data))):
        print(f'{i + 1}. Label={undersampled_labels[i]}, Data={undersampled_data[i]}')

    return oversampled_data, oversampled_labels, undersampled_data, undersampled_labels


if __name__ == '__main__':
    # random seed 설정 (재현성을 위해)
    random.seed(42)
    main()
