"""
기초데이터 서비스 — 계산된 기준 데이터
1. 금리정보  : IrCurveSpot (E_IR_CURVE_SPOT)
2. 금리스프레드: SprdAfnsBiz (E_IR_SPRD_AFNS_BIZ)
3. Swap변동성 : IrVolSwpn (E_IR_VOL_SWPN)
4. 매개변수  : IrParamHwCalc, IrParamHwBiz (E_IR_PARAM_HW_CALC/BIZ)
              IrParamAfnsBiz (E_IR_PARAM_AFNS_BIZ)
              IrParamModel (E_IR_PARAM_MODEL)
"""
from db.database import get_session
from db.models.ir_curve      import IrCurve, IrCurveSpot
from db.models.ir_param_hw   import IrParamHwCalc, IrParamHwBiz
from db.models.ir_param_model import IrParamModel, IrParamAfnsBiz, IrVolSwpn
from db.models.sprd_curve    import SprdAfnsBiz
from db.utils import paginate, upsert, delete_by_pk, distinct_values, query_all


class IrCurveBaseService:
    # ─── 금리 커브 현물 목록 ────────────────────────────────────
    @staticmethod
    def get_ir_curve_list(ir_curve_id: str = "", base_yymm: str = "",
                          page: int = 1, page_size: int = 20) -> tuple[list[dict], int]:
        with get_session() as session:
            q = session.query(IrCurveSpot)
            if base_yymm:
                q = q.filter(IrCurveSpot.base_date.like(f"{base_yymm}%"))
            if ir_curve_id:
                q = q.filter(IrCurveSpot.ir_curve_id == ir_curve_id)
            rows, total = paginate(
                q.order_by(IrCurveSpot.base_date, IrCurveSpot.mat_cd), page, page_size)
            return ([{
                "base_date":   r.base_date,
                "ir_curve_id": r.ir_curve_id,
                "mat_cd":      r.mat_cd,
                "spot_rate":   float(r.spot_rate) if r.spot_rate is not None else None,
            } for r in rows], total)

    # ─── 커브 ID 드롭다운 (use_yn 기준) ─────────────────────────
    @staticmethod
    def get_ir_curve_id_options() -> list[str]:
        with get_session() as session:
            rows = session.query(IrCurve.ir_curve_id)\
                          .filter(IrCurve.use_yn == "Y")\
                          .order_by(IrCurve.ir_curve_id).all()
            return [r[0] for r in rows]


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
                "base_yymm":        r.base_yymm,
                "ir_model_id":      r.ir_model_id,
                "ir_curve_id":      r.ir_curve_id,
                "mat_cd":           r.mat_cd,
                "param_typ_cd":     r.param_typ_cd,
                "param_val":        float(r.param_val) if r.param_val is not None else None,
                "last_modified_by": r.last_modified_by,
                "last_update_date": str(r.last_update_date) if r.last_update_date else "",
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
                "base_yymm":        r.base_yymm,
                "ir_model_id":      r.ir_model_id,
                "ir_curve_id":      r.ir_curve_id,
                "mat_cd":           r.mat_cd,
                "param_typ_cd":     r.param_typ_cd,
                "param_val":        float(r.param_val) if r.param_val is not None else None,
                "last_modified_by": r.last_modified_by,
                "last_update_date": str(r.last_update_date) if r.last_update_date else "",
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


