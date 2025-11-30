'''
데이터베이스 모델 및 세션 관리 모듈
SQLAlchemy 2.0 스타일 사용
'''

from datetime import datetime
from typing import Optional

from sqlalchemy import (
    create_engine,
    String,
    Integer,
    DateTime,
    Index,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    sessionmaker,
    scoped_session,
)


# ====== Base 클래스 정의 (SQLAlchemy 2.0 스타일) ======
class Base(DeclarativeBase):
    '''모든 ORM 모델의 기본 클래스'''
    pass


# ====== ORM 모델 정의 ======
class ParmData(Base):
    '''
    스마트 팜 센서 데이터 테이블

    Attributes:
        data_id: 자동 증가 PRIMARY KEY
        sensor_name: 센서 고유 이름 (Farm-1~5)
        input_time: 데이터 입력 시간
        temperature: 온도 (20~30)
        illuminance: 조도 (5000~10000)
        humidity: 습도 (40~70)
    '''
    __tablename__ = 'parm_data'

    # 타입 힌트와 함께 컬럼 정의 (SQLAlchemy 2.0 필수)
    data_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment='데이터 고유 ID'
    )

    sensor_name: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        comment='센서 고유 이름 (Farm-1~5)'
    )

    input_time: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        comment='데이터 입력 시간'
    )

    temperature: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment='온도 (20~30)'
    )

    illuminance: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment='조도 (5000~10000)'
    )

    humidity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment='습도 (40~70)'
    )

    # 테이블 레벨 설정
    __table_args__ = (
        # 복합 인덱스: 센서별 시간 역순 조회 최적화
        Index('idx_sensor_time', 'sensor_name', 'input_time'),
        {
            'mysql_engine': 'InnoDB',
            'mysql_charset': 'utf8mb4',
            'mysql_collate': 'utf8mb4_unicode_ci',
            'comment': '스마트 팜 센서 데이터 저장 테이블'
        }
    )

    def __repr__(self) -> str:
        '''디버깅용 문자열 표현'''
        return (f'<ParmData(id={self.data_id}, sensor={self.sensor_name}, '
                f'time={self.input_time}, temp={self.temperature})>')


# ====== 데이터베이스 엔진 및 세션 설정 ======
class DatabaseConfig:
    '''데이터베이스 설정 및 세션 관리 클래스'''

    # 데이터베이스 연결 URL (환경 변수로 분리 권장)
    DB_URL = (
        'mysql+pymysql://ohgiraffers:ohgiraffers@localhost:3306/menudb'
        '?charset=utf8mb4'
    )

    # Connection Pool 설정
    POOL_SIZE = 5  # 센서 개수와 동일
    MAX_OVERFLOW = 2  # 추가로 생성 가능한 연결 수
    POOL_RECYCLE = 3600  # 1시간마다 연결 재생성 (MySQL 8시간 타임아웃 대비)
    POOL_PRE_PING = True  # 연결 사용 전 헬스체크

    def __init__(self):
        '''엔진 및 세션 팩토리 초기화'''
        # Engine 생성: Connection Pool 자동 관리
        self.engine = create_engine(
            self.DB_URL,
            pool_size=self.POOL_SIZE,
            max_overflow=self.MAX_OVERFLOW,
            pool_recycle=self.POOL_RECYCLE,
            pool_pre_ping=self.POOL_PRE_PING,
            echo=False,  # True 설정 시 모든 SQL 로깅 (디버깅용)
        )

        # Session Factory 생성
        session_factory = sessionmaker(
            bind=self.engine,
            autocommit=False,  # 명시적 트랜잭션 관리
            autoflush=False,  # 성능 최적화 (필요 시만 flush)
            expire_on_commit=True  # 커밋 후 객체 상태 만료
        )

        # Scoped Session: 스레드마다 독립적인 세션 보장
        self.Session = scoped_session(session_factory)

    def create_tables(self):
        '''테이블 생성 (없을 경우에만)'''
        Base.metadata.create_all(self.engine)
        print(f'테이블 생성 완료: {list(Base.metadata.tables.keys())}')

    def drop_tables(self):
        '''모든 테이블 삭제 (주의: 데이터 손실)'''
        Base.metadata.drop_all(self.engine)
        print('모든 테이블 삭제 완료')

    def get_session(self):
        '''
        스레드 안전한 세션 반환

        Returns:
            scoped_session: 현재 스레드의 세션
        '''
        return self.Session()

    def remove_session(self):
        '''현재 스레드의 세션 제거 (스레드 종료 시 호출)'''
        self.Session.remove()

    def dispose_engine(self):
        '''엔진 종료 (프로그램 종료 시 호출)'''
        self.engine.dispose()
        print('엔진 종료 완료')


# ====== 전역 Database 인스턴스 ======
db_config = DatabaseConfig()
