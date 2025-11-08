import csv
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
import pandas as pd

def main():
    # 1. 전복데이터의 성별을 데이터 -> label 에 저장
    labels = []
    with open('abalone.txt', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            labels.append(row[0])

    # 2. Sckit-Learn LabelEncoder 수행
    label_encoder = LabelEncoder()
    encoded_labels = label_encoder.fit_transform(labels)
    pd_encoded_labels = pd.DataFrame(encoded_labels)

    # 3. 라벨 인코딩 결과 확인
    print('라벨 인코딩 결과:')
    # print(encoded_labels[:10])
    print(pd_encoded_labels.describe())
    print("shape: ", pd_encoded_labels.shape)
    print(pd_encoded_labels)


    # 4. 원핫 엔코딩 진행
    # Reshape for OneHotEncoder
    encoded_labels_reshaped = encoded_labels.reshape(-1, 1)

    # Scikit-learn OneHotEncoder 사용
    one_hot_encoder = OneHotEncoder(sparse_output=False)
    one_hot_encoded = one_hot_encoder.fit_transform(encoded_labels_reshaped)
    pd_one_hot_encoded = pd.DataFrame(one_hot_encoded)

    # 5. 최종적 결과 확인
    print('\n원핫 인코딩 결과:')
    for i in range(10):
        print(f'{labels[i]}: {one_hot_encoded[i]}')

    print(pd_one_hot_encoded.describe())
    print("shape: ", pd_one_hot_encoded.shape)
    print(pd_one_hot_encoded.count())


if __name__ == '__main__':
    main()
