import os
import glob
import cv2
import zipfile
from typing import List, Optional, Tuple


class ImageProcessor:
    """CCTV 이미지 처리를 위한 클래스"""

    SUPPORTED_FORMATS = ('.jpg', '.jpeg')

    def __init__(self, folder_path: str = 'CCTV'):
        self.folder_path = folder_path
        self.image_files: List[str] = []
        self.current_index = 0

        # 사람 감지를 위한 HOG descriptor 초기화
        self.hog = cv2.HOGDescriptor()
        # HOG (Histogram of Oriented Gradients): 이미지에서 객체의 형태나 윤곽선을 효과적으로 표현하는 방법(Feature Descriptor). 이미지의 작은 구역들마다 픽셀 밝기 변화의 방향과 크기를 분석하여 '어느 방향의 선이 얼마나 많은지'를 계산합니다. 사람은 특유의 실루엣(머리, 어깨, 팔, 다리 등)을 가지고 있기 때문에, HOG는 사람을 감지하는 데 매우 효과적입니다.
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

        # 성능 이슈 이유
        # 1.오래된 기술: HOG는 딥러닝이 대중화되기 전의 '클래식' 컴퓨터 비전 알고리즘. 사람의 형태(실루엣)를 기반으로 감지하기 때문에, 가려짐(occlusion), 다양한 자세, 복잡한 배경에 취약.
        # 2.느린 속도: 이미지의 크기를 바꿔가며 모든 영역을 일일이 확인하는 '슬라이딩 윈도우' 방식으로 처리 속도가 느립니다.
        # 3.높은 오탐지율: 사람이 아닌데 사람으로 감지하거나(False Positive), 실제 사람을 놓치는(False Negative) 경우가 많음.
        # 4.중복된 경계 박스: 한 명의 사람에 대해 여러 개의 겹치는 사각형을 그리는 경향이 있습니다

    def load_image_files(self) -> bool:
        """이미지 파일 목록을 로드하고 유효성을 검증"""
        try:
            if not os.path.exists(self.folder_path):
                print(f'폴더가 존재하지 않습니다: {self.folder_path}')
                return False

            # 지원하는 이미지 형식만 필터링
            all_files = []
            for ext in self.SUPPORTED_FORMATS:
                pattern = os.path.join(self.folder_path, f'*{ext}')
                all_files.extend(glob.glob(pattern, recursive=False))
                pattern_upper = os.path.join(self.folder_path, f'*{ext.upper()}')
                all_files.extend(glob.glob(pattern_upper, recursive=False))

            self.image_files = sorted(list(set(all_files))) # 중복 제거 및 정렬

            if not self.image_files:
                print(f'{self.folder_path} 폴더에 이미지 파일이 없습니다.')
                return False

            print(f'{len(self.image_files)}개의 이미지 파일을 찾았습니다.')
            return True

        except Exception as e:
            print(f'파일 로드 중 오류 발생: {e}')
            return False

    def load_and_validate_image(self, file_path: str) -> Optional[cv2.Mat]:
        try:
            image = cv2.imread(file_path)
            if image is None:
                print(f'이미지 로드 실패: {file_path}')
                return None
            return image
        except Exception as e:
            print(f'이미지 로드 중 오류: {e}')
            return None

    def resize_image_for_display(self, image: cv2.Mat, max_width: int = 1200, max_height: int = 800) -> cv2.Mat:
        height, width = image.shape[:2]

        # 비율을 유지하면서 크기 조정
        scale_w = max_width / width
        scale_h = max_height / height
        scale = min(scale_w, scale_h)

        if scale < 1:
            new_width = int(width * scale)
            new_height = int(height * scale)
            return cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)

        return image

    def detect_people(self, image: cv2.Mat) -> Tuple[List[Tuple[int, int, int, int]], cv2.Mat]:
        try:
            # 사람 감지 수행
            boxes, weights = self.hog.detectMultiScale(
                image,
                winStride=(8, 8),
                padding=(32, 32),
                scale=1.05,
                hitThreshold=-0.95
            )

            # 감지된 사람 주위에 사각형 그리기
            result_image = image.copy()
            detected_people = []

            for (x, y, w, h) in boxes:
                detected_people.append((x, y, w, h))
                cv2.rectangle(result_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(result_image, 'Person', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            return detected_people, result_image

        except Exception as e:
            print(f'사람 감지 중 오류: {e}')
            return [], image

    def is_window_open(self, window_name: str) -> bool:
        """창이 열려있는지 확인하는 안전한 메서드"""
        try:
            return cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) >= 1
        except cv2.error:
            return False


def _unzip_cctv_if_exists(zip_filename: str = 'cctv.zip', extract_folder: str = 'CCTV'):
    if os.path.exists(zip_filename):
        print(f"'{zip_filename}' 파일을 찾았습니다. '{extract_folder}' 폴더에 압축을 해제합니다.")
        try:
            os.makedirs(extract_folder, exist_ok=True)

            with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
                zip_ref.extractall(extract_folder)

            print(f"'{extract_folder}' 폴더에 압축 해제가 완료되었습니다.\n")
        except zipfile.BadZipFile:
            print(f"오류: '{zip_filename}'은 유효한 zip 파일이 아닙니다.\n")
        except Exception as e:
            print(f"압축 해제 중 오류 발생: {e}")


def problem1_image_viewer():
    print('=== 문제 1: 이미지 뷰어 ===')
    _unzip_cctv_if_exists()

    print('방향키: ← (이전), → (다음), ESC 또는 창 닫기 (종료)')

    processor = ImageProcessor()

    if not processor.load_image_files():
        return

    window_name = 'CCTV Image Viewer'
    cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)

    while True:
        current_file = processor.image_files[processor.current_index]
        print(f'현재 이미지: {os.path.basename(current_file)} '
              f'({processor.current_index + 1}/{len(processor.image_files)})')

        image = processor.load_and_validate_image(current_file)
        if image is None:
            processor.image_files.pop(processor.current_index) # 문제가 있는 이미지는 목록에서 제거하고 계속 진행
            if not processor.image_files:
                print('더 이상 표시할 이미지가 없습니다.')
                break
            # 인덱스가 범위를 벗어나지 않도록 조정
            processor.current_index %= len(processor.image_files)
            continue

        # 화면 크기에 맞게 조정 & 이미지 표시
        display_image = processor.resize_image_for_display(image)
        cv2.imshow(window_name, display_image)

        # 키 입력 대기
        while True:
            key = cv2.waitKey(30) & 0xFF

            if not processor.is_window_open(window_name):
                print('이미지 뷰어를 종료합니다.')
                return

            if key == 27:  # ESC 키
                cv2.destroyWindow(window_name)
                cv2.waitKey(1)  # macOS에서 창이 확실히 닫히도록 처리
                print('이미지 뷰어를 종료합니다.')
                return
            elif key == 81 or key == 2:  # 왼쪽 방향키
                if processor.current_index > 0:
                    processor.current_index -= 1
                    break
                else:
                    print('First picture')
            elif key == 83 or key == 3:  # 오른쪽 방향키
                if processor.current_index < len(processor.image_files) - 1:
                    processor.current_index += 1
                    break
                else:
                    print('Last picture')


