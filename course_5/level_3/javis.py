import os
import csv
import glob
import wave
import time
import threading
from datetime import datetime
from typing import List, Tuple, Optional
import pyaudio
import speech_recognition as sr

SAMPLE_RATE = 44100  # 샘플링 주파수는 최소 40kHz 이상이어야 정보 손실 없이 디지털화가 가능. 실제로는 44.1kHz(CD품질)가 널리 쓰입니다.
CHANNELS = 1  # 모노(1채널) 녹음 (STT에 최적)
CHUNK_SIZE = 1024  # 실제 오디오 데이터에 사용되어지는 샘플 크기(512, 1024, 2048 등이 쓰임)
AUDIO_FORMAT = pyaudio.paInt16  # 16비트 정수 형식으로 8비트보다 자연스럽고 노이즈가 적으며, 사람의 귀가 구분할 수 있는 충분한 음량 폭 커버
RECORDS_DIR = 'records'  # 녹음 파일 저장 디렉토리
TIMEOUT_SECONDS = 30  # STT 타임아웃으로 아무런 음성 입력이 없거나 STT 처리가 종료되지 않으면 강제종료 시간 설정


class AudioRecorder:

    def __init__(self):
        self.audio = None
        self.stream = None
        self.is_recording = False
        self.frames = []
        self._ensure_records_directory()

    def _ensure_records_directory(self) -> None:
        try:
            if not os.path.exists(RECORDS_DIR):
                os.makedirs(RECORDS_DIR)
                print(f'{RECORDS_DIR} 디렉토리를 생성했습니다.')
        except PermissionError as e:
            raise PermissionError(f'디렉토리 생성 권한이 없습니다: {RECORDS_DIR}') from e
        except OSError as e:
            raise OSError(f'디렉토리 생성 중 오류 발생: {e}') from e

    def start_recording(self) -> None:
        try:
            self.audio = pyaudio.PyAudio()

            # 오디오 스트림 설정
            self.stream = self.audio.open(
                format=AUDIO_FORMAT,
                channels=CHANNELS,
                rate=SAMPLE_RATE,
                input=True,
                frames_per_buffer=CHUNK_SIZE
            )

            self.is_recording = True
            self.frames = []
            print('녹음을 시작합니다. Enter를 눌러 중지하세요.')

            # 별도 스레드에서 녹음 진행
            recording_thread = threading.Thread(target=self._record_audio)
            recording_thread.daemon = True  # 메인 스레드 종료 시 함께 종료
            recording_thread.start()

        except OSError as e:
            # 마이크 접근 불가 또는 오디오 디바이스 문제
            raise OSError(f'오디오 디바이스 접근 실패: {e}') from e
        except Exception as e:
            # 예상치 못한 녹음 시작 오류
            raise RuntimeError(f'녹음 시작 중 오류: {e}') from e

    def _record_audio(self) -> None:
        try:
            while self.is_recording:
                # exception_on_overflow=False - 실시간 스트림에서 데이터 손실 방지
                data = self.stream.read(CHUNK_SIZE, exception_on_overflow=False)
                self.frames.append(data)
        except Exception as e:
            print(f'녹음 중 오류 발생: {e}')
            self.is_recording = False

    def stop_recording(self) -> str:
        if not self.is_recording:
            raise RuntimeError('녹음이 진행 중이 아닙니다.')

        self.is_recording = False
        time.sleep(0.1)  # 녹음 스레드 완료 대기

        try:
            # 스트림 정리
            if self.stream:
                self.stream.stop_stream()
                self.stream.close()
            if self.audio:
                self.audio.terminate()

            timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
            filename = f'{timestamp}.wav'
            filepath = os.path.join(RECORDS_DIR, filename)

            with wave.open(filepath, 'wb') as wf:
                wf.setnchannels(CHANNELS)
                # 오디오 파일 저장시 샘플 바이트 단위를 명시해야 하며, 16비트는 2바이트 / 8비트는 1바이트 / 24비트는 3바이트 이다.
                # 16비트 2 바이트가 음질,효율,호환성 측면의 표준
                wf.setsampwidth(self.audio.get_sample_size(AUDIO_FORMAT) if self.audio else 2)
                wf.setframerate(SAMPLE_RATE)
                wf.writeframes(b''.join(self.frames))

            print(f'녹음이 완료되어 저장되었습니다: {filepath}')
            return filepath

        except PermissionError as e:
            # 파일 저장 권한 없음
            raise PermissionError(f'파일 저장 권한이 없습니다: {e}') from e
        except OSError as e:
            # 디스크 공간 부족 등 파일 시스템 오류
            raise OSError(f'파일 저장 중 오류: {e}') from e
        except Exception as e:
            # 기타 예상치 못한 오류
            raise RuntimeError(f'녹음 중지 중 오류: {e}') from e


