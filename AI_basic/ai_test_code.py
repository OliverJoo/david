"""
Anaconda py312 환경에서 ML 패키지 검증 스크립트
Apple Silicon Mac에서 모든 패키지의 GPU 가속 동작 확인
"""

import sys
import warnings
import platform

warnings.filterwarnings('ignore')


def system_info():
    """시스템 및 환경 정보"""
    print("=== 시스템 정보 ===")
    print(f"Python 버전: {sys.version}")
    print(f"플랫폼: {platform.platform()}")
    print(f"아키텍처: {platform.architecture()}")
    print(f"프로세서: {platform.processor()}")


def check_pytorch_advanced():
    """PyTorch 고급 검증"""
    print("\n=== PyTorch 고급 검증 ===")
    try:
        import torch
        print(f"PyTorch 버전: {torch.__version__}")
        print(f"MPS 사용 가능: {torch.backends.mps.is_available()}")
        print(f"MPS 빌드됨: {torch.backends.mps.is_built()}")

        if torch.backends.mps.is_available():
            # 디바이스별 성능 테스트
            device_mps = torch.device("mps")
            device_cpu = torch.device("cpu")

            import time

            # MPS 테스트
            x_mps = torch.randn(2000, 2000, device=device_mps)
            y_mps = torch.randn(2000, 2000, device=device_mps)

            start = time.time()
            z_mps = torch.mm(x_mps, y_mps)
            mps_time = time.time() - start

            # CPU 테스트
            x_cpu = torch.randn(2000, 2000, device=device_cpu)
            y_cpu = torch.randn(2000, 2000, device=device_cpu)

            start = time.time()
            z_cpu = torch.mm(x_cpu, y_cpu)
            cpu_time = time.time() - start

            print(f"MPS 연산 시간: {mps_time:.4f}초")
            print(f"CPU 연산 시간: {cpu_time:.4f}초")
            print(f"성능 향상: {cpu_time / mps_time:.2f}x")

            return True
        else:
            print("⚠️  MPS 사용 불가능")
            return False
    except Exception as e:
        print(f"❌ PyTorch 오류: {e}")
        return False


def check_tensorflow_advanced():
    """TensorFlow 고급 검증"""
    print("\n=== TensorFlow 검증 ===")
    try:
        import tensorflow as tf
        print(f"TensorFlow 버전: {tf.__version__}")

        # GPU 디바이스 확인
        gpus = tf.config.list_physical_devices('GPU')
        print(f"감지된 GPU: {len(gpus)}개")

        for i, gpu in enumerate(gpus):
            print(f"  GPU {i}: {gpu}")

        if gpus:
            # GPU 메모리 증가 허용
            try:
                tf.config.experimental.set_memory_growth(gpus[0], True)
            except:
                pass

            # Metal GPU 연산 테스트
            with tf.device('/GPU:0'):
                a = tf.random.normal([1000, 1000])
                b = tf.random.normal([1000, 1000])

                import time
                start = time.time()
                c = tf.matmul(a, b)
                gpu_time = time.time() - start

            # CPU 연산 테스트
            with tf.device('/CPU:0'):
                a_cpu = tf.random.normal([1000, 1000])
                b_cpu = tf.random.normal([1000, 1000])

                start = time.time()
                c_cpu = tf.matmul(a_cpu, b_cpu)
                cpu_time = time.time() - start

            print(f"Metal GPU 시간: {gpu_time:.4f}초")
            print(f"CPU 시간: {cpu_time:.4f}초")
            print(f"성능 향상: {cpu_time / gpu_time:.2f}x")

            return True
        else:
            print("⚠️  GPU 사용 불가능")
            return False

    except ImportError:
        print("❌ TensorFlow 설치되지 않음")
        return False
    except Exception as e:
        print(f"❌ TensorFlow 오류: {e}")
        return False


