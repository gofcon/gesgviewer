"""
Hull-White 파라미터 서비스
Spring: ParamHwServiceImpl → Python 포팅
"""
from db.database import get_session
from db.models.ir_param_hw import IrParamHwCalc, IrParamHwBiz
from db.utils import paginate, distinct_values, query_all


class ParamHwService:
    # ─── 콤보박스용 코드 조회 ─────────────────────────────────
    @staticmethod
    def get_ir_curve_id_list() -> list[str]:
        with get_session() as session:
            return distinct_values(session, IrParamHwCalc.ir_curve_id)

    @staticmethod
    def get_ir_model_id_list() -> list[str]:
        with get_session() as session:
            return distinct_values(session, IrParamHwBiz.ir_model_id)

    @staticmethod
    def get_appl_biz_dv_list() -> list[str]:
        with get_session() as session:
            return distinct_values(session, IrParamHwBiz.appl_biz_dv)

    # ─── HW Calc 목록 ─────────────────────────────────────────
    @staticmethod
    def get_param_hw_calc_list(base_yymm: str = "", ir_curve_id: str = "",
                               page: int = 1, page_size: int = 20) -> tuple[list[dict], int]:
        with get_session() as session:
            q = session.query(IrParamHwCalc)
            if base_yymm:
                q = q.filter(IrParamHwCalc.base_yymm == base_yymm)
            if ir_curve_id:
                q = q.filter(IrParamHwCalc.ir_curve_id == ir_curve_id)
            rows, total = paginate(
                q.order_by(IrParamHwCalc.ir_model_id, IrParamHwCalc.mat_cd), page, page_size)
            return ([{
                "base_yymm":    r.base_yymm,
                "ir_model_id":  r.ir_model_id,
                "ir_curve_id":  r.ir_curve_id,
                "mat_cd":       r.mat_cd,
                "param_typ_cd": r.param_typ_cd,
                "param_val":    float(r.param_val) if r.param_val is not None else None,
                "last_modified_by":  r.last_modified_by,
                "last_update_date":  str(r.last_update_date) if r.last_update_date else "",
            } for r in rows], total)

    @staticmethod
    def get_param_hw_calc_all(base_yymm: str = "", ir_curve_id: str = "") -> list[dict]:
        """Excel 내보내기용 전체 조회"""
        with get_session() as session:
            q = session.query(IrParamHwCalc)
            if base_yymm:
                q = q.filter(IrParamHwCalc.base_yymm == base_yymm)
            if ir_curve_id:
                q = q.filter(IrParamHwCalc.ir_curve_id == ir_curve_id)
            rows = query_all(q.order_by(IrParamHwCalc.ir_model_id, IrParamHwCalc.mat_cd))
            return [{
                "base_yymm":    r.base_yymm,
                "ir_model_id":  r.ir_model_id,
                "ir_curve_id":  r.ir_curve_id,
                "mat_cd":       r.mat_cd,
                "param_typ_cd": r.param_typ_cd,
                "param_val":    float(r.param_val) if r.param_val is not None else None,
                "last_modified_by":  r.last_modified_by,
                "last_update_date":  str(r.last_update_date) if r.last_update_date else "",
            } for r in rows]

    # ─── HW Chart 데이터 ────────────────────────────────────────
    @staticmethod
    def get_param_hw_chart_list(base_yymm: str = "", ir_curve_id: str = "",
                                ir_model_id: str = "") -> list[dict]:
        with get_session() as session:
            q = session.query(IrParamHwCalc)
            if base_yymm:
                q = q.filter(IrParamHwCalc.base_yymm == base_yymm)
            if ir_curve_id:
                q = q.filter(IrParamHwCalc.ir_curve_id == ir_curve_id)
            if ir_model_id:
                q = q.filter(IrParamHwCalc.ir_model_id == ir_model_id)
            rows = query_all(q.order_by(IrParamHwCalc.mat_cd))
            return [{
                "base_yymm":    r.base_yymm,
                "mat_cd":       r.mat_cd,
                "param_typ_cd": r.param_typ_cd,
                "param_val":    float(r.param_val) if r.param_val is not None else 0.0,
            } for r in rows]

    # ─── HW Biz 목록 ─────────────────────────────────────────
    @staticmethod
    def get_param_hw_biz_list(base_yymm: str = "", appl_biz_dv: str = "",
                              ir_model_id: str = "", ir_curve_id: str = "",
                              page: int = 1, page_size: int = 20) -> tuple[list[dict], int]:
        with get_session() as session:
            q = session.query(IrParamHwBiz)
            if base_yymm:
                q = q.filter(IrParamHwBiz.base_yymm == base_yymm)
            if appl_biz_dv:
                q = q.filter(IrParamHwBiz.appl_biz_dv == appl_biz_dv)
            if ir_model_id:
                q = q.filter(IrParamHwBiz.ir_model_id == ir_model_id)
            if ir_curve_id:
                q = q.filter(IrParamHwBiz.ir_curve_id == ir_curve_id)
            rows, total = paginate(
                q.order_by(IrParamHwBiz.ir_model_id, IrParamHwBiz.mat_cd), page, page_size)
            return ([{
                "base_yymm":    r.base_yymm,
                "appl_biz_dv":  r.appl_biz_dv,
                "ir_model_id":  r.ir_model_id,
                "ir_curve_id":  r.ir_curve_id,
                "mat_cd":       r.mat_cd,
                "param_typ_cd": r.param_typ_cd,
                "param_val":    float(r.param_val) if r.param_val is not None else None,
            } for r in rows], total)
