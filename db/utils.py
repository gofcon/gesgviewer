"""
DB 계층 공통 유틸리티
서비스 레이어에서 반복되는 페이지네이션 / upsert / delete / 콤보값 조회 패턴을 추출.
"""
from __future__ import annotations

from typing import Any


def paginate(q, page: int, page_size: int) -> tuple[list, int]:
    """페이지네이션 적용 후 (rows, total) 반환."""
    total = q.count()
    rows = q.offset((page - 1) * page_size).limit(page_size).all()
    return rows, total


def upsert(session, model_cls, pk: Any, data: dict) -> None:
    """pk로 조회 후 있으면 필드 업데이트, 없으면 신규 삽입 후 commit."""
    row = session.get(model_cls, pk)
    if row:
        for k, v in data.items():
            if hasattr(row, k):
                setattr(row, k, v)
    else:
        session.add(model_cls(**data))
    session.commit()


def delete_by_pk(session, model_cls, pk: Any) -> bool:
    """pk로 조회 후 있으면 삭제. 삭제 시 True, 없으면 False 반환."""
    row = session.get(model_cls, pk)
    if row:
        session.delete(row)
        session.commit()
        return True
    return False


def distinct_values(session, column, extra_filter=None) -> list:
    """특정 컬럼의 DISTINCT 값을 오름차순으로 반환."""
    q = session.query(column).distinct()
    if extra_filter is not None:
        q = q.filter(extra_filter)
    return [r[0] for r in q.order_by(column).all()]


def query_all(q) -> list:
    """페이지네이션 없이 쿼리 전체 결과 반환 (export / chart 용)."""
    return q.all()
