"""
산출결과 서비스
1. 할인율   : IrDcntRateBiz (E_IR_DCNT_RATE_BIZ), IrDcntSceSto (E_IR_DCNT_SCE_STO_BIZ)
2. 기업부도율 : RcCorpPdBiz (E_RC_CORP_PD_BIZ), RcCorpPd (E_RC_CORP_PD)
"""
from db.database import get_session
from db.models.dcnt_rate  import IrDcntRateBiz, IrDcntSceSto
from db.models.ir_param_sw import IrParamSwUsr
from db.utils import paginate, distinct_values, query_all


class DcntRateService:
    # ─── 시나리오 번호 목록 ─────────────────────────────────────
    @staticmethod
    def get_sce_no_list(appl_biz_dv: str = "", ir_curve_id: str = "",
                        base_yymm: str = "") -> list[dict]:
        with get_session() as session:
            q = session.query(
                IrParamSwUsr.ir_curve_sce_no,
                IrParamSwUsr.ir_curve_sce_nm,
            ).distinct()
            if appl_biz_dv:
                q = q.filter(IrParamSwUsr.appl_biz_dv == appl_biz_dv)
            if ir_curve_id:
                q = q.filter(IrParamSwUsr.ir_curve_id == ir_curve_id)
            if base_yymm:
                q = q.filter(IrParamSwUsr.appl_st_yymm <= base_yymm,
                              IrParamSwUsr.appl_ed_yymm >= base_yymm)
            rows = q.order_by(IrParamSwUsr.ir_curve_sce_no).all()
            return [{"ir_curve_sce_no": r[0], "ir_curve_sce_nm": r[1]} for r in rows]

    # ─── 할인율 비즈 목록 ───────────────────────────────────────
    @staticmethod
    def get_dcnt_rate_biz_list(base_yymm: str = "", appl_biz_dv: str = "",
                               ir_curve_id: str = "", ir_curve_sce_no: int | None = None,
                               page: int = 1, page_size: int = 20) -> tuple[list[dict], int]:
        with get_session() as session:
            q = session.query(IrDcntRateBiz)
            if base_yymm:
                q = q.filter(IrDcntRateBiz.base_yymm == base_yymm)
            if appl_biz_dv:
                q = q.filter(IrDcntRateBiz.appl_biz_dv == appl_biz_dv)
            if ir_curve_id:
                q = q.filter(IrDcntRateBiz.ir_curve_id == ir_curve_id)
            if ir_curve_sce_no is not None:
                q = q.filter(IrDcntRateBiz.ir_curve_sce_no == ir_curve_sce_no)
            rows, total = paginate(q.order_by(IrDcntRateBiz.mat_cd), page, page_size)
            return ([{
                "base_yymm":       r.base_yymm,
                "appl_biz_dv":     r.appl_biz_dv,
                "ir_curve_id":     r.ir_curve_id,
                "ir_curve_sce_no": r.ir_curve_sce_no,
                "mat_cd":          r.mat_cd,
                "spot_rate":       float(r.spot_rate) if r.spot_rate is not None else None,
                "fwd_rate":        float(r.fwd_rate)  if r.fwd_rate  is not None else None,
            } for r in rows], total)

    @staticmethod
    def get_dcnt_rate_biz_all(base_yymm: str = "", appl_biz_dv: str = "",
                              ir_curve_id: str = "") -> list[dict]:
        with get_session() as session:
            q = session.query(IrDcntRateBiz)
            if base_yymm:
                q = q.filter(IrDcntRateBiz.base_yymm == base_yymm)
            if appl_biz_dv:
                q = q.filter(IrDcntRateBiz.appl_biz_dv == appl_biz_dv)
            if ir_curve_id:
                q = q.filter(IrDcntRateBiz.ir_curve_id == ir_curve_id)
            rows = query_all(q.order_by(IrDcntRateBiz.mat_cd))
            return [{
                "base_yymm":       r.base_yymm,
                "appl_biz_dv":     r.appl_biz_dv,
                "ir_curve_id":     r.ir_curve_id,
                "ir_curve_sce_no": r.ir_curve_sce_no,
                "mat_cd":          r.mat_cd,
                "spot_rate":       float(r.spot_rate) if r.spot_rate is not None else None,
                "fwd_rate":        float(r.fwd_rate)  if r.fwd_rate  is not None else None,
            } for r in rows]

    # ─── 할인율 시나리오 저장 목록 ─────────────────────────────
    @staticmethod
    def get_dcnt_sto_biz_list(base_yymm: str = "", appl_biz_dv: str = "",
                              ir_curve_id: str = "",
                              page: int = 1, page_size: int = 20) -> tuple[list[dict], int]:
        with get_session() as session:
            q = session.query(IrDcntSceSto)
            if base_yymm:
                q = q.filter(IrDcntSceSto.base_yymm == base_yymm)
            if appl_biz_dv:
                q = q.filter(IrDcntSceSto.appl_biz_dv == appl_biz_dv)
            if ir_curve_id:
                q = q.filter(IrDcntSceSto.ir_curve_id == ir_curve_id)
            rows, total = paginate(
                q.order_by(IrDcntSceSto.ir_curve_sce_no, IrDcntSceSto.sce_no),
                page, page_size)
            return ([{
                "base_yymm":       r.base_yymm,
                "appl_biz_dv":     r.appl_biz_dv,
                "ir_curve_id":     r.ir_curve_id,
                "ir_curve_sce_no": r.ir_curve_sce_no,
                "sce_no":          r.sce_no,
                "mat_cd":          r.mat_cd,
                "spot_rate":       float(r.spot_rate) if r.spot_rate is not None else None,
                "fwd_rate":        float(r.fwd_rate)  if r.fwd_rate  is not None else None,
            } for r in rows], total)

    # ─── 콤보 코드 ──────────────────────────────────────────────
    @staticmethod
    def get_appl_biz_dv_list() -> list[str]:
        with get_session() as session:
            return distinct_values(session, IrDcntRateBiz.appl_biz_dv)

    @staticmethod
    def get_ir_curve_id_list() -> list[str]:
        with get_session() as session:
            return distinct_values(session, IrDcntRateBiz.ir_curve_id)
