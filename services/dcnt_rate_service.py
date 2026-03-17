"""
할인율 서비스
Spring: DcntRateBizServiceImpl, DcntStoBizServiceImpl → Python 포팅
"""
from db.database import get_session
from db.models.dcnt_rate import IrDcntRateBiz, IrDcntStoBiz
from db.models.ir_param_sw import IrParamSwUsr


class DcntRateService:
    # ─── 시나리오 번호 목록 (날짜 범위 필터) ───────────────────
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
            total = q.count()
            rows = q.order_by(IrDcntRateBiz.mat_cd)\
                    .offset((page - 1) * page_size).limit(page_size).all()
            return ([{
                "base_yymm":       r.base_yymm,
                "appl_biz_dv":     r.appl_biz_dv,
                "ir_curve_id":     r.ir_curve_id,
                "ir_curve_sce_no": r.ir_curve_sce_no,
                "mat_cd":          r.mat_cd,
                "dcnt_rate":       float(r.dcnt_rate) if r.dcnt_rate is not None else None,
                "spot_rate":       float(r.spot_rate) if r.spot_rate is not None else None,
                "fwd_rate":        float(r.fwd_rate)  if r.fwd_rate  is not None else None,
            } for r in rows], total)

    @staticmethod
    def get_dcnt_rate_biz_all(base_yymm: str = "", appl_biz_dv: str = "",
                              ir_curve_id: str = "") -> list[dict]:
        rows, _ = DcntRateService.get_dcnt_rate_biz_list(
            base_yymm=base_yymm, appl_biz_dv=appl_biz_dv,
            ir_curve_id=ir_curve_id, page=1, page_size=999999)
        return rows

    # ─── 할인율 시나리오 저장 목록 ─────────────────────────────
    @staticmethod
    def get_dcnt_sto_biz_list(base_yymm: str = "", appl_biz_dv: str = "",
                              ir_curve_id: str = "",
                              page: int = 1, page_size: int = 20) -> tuple[list[dict], int]:
        with get_session() as session:
            q = session.query(IrDcntStoBiz)
            if base_yymm:
                q = q.filter(IrDcntStoBiz.base_yymm == base_yymm)
            if appl_biz_dv:
                q = q.filter(IrDcntStoBiz.appl_biz_dv == appl_biz_dv)
            if ir_curve_id:
                q = q.filter(IrDcntStoBiz.ir_curve_id == ir_curve_id)
            total = q.count()
            rows = q.order_by(IrDcntStoBiz.ir_curve_sce_no, IrDcntStoBiz.sce_path_no)\
                    .offset((page - 1) * page_size).limit(page_size).all()
            return ([{
                "base_yymm":       r.base_yymm,
                "appl_biz_dv":     r.appl_biz_dv,
                "ir_curve_id":     r.ir_curve_id,
                "ir_curve_sce_no": r.ir_curve_sce_no,
                "sce_path_no":     r.sce_path_no,
                "mat_cd":          r.mat_cd,
                "rate_val":        float(r.rate_val) if r.rate_val is not None else None,
            } for r in rows], total)

    # ─── 콤보 코드 ──────────────────────────────────────────────
    @staticmethod
    def get_appl_biz_dv_list() -> list[str]:
        with get_session() as session:
            rows = session.query(IrDcntRateBiz.appl_biz_dv)\
                          .distinct().order_by(IrDcntRateBiz.appl_biz_dv).all()
            return [r[0] for r in rows]

    @staticmethod
    def get_ir_curve_id_list() -> list[str]:
        with get_session() as session:
            rows = session.query(IrDcntRateBiz.ir_curve_id)\
                          .distinct().order_by(IrDcntRateBiz.ir_curve_id).all()
            return [r[0] for r in rows]