def problem2_people_detection():
    print('=== 문제 2: 사람 감지 시스템 ===')
    print('Enter 또는 →: 다음 이미지, ←: 이전 이미지, ESC 또는 창 닫기: 종료')

    processor = ImageProcessor()
    if not processor.load_image_files():
        return

    current_index = 0
    window_name = 'CCTV People Detection'
    cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)

    def display_current_image_with_detection(index: int) -> bool:
        if index >= len(processor.image_files):
            return False

        current_file = processor.image_files[index]
        image = processor.load_and_validate_image(current_file)
        if image is None:
            print(f'이미지 로드 실패: {os.path.basename(current_file)}')
            return False

        detected_people, result_image = processor.detect_people(image)

        if detected_people:
            print(f'현재 이미지: {os.path.basename(current_file)} ({index + 1}/{len(processor.image_files)}) - {len(detected_people)}명 감지됨')
        else:
            print(f'현재 이미지: {os.path.basename(current_file)} ({index + 1}/{len(processor.image_files)}) - 사람 없음')

        display_image = processor.resize_image_for_display(result_image)
        cv2.imshow(window_name, display_image)

        return True

    # 첫 번째 이미지 표시
    if not display_current_image_with_detection(current_index):
        print('첫 번째 이미지를 로드할 수 없습니다.')
        cv2.destroyAllWindows()
        return

    while True:
        key = cv2.waitKey(30) & 0xFF

        if not processor.is_window_open(window_name):
            break

        if key == 27:  # ESC 키
            break
        elif key == 81 or key == 2:  # 왼쪽 방향키
            if current_index > 0:
                current_index -= 1
                display_current_image_with_detection(current_index)
        elif key == 83 or key == 3 or key == 13 or key == 10:  # 오른쪽 방향키 또는 Enter
            if current_index < len(processor.image_files) - 1:
                current_index += 1
                display_current_image_with_detection(current_index)
            else:
                print('검색이 끝났습니다.')
                break

    cv2.destroyWindow(window_name)
    cv2.waitKey(1)  # macOS에서 창이 확실히 닫히도록 처리
    print('사람 감지 시스템을 종료합니다.')


def main():
    print('CCTV 이미지 처리 시스템')
    print('=' * 30)

    while True:
        print('\n기능을 선택하세요:')
        print('1. 이미지 뷰어')
        print('2. 사람 감지 시스템')
        print('0. 종료')

        try:
            choice = input('선택 (0-2): ').strip()

            if choice == '1':
                problem1_image_viewer()
            elif choice == '2':
                problem2_people_detection()
            elif choice == '0':
                print('프로그램을 종료합니다.')
                break
            else:
                print('잘못된 선택입니다. 0, 1, 2 중에서 선택하세요.')

        except KeyboardInterrupt:
            print('\n프로그램을 중단합니다.')
            break
        except Exception as e:
            print(f'오류 발생: {e}')


if __name__ == '__main__':
    main()
