from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import numpy as np

def data_check():
    iris = load_iris()
    X = iris.data
    y = iris.target
    print(f'=== DataSet-X ===\n{X[:5]}')
    print(f'=== DataSet-y ===\n{y}')
    print(f'=== DataSet-DESCR ===\n{iris.DESCR}')
    print(f'=== DataSet-target_name ===\n{iris.target_names}\n')
    print(f'=== DataSet-feature_names ===\n{iris.feature_names}\n')
    print(f'=== DataSet-data ===\n{iris.data[:5]}\n')
    print(f'=== DataSet-data(shape) ===\n{iris.data.shape}\n')
    print(f'=== DataSet-data(ndim) ===\n{iris.data.ndim}\n')
    print(f'=== DataSet-data(type) ===\n{type(iris.data)}\n')
    print(f'=== DataSet-data(sample) ===\n{iris.data[:5]}\n')


def main():
    iris = load_iris()
    X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, random_state=0)

    print(f"X_train 크기: {X_train.shape} | y_train 크기: {y_train.shape}")
    print(f"X_test 크기: {X_test.shape} | y_test 크기: {y_test.shape}")

    knn = KNeighborsClassifier(n_neighbors=1)
    knn.fit(X_train, y_train)

    X_new = np.array([[5, 2.9, 1, 0.2]])
    prediction = knn.predict(X_new)
    print(f"새로운 데이터의 예측: {iris.target_names[prediction]}")

    print(f"훈련 세트 정확도: {knn.score(X_train, y_train):.3f}")
    print(f"테스트 세트 정확도: {knn.score(X_test, y_test):.3f}")



if __name__ == '__main__':
    data_check()
    main()
