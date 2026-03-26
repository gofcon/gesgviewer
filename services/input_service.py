"""
사용자 입력 서비스 — 사용자가 직접 입력하는 _USR 테이블
1. 금리정보  : IrCurveYtmUsr (E_IR_CURVE_YTM_USR)
2. 금리스프레드: SprdCurve (E_IR_SPRD_CURVE)
3. 매개변수  : IrParamSwUsr (E_IR_PARAM_SW_USR)
"""
from db.database import get_session
from db.models.ir_curve    import IrCurve, IrCurveYtmUsr
from db.models.ir_param_sw import IrParamSwUsr
from db.models.sprd_curve  import SprdCurve
from db.utils import paginate, upsert, delete_by_pk


class IrCurveInputService:
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
                "ytm":         float(r.ytm) if r.ytm is not None else None,
            } for r in rows], total)

    @staticmethod
    def save_ytm_usr(data: dict) -> None:
        with get_session() as session:
            pk = (data["base_date"], data["ir_curve_id"], data["mat_cd"])
            row = session.get(IrCurveYtmUsr, pk)
            if row:
                row.ytm = data.get("ytm")
            else:
                session.add(IrCurveYtmUsr(**{k: v for k, v in data.items()
                                             if hasattr(IrCurveYtmUsr, k)}))
            session.commit()

    @staticmethod
    def delete_ytm_usr(base_date: str, ir_curve_id: str, mat_cd: str) -> None:
        with get_session() as session:
            delete_by_pk(session, IrCurveYtmUsr, (base_date, ir_curve_id, mat_cd))

    # ─── 커브 ID 드롭다운 ────────────────────────────────────────
    @staticmethod
    def get_ir_curve_id_options() -> list[str]:
        with get_session() as session:
            rows = session.query(IrCurve.ir_curve_id)\
                          .filter(IrCurve.use_yn == "Y")\
                          .order_by(IrCurve.ir_curve_id).all()
            return [r[0] for r in rows]


class ParamSwInputService:
    # ─── SW 사용자 파라미터 목록 ────────────────────────────────
    @staticmethod
    def get_sw_usr_list(appl_st_yymm: str = "", appl_biz_dv: str = "",
                        ir_curve_id: str = "",
                        page: int = 1, page_size: int = 20) -> tuple[list[dict], int]:
        with get_session() as session:
            q = session.query(IrParamSwUsr)
            if appl_st_yymm:
                q = q.filter(IrParamSwUsr.appl_st_yymm == appl_st_yymm)
            if appl_biz_dv:
                q = q.filter(IrParamSwUsr.appl_biz_dv == appl_biz_dv)
            if ir_curve_id:
                q = q.filter(IrParamSwUsr.ir_curve_id == ir_curve_id)
            rows, total = paginate(
                q.order_by(IrParamSwUsr.appl_st_yymm, IrParamSwUsr.appl_biz_dv), page, page_size)
            return ([_sw_usr_to_dict(r) for r in rows], total)

    @staticmethod
    def save_sw_usr(data: dict) -> None:
        with get_session() as session:
            pk = (data["appl_st_yymm"], data["appl_biz_dv"],
                  data["ir_curve_id"], int(data["ir_curve_sce_no"]))
            upsert(session, IrParamSwUsr, pk, data)

    @staticmethod
    def delete_sw_usr(appl_st_yymm: str, appl_biz_dv: str,
                      ir_curve_id: str, ir_curve_sce_no: int) -> None:
        with get_session() as session:
            delete_by_pk(session, IrParamSwUsr,
                         (appl_st_yymm, appl_biz_dv, ir_curve_id, ir_curve_sce_no))


class SprdInputService:
    # ─── 위험스프레드 커브 목록 ─────────────────────────────────
    @staticmethod
    def get_sprd_curve_list(base_yymm: str = "", ir_curve_id: str = "",
                            page: int = 1, page_size: int = 20) -> tuple[list[dict], int]:
        with get_session() as session:
            q = session.query(SprdCurve)
            if base_yymm:
                q = q.filter(SprdCurve.base_yymm == base_yymm)
            if ir_curve_id:
                q = q.filter(SprdCurve.ir_curve_id == ir_curve_id)
            rows, total = paginate(q.order_by(SprdCurve.mat_cd), page, page_size)
            return ([{
                "base_yymm":    r.base_yymm,
                "ir_curve_id":  r.ir_curve_id,
                "ir_typ_dv_cd": r.ir_typ_dv_cd,
                "mat_cd":       r.mat_cd,
                "int_rate":     float(r.int_rate)  if r.int_rate  is not None else None,
                "crd_sprd":     float(r.crd_sprd)  if r.crd_sprd  is not None else None,
            } for r in rows], total)


def _sw_usr_to_dict(r: IrParamSwUsr) -> dict:
    return {
        "appl_st_yymm":    r.appl_st_yymm,
        "appl_ed_yymm":    r.appl_ed_yymm,
        "appl_biz_dv":     r.appl_biz_dv,
        "ir_curve_id":     r.ir_curve_id,
        "ir_curve_sce_no": r.ir_curve_sce_no,
        "ir_curve_sce_nm": r.ir_curve_sce_nm,
        "cur_cd":          r.cur_cd,
        "freq":            r.freq,
        "llp":             r.llp,
        "ltfr":            float(r.ltfr)         if r.ltfr         is not None else None,
        "ltfr_cp":         r.ltfr_cp,
        "liq_prem":        float(r.liq_prem)     if r.liq_prem     is not None else None,
        "liq_prem_appl_dv":r.liq_prem_appl_dv,
        "shk_sprd_sce_no": r.shk_sprd_sce_no,
        "sw_alpha_ytm":    float(r.sw_alpha_ytm) if r.sw_alpha_ytm is not None else None,
        "sto_sce_gen_yn":  r.sto_sce_gen_yn,
        "fwd_mat_cd":      r.fwd_mat_cd,
        "mult_int_rate":   float(r.mult_int_rate) if r.mult_int_rate is not None else None,
        "add_sprd":        float(r.add_sprd)      if r.add_sprd      is not None else None,
        "last_modified_by":r.last_modified_by,
        "last_update_date":str(r.last_update_date) if r.last_update_date else "",
    }
