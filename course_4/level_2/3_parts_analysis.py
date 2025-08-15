import os
from typing import Tuple

import numpy as np

DATA_DIR = 'data_source'
RESULT_DIR = 'result'

SRC_FILES = [
    os.path.join(DATA_DIR, 'mars_base_main_parts-001.csv'),
    os.path.join(DATA_DIR, 'mars_base_main_parts-002.csv'),
    os.path.join(DATA_DIR, 'mars_base_main_parts-003.csv'),
]
OUT_FILE = os.path.join(RESULT_DIR, 'parts_to_work_on.csv')


def ensure_dir(path: str) -> None:
    try:
        os.makedirs(path, exist_ok=True)
    except OSError as e:
        print(f'[에러] 디렉터리 생성 실패({path}): {e}')


def load_csv_as_ndarray(path: str) -> np.ndarray:
    """CSV를 숫자 ndarray로 로드.
    - BOM/헤더/문자열 섞임 허용, 비정상 값은 NaN으로 수용
    - 전부 NaN인 열/행 제거로 downstream 경고 방지
    - 빈/헤더만 있는 파일은 (0,0) 반환
    """
    if not os.path.exists(path):
        print(f'[경고] 파일이 존재하지 않습니다: {path}')
        return np.empty((0, 0), dtype=float)

    try:
        arr = np.genfromtxt(
            path,
            delimiter=',',
            dtype=float,
            autostrip=True,
            encoding='utf-8-sig'
        )

        # 2D 보장
        if arr.ndim == 1:
            arr = arr.reshape(1, -1) if arr.size > 0 else np.empty((0, 0), dtype=float)

        if arr.size == 0:
            return np.empty((0, 0), dtype=float)

        # 전부 NaN인 열 제거
        try:
            col_all_nan = np.isnan(arr).all(axis=0)
            # print(f'전부 NaN인 열 제거 :{col_all_nan} \n')
            if col_all_nan.any():
                arr = arr[:, ~col_all_nan]
        except Exception:
            # NaN 검사 중 문제 시 원본 유지
            pass

        # 전부 NaN인 행 제거
        try:
            if arr.size > 0 and arr.shape[1] > 0:
                row_all_nan = np.isnan(arr).all(axis=1)
                # print(f'전부 NaN인 행 제거 :{row_all_nan} \n')
                if row_all_nan.any():
                    arr = arr[~row_all_nan]
        except Exception:
            pass

        # 요소, 행, 열의 각각의 개수가 0 인지 체크
        if arr.size == 0 or arr.shape[1] == 0 or arr.shape[0] == 0:
            return np.empty((0, 0), dtype=float)

        return arr

    except Exception as e:
        print(f'[에러] CSV 로드 실패({path}): {e}')
        return np.empty((0, 0), dtype=float)


