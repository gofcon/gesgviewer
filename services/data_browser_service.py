"""
데이터 브라우저 서비스 — SQLite 메타데이터 기반 동적 테이블 조회

ORM 모델 정의 없이 esg.db 내 모든 테이블을 탐색할 수 있도록 지원.
SQLite PRAGMA 와 직접 SQL 을 사용하여 테이블 목록·컬럼·데이터를 반환한다.
"""
from sqlalchemy import text
from db.database import get_session


class DataBrowserService:

    @staticmethod
    def get_table_list() -> list[str]:
        """esg.db 내 모든 사용자 테이블 이름 목록 반환 (sqlite 시스템 테이블 제외)."""
        with get_session() as session:
            result = session.execute(text(
                "SELECT name FROM sqlite_master "
                "WHERE type='table' AND name NOT LIKE 'sqlite_%' "
                "ORDER BY name"
            ))
            return [row[0] for row in result.fetchall()]

    @staticmethod
    def get_columns(table_name: str) -> list[str]:
        """PRAGMA table_info 로 컬럼 이름 목록 반환.
        row 구조: (cid, name, type, notnull, dflt_value, pk)
        """
        with get_session() as session:
            result = session.execute(
                text(f'PRAGMA table_info("{table_name}")')
            )
            return [row[1] for row in result.fetchall()]

    # 기준년월 LIKE 조건을 적용할 추가 날짜 컬럼 (정확한 이름 매칭, 대소문자 무시)
    _DATE_COL_CANDIDATES = ("base_date", "appl_st_date")

    @staticmethod
    def detect_yymm_col(columns: list[str]) -> str:
        """컬럼 목록에서 기준년월/기준일자 컬럼명 자동 탐지.

        우선순위:
          1. 'YYMM' 을 포함하는 첫 번째 컬럼
          2. base_date
          3. appl_st_date
        해당 컬럼이 없으면 빈 문자열 반환.
        """
        # ① YYMM 포함 컬럼 우선
        for col in columns:
            if "YYMM" in col.upper():
                return col
        # ② base_date / appl_st_date (선언 순서대로 우선)
        lower_map = {c.lower(): c for c in columns}
        for candidate in DataBrowserService._DATE_COL_CANDIDATES:
            if candidate in lower_map:
                return lower_map[candidate]
        return ""

    @staticmethod
    def get_data(
        table_name: str,
        page: int = 1,
        page_size: int = 20,
        yymm_col: str = "",
        yymm_like: str = "",
    ) -> tuple[list[dict], int]:
        """테이블 데이터를 페이지네이션하여 (rows, total) 반환.
        yymm_col + yymm_like 가 모두 주어지면 WHERE {col} LIKE '{like}%' 조건 적용.
        """
        with get_session() as session:
            where  = f'WHERE "{yymm_col}" LIKE :yymm' if (yymm_col and yymm_like) else ""
            params: dict = {}
            if where:
                params["yymm"] = f"{yymm_like}%"

            total = session.execute(
                text(f'SELECT COUNT(*) FROM "{table_name}" {where}'),
                params,
            ).scalar() or 0

            offset = (page - 1) * page_size
            data_params = {**params, "lim": page_size, "ofs": offset}
            result = session.execute(
                text(f'SELECT * FROM "{table_name}" {where} LIMIT :lim OFFSET :ofs'),
                data_params,
            )
            cols = list(result.keys())
            rows = [dict(zip(cols, row)) for row in result.fetchall()]
            return rows, total

    @staticmethod
    def get_remaining_data(
        table_name: str,
        offset: int,
        yymm_col: str = "",
        yymm_like: str = "",
    ) -> list[dict]:
        """offset 이후 모든 행 반환 — 필터 적용 전 나머지 데이터 전체 로드용.
        LIMIT -1 은 SQLite 에서 '제한 없음'을 의미한다.
        """
        with get_session() as session:
            where  = f'WHERE "{yymm_col}" LIKE :yymm' if (yymm_col and yymm_like) else ""
            params: dict = {"ofs": offset}
            if where:
                params["yymm"] = f"{yymm_like}%"

            result = session.execute(
                text(f'SELECT * FROM "{table_name}" {where} LIMIT -1 OFFSET :ofs'),
                params,
            )
            cols = list(result.keys())
            return [dict(zip(cols, row)) for row in result.fetchall()]
