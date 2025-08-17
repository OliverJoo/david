# ============= Enum 완벽 마스터 =============
from enum import Enum, IntEnum, Flag, IntFlag, auto
import copy
from typing import Dict, Any


def demonstrate_enum():
    """Enum의 모든 기능과 실전 활용"""

    print("=== 1. 기본 Enum 클래스 ===")

    # 기본 Enum 정의
    class Status(Enum):
        PENDING = 1
        PROCESSING = 2
        COMPLETED = 3
        FAILED = 4
        CANCELLED = 5

    class Priority(Enum):
        LOW = "low"
        MEDIUM = "medium"
        HIGH = "high"
        CRITICAL = "critical"

    # Enum 기본 사용법
    print(f"상태: {Status.PENDING}")
    print(f"상태 이름: {Status.PENDING.name}")
    print(f"상태 값: {Status.PENDING.value}")
    print(f"우선순위: {Priority.HIGH}")

    # Enum 비교
    print(f"같은 상태 비교: {Status.PENDING == Status.PENDING}")
    print(f"다른 상태 비교: {Status.PENDING == Status.COMPLETED}")

    # Enum 순회
    print(f"모든 상태: {[status.name for status in Status]}")
    print(f"모든 우선순위: {[priority.value for priority in Priority]}")

    print(f"\n=== 2. auto()를 사용한 자동 값 할당 ===")

    class Color(Enum):
        RED = auto()
        GREEN = auto()
        BLUE = auto()
        YELLOW = auto()

    print(f"색상과 값: {[(color.name, color.value) for color in Color]}")

    print(f"\n=== 3. IntEnum - 정수와 호환되는 Enum ===")

    class HttpStatus(IntEnum):
        OK = 200
        NOT_FOUND = 404
        INTERNAL_ERROR = 500

    # IntEnum은 정수와 비교 가능
    print(f"HTTP 200 == 200: {HttpStatus.OK == 200}")
    print(f"HTTP 200 < 404: {HttpStatus.OK < HttpStatus.NOT_FOUND}")
    print(f"HTTP 상태 + 1: {HttpStatus.OK + 1}")

    print(f"\n=== 4. Flag Enum - 비트 플래그 ===")

    class Permission(Flag):
        READ = auto()
        WRITE = auto()
        EXECUTE = auto()

    # Flag 조합
    combined_permission = Permission.READ | Permission.WRITE
    print(f"읽기+쓰기 권한: {combined_permission}")
    print(f"실행 권한 포함 여부: {Permission.EXECUTE in combined_permission}")
    print(f"읽기 권한 포함 여부: {Permission.READ in combined_permission}")

    # 모든 권한
    all_permissions = Permission.READ | Permission.WRITE | Permission.EXECUTE
    print(f"모든 권한: {all_permissions}")

    print(f"\n=== 5. 실전 활용 예제 ===")

    # 1. 게임 캐릭터 상태 시스템
    class GameState(Enum):
        MAIN_MENU = "main_menu"
        PLAYING = "playing"
        PAUSED = "paused"
        GAME_OVER = "game_over"
        SETTINGS = "settings"

    class PlayerAction(Enum):
        MOVE_UP = "move_up"
        MOVE_DOWN = "move_down"
        MOVE_LEFT = "move_left"
        MOVE_RIGHT = "move_right"
        ATTACK = "attack"
        DEFEND = "defend"
        USE_ITEM = "use_item"

    class GameEngine:
        def __init__(self):
            self.state = GameState.MAIN_MENU
            self.score = 0
            self.valid_transitions = {
                GameState.MAIN_MENU: [GameState.PLAYING, GameState.SETTINGS],
                GameState.PLAYING: [GameState.PAUSED, GameState.GAME_OVER],
                GameState.PAUSED: [GameState.PLAYING, GameState.MAIN_MENU],
                GameState.GAME_OVER: [GameState.MAIN_MENU],
                GameState.SETTINGS: [GameState.MAIN_MENU]
            }

        def change_state(self, new_state: GameState) -> bool:
            """상태 전환 (유효성 검사 포함)"""
            if new_state in self.valid_transitions.get(self.state, []):
                old_state = self.state
                self.state = new_state
                print(f"상태 변경: {old_state.value} → {new_state.value}")
                return True
            else:
                print(f"❌ 잘못된 상태 전환: {self.state.value} → {new_state.value}")
                return False

        def handle_action(self, action: PlayerAction):
            """플레이어 액션 처리"""
            if self.state == GameState.PLAYING:
                print(f"🎮 액션 실행: {action.value}")
                if action == PlayerAction.ATTACK:
                    self.score += 10
            else:
                print(f"⏸️  현재 상태({self.state.value})에서는 액션 불가")

    # 게임 엔진 테스트
    game = GameEngine()
    print("게임 상태 시스템 테스트:")

    game.change_state(GameState.PLAYING)  # 성공
    game.handle_action(PlayerAction.ATTACK)  # 성공
    game.change_state(GameState.SETTINGS)  # 실패 (PLAYING → SETTINGS 불가)
    game.change_state(GameState.PAUSED)  # 성공
    game.handle_action(PlayerAction.MOVE_UP)  # 실패 (PAUSED 상태)

    print(f"최종 점수: {game.score}")

    # 2. API 응답 상태 관리
    class ApiResponseStatus(Enum):
        SUCCESS = "success"
        ERROR = "error"
        WARNING = "warning"
        PENDING = "pending"

    class ErrorType(Enum):
        VALIDATION_ERROR = "validation_error"
        AUTHENTICATION_ERROR = "authentication_error"
        PERMISSION_ERROR = "permission_error"
        SERVER_ERROR = "server_error"
        NETWORK_ERROR = "network_error"

    def create_api_response(status: ApiResponseStatus, data: Any = None,
                            error_type: ErrorType = None, message: str = None):
        """API 응답 생성"""
        response = {
            "status": status.value,
            "timestamp": "2024-08-10T15:30:45Z"
        }

        if status == ApiResponseStatus.SUCCESS:
            response["data"] = data
        elif status == ApiResponseStatus.ERROR:
            response["error"] = {
                "type": error_type.value if error_type else None,
                "message": message
            }
        elif status == ApiResponseStatus.WARNING:
            response["data"] = data
            response["warning"] = message

        return response

    # API 응답 예제
    print(f"\nAPI 응답 예제:")

    success_response = create_api_response(
        ApiResponseStatus.SUCCESS,
        {"users": ["김철수", "박영희"]}
    )
    print(f"성공 응답: {success_response}")

    error_response = create_api_response(
        ApiResponseStatus.ERROR,
        error_type=ErrorType.VALIDATION_ERROR,
        message="이메일 형식이 올바르지 않습니다"
    )
    print(f"오류 응답: {error_response}")

    # 3. 설정 관리 시스템
    class Environment(Enum):
        DEVELOPMENT = "dev"
        TESTING = "test"
        STAGING = "staging"
        PRODUCTION = "prod"

    class LogLevel(IntEnum):
        DEBUG = 10
        INFO = 20
        WARNING = 30
        ERROR = 40
        CRITICAL = 50

    class ConfigManager:
        def __init__(self, env: Environment):
            self.environment = env
            self.config = self._load_config()

        def _load_config(self) -> Dict[str, Any]:
            """환경별 설정 로드"""
            base_config = {
                "app_name": "MyApp",
                "version": "1.0.0"
            }

            env_configs = {
                Environment.DEVELOPMENT: {
                    **base_config,
                    "debug": True,
                    "log_level": LogLevel.DEBUG,
                    "database_url": "sqlite:///dev.db"
                },
                Environment.TESTING: {
                    **base_config,
                    "debug": True,
                    "log_level": LogLevel.WARNING,
                    "database_url": "sqlite:///test.db"
                },
                Environment.PRODUCTION: {
                    **base_config,
                    "debug": False,
                    "log_level": LogLevel.ERROR,
                    "database_url": "postgresql://prod.db"
                }
            }

            return env_configs.get(self.environment, base_config)

        def get_log_level(self) -> LogLevel:
            return self.config["log_level"]

        def should_log(self, level: LogLevel) -> bool:
            return level.value >= self.get_log_level().value

    # 설정 관리 테스트
    print(f"\n설정 관리 시스템:")

    for env in [Environment.DEVELOPMENT, Environment.PRODUCTION]:
        config = ConfigManager(env)
        print(f"{env.value} 환경:")
        print(f"  로그 레벨: {config.get_log_level().name}")
        print(f"  DEBUG 로그 출력: {config.should_log(LogLevel.DEBUG)}")
        print(f"  ERROR 로그 출력: {config.should_log(LogLevel.ERROR)}")


demonstrate_enum()