class ParamBaseService:
    # ─── 파라미터 모델 관리 ─────────────────────────────────────
    @staticmethod
    def get_param_model_list(page: int = 1, page_size: int = 20) -> tuple[list[dict], int]:
        with get_session() as session:
            q = session.query(IrParamModel)
            rows, total = paginate(q.order_by(IrParamModel.ir_model_id), page, page_size)
            return ([{
                "ir_model_id": r.ir_model_id,
                "ir_curve_id": r.ir_curve_id,
                "ir_model_nm": r.ir_model_nm,
                "use_yn":      r.use_yn,
            } for r in rows], total)

    @staticmethod
    def save_param_model(data: dict) -> None:
        with get_session() as session:
            upsert(session, IrParamModel, (data["ir_model_id"], data["ir_curve_id"]), data)

    @staticmethod
    def delete_param_model(ir_model_id: str, ir_curve_id: str) -> None:
        with get_session() as session:
            delete_by_pk(session, IrParamModel, (ir_model_id, ir_curve_id))

    # ─── AFNS 모수생성결과 목록 ─────────────────────────────────
    @staticmethod
    def get_param_afns_list(base_yymm: str = "", ir_model_id: str = "",
                            ir_curve_id: str = "",
                            page: int = 1, page_size: int = 20) -> tuple[list[dict], int]:
        with get_session() as session:
            q = session.query(IrParamAfnsBiz)
            if base_yymm:
                q = q.filter(IrParamAfnsBiz.base_yymm == base_yymm)
            if ir_model_id:
                q = q.filter(IrParamAfnsBiz.ir_model_id == ir_model_id)
            if ir_curve_id:
                q = q.filter(IrParamAfnsBiz.ir_curve_id == ir_curve_id)
            rows, total = paginate(
                q.order_by(IrParamAfnsBiz.ir_model_id, IrParamAfnsBiz.param_typ_cd), page, page_size)
            return ([{
                "base_yymm":    r.base_yymm,
                "ir_model_id":  r.ir_model_id,
                "ir_curve_id":  r.ir_curve_id,
                "param_typ_cd": r.param_typ_cd,
                "param_val":    float(r.param_val) if r.param_val is not None else None,
            } for r in rows], total)

    # ─── 변동성/스왑션 목록 ──────────────────────────────────────
    @staticmethod
    def get_vol_swpn_list(base_yymm: str = "", ir_curve_id: str = "",
                          page: int = 1, page_size: int = 20) -> tuple[list[dict], int]:
        with get_session() as session:
            q = session.query(IrVolSwpn)
            if base_yymm:
                q = q.filter(IrVolSwpn.base_yymm == base_yymm)
            if ir_curve_id:
                q = q.filter(IrVolSwpn.ir_curve_id == ir_curve_id)
            rows, total = paginate(
                q.order_by(IrVolSwpn.swpn_mat_num, IrVolSwpn.swap_ten_num), page, page_size)
            return ([{
                "base_yymm":    r.base_yymm,
                "ir_curve_id":  r.ir_curve_id,
                "swpn_mat_num": float(r.swpn_mat_num),
                "swap_ten_num": float(r.swap_ten_num),
                "vol":          float(r.vol) if r.vol is not None else None,
            } for r in rows], total)


class SprdBaseService:
    # ─── AFNS 충격 스프레드 목록 ────────────────────────────────
    @staticmethod
    def get_sprd_afns_list(base_yymm: str = "", ir_model_id: str = "",
                           ir_curve_id: str = "",
                           page: int = 1, page_size: int = 20) -> tuple[list[dict], int]:
        with get_session() as session:
            q = session.query(SprdAfnsBiz)
            if base_yymm:
                q = q.filter(SprdAfnsBiz.base_yymm == base_yymm)
            if ir_model_id:
                q = q.filter(SprdAfnsBiz.ir_model_id == ir_model_id)
            if ir_curve_id:
                q = q.filter(SprdAfnsBiz.ir_curve_id == ir_curve_id)
            rows, total = paginate(
                q.order_by(SprdAfnsBiz.ir_curve_sce_no, SprdAfnsBiz.mat_cd), page, page_size)
            return ([{
                "base_yymm":        r.base_yymm,
                "ir_model_id":      r.ir_model_id,
                "ir_curve_id":      r.ir_curve_id,
                "ir_curve_sce_no":  r.ir_curve_sce_no,
                "mat_cd":           r.mat_cd,
                "shk_sprd_cont":    float(r.shk_sprd_cont) if r.shk_sprd_cont is not None else None,
            } for r in rows], total)