class SpeechToTextProcessor:

    def __init__(self):
        # 환경 적응형 음성 인식 설정
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 4000  # 주변 소음에 맞춰 에너지 임계값 자동 조정(기본값보다 높게 설정하여 노이즈 차단)
        self.recognizer.dynamic_energy_threshold = True # 주변 환경에 따라 자동으로 임계값 조정 허용

    def get_audio_files(self) -> List[str]:
        try:
            if not os.path.exists(RECORDS_DIR):
                raise FileNotFoundError(f'{RECORDS_DIR} 디렉토리가 존재하지 않습니다.')

            pattern = os.path.join(RECORDS_DIR, '*.wav')
            wav_files = glob.glob(pattern)

            if not wav_files:
                print(f'{RECORDS_DIR} 디렉토리에 WAV 파일이 없습니다.')
                return []

            return sorted(wav_files)

        except PermissionError as e:
            raise PermissionError(f'디렉토리 접근 권한이 없습니다: {e}') from e
        except Exception as e:
            raise RuntimeError(f'파일 목록 조회 중 오류: {e}') from e

    def transcribe_audio(self, audio_filepath: str) -> List[Tuple[str, str]]:
        if not os.path.exists(audio_filepath):
            raise FileNotFoundError(f'오디오 파일이 존재하지 않습니다: {audio_filepath}')

        results = []

        try:
            with sr.AudioFile(audio_filepath) as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5) # 주변 소음 레벨에 맞춰 조정

                audio_data = self.recognizer.record(source) # 전체 오디오 로드

                # 구간별로 나누어 처리 (긴 오디오 처리를 위해)
                duration = len(audio_data.frame_data) / (audio_data.sample_rate * audio_data.sample_width)

                # 전체 오디오에 대해 STT 수행
                start_time = '00:00:00'
                end_time = self._seconds_to_timestamp(duration)

                try:
                    # Google Speech Recognition API 사용
                    text = self.recognizer.recognize_google(
                        audio_data,
                        language='ko-KR',  # 한국어 우선, 다른 언어도 자동 감지
                        show_all=False
                    )

                    if text.strip():  # 빈 텍스트 제외
                        results.append((f'{start_time}-{end_time}', text))
                        print(f'인식 완료: {text[:50]}...')
                    else:
                        results.append((f'{start_time}-{end_time}', '[인식된 음성 없음]'))

                except sr.UnknownValueError:
                    results.append((f'{start_time}-{end_time}', '[음성 인식 실패]'))
                    print(f'음성을 인식할 수 없습니다: {audio_filepath}')

                except sr.RequestError as e:
                    error_msg = f'[STT API 오류: {e}]'
                    results.append((f'{start_time}-{end_time}', error_msg))
                    print(f'STT API 요청 실패: {e}') # API 요청 실패 (네트워크, 할당량 등)

        except FileNotFoundError as e:
            raise FileNotFoundError(f'오디오 파일을 찾을 수 없습니다: {e}') from e
        except PermissionError as e:
            raise PermissionError(f'오디오 파일 접근 권한이 없습니다: {e}') from e
        except ValueError as e:
            raise ValueError(f'지원하지 않는 오디오 형식입니다: {e}') from e
        except Exception as e:
            raise RuntimeError(f'STT 처리 중 오류: {e}') from e

        return results

    def _seconds_to_timestamp(self, seconds: float) -> str:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f'{hours:02d}:{minutes:02d}:{secs:02d}'

    def save_to_csv(self, transcription_results: List[Tuple[str, str]],
                   output_filepath: str) -> None:
        try:
            with open(output_filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)

                writer.writerow(['시간', '인식된 텍스트'])

                for time_info, text in transcription_results:
                    writer.writerow([time_info, text])

                print(f'CSV 파일이 저장되었습니다: {output_filepath}')

        except PermissionError as e:
            raise PermissionError(f'CSV 파일 저장 권한이 없습니다: {e}') from e
        except OSError as e:
            raise OSError(f'CSV 파일 저장 중 오류: {e}') from e
        except Exception as e:
            raise RuntimeError(f'CSV 저장 중 오류: {e}') from e


def record_audio() -> Optional[str]:
    recorder = AudioRecorder()

    try:
        recorder.start_recording()
        input('녹음 중... Enter를 눌러 중지하세요: ')

        return recorder.stop_recording()

    except KeyboardInterrupt:
        print('\n녹음이 사용자에 의해 중단되었습니다.') # Ctrl+C로 중단
        recorder.is_recording = False
        return None
    except Exception as e:
        print(f'녹음 중 오류 발생: {e}')
        recorder.is_recording = False
        return None


def process_all_audio_files() -> None:
    processor = SpeechToTextProcessor()

    try:
        audio_files = processor.get_audio_files()

        if not audio_files:
            print('처리할 오디오 파일이 없습니다.')
            return

        print(f'{len(audio_files)}개의 오디오 파일을 처리합니다.')

        for audio_file in audio_files:
            print(f'\n처리 중: {os.path.basename(audio_file)}')

            try:
                results = processor.transcribe_audio(audio_file)

                base_name = os.path.splitext(os.path.basename(audio_file))[0] # CSV 파일명 생성 (확장자만 변경)
                csv_filename = f'{base_name}.csv'
                csv_filepath = os.path.join(RECORDS_DIR, csv_filename)

                processor.save_to_csv(results, csv_filepath) # CSV로 저장

            except Exception as e:
                print(f'{audio_file} 처리 중 오류: {e}')
                continue

        print('\n모든 파일 처리가 완료되었습니다.')

    except Exception as e:
        print(f'파일 처리 중 오류 발생: {e}')


def main() -> None:
    """메인 실행 함수"""
    print('=== JAVIS 음성 녹음 및 STT 시스템 ===')

    while True:
        print('\n1. 음성 녹음')
        print('2. 녹음된 파일들 STT 처리')
        print('3. 종료')

        try:
            choice = input('\n선택하세요 (1-3): ').strip()

            if choice == '1':
                print('\n=== 음성 녹음 시작 ===')
                audio_file = record_audio()
                if audio_file:
                    print(f'녹음 완료: {audio_file}')

            elif choice == '2':
                print('\n=== STT 처리 시작 ===')
                process_all_audio_files()

            elif choice == '3':
                print('프로그램을 종료합니다.')
                break

            else:
                print('잘못된 선택입니다. 1-3 중에서 선택하세요.')

        except KeyboardInterrupt:
            print('\n프로그램이 중단되었습니다.')
            break
        except Exception as e:
            print(f'실행 중 오류 발생: {e}')


if __name__ == '__main__':
    main()
