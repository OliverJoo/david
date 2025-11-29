# 문제 3. abalone_minmax

## 문제 설명
제공된 두 파일 abalone_attributes.ext, abalone.txt를 읽어 하나의 DataFrame으로 구성하시오. 전복은 유아기에 성별이 정해지지 않다가 성장하며 성별이 정해지는 특성이 있으므로, 'Sex' 컬럼을 별도 'label' 컬럼으로 분리한 뒤, 원본 'sex' 컬럼은 제거한다. 이후 label을 제외한 **모든 수치 컬럼**에 대해 Min-Max scaling을 *직접 수식 구현* 으로면 적용하시오.

file: 전복데이터.zip


## 요구사항: 다음을 모두 충족하는 프로그램을 작성하시오

### 데이터 적재
- 현재 작업 디렉터리의 abalone_attributes.txt에서 열 이름 목록을 읽어들인다. (행단위 텍스트 -> 리스트)
- 같은 디렉터리의 abalone.txt를 콤마 구분(,)으로 읽어, pandas.DataFrame을 생성하고, 앞서 읽은 열 이름을 컬럼명으로 적용합니다.

### 라벨 분리
- Sex 컬럼을 그대로 복사하여 label 컬럼을 만든다. (값 예: 'M', 'F', 'I')
- 원본 'Sex'컬럼은 제거한다(즉, 결과 테이블에는 label만 남김)

### Scaling 대상 / 방법
- label을 제외한 모든 수치 column에 대해 열별로 Min-max Scaling(직접수식)을 적용한다.

x' = max(x) - min(x)x - min(x)
수식: x' = x - min(x)max(x) = min(x)
x' = \frac{x-\min(x)}{\max(x)-\min(x)}
    - 분모가 0(상수열)인 경우, 해당 열은 0.0으로 채워줍니다.

### 출력 형식 (정확히 아래 순서로 print() 3회)
- 원본 DataFrame 모양: df.shape [예ㅣ (N, 9)]
- 라벨 분포: label.value_counts().to_dict()
- 스케일 결과의 상.하한 요약: scaled.describe().loc[['min', 'max']].round(6).to_dict()
  - (대상 열들의 min ~= 0.0, max ~=1.0 임을 확인)


### 예외처리(우선순위)
- 파일 열기 실패: 'File open error.'
- 디코딩 오류: 'Decoding error.'
- 파싱/스케일링 단계 오류: 'Processing error.'
※ 각 경우 정확한 문자열을 print()하고 return으로 종료


## 구현 방식 및 제약 사양
- 파일명: abalone_minmax.py
- 의존성: 
  - 허용: 표준 라이브러리, pandas
  - 금지: Scikit-learn 전부
- 입출력/인코딩:
  - 파일 경로는 고정, 인자는 받지 않음
  - 'abalone_attributes.txt', 'abalone.txt'
  - 텍스트 파일은 UTF-8로 가정하고, 파일 열기/디코딩 실패 시 "예외메시지"로 처리.
- 코드 구조(권장)
  - load_attributes(), load_data(), make_label(df), minmax_manual(df) 등으로 함수 분리
  - 상수열(분모 = 0일때) 예외처리 로직 포함
- 출력 규칙:
  - 위 3개 print()만 수행
  - 부가 출력 금지
- PEP8 준수할 것
- 엔트리 포인트:
  - if __name__ == "__main__":
    - main()