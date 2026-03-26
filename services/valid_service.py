"""
결과검증 서비스
1. 시나리오 선도 검증 : IrDcntRate (E_IR_DCNT_RATE)
2. 시나리오 랜덤 검증 : IrValidRnd (E_IR_VALID_RND)
3. 시나리오 저장 검증 : IrValidSceSto (E_IR_VALID_SCE_STO)
"""
from db.database import get_session
from db.models.sprd_curve import IrDcntRate, IrValidRnd, IrValidSceSto
from db.utils import paginate


class ValidService:
    # ─── 시나리오 선도 검증 (E_IR_DCNT_RATE) ────────────────────
    @staticmethod
    def get_valid_fwd_list(base_yymm: str = "",
                           page: int = 1, page_size: int = 20) -> tuple[list[dict], int]:
        with get_session() as session:
            q = session.query(IrDcntRate)
            if base_yymm:
                q = q.filter(IrDcntRate.base_yymm == base_yymm)
            rows, total = paginate(q, page, page_size)
            return ([{
                "base_yymm":       r.base_yymm,
                "appl_biz_dv":     r.appl_biz_dv,
                "ir_curve_id":     r.ir_curve_id,
                "ir_curve_sce_no": r.ir_curve_sce_no,
                "mat_cd":          r.mat_cd,
                "spot_rate":       float(r.spot_rate)     if r.spot_rate     is not None else None,
                "fwd_rate":        float(r.fwd_rate)      if r.fwd_rate      is not None else None,
                "adj_spot_rate":   float(r.adj_spot_rate) if r.adj_spot_rate is not None else None,
                "adj_fwd_rate":    float(r.adj_fwd_rate)  if r.adj_fwd_rate  is not None else None,
            } for r in rows], total)

    # ─── 시나리오 랜덤 검증 (E_IR_VALID_RND) ─────────────────────
    @staticmethod
    def get_valid_rnd_list(base_yymm: str = "",
                           page: int = 1, page_size: int = 20) -> tuple[list[dict], int]:
        with get_session() as session:
            q = session.query(IrValidRnd)
            if base_yymm:
                q = q.filter(IrValidRnd.base_yymm == base_yymm)
            rows, total = paginate(q, page, page_size)
            return ([{
                "base_yymm":   r.base_yymm,
                "ir_model_id": r.ir_model_id,
                "ir_curve_id": r.ir_curve_id,
                "valid_dv":    r.valid_dv,
                "valid_seq":   r.valid_seq,
                "valid_val1":  float(r.valid_val1) if r.valid_val1 is not None else None,
                "valid_val2":  float(r.valid_val2) if r.valid_val2 is not None else None,
                "valid_val3":  float(r.valid_val3) if r.valid_val3 is not None else None,
                "valid_val4":  float(r.valid_val4) if r.valid_val4 is not None else None,
                "valid_val5":  float(r.valid_val5) if r.valid_val5 is not None else None,
            } for r in rows], total)

    # ─── 시나리오 저장 검증 (E_IR_VALID_SCE_STO) ─────────────────
    @staticmethod
    def get_valid_sce_sto_list(base_yymm: str = "",
                               page: int = 1, page_size: int = 20) -> tuple[list[dict], int]:
        with get_session() as session:
            q = session.query(IrValidSceSto)
            if base_yymm:
                q = q.filter(IrValidSceSto.base_yymm == base_yymm)
            rows, total = paginate(q, page, page_size)
            return ([{
                "base_yymm":       r.base_yymm,
                "appl_biz_dv":     r.appl_biz_dv,
                "ir_model_id":     r.ir_model_id,
                "ir_curve_id":     r.ir_curve_id,
                "ir_curve_sce_no": r.ir_curve_sce_no,
                "valid_dv":        r.valid_dv,
                "valid_seq":       r.valid_seq,
                "valid_val1":      float(r.valid_val1) if r.valid_val1 is not None else None,
                "valid_val2":      float(r.valid_val2) if r.valid_val2 is not None else None,
                "valid_val3":      float(r.valid_val3) if r.valid_val3 is not None else None,
                "valid_val4":      float(r.valid_val4) if r.valid_val4 is not None else None,
                "valid_val5":      float(r.valid_val5) if r.valid_val5 is not None else None,
            } for r in rows], total)
