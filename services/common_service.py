"""
공통 / 배치 / ESG 작업 / 공지사항 서비스
"""
from datetime import datetime
from db.database import get_session
from db.models.common import (CoEsgMeta, CoJobList, CoJobHist,
                               BatchOpert, BatchResult, BatchSchdul, CopBbs,
                               MnuMng, PgmMng)
from db.models.sprd_curve import SprdCurve, SprdAfnsBiz, CorpPd, CrdCorpPd
from db.models.sprd_curve import ValidSceFwd, ValidRnd, ValidSceSto
from db.models.ir_param_model import IrParamAfnsBiz, VolSwpn


class CommonService:
    # ─── ESG 메타 ───────────────────────────────────────────────
    @staticmethod
    def get_meta(group_id: str, param_key: str) -> str | None:
        with get_session() as session:
            row = session.get(CoEsgMeta, (group_id, param_key))
            return row.param_val if row else None

    # ─── ESG 작업 이력 (CoJobList.jsp) ─────────────────────────
    @staticmethod
    def get_job_hist_list(base_yymm: str = "", calc_sttus: str = "",
                          page: int = 1, page_size: int = 20) -> tuple[list[dict], int]:
        with get_session() as session:
            q = session.query(CoJobHist)
            if base_yymm:
                q = q.filter(CoJobHist.base_yymm == base_yymm)
            if calc_sttus:
                q = q.filter(CoJobHist.calc_sttus == calc_sttus)
            total = q.count()
            rows = q.order_by(CoJobHist.job_hist_id.desc())\
                    .offset((page - 1) * page_size).limit(page_size).all()
            return ([{
                "job_hist_id":    r.job_hist_id,
                "job_id":         r.job_id,
                "base_yymm":      r.base_yymm,
                "calc_dt":        r.calc_dt,
                "calc_start_dt":  str(r.calc_start_dt) if r.calc_start_dt else "",
                "calc_end_dt":    str(r.calc_end_dt)   if r.calc_end_dt   else "",
                "calc_sttus":     r.calc_sttus,
                "error_msg":      r.error_msg,
            } for r in rows], total)


class BatchService:
    # ─── 배치 작업 ──────────────────────────────────────────────
    @staticmethod
    def get_batch_opert_list(batch_opert_nm: str = "", batch_progrm: str = "",
                             page: int = 1, page_size: int = 20) -> tuple[list[dict], int]:
        with get_session() as session:
            q = session.query(BatchOpert)
            if batch_opert_nm:
                q = q.filter(BatchOpert.batch_opert_nm.like(f"%{batch_opert_nm}%"))
            if batch_progrm:
                q = q.filter(BatchOpert.batch_progrm.like(f"%{batch_progrm}%"))
            total = q.count()
            rows = q.order_by(BatchOpert.batch_opert_id)\
                    .offset((page - 1) * page_size).limit(page_size).all()
            return ([{
                "batch_opert_id": r.batch_opert_id,
                "batch_opert_nm": r.batch_opert_nm,
                "batch_progrm":   r.batch_progrm,
                "paramtr":        r.paramtr,
                "use_at":         r.use_at,
            } for r in rows], total)

    @staticmethod
    def save_batch_opert(data: dict) -> None:
        with get_session() as session:
            row = session.get(BatchOpert, data["batch_opert_id"])
            if row:
                for k, v in data.items():
                    if hasattr(row, k):
                        setattr(row, k, v)
                row.last_updt_pnttm = datetime.now()
            else:
                session.add(BatchOpert(**data))
            session.commit()

    # ─── 배치 결과 ──────────────────────────────────────────────
    @staticmethod
    def get_batch_result_list(batch_opert_nm: str = "", sttus: str = "",
                              page: int = 1, page_size: int = 20) -> tuple[list[dict], int]:
        with get_session() as session:
            q = session.query(BatchResult)
            if sttus:
                q = q.filter(BatchResult.sttus == sttus)
            total = q.count()
            rows = q.order_by(BatchResult.frst_regist_pnttm.desc())\
                    .offset((page - 1) * page_size).limit(page_size).all()
            return ([{
                "batch_result_id":  r.batch_result_id,
                "batch_schdul_id":  r.batch_schdul_id,
                "batch_opert_id":   r.batch_opert_id,
                "paramtr":          r.paramtr,
                "sttus":            r.sttus,
                "error_info":       r.error_info,
                "execut_begin_tm":  r.execut_begin_tm,
                "execut_end_tm":    r.execut_end_tm,
            } for r in rows], total)

    @staticmethod
    def save_batch_schdul(data: dict) -> None:
        with get_session() as session:
            row = session.get(BatchSchdul, data["batch_schdul_id"])
            if row:
                for k, v in data.items():
                    if hasattr(row, k):
                        setattr(row, k, v)
                row.last_updt_pnttm = datetime.now()
            else:
                session.add(BatchSchdul(**data))
            session.commit()

    @staticmethod
    def delete_batch_schdul(batch_schdul_id: str) -> None:
        with get_session() as session:
            row = session.get(BatchSchdul, batch_schdul_id)
            if row:
                session.delete(row)
                session.commit()

    # ─── 배치 스케줄 ────────────────────────────────────────────
    @staticmethod
    def get_batch_schdul_list(page: int = 1, page_size: int = 20) -> tuple[list[dict], int]:
        with get_session() as session:
            q = session.query(BatchSchdul)
            total = q.count()
            rows = q.order_by(BatchSchdul.batch_schdul_id)\
                    .offset((page - 1) * page_size).limit(page_size).all()
            return ([{
                "batch_schdul_id":    r.batch_schdul_id,
                "batch_opert_id":     r.batch_opert_id,
                "execut_cycle":       r.execut_cycle,
                "execut_schdul_de":   r.execut_schdul_de,
                "execut_schdul_hour": r.execut_schdul_hour,
                "execut_schdul_mnt":  r.execut_schdul_mnt,
                "execut_schdul_secnd":r.execut_schdul_secnd,
            } for r in rows], total)


class ContentService:
    """공지사항 / 메뉴 / 프로그램 CRUD"""

    # ─── 공지사항 ────────────────────────────────────────────────
    @staticmethod
    def save_cop_bbs(data: dict) -> None:
        with get_session() as session:
            ntt_id = data.get("ntt_id")
            if ntt_id:
                row = session.get(CopBbs, ntt_id)
                if row:
                    for k, v in data.items():
                        if hasattr(row, k):
                            setattr(row, k, v)
                    row.last_updt_pnttm = datetime.now()
                    session.commit()
                    return
            # 신규
            new_row = CopBbs(
                bbs_id=data.get("bbs_id", "NOTICE"),
                ntt_sj=data.get("ntt_sj", ""),
                ntt_cn=data.get("ntt_cn", ""),
                frst_register_nm=data.get("frst_register_nm", ""),
            )
            session.add(new_row)
            session.commit()

    @staticmethod
    def delete_cop_bbs(ntt_id: int) -> None:
        with get_session() as session:
            row = session.get(CopBbs, ntt_id)
            if row:
                session.delete(row)
                session.commit()

    # ─── 메뉴 관리 ──────────────────────────────────────────────
    @staticmethod
    def save_mnu_mng(data: dict) -> None:
        with get_session() as session:
            menu_no = data.get("menu_no")
            if menu_no:
                row = session.get(MnuMng, menu_no)
                if row:
                    for k, v in data.items():
                        if hasattr(row, k):
                            setattr(row, k, v)
                    session.commit()
                    return
            # 신규 (menu_no autoincrement)
            new_row = MnuMng(**{k: v for k, v in data.items()
                                if k != "menu_no" and hasattr(MnuMng, k)})
            session.add(new_row)
            session.commit()

    @staticmethod
    def delete_mnu_mng(menu_no: int) -> None:
        with get_session() as session:
            row = session.get(MnuMng, menu_no)
            if row:
                session.delete(row)
                session.commit()

    # ─── 프로그램 관리 ──────────────────────────────────────────
    @staticmethod
    def save_pgm_mng(data: dict) -> None:
        with get_session() as session:
            row = session.get(PgmMng, data["progrm_file_nm"])
            if row:
                for k, v in data.items():
                    if hasattr(row, k):
                        setattr(row, k, v)
            else:
                session.add(PgmMng(**data))
            session.commit()

    @staticmethod
    def delete_pgm_mng(progrm_file_nm: str) -> None:
        with get_session() as session:
            row = session.get(PgmMng, progrm_file_nm)
            if row:
                session.delete(row)
                session.commit()


