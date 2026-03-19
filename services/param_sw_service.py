"""
Smith-Wilson 파라미터 서비스
Spring: SwUsrServiceImpl → Python 포팅
"""
from db.database import get_session
from db.models.ir_param_sw   import IrParamSwUsr, IrParamSw
from db.models.ir_param_model import IrParamModel
from db.models.ir_curve       import IrCurve
from db.utils import paginate, upsert, delete_by_pk


class ParamSwService:
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
                "ir_model_dc": r.ir_model_dc,
                "use_at": r.use_at,
            } for r in rows], total)

    @staticmethod
    def save_param_model(data: dict) -> None:
        with get_session() as session:
            upsert(session, IrParamModel, (data["ir_model_id"], data["ir_curve_id"]), data)

    @staticmethod
    def delete_param_model(ir_model_id: str, ir_curve_id: str) -> None:
        with get_session() as session:
            delete_by_pk(session, IrParamModel, (ir_model_id, ir_curve_id))

    # ─── 금리 커브 관리 ────────────────────────────────────────
    @staticmethod
    def get_ir_curve_list(page: int = 1, page_size: int = 20) -> tuple[list[dict], int]:
        with get_session() as session:
            q = session.query(IrCurve)
            rows, total = paginate(q.order_by(IrCurve.ir_curve_id), page, page_size)
            return ([{
                "ir_curve_id": r.ir_curve_id,
                "ir_curve_nm": r.ir_curve_nm,
                "cur_cd": r.cur_cd,
                "ir_curve_typ_cd": r.ir_curve_typ_cd,
                "use_at": r.use_at,
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
        "ltfr":            float(r.ltfr) if r.ltfr is not None else None,
        "ltfr_cp":         r.ltfr_cp,
        "liq_prem":        float(r.liq_prem) if r.liq_prem is not None else None,
        "liq_prem_appl_dv":r.liq_prem_appl_dv,
        "shk_sprd_sce_no": r.shk_sprd_sce_no,
        "sw_alpha_ytm":    float(r.sw_alpha_ytm) if r.sw_alpha_ytm is not None else None,
        "sto_sce_gen_yn":  r.sto_sce_gen_yn,
        "fwd_mat_cd":      r.fwd_mat_cd,
        "mult_int_rate":   float(r.mult_int_rate) if r.mult_int_rate is not None else None,
        "add_sprd":        float(r.add_sprd) if r.add_sprd is not None else None,
        "last_modified_by":r.last_modified_by,
        "last_update_date":str(r.last_update_date) if r.last_update_date else "",
    }
