import pandas as pd

ATTR_FILE = 'abalone_attributes.txt'
DATA_FILE = 'abalone.txt'


def load_attributes(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            attributes = [line.strip() for line in f.readlines()]
        return attributes
    except FileNotFoundError:
        raise FileNotFoundError('File open error.')
    except UnicodeDecodeError:
        raise UnicodeDecodeError('Decoding error.')

def load_data(path, columns):
    try:
        df = pd.read_csv(path, header=None, names=columns)
        return df
    except FileNotFoundError:
        raise FileNotFoundError('File open error.')
    except Exception as e:
        raise ValueError(f'Processing error: {e}')


def minmax_manual_scale(df):
    # scaled_df = df.copy()
    numeric_cols = df.select_dtypes(include='number').columns

    for col in numeric_cols:
        min_val = df[col].min()
        max_val = df[col].max()
        range_val = max_val - min_val

        if range_val == 0:
            df[col] = 0.0
        else:
            df[col] = (df[col] - min_val) / range_val
            
    return df

def main():
    try:
        # 1. 데이터 적재
        columns = load_attributes(ATTR_FILE)
        df = load_data(DATA_FILE, columns)
        
        # 요구사항 1: 원본 DataFrame 모양 출력
        print(df.shape)

        # 2. 라벨 분리
        df['label'] = df['Sex']
        df = df.drop(columns=['Sex'])

        # 요구사항 2: 라벨 분포 출력
        print(df['label'].value_counts().to_dict())

        # 3. Min-Max 스케일링
        data_to_scale = df.drop(columns=['label'])
        scaled_data = minmax_manual_scale(data_to_scale)
        
        # 요구사항 3: 스케일 결과의 상/하한 요약 출력
        print(scaled_data.describe().loc[['min', 'max']].round(6).to_dict())

    except (FileNotFoundError, UnicodeDecodeError) as e:
        print(e.args[0])
        return
    except (ValueError, Exception):
        print(f"Processing error.")
        return

# def test():
#     """요구사항 충족 여부를 검증하는 테스트 함수"""
#     print("\n" + "="*30)
#     print("   Running Verification Tests")
#     print("="*30 + "\n")
#
#     # 테스트 1: 데이터 적재 기능 검증
#     print("[Test 1] Data Loading Verification")
#     try:
#         columns = load_attributes(ATTR_FILE)
#         assert isinstance(columns, list) and len(columns) == 9
#         print("  - PASSED: `load_attributes` returns a list of 9 column names.")
#
#         df_orig = load_data(DATA_FILE, columns)
#         assert isinstance(df_orig, pd.DataFrame)
#         assert df_orig.shape[0] > 4000 and df_orig.shape[1] == 9
#         assert list(df_orig.columns) == columns
#         print(f"  - PASSED: `load_data` creates a DataFrame with shape {df_orig.shape} and correct columns.")
#     except Exception as e:
#         print(f"  - FAILED: Data loading test failed. {e}")
#         return
#
#     # 테스트 데이터 준비: main 함수와 동일하게 라벨 분리 수행
#     df = df_orig.copy()
#     df['label'] = df['Sex']
#     df = df.drop(columns=['Sex'])
#
#     # 테스트 2: 라벨 분리 기능 검증
#     print("\n[Test 2] Label Separation Verification")
#     assert 'label' in df.columns
#     assert 'Sex' not in df.columns
#     assert df.shape[1] == df_orig.shape[1]
#     print("  - PASSED: 'label' column created and 'Sex' column dropped successfully.")
#
#     # 테스트 3: Min-Max 스케일링 기능 검증
#     print("\n[Test 3] Min-Max Scaling Verification")
#     # 3-1: 일반 스케일링 테스트
#     test_df = pd.DataFrame({'A': [1, 2, 3, 4, 5], 'B': [10, 20, 30, 40, 50]})
#     scaled_test_df = minmax_manual_scale(test_df)
#     assert round(scaled_test_df['A'].min(), 6) == 0.0 and round(scaled_test_df['A'].max(), 6) == 1.0
#     assert round(scaled_test_df['B'].min(), 6) == 0.0 and round(scaled_test_df['B'].max(), 6) == 1.0
#     print("  - PASSED: Standard scaling works correctly (min=0.0, max=1.0).")
#
#     # 3-2: 상수열(분모=0) 처리 테스트
#     const_df = pd.DataFrame({'A': [5, 5, 5, 5], 'B': [1, 2, 3, 4]})
#     scaled_const_df = minmax_manual_scale(const_df)
#     assert all(scaled_const_df['A'] == 0.0)
#     print("  - PASSED: Constant column (denominator is zero) is correctly scaled to 0.0.")
#
#     # 테스트 4: 예외 처리 검증
#     print("\n[Test 4] Exception Handling Verification")
#     # 4-1: 파일 없음 예외
#     try:
#         load_attributes("non_existent_file.txt")
#     except FileNotFoundError as e:
#         assert e.args[0] == 'File open error.'
#         print("  - PASSED: `FileNotFoundError` is handled as 'File open error.'.")
#
#     # 테스트 5: 최종 출력 형식 검증 (main 함수 결과와 비교)
#     print("\n[Test 5] Final Output Format Verification")
#     print("  - INFO: Verifying the structure of outputs from main logic.")
#
#     # Shape (원본 데이터 기준)
#     shape_val = df_orig.shape
#     assert isinstance(shape_val, tuple) and len(shape_val) == 2
#     print(f"  - PASSED: Output 1 (shape) is a tuple: {shape_val}")
#
#     # Label distribution (라벨 분리된 데이터 기준)
#     label_dist = df['label'].value_counts().to_dict()
#     assert isinstance(label_dist, dict)
#     print(f"  - PASSED: Output 2 (label distribution) is a dict: {label_dist}")
#
#     # Scaled summary (라벨 분리된 데이터 기준)
#     scaled_summary = minmax_manual_scale(df.drop(columns=['label'])).describe().loc[['min', 'max']].round(6).to_dict()
#     assert isinstance(scaled_summary, dict)
#     for col, stats in scaled_summary.items():
#         assert 'min' in stats and 'max' in stats
#     print(f"  - PASSED: Output 3 (scaled summary) is a dict with 'min' and 'max'.")
#
#     print("\n" + "="*30)
#     print("   All Verification Tests Passed")
#     print("="*30)


if __name__ == "__main__":
    main()
    # test()
