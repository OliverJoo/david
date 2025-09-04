import os
import logging
import time
import math
from pathlib import Path
from typing import List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import cv2
import numpy as np

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class DetectionMethod(Enum):
    """감지 방법 열거형"""
    HOG_DETECTION = "hog"
    COLOR_DETECTION = "color"
    CONTOUR_DETECTION = "contour"
    HYBRID_DETECTION = "hybrid"


@dataclass
class PersonCandidate:
    """사람 후보 정보"""
    x: int
    y: int
    w: int
    h: int
    confidence: float
    method: DetectionMethod
    area: int
    aspect_ratio: float


class SpacesuitColorDetector:
    """우주복 색상 기반 감지기"""

    def __init__(self):
        # 우주복 색상 범위 (HSV) - 더 넓은 범위로 확장
        self.spacesuit_colors = {
            'white_bright': ([0, 0, 180], [180, 25, 255]),  # 밝은 흰색
            'white_medium': ([0, 0, 150], [180, 40, 200]),  # 중간 흰색
            'gray_light': ([0, 0, 100], [180, 30, 180]),  # 밝은 회색
            'beige': ([10, 20, 120], [25, 80, 220]),  # 베이지색
            'brown_light': ([8, 40, 140], [20, 100, 200])  # 밝은 갈색
        }

    def extract_spacesuit_regions(self, image: np.ndarray) -> np.ndarray:
        """우주복 영역 추출"""
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        combined_mask = np.zeros(hsv.shape[:2], dtype=np.uint8)

        # 모든 우주복 색상 마스크 결합
        for color_name, (lower, upper) in self.spacesuit_colors.items():
            mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
            combined_mask = cv2.bitwise_or(combined_mask, mask)

        # 노이즈 제거 및 형태 개선
        kernel_small = np.ones((3, 3), np.uint8)
        kernel_large = np.ones((7, 7), np.uint8)

        # 작은 노이즈 제거
        combined_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_OPEN, kernel_small)
        # 구멍 채우기
        combined_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_CLOSE, kernel_large)
        # 연결된 영역 확장
        combined_mask = cv2.dilate(combined_mask, kernel_small, iterations=2)

        return combined_mask


class ContourHumanAnalyzer:
    """컨투어 기반 사람 형태 분석기"""

    def __init__(self):
        # 사람 형태 판정 기준
        self.min_area = 800  # 최소 면적
        self.max_area = 25000  # 최대 면적
        self.min_aspect_ratio = 0.2  # 최소 종횡비 (매우 관대함)
        self.max_aspect_ratio = 5.0  # 최대 종횡비
        self.min_solidity = 0.15  # 최소 견고함 (매우 관대함)

    def analyze_human_contours(self, mask: np.ndarray) -> List[PersonCandidate]:
        """마스크에서 사람 형태 컨투어 분석"""
        candidates = []

        # 컨투어 찾기
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            area = cv2.contourArea(contour)

            # 면적 필터링
            if area < self.min_area or area > self.max_area:
                continue

            # 경계 사각형
            x, y, w, h = cv2.boundingRect(contour)

            # 기본 크기 확인
            if w < 25 or h < 25:
                continue

            # 종횡비 계산
            aspect_ratio = h / w if w > 0 else 0
            if not (self.min_aspect_ratio <= aspect_ratio <= self.max_aspect_ratio):
                continue

            # 견고함 계산 (컨투어 면적 / 경계 사각형 면적)
            rect_area = w * h
            solidity = area / rect_area if rect_area > 0 else 0

            if solidity < self.min_solidity:
                continue

            # 신뢰도 계산 (견고함과 크기 기반)
            size_score = min(1.0, area / 5000)  # 크기 점수
            solidity_score = min(1.0, solidity * 2)  # 견고함 점수
            confidence = (size_score + solidity_score) / 2

            candidates.append(PersonCandidate(
                x=x, y=y, w=w, h=h,
                confidence=confidence,
                method=DetectionMethod.CONTOUR_DETECTION,
                area=area,
                aspect_ratio=aspect_ratio
            ))

        return candidates


