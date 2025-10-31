import numpy as np
from sklearn import datasets
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


def load_digits_dataset():
    digits = datasets.load_digits()
    data = digits.data
    labels = digits.target
    description = digits.DESCR

    return data, labels, description


def display_sample_images(data, num_samples=5):
    print(f'\n{"=" * 60}')
    print(f'샘플 이미지 출력 (8x8, {num_samples}개)')
    print(f'{"=" * 60}\n')

    for i in range(min(num_samples, len(data))):
        image_8x8 = data[i].reshape(8, 8)
        print(f'샘플 #{i + 1}:')
        print(image_8x8)
        print()


def standardize_data(data):
    mean = np.mean(data, axis=0)
    std = np.std(data, axis=0)

    std_safe = np.where(std == 0, 1.0, std)

    standardized_data = (data - mean) / std_safe

    return standardized_data, mean, std


def compute_pca(data, num_components=2):
    standardized_data, mean, std = standardize_data(data)

    covariance_matrix = np.cov(standardized_data, rowvar=False)

    eigenvalues, eigenvectors = np.linalg.eigh(covariance_matrix)

    sorted_indices = np.argsort(eigenvalues)[::-1]
    sorted_eigenvalues = eigenvalues[sorted_indices]
    sorted_eigenvectors = eigenvectors[:, sorted_indices]

    principal_components = sorted_eigenvectors[:, :num_components]

    transformed_data = np.dot(standardized_data, principal_components)

    total_variance = np.sum(sorted_eigenvalues)
    explained_variance_ratio = sorted_eigenvalues[:num_components] / total_variance

    return transformed_data, principal_components, explained_variance_ratio


def compute_pca_sklearn(data, num_components=2):
    scaler = StandardScaler()
    standardized_data = scaler.fit_transform(data)

    pca = PCA(n_components=num_components)
    transformed_data = pca.fit_transform(standardized_data)

    principal_components = pca.components_.T
    explained_variance_ratio = pca.explained_variance_ratio_

    return transformed_data, principal_components, explained_variance_ratio


def main():
    print('sklearn digits 데이터셋 PCA 분석')
    print('=' * 60)

    data, labels, description = load_digits_dataset()

    print('\n[데이터셋 설명 (DESCR)]')
    print('-' * 60)
    print(description)
    print('-' * 60)

    print(f'\n[데이터 기본 정보]')
    print(f'데이터 shape: {data.shape}')
    print(f'레이블 shape: {labels.shape}')
    print(f'데이터 타입: {data.dtype}')
    print(f'레이블 범위: {labels.min()} ~ {labels.max()}')

    display_sample_images(data, num_samples=3)

    print('\n[직접 구현한 PCA 수행: 64차원 → 2차원]')
    print('-' * 60)

    num_components = 2
    # transformed_data, principal_components, explained_variance_ratio = compute_pca(data, num_components=num_components)
    #
    # print(f'변환된 데이터 shape: {transformed_data.shape}')
    # print(f'주성분 벡터 shape: {principal_components.shape}')
    # print(f'\n각 주성분의 설명된 분산 비율:')
    #
    # for i, ratio in enumerate(explained_variance_ratio, 1):
    #     print(f'  PC{i}: {ratio:.4f} ({ratio * 100:.2f}%)')
    #
    # cumulative_variance = np.cumsum(explained_variance_ratio)
    # print(f'\n누적 설명된 분산: {cumulative_variance[-1]:.4f} ({cumulative_variance[-1] * 100:.2f}%)')
    #
    #
    # print(f'\n[변환된 데이터 샘플 (처음 5개)]')
    # print('-' * 60)
    # print('원본 차원: 64 → 축소 차원: 2')
    # print(f'{"샘플 #":<10}{"PC1":<15}{"PC2":<15}{"레이블":<10}')
    # print('-' * 60)
    #
    # for i in range(5):
    #     print(f'{i + 1:<10}{transformed_data[i, 0]:<15.4f}{transformed_data[i, 1]:<15.4f}{labels[i]:<10}')

    # --- Scikit-learn을 사용한 PCA ---
    print('\n[sklearn 라이브러리 PCA 수행: 64차원 → 2차원]')
    print('-' * 60)

    transformed_data_sk, principal_components_sk, explained_variance_ratio_sk = compute_pca_sklearn(data, num_components=num_components)

    print(f'변환된 데이터 shape: {transformed_data_sk.shape}')
    print(f'주성분 벡터 shape: {principal_components_sk.shape}')
    print(f'\n각 주성분의 설명된 분산 비율:')

    for i, ratio in enumerate(explained_variance_ratio_sk, 1):
        print(f'  PC{i}: {ratio:.4f} ({ratio * 100:.2f}%)')

    cumulative_variance_sk = np.cumsum(explained_variance_ratio_sk)
    print(f'\n누적 설명된 분산: {cumulative_variance_sk[-1]:.4f} ({cumulative_variance_sk[-1] * 100:.2f}%)')

    print(f'\n[변환된 데이터 샘플 (처음 5개) - sklearn]')
    print(f'{"샘플 #":<10}{"PC1":<15}{"PC2":<15}{"레이블":<10}')
    print('-' * 60)
    for i in range(5):
        print(f'{i + 1:<10}{transformed_data_sk[i, 0]:<15.4f}{transformed_data_sk[i, 1]:<15.4f}{labels[i]:<10}')


if __name__ == '__main__':
    main()