def merge_arrays(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """두 배열을 세로 방향으로 병합.
    - 서로 다른 열 수는 최소 공통 열로 자른 후 병합
    - 공통 열이 0이면 (0,0) 반환
    """
    if a.size == 0:
        return b
    if b.size == 0:
        return a

    cols_a = a.shape[1]
    cols_b = b.shape[1]
    min_cols = min(cols_a, cols_b)

    if min_cols == 0:
        # print(f'[경고] 병합 불가: 공통 열이 0개입니다. a={a.shape}, b={b.shape}')
        return np.empty((0, 0), dtype=float)

    if cols_a != cols_b:
        # print(f'[정보] 열 수 불일치: {cols_a} vs {cols_b} → {min_cols}열로 정렬')
        a = a[:, :min_cols]
        b = b[:, :min_cols]

    try:
        return np.vstack([a, b])
    except Exception as e:
        print(f'[에러] 배열 병합 실패: {e}')
        return np.empty((0, 0), dtype=float)


def compute_column_means(parts: np.ndarray) -> np.ndarray:
    """열 평균 계산. 비었거나 모두 NaN이면 빈 배열 반환."""
    if parts.size == 0:
        return np.array([], dtype=float)
    if np.isnan(parts).all():
        return np.array([], dtype=float)
    # print(f'np shape : {np.shape(parts)}')
    return np.nanmean(parts, axis=0)


def filter_rows_by_mean(parts: np.ndarray, threshold: float = 50.0) -> np.ndarray:
    """행 평균 < threshold인 행만 필터링.
    - 비었거나 전부 NaN이면 빈 (0,0) 반환
    - Mean of empty slice 경고 방지를 위해 사전 가드
    """
    if parts.size == 0:
        return np.empty((0, 0), dtype=float)
    if np.isnan(parts).all():
        print('[경고] 모든 값이 NaN입니다. 필터링 결과는 빈 배열입니다.')
        return np.empty((0, 0), dtype=float)

    try:
        row_means = np.nanmean(parts, axis=1)
    except RuntimeWarning:
        # 방어: 경고 상황에서도 빈 결과 반환
        return np.empty((0, 0), dtype=float)

    if row_means.size == 0:
        return np.empty((0, 0), dtype=float)

    mask = row_means < threshold
    try:
        filtered = parts[mask]
    except Exception:
        filtered = np.empty((0, 0), dtype=float)

    if filtered.size == 0:
        return np.empty((0, 0), dtype=float)

    return filtered


def save_csv_safely(arr: np.ndarray, path: str) -> bool:
    """CSV 저장. 빈 배열이면 빈 파일로 저장."""
    ensure_dir(os.path.dirname(path))
    try:
        if arr.size == 0:
            # 빈 파일 생성
            with open(path, 'w', encoding='utf-8') as f:
                f.write('')
            print(f'[정보] 비어있는 결과를 저장했습니다: {path}')
            return True
        np.savetxt(path, arr, delimiter=',', fmt='%.3f')
        print(f'[정보] 저장 완료: {path}')
        return True
    except (IOError, OSError) as e:
        print(f'[에러] 파일 저장에 실패했습니다({path}): {e}')
    except Exception as e:
        print(f'[에러] 저장 실패({path}): {e}')
        return False


def reload_and_transpose(path: str) -> Tuple[np.ndarray, np.ndarray]:
    parts2 = load_csv_as_ndarray(path)
    parts3 = parts2.T if parts2.size > 0 else parts2
    return parts2, parts3


def main() -> None:
    print('[Mars 부품 데이터 통합 분석]')
    arrs = [load_csv_as_ndarray(p) for p in SRC_FILES]

    parts = np.empty((0, 0), dtype=float)
    for a in arrs:
        parts = merge_arrays(parts, a)

    if parts.size == 0 or parts.shape[0] == 0 or parts.shape[1] == 0:
        print(f'[경고] 유효한 데이터가 없어 종료합니다. parts shape={parts.shape}')
        # 그래도 비어있는 결과 파일은 생성
        save_csv_safely(np.empty((0, 0), dtype=float), OUT_FILE)
        return

    col_means = compute_column_means(parts)
    if col_means.size > 0:
        print(f'열 평균(소수점 3자리): {np.array2string(col_means, precision=3)}')
    else:
        print('[정보] 열 평균 계산 불가(데이터 없음 또는 모두 NaN)')

    # 요구사항: 행 평균 < 50인 항목 저장
    parts_to_work = filter_rows_by_mean(parts, 50.0)
    if parts_to_work.size == 0:
        print('[정보] 작업 대상 행이 없습니다(모든 행 평균≥50이거나 유효 데이터 없음).')

    save_csv_safely(parts_to_work, OUT_FILE)

    # 보너스: 재로딩 후 전치
    parts2, parts3 = reload_and_transpose(OUT_FILE)
    if parts2.size > 0:
        print('--- parts2 (재로딩 출력) ---')
        print(np.array2string(parts2, precision=3))
        print('--- parts3 (전치 행렬) ---')
        print(np.array2string(parts3, precision=3))
        print()
        print(f'last : {parts2}')

if __name__ == '__main__':
    main()
