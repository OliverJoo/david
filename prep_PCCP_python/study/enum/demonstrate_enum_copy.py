from enum import Enum
import copy

# ============= Enum 복사 특성 =============
def demonstrate_enum_copy():
    """Enum의 복사 특성 (싱글톤 패턴)"""

    print(f"\n=== Enum 복사 특성 ===")

    class State(Enum):
        ACTIVE = 1
        INACTIVE = 2
        PENDING = ["waiting", "in_queue"]  # 가변 객체를 값으로 사용

    original_state = State.PENDING

    # Enum 인스턴스는 싱글톤이므로 복사해도 같은 객체
    shallow_copy = copy.copy(original_state)
    deep_copy = copy.deepcopy(original_state)

    print(f"원본 Enum: {original_state}")
    print(f"얕은 복사: {shallow_copy}")
    print(f"깊은 복사: {deep_copy}")
    print(f"모든 ID 동일: {id(original_state) == id(shallow_copy) == id(deep_copy)}")

    # Enum 값이 가변 객체인 경우의 주의사항
    print(f"\n=== Enum 값이 가변 객체인 경우 ===")
    print(f"원본 값: {State.PENDING.value}")

    # Enum 값 수정 (주의: 이는 권장되지 않음!)
    State.PENDING.value[0] = "modified"

    print(f"수정 후 값: {State.PENDING.value}")
    print(f"모든 인스턴스 영향받음 (싱글톤): {shallow_copy.value}")

    # 안전한 방법: Enum 값으로 불변 객체 사용
    class SafeState(Enum):
        ACTIVE = 1
        INACTIVE = 2
        PENDING = ("waiting", "in_queue")  # 튜플 사용 (불변)

    print(f"안전한 Enum (튜플 사용): {SafeState.PENDING.value}")


demonstrate_enum_copy()
