"""
금리 커브 서비스
Spring: IrCurveServiceImpl, YtmUsrServiceImpl → Python 포팅
"""
from db.database import get_session
from db.models.ir_curve import IrCurve, IrCurveSpot, IrCurveYtmUsr
from db.utils import paginate, delete_by_pk


class IrCurveService:
    # ─── 금리 커브 목록 ─────────────────────────────────────────
    @staticmethod
    def get_ir_curve_list(ir_curve_id: str = "", base_yymm: str = "",
                          page: int = 1, page_size: int = 20) -> tuple[list[dict], int]:
        with get_session() as session:
            q = session.query(IrCurveSpot)
            if base_yymm:
                q = q.filter(IrCurveSpot.base_yymm == base_yymm)
            if ir_curve_id:
                q = q.filter(IrCurveSpot.ir_curve_id == ir_curve_id)
            rows, total = paginate(
                q.order_by(IrCurveSpot.base_yymm, IrCurveSpot.mat_cd), page, page_size)
            return ([{
                "base_yymm":   r.base_yymm,
                "appl_biz_dv": r.appl_biz_dv,
                "ir_curve_id": r.ir_curve_id,
                "mat_cd":      r.mat_cd,
                "spot_rate":   float(r.spot_rate) if r.spot_rate is not None else None,
                "dcnt_rate":   float(r.dcnt_rate) if r.dcnt_rate is not None else None,
            } for r in rows], total)

    # ─── YTM 사용자 입력 목록 ──────────────────────────────────
    @staticmethod
    def get_ytm_usr_list(base_yymm: str = "", ir_curve_id: str = "",
                         page: int = 1, page_size: int = 20) -> tuple[list[dict], int]:
        with get_session() as session:
            q = session.query(IrCurveYtmUsr)
            if base_yymm:
                q = q.filter(IrCurveYtmUsr.base_date.like(f"{base_yymm}%"))
            if ir_curve_id:
                q = q.filter(IrCurveYtmUsr.ir_curve_id == ir_curve_id)
            rows, total = paginate(
                q.order_by(IrCurveYtmUsr.base_date, IrCurveYtmUsr.mat_cd), page, page_size)
            return ([{
                "base_date":   r.base_date,
                "ir_curve_id": r.ir_curve_id,
                "mat_cd":      r.mat_cd,
                "ytm_rate":    float(r.ytm_rate) if r.ytm_rate is not None else None,
            } for r in rows], total)

    @staticmethod
    def save_ytm_usr(data: dict) -> None:
        with get_session() as session:
            pk = (data["base_date"], data["ir_curve_id"], data["mat_cd"])
            row = session.get(IrCurveYtmUsr, pk)
            if row:
                row.ytm_rate = data.get("ytm_rate")
            else:
                session.add(IrCurveYtmUsr(**data))
            session.commit()

    @staticmethod
    def delete_ytm_usr(base_date: str, ir_curve_id: str, mat_cd: str) -> None:
        with get_session() as session:
            delete_by_pk(session, IrCurveYtmUsr, (base_date, ir_curve_id, mat_cd))

    # ─── 콤보 코드 ──────────────────────────────────────────────
    @staticmethod
    def get_ir_curve_id_options() -> list[str]:
        with get_session() as session:
            rows = session.query(IrCurve.ir_curve_id)\
                          .filter(IrCurve.use_at == "Y")\
                          .order_by(IrCurve.ir_curve_id).all()
            return [r[0] for r in rows]