class SprdService:
    @staticmethod
    def get_sprd_curve_list(base_yymm: str = "", ir_curve_id: str = "",
                            page: int = 1, page_size: int = 20) -> tuple[list[dict], int]:
        with get_session() as session:
            q = session.query(SprdCurve)
            if base_yymm:
                q = q.filter(SprdCurve.base_yymm == base_yymm)
            if ir_curve_id:
                q = q.filter(SprdCurve.ir_curve_id == ir_curve_id)
            total = q.count()
            rows = q.order_by(SprdCurve.mat_cd)\
                    .offset((page - 1) * page_size).limit(page_size).all()
            return ([{
                "base_yymm":   r.base_yymm,
                "ir_curve_id": r.ir_curve_id,
                "ir_typ_cd":   r.ir_typ_cd,
                "mat_cd":      r.mat_cd,
                "sprd_val":    float(r.sprd_val) if r.sprd_val is not None else None,
            } for r in rows], total)


class ValidService:
    @staticmethod
    def get_valid_sce_fwd_list(base_yymm: str = "",
                               page: int = 1, page_size: int = 20) -> tuple[list[dict], int]:
        with get_session() as session:
            q = session.query(ValidSceFwd)
            if base_yymm:
                q = q.filter(ValidSceFwd.base_yymm == base_yymm)
            total = q.count()
            rows = q.offset((page - 1) * page_size).limit(page_size).all()
            return ([{
                "base_yymm":       r.base_yymm,
                "appl_biz_dv":     r.appl_biz_dv,
                "ir_curve_id":     r.ir_curve_id,
                "ir_curve_sce_no": r.ir_curve_sce_no,
                "mat_cd":          r.mat_cd,
                "valid_val":       float(r.valid_val) if r.valid_val is not None else None,
            } for r in rows], total)

    @staticmethod
    def get_valid_rnd_list(base_yymm: str = "",
                           page: int = 1, page_size: int = 20) -> tuple[list[dict], int]:
        with get_session() as session:
            q = session.query(ValidRnd)
            if base_yymm:
                q = q.filter(ValidRnd.base_yymm == base_yymm)
            total = q.count()
            rows = q.offset((page - 1) * page_size).limit(page_size).all()
            return ([{
                "base_yymm":       r.base_yymm,
                "appl_biz_dv":     r.appl_biz_dv,
                "ir_curve_id":     r.ir_curve_id,
                "ir_curve_sce_no": r.ir_curve_sce_no,
                "rnd_seq":         r.rnd_seq,
                "rnd_val":         float(r.rnd_val) if r.rnd_val is not None else None,
            } for r in rows], total)

    @staticmethod
    def get_valid_sce_sto_list(base_yymm: str = "",
                               page: int = 1, page_size: int = 20) -> tuple[list[dict], int]:
        with get_session() as session:
            q = session.query(ValidSceSto)
            if base_yymm:
                q = q.filter(ValidSceSto.base_yymm == base_yymm)
            total = q.count()
            rows = q.offset((page - 1) * page_size).limit(page_size).all()
            return ([{
                "base_yymm":       r.base_yymm,
                "appl_biz_dv":     r.appl_biz_dv,
                "ir_curve_id":     r.ir_curve_id,
                "ir_curve_sce_no": r.ir_curve_sce_no,
                "valid_typ_cd":    r.valid_typ_cd,
                "valid_val":       float(r.valid_val) if r.valid_val is not None else None,
            } for r in rows], total)