def check_scikit_learn_advanced():
    """scikit-learn 고급 검증"""
    print("\n=== scikit-learn 검증 ===")
    try:
        import sklearn
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.datasets import make_classification
        from sklearn.model_selection import train_test_split
        import time
        import os

        print(f"scikit-learn 버전: {sklearn.__version__}")
        print(f"사용 가능한 CPU 코어: {os.cpu_count()}")

        # 대용량 데이터셋으로 성능 테스트
        print("대용량 데이터셋 생성 중...")
        X, y = make_classification(
            n_samples=50000,
            n_features=100,
            n_informative=50,
            n_redundant=10,
            random_state=42
        )
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # 단일 스레드 테스트
        clf_single = RandomForestClassifier(
            n_estimators=100,
            random_state=42,
            n_jobs=1
        )

        start = time.time()
        clf_single.fit(X_train, y_train)
        single_time = time.time() - start
        single_accuracy = clf_single.score(X_test, y_test)

        # 멀티 스레드 테스트
        clf_multi = RandomForestClassifier(
            n_estimators=100,
            random_state=42,
            n_jobs=-1  # 모든 CPU 코어 사용
        )

        start = time.time()
        clf_multi.fit(X_train, y_train)
        multi_time = time.time() - start
        multi_accuracy = clf_multi.score(X_test, y_test)

        print(f"단일 스레드 - 시간: {single_time:.2f}초, 정확도: {single_accuracy:.4f}")
        print(f"멀티 스레드 - 시간: {multi_time:.2f}초, 정확도: {multi_accuracy:.4f}")
        print(f"멀티스레딩 성능 향상: {single_time / multi_time:.2f}x")

        return True
    except Exception as e:
        print(f"❌ scikit-learn 오류: {e}")
        return False


def check_conda_environment():
    """conda 환경 정보 확인"""
    print("\n=== Conda 환경 정보 ===")
    import os
    try:
        conda_default_env = os.environ.get('CONDA_DEFAULT_ENV', 'Not in conda env')
        print(f"활성 환경: {conda_default_env}")

        conda_prefix = os.environ.get('CONDA_PREFIX', 'Not set')
        print(f"환경 경로: {conda_prefix}")

        # 주요 패키지 버전 확인
        import subprocess
        result = subprocess.run(['conda', 'list', '-f', 'pytorch', 'tensorflow', 'scikit-learn'],
                                capture_output=True, text=True)
        if result.returncode == 0:
            print("설치된 주요 패키지:")
            print(result.stdout)
    except Exception as e:
        print(f"환경 정보 확인 중 오류: {e}")


def main():
    """메인 검증 함수"""
    print("🍎 Anaconda py312 환경 Apple Silicon ML 검증")
    print("=" * 60)

    system_info()
    check_conda_environment()

    results = []
    results.append(("PyTorch MPS", check_pytorch_advanced()))
    results.append(("TensorFlow Metal", check_tensorflow_advanced()))
    results.append(("scikit-learn", check_scikit_learn_advanced()))

    print("\n" + "=" * 60)
    print("📊 최종 검증 결과")
    print("=" * 60)

    for name, success in results:
        status = "✅ 성공" if success else "❌ 실패"
        print(f"{name:20s}: {status}")

    success_count = sum(result[1] for result in results)
    total_count = len(results)

    print(f"\n전체 {total_count}개 중 {success_count}개 성공")

    if success_count == total_count:
        print("🎉 모든 패키지가 성공적으로 설치되고 작동합니다!")
        print("GPU 가속이 정상적으로 활성화되었습니다.")
    else:
        print("⚠️  일부 패키지에 문제가 있습니다.")
        print("위의 오류 메시지를 확인하여 문제를 해결하세요.")

        # 해결 방법 제안
        print("\n💡 문제 해결 방법:")
        if not results[0][1]:  # PyTorch 실패
            print("- PyTorch: macOS 12.0 이상인지 확인")
        if not results[1][1]:  # TensorFlow 실패
            print("- TensorFlow: Python 3.12 호환성 확인 또는 Python 3.11 환경 사용 고려")
        if not results[2][1]:  # scikit-learn 실패
            print("- scikit-learn: conda-forge 채널에서 재설치 시도")


if __name__ == "__main__":
    main()

# 예상 출력:
# 🍎 Anaconda py312 환경 Apple Silicon ML 검증
# Python 버전: 3.12.11
# 활성 환경: py312
# PyTorch 버전: 2.x.x
# MPS 사용 가능: True
# 성능 향상: 3.2x
# 🎉 모든 패키지가 성공적으로 설치되고 작동합니다!
