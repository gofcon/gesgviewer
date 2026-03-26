"""
환경설정 서비스
1. ESG 작업정보 (E_CO_ESG_META, E_CO_JOB_INFO)
2. 배치관리 (COMTNBATCHOPERT, COMTNBATCHRESULT, COMTNBATCHSCHDUL)
"""
from datetime import datetime
from db.database import get_session
from db.models.common import CoEsgMeta, CoJobInfo, BatchOpert, BatchResult, BatchSchdul
from db.utils import paginate, delete_by_pk


class ConfigService:
    # ─── ESG 메타 ───────────────────────────────────────────────
    @staticmethod
    def get_meta(group_id: str, param_key: str) -> str | None:
        with get_session() as session:
            row = session.get(CoEsgMeta, (group_id, param_key))
            return row.param_value if row else None

    # ─── ESG 작업 이력 ──────────────────────────────────────────
    @staticmethod
    def get_job_info_list(base_yymm: str = "", calc_scd: str = "",
                          page: int = 1, page_size: int = 20) -> tuple[list[dict], int]:
        with get_session() as session:
            q = session.query(CoJobInfo)
            if base_yymm:
                q = q.filter(CoJobInfo.base_yymm == base_yymm)
            if calc_scd:
                q = q.filter(CoJobInfo.calc_scd == calc_scd)
            rows, total = paginate(
                q.order_by(CoJobInfo.base_yymm.desc(), CoJobInfo.job_id), page, page_size)
            return ([{
                "job_id":     r.job_id,
                "base_yymm":  r.base_yymm,
                "calc_date":  r.calc_date,
                "job_nm":     r.job_nm,
                "calc_start": r.calc_start,
                "calc_end":   r.calc_end,
                "calc_elps":  r.calc_elps,
                "calc_scd":   r.calc_scd,
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
            rows, total = paginate(q.order_by(BatchOpert.batch_opert_id), page, page_size)
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
            rows, total = paginate(
                q.order_by(BatchResult.frst_regist_pnttm.desc()), page, page_size)
            return ([{
                "batch_result_id": r.batch_result_id,
                "batch_schdul_id": r.batch_schdul_id,
                "batch_opert_id":  r.batch_opert_id,
                "paramtr":         r.paramtr,
                "sttus":           r.sttus,
                "error_info":      r.error_info,
                "execut_begin_tm": r.execut_begin_tm,
                "execut_end_tm":   r.execut_end_tm,
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
            delete_by_pk(session, BatchSchdul, batch_schdul_id)

    # ─── 배치 스케줄 ────────────────────────────────────────────
    @staticmethod
    def get_batch_schdul_list(page: int = 1, page_size: int = 20) -> tuple[list[dict], int]:
        with get_session() as session:
            q = session.query(BatchSchdul)
            rows, total = paginate(q.order_by(BatchSchdul.batch_schdul_id), page, page_size)
            return ([{
                "batch_schdul_id":     r.batch_schdul_id,
                "batch_opert_id":      r.batch_opert_id,
                "execut_cycle":        r.execut_cycle,
                "execut_schdul_de":    r.execut_schdul_de,
                "execut_schdul_hour":  r.execut_schdul_hour,
                "execut_schdul_mnt":   r.execut_schdul_mnt,
                "execut_schdul_secnd": r.execut_schdul_secnd,
            } for r in rows], total)