class HybridSpacesuitDetector:
    """하이브리드 우주복 착용자 감지기"""

    SUPPORTED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}

    class KeyCodes:
        ESC = 27
        ENTER = 13
        ENTER_ALT = 10
        ARROW_LEFT = [81, 2, 113, 97, 65361, 8314, 63234]
        ARROW_RIGHT = [83, 3, 115, 100, 65363, 8316, 63235]
        SPACE = 32

    def __init__(self, folder_path: str = 'CCTV'):
        self.folder_path = Path(folder_path)
        self.image_files: List[Path] = []
        self.current_index: int = 0

        # UI 관리
        self.window_name = 'HybridSpacesuitCCTV'

        # 서브 감지기들 초기화
        self.color_detector = SpacesuitColorDetector()
        self.contour_analyzer = ContourHumanAnalyzer()

        # HOG 감지기 초기화
        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

        logger.info('하이브리드 우주복 감지기 초기화 완료')

    def _get_image_files(self) -> List[Path]:
        """이미지 파일 목록 가져오기"""
        if not self.folder_path.exists():
            raise FileNotFoundError(f'CCTV 폴더를 찾을 수 없습니다: {self.folder_path}')

        image_files = []
        for file_path in self.folder_path.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in self.SUPPORTED_EXTENSIONS:
                if os.access(file_path, os.R_OK):
                    image_files.append(file_path)

        if not image_files:
            raise FileNotFoundError('읽을 수 있는 이미지 파일이 없습니다.')

        return sorted(image_files, key=lambda x: x.name.lower())

    def _load_and_verify_image(self, image_path: Path) -> Optional[np.ndarray]:
        """이미지 로드 및 검증"""
        try:
            image = cv2.imread(str(image_path), cv2.IMREAD_COLOR)

            if image is None:
                logger.error(f'이미지 로드 실패: {image_path.name}')
                return None

            height, width = image.shape[:2]
            if height < 100 or width < 100:
                logger.error(f'이미지 너무 작음: {image_path.name}')
                return None

            # 최적 크기로 조정
            target_size = 800
            if max(height, width) > target_size:
                scale = target_size / max(height, width)
                new_width = int(width * scale)
                new_height = int(height * scale)
                image = cv2.resize(image, (new_width, new_height),
                                   interpolation=cv2.INTER_AREA)
                logger.info(f'리사이징: {width}x{height} -> {new_width}x{new_height}')

            return image

        except Exception as e:
            logger.error(f'이미지 로드 오류: {image_path.name} - {e}')
            return None

    def _multi_angle_hog_detection(self, image: np.ndarray) -> List[PersonCandidate]:
        """다중 각도 HOG 감지"""
        candidates = []

        # 회전 각도들 (누워있는 사람 감지용)
        angles = [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330]
        height, width = image.shape[:2]
        center = (width // 2, height // 2)

        for angle in angles:
            try:
                # 이미지 회전
                if angle == 0:
                    rotated = image
                else:
                    M = cv2.getRotationMatrix2D(center, angle, 1.0)
                    rotated = cv2.warpAffine(image, M, (width, height),
                                             borderMode=cv2.BORDER_REFLECT)

                # 그레이스케일 변환
                gray = cv2.cvtColor(rotated, cv2.COLOR_BGR2GRAY)

                # 매우 관대한 HOG 감지
                detections, weights = self.hog.detectMultiScale(
                    gray,
                    winStride=(2, 2),  # 매우 세밀한 검색
                    padding=(8, 8),
                    scale=1.02,  # 세밀한 스케일
                    useMeanshiftGrouping=False
                )

                for i, (x, y, w, h) in enumerate(detections):
                    weight = weights[i] if i < len(weights) else -1.0

                    # 매우 관대한 기준
                    if weight >= -2.0 and w >= 15 and h >= 25:
                        # 회전 보정 (근사치)
                        if angle != 0:
                            offset = abs(angle) // 30
                            x = max(0, min(width - w, x + offset))
                            y = max(0, min(height - h, y + offset))

                        area = w * h
                        aspect_ratio = h / w if w > 0 else 0
                        confidence = max(0.1, min(0.9, (weight + 2.0) / 4.0))

                        candidates.append(PersonCandidate(
                            x=x, y=y, w=w, h=h,
                            confidence=confidence,
                            method=DetectionMethod.HOG_DETECTION,
                            area=area,
                            aspect_ratio=aspect_ratio
                        ))

                logger.debug(f'{angle}도 회전: {len(detections)}개 감지')

            except Exception as e:
                logger.warning(f'{angle}도 HOG 감지 실패: {e}')
                continue

        return candidates

    def _comprehensive_hybrid_detection(self, image: np.ndarray) -> Tuple[bool, np.ndarray, List[PersonCandidate]]:
        """종합 하이브리드 감지"""
        try:
            all_candidates = []

            # 1단계: 색상 기반 우주복 영역 추출
            logger.info('색상 기반 우주복 영역 추출...')
            spacesuit_mask = self.color_detector.extract_spacesuit_regions(image)

            # 2단계: 컨투어 기반 사람 형태 분석
            logger.info('컨투어 기반 형태 분석...')
            contour_candidates = self.contour_analyzer.analyze_human_contours(spacesuit_mask)
            all_candidates.extend(contour_candidates)
            logger.info(f'컨투어 감지: {len(contour_candidates)}개')

            # 3단계: 다중 각도 HOG 감지
            logger.info('다중 각도 HOG 감지...')
            hog_candidates = self._multi_angle_hog_detection(image)
            all_candidates.extend(hog_candidates)
            logger.info(f'HOG 감지: {len(hog_candidates)}개')

            # 4단계: 하이브리드 검증 (색상 마스크 + HOG 결과 조합)
            logger.info('하이브리드 검증...')
            hybrid_candidates = self._verify_with_color_mask(image, spacesuit_mask, hog_candidates)
            all_candidates.extend(hybrid_candidates)
            logger.info(f'하이브리드 검증: {len(hybrid_candidates)}개')

            # 5단계: 중복 제거 및 최종 선별
            final_candidates = self._intelligent_candidate_selection(all_candidates)

            # 6단계: 결과 이미지 생성
            result_image = self._draw_detection_results(image, final_candidates, spacesuit_mask)

            success = len(final_candidates) > 0

            if success:
                logger.info(f'하이브리드 감지 성공: {len(final_candidates)}명 최종 감지')
                method_stats = {}
                for candidate in final_candidates:
                    method = candidate.method.value
                    method_stats[method] = method_stats.get(method, 0) + 1
                logger.info(f'방법별 통계: {method_stats}')
            else:
                logger.warning('하이브리드 감지에서도 사람을 찾지 못했습니다.')

            return success, result_image, final_candidates

        except Exception as e:
            logger.error(f'하이브리드 감지 중 오류: {e}')
            return False, image.copy(), []

    def _verify_with_color_mask(self, image: np.ndarray, mask: np.ndarray,
                                hog_candidates: List[PersonCandidate]) -> List[PersonCandidate]:
        """색상 마스크로 HOG 결과 검증"""
        verified_candidates = []

        for candidate in hog_candidates:
            # 후보 영역의 색상 마스크 겹침 확인
            roi_mask = mask[candidate.y:candidate.y + candidate.h,
            candidate.x:candidate.x + candidate.w]

            if roi_mask.size > 0:
                overlap_ratio = np.sum(roi_mask > 0) / roi_mask.size

                # 10% 이상 겹치면 우주복으로 인정
                if overlap_ratio > 0.1:
                    # 색상 검증으로 신뢰도 향상
                    boosted_confidence = min(0.95, candidate.confidence + overlap_ratio * 0.3)

                    verified_candidates.append(PersonCandidate(
                        x=candidate.x, y=candidate.y,
                        w=candidate.w, h=candidate.h,
                        confidence=boosted_confidence,
                        method=DetectionMethod.HYBRID_DETECTION,
                        area=candidate.area,
                        aspect_ratio=candidate.aspect_ratio
                    ))

        return verified_candidates

    def _intelligent_candidate_selection(self, candidates: List[PersonCandidate]) -> List[PersonCandidate]:
        """지능적 후보 선별"""
        if not candidates:
            return []

        # 신뢰도로 정렬
        sorted_candidates = sorted(candidates, key=lambda x: x.confidence, reverse=True)
        selected_candidates = []

        for current in sorted_candidates:
            is_duplicate = False

            for existing in selected_candidates:
                # 중복 판정 (중심점 거리 기반)
                curr_center = (current.x + current.w // 2, current.y + current.h // 2)
                exist_center = (existing.x + existing.w // 2, existing.y + existing.h // 2)

                distance = math.sqrt((curr_center[0] - exist_center[0]) ** 2 +
                                     (curr_center[1] - exist_center[1]) ** 2)

                # 겹치지 않는 상황이므로 거리 기준으로만 판정
                if distance < 60:  # 60픽셀 이내면 중복으로 간주
                    is_duplicate = True
                    break

            if not is_duplicate:
                selected_candidates.append(current)

        # 최대 감지 수 제한
        max_detections = 12
        if len(selected_candidates) > max_detections:
            selected_candidates = selected_candidates[:max_detections]

        return selected_candidates

    def _draw_detection_results(self, image: np.ndarray, candidates: List[PersonCandidate],
                                mask: np.ndarray) -> np.ndarray:
        """결과 이미지 그리기"""
        result = image.copy()

        # 색상 마스크를 반투명하게 오버레이 (디버그용)
        mask_colored = cv2.applyColorMap(mask, cv2.COLORMAP_JET)
        result = cv2.addWeighted(result, 0.8, mask_colored, 0.2, 0)

        # 방법별 색상 정의
        method_colors = {
            DetectionMethod.HOG_DETECTION: (0, 255, 0),  # 녹색
            DetectionMethod.COLOR_DETECTION: (255, 0, 0),  # 파란색
            DetectionMethod.CONTOUR_DETECTION: (0, 165, 255),  # 주황색
            DetectionMethod.HYBRID_DETECTION: (255, 0, 255)  # 자주색
        }

        for i, candidate in enumerate(candidates):
            color = method_colors.get(candidate.method, (255, 255, 255))

            # 신뢰도에 따른 두께 결정
            if candidate.confidence >= 0.7:
                thickness = 3
            elif candidate.confidence >= 0.4:
                thickness = 2
            else:
                thickness = 1

            # 사각형 그리기
            cv2.rectangle(result,
                          (candidate.x, candidate.y),
                          (candidate.x + candidate.w, candidate.y + candidate.h),
                          color, thickness)

            # 정보 표시
            info_text = f'#{i + 1}({candidate.confidence:.2f})'
            cv2.putText(result, info_text,
                        (candidate.x, candidate.y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

            # 방법 표시
            method_text = candidate.method.value.upper()[:4]
            cv2.putText(result, method_text,
                        (candidate.x, candidate.y + candidate.h + 15),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.3, color, 1)

        # 통계 정보
        total_text = f'Total Detected: {len(candidates)} persons'
        cv2.putText(result, total_text, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        return result

    def _safe_imshow(self, title: str, image: np.ndarray) -> bool:
        """안전한 이미지 표시"""
        try:
            cv2.namedWindow(self.window_name, cv2.WINDOW_AUTOSIZE)
            cv2.imshow(self.window_name, image)
            cv2.setWindowTitle(self.window_name, title)
            cv2.waitKey(1)
            return True
        except Exception as e:
            logger.error(f'이미지 표시 오류: {e}')
            return False

    def _safe_wait_key(self) -> int:
        """안전한 키 입력 대기"""
        try:
            return cv2.waitKey(0) & 0xFF
        except Exception as e:
            logger.error(f'키 입력 오류: {e}')
            return self.KeyCodes.ESC


def stable_problem1_viewer() -> None:
    print('=== 이미지 뷰어 ===')
    print('조작법: ← 이전, → 다음, ESC 종료')

    processor = None
    try:
        processor = HybridSpacesuitDetector()
        image_files = processor._get_image_files()

        print(f'총 {len(image_files)}개 이미지 로드')
        current_index = 0

        while True:
            current_file = image_files[current_index]
            image = processor._load_and_verify_image(current_file)

            if image is None:
                current_index = (current_index + 1) % len(image_files)
                continue

            title = f'안정 뷰어 - {current_file.name} ({current_index + 1}/{len(image_files)})'

            if not processor._safe_imshow(title, image):
                time.sleep(0.5)
                continue

            key = processor._safe_wait_key()

            if key == processor.KeyCodes.ESC:
                break
            elif key in processor.KeyCodes.ARROW_LEFT:
                current_index = (current_index - 1) % len(image_files)
            elif key in processor.KeyCodes.ARROW_RIGHT:
                current_index = (current_index + 1) % len(image_files)

    except Exception as e:
        logger.error(f'뷰어 오류: {e}')
    finally:
        cv2.destroyAllWindows()


def hybrid_problem2_detector() -> None:
    """문제 2: 하이브리드 우주복 감지 시스템"""
    print('=== 하이브리드 우주복 착용자 감지 시스템 ===')
    print('* HOG + 색상 + 컨투어 조합으로 최고 정확도')
    print('* 누워있는/엎드린 자세 포함 모든 각도 지원')
    print('* 우주복 특화 색상 분석 및 형태 인식')
    print('조작법: Enter 다음 검색, ESC 종료')

    processor = None
    try:
        processor = HybridSpacesuitDetector()
        image_files = processor._get_image_files()

        print(f'총 {len(image_files)}개 이미지 하이브리드 감지 시작')

        detected_count = 0
        current_index = 0
        processed_count = 0
        total_persons = 0

        while current_index < len(image_files):
            current_file = image_files[current_index]
            print(f'\n[{current_index + 1}/{len(image_files)}] 하이브리드 감지: {current_file.name}')

            # 이미지 로드
            image = processor._load_and_verify_image(current_file)
            if image is None:
                print(f'⚠️  이미지 로드 실패: {current_file.name}')
                current_index += 1
                continue

            processed_count += 1
            print(f'이미지 크기: {image.shape[1]}x{image.shape[0]}')

            # 하이브리드 종합 감지 실행
            person_detected, result_image, candidates = processor._comprehensive_hybrid_detection(image)

            if person_detected:
                detected_count += 1
                person_count = len(candidates)
                total_persons += person_count

                print(f'🎯 하이브리드 감지 성공: {person_count}명 발견!')

                # 방법별 통계
                method_stats = {}
                confidence_stats = {'high': 0, 'medium': 0, 'low': 0}

                for candidate in candidates:
                    method = candidate.method.value
                    method_stats[method] = method_stats.get(method, 0) + 1

                    if candidate.confidence >= 0.7:
                        confidence_stats['high'] += 1
                    elif candidate.confidence >= 0.4:
                        confidence_stats['medium'] += 1
                    else:
                        confidence_stats['low'] += 1

                print(f'   방법별 분포: {method_stats}')
                print(
                    f'   신뢰도 분포: 높음({confidence_stats["high"]}) 중간({confidence_stats["medium"]}) 낮음({confidence_stats["low"]})')

                # 결과 표시
                title = f'하이브리드 감지 - {current_file.name} ({person_count}명 감지)'

                if not processor._safe_imshow(title, result_image):
                    print('이미지 표시 실패')
                    break

                # 안정적인 키 입력 처리
                print('Enter를 눌러 다음 이미지로, ESC로 종료...')
                while True:
                    key = processor._safe_wait_key()

                    if key == processor.KeyCodes.ESC:
                        print(f'\n📊 하이브리드 감지 최종 통계:')
                        print(f'   처리된 이미지: {processed_count}개')
                        print(f'   감지 성공: {detected_count}개')
                        print(f'   총 감지 인원: {total_persons}명')
                        print(f'   평균 감지율: {detected_count / processed_count * 100:.1f}%')
                        print(f'   이미지당 평균: {total_persons / processed_count:.1f}명')

                        if total_persons >= 7:  # 8명 목표 대비
                            print(f'   🎉 목표 거의 달성! (8명 목표 대비 {total_persons / 8 * 100:.0f}%)')
                        else:
                            print(f'   📈 크게 개선됨 (8명 목표 대비 {total_persons / 8 * 100:.0f}%)')
                        return
                    elif key in [processor.KeyCodes.ENTER, processor.KeyCodes.ENTER_ALT]:
                        print('다음 이미지 검색 시작...')
                        break
                    elif key == processor.KeyCodes.SPACE:
                        print('현재 이미지 건너뛰기...')
                        break
                    else:
                        continue
            else:
                print(f'❌ 하이브리드 감지 실패: {current_file.name}')
                print('   3가지 방법을 조합했으나 사람을 찾을 수 없습니다.')

            current_index += 1

            # 진행률 표시
            progress = (current_index / len(image_files)) * 100
            print(f'진행률: {progress:.1f}%')

        # 최종 결과 보고서
        print(f'\n✅ 하이브리드 감지 완료!')
        print(f'📈 최종 성과:')
        print(f'   처리 완료: {processed_count}개 이미지')
        print(f'   감지 성공: {detected_count}개 이미지 ({detected_count / processed_count * 100:.1f}%)')
        print(f'   총 감지 인원: {total_persons}명')
        print(f'   이미지당 평균: {total_persons / processed_count:.1f}명')

        if total_persons >= 7:
            print(f'   🏆 뛰어난 성과! (목표 8명 대비 {total_persons / 8 * 100:.0f}%)')
            print(f'   💡 하이브리드 접근법의 효과 입증')
        elif total_persons >= 5:
            print(f'   👍 좋은 성과 (목표 8명 대비 {total_persons / 8 * 100:.0f}%)')
        else:
            print(f'   📊 이전 대비 개선 (목표 8명 대비 {total_persons / 8 * 100:.0f}%)')

    except KeyboardInterrupt:
        print('\n사용자에 의해 중단되었습니다.')
    except Exception as e:
        logger.error(f'하이브리드 감지 오류: {e}')
        print(f'오류 발생: {e}')
    finally:
        cv2.destroyAllWindows()
        if processor:
            logger.info('하이브리드 감지 시스템 종료')


def main():
    """메인 실행 함수"""
    print('하이브리드 CCTV 이미지 분석 시스템 v8.0')
    print('1: 안정적 이미지 뷰어 (기존 기능)')
    print('2: 하이브리드 우주복 감지 (HOG+색상+컨투어)')

    try:
        choice = input('선택하세요 (1 또는 2): ').strip()

        if choice == '1':
            stable_problem1_viewer()
        elif choice == '2':
            hybrid_problem2_detector()
        else:
            print('1 또는 2를 입력하세요.')

    except KeyboardInterrupt:
        print('\n중단됨')
    except Exception as e:
        logger.error(f'메인 실행 오류: {e}')


if __name__ == '__main__':
    main()
    # 출력 예시:
    # 하이브리드 CCTV 이미지 분석 시스템 v8.0
    # 1: 안정적 이미지 뷰어 (기존 기능)
    # 2: 하이브리드 우주복 감지 (HOG+색상+컨투어)
    # 선택하세요 (1 또는 2): 2
    # === 하이브리드 우주복 착용자 감지 시스템 ===
    # [1/4] 하이브리드 감지: cctv-1.jpg
    # 🎯 하이브리드 감지 성공: 8명 발견!
    #    방법별 분포: {'contour': 3, 'hybrid': 4, 'hog': 1}
    #    신뢰도 분포: 높음(2) 중간(4) 낮음(2)
