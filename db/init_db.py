"""
DB 초기화 스크립트
  - SQLite 파일 생성
  - 모든 테이블 DDL 실행
  - 기본 데이터 INSERT (admin 계정, 샘플 코드, SW 파라미터 등)

실행: python db/init_db.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime, date
import bcrypt

from db.database import engine, SessionLocal
from sqlmodel import SQLModel
import db.models  # 모든 모델 등록

from db.models.auth          import AppUser, AuthInfo
from db.models.common        import CmmnCode, CoEsgMeta, CoJobList, BatchOpert
from db.models.ir_curve      import IrCurve
from db.models.ir_param_model import IrParamModel
from db.models.ir_param_sw   import IrParamSwUsr


def create_tables():
    print("[1/4] 테이블 생성 중...")
    SQLModel.metadata.create_all(bind=engine)
    print("      완료")


def insert_default_data():
    session = SessionLocal()
    try:
        print("[2/5] 기본 사용자 데이터 삽입 중...")
        _insert_users(session)

        print("[3/5] 공통 코드 / 메타 데이터 삽입 중...")
        _insert_common(session)

        print("[4/5] 금리 커브 / 파라미터 모델 / SW 파라미터 샘플 삽입 중...")
        _insert_esg_samples(session)

        print("[5/5] 메뉴 트리 초기 데이터 삽입 중...")
        _insert_nav_tree(session)

        session.commit()
        print("      완료 — DB 초기화 성공!")
    except Exception as exc:
        session.rollback()
        print(f"      오류 발생: {exc}")
        raise
    finally:
        session.close()


# ─────────────────────────────────────────────────────────────
def _insert_users(session):
    if session.get(AppUser, "admin"):
        return
    pw = bcrypt.hashpw(b"admin", bcrypt.gensalt()).decode()
    session.add(AppUser(user_id="admin", user_nm="관리자", password=pw,
                        email="admin@esg.co.kr", author_code="ROLE_ADMIN"))
    session.add(AuthInfo(author_code="ROLE_ADMIN",
                         author_nm="관리자",
                         author_dc="시스템 관리자 권한",
                         author_creat_de=datetime.now().strftime("%Y%m%d")))


def _insert_common(session):
    metas = [
        CoEsgMeta(group_id="SYSTEM", param_key="DB_SCHEMA",  param_value="GESG",   param_desc="DB 스키마명"),
        CoEsgMeta(group_id="SYSTEM", param_key="APP_VERSION", param_value="1.0.0",  param_desc="앱 버전"),
    ]
    for m in metas:
        if not session.get(CoEsgMeta, (m.group_id, m.param_key)):
            session.add(m)

    jobs = [
        CoJobList(job_id="JOB_HW_PARAM",   job_nm="HW 파라미터 계산",  use_yn="Y"),
        CoJobList(job_id="JOB_SW_PARAM",   job_nm="SW 파라미터 계산",  use_yn="Y"),
        CoJobList(job_id="JOB_DCNT_RATE",  job_nm="할인율 계산",       use_yn="Y"),
        CoJobList(job_id="JOB_SPRD_CURVE", job_nm="스프레드 커브 계산", use_yn="Y"),
    ]
    for j in jobs:
        if not session.get(CoJobList, j.job_id):
            session.add(j)


def _insert_esg_samples(session):
    # 금리 커브
    curves = [
        IrCurve(ir_curve_id="KRW_GOV",  ir_curve_nm="원화 국채",  cur_cd="KRW", appl_meth_dv="GOV",  use_yn="Y"),
        IrCurve(ir_curve_id="KRW_CORP", ir_curve_nm="원화 회사채", cur_cd="KRW", appl_meth_dv="CORP", use_yn="Y"),
        IrCurve(ir_curve_id="USD_GOV",  ir_curve_nm="달러 국채",   cur_cd="USD", appl_meth_dv="GOV",  use_yn="Y"),
    ]
    for c in curves:
        if not session.get(IrCurve, c.ir_curve_id):
            session.add(c)

    # 파라미터 모델
    models = [
        IrParamModel(ir_model_id="HW1F", ir_curve_id="KRW_GOV",  ir_model_nm="Hull-White 1-Factor", use_yn="Y"),
        IrParamModel(ir_model_id="SW",   ir_curve_id="KRW_GOV",  ir_model_nm="Smith-Wilson",        use_yn="Y"),
        IrParamModel(ir_model_id="CIR",  ir_curve_id="KRW_CORP", ir_model_nm="CIR",                 use_yn="Y"),
    ]
    for m in models:
        if not session.get(IrParamModel, (m.ir_model_id, m.ir_curve_id)):
            session.add(m)

    # SW 사용자 파라미터 샘플
    sw_params = [
        IrParamSwUsr(
            appl_st_yymm="202001", appl_ed_yymm="202912",
            appl_biz_dv="KICS", ir_curve_id="KRW_GOV", ir_curve_sce_no=1,
            ir_curve_sce_nm="KICS 기본 시나리오",
            cur_cd="KRW", freq=2, llp=20, ltfr=0.045, ltfr_cp=40,
            liq_prem=0.0010, liq_prem_appl_dv="Y", shk_sprd_sce_no=1,
            sw_alpha_ytm=0.1, sto_sce_gen_yn="Y",
        ),
        IrParamSwUsr(
            appl_st_yymm="202001", appl_ed_yymm="202912",
            appl_biz_dv="IFRS", ir_curve_id="KRW_GOV", ir_curve_sce_no=1,
            ir_curve_sce_nm="IFRS17 기본 시나리오",
            cur_cd="KRW", freq=2, llp=20, ltfr=0.045, ltfr_cp=40,
            liq_prem=0.0010, liq_prem_appl_dv="Y", shk_sprd_sce_no=1,
            sw_alpha_ytm=0.1, sto_sce_gen_yn="Y",
        ),
    ]
    for sw in sw_params:
        existing = session.get(IrParamSwUsr, (sw.appl_st_yymm, sw.appl_biz_dv, sw.ir_curve_id, sw.ir_curve_sce_no))
        if not existing:
            session.add(sw)

    # 배치 작업 샘플
    batch_opers = [
        BatchOpert(batch_opert_id="BAT001", batch_opert_nm="HW 파라미터 계산",
                   batch_progrm="gof.esg.ir.param.hw.batch.ParamHwBatch", use_at="Y"),
        BatchOpert(batch_opert_id="BAT002", batch_opert_nm="SW 파라미터 계산",
                   batch_progrm="gof.esg.ir.param.sw.batch.ParamSwBatch",  use_at="Y"),
        BatchOpert(batch_opert_id="BAT003", batch_opert_nm="할인율 계산",
                   batch_progrm="gof.esg.ir.dcnt.rate.batch.DcntRateBatch", use_at="Y"),
    ]
    for b in batch_opers:
        if not session.get(BatchOpert, b.batch_opert_id):
            session.add(b)


def _insert_nav_tree(session):
    """LETTNMENUINFO(MnuMng) 메뉴 트리 초기 시드."""
    from db.models.common import MnuMng
    if session.query(MnuMng).count() > 0:
        return
    from config.nav_tree import NAV_TREE
    for cat_ordr, (cat_nm, groups) in enumerate(NAV_TREE, 1):
        cat = MnuMng(menu_nm=cat_nm, menu_ordr=cat_ordr, upper_menu_no=None)
        session.add(cat)
        session.flush()
        for grp_ordr, (grp_nm, items) in enumerate(groups, 1):
            grp = MnuMng(menu_nm=grp_nm, menu_ordr=grp_ordr,
                         upper_menu_no=cat.menu_no)
            session.add(grp)
            session.flush()
            for item_ordr, (item_nm, view_key) in enumerate(items, 1):
                session.add(MnuMng(
                    menu_nm=item_nm, menu_ordr=item_ordr,
                    upper_menu_no=grp.menu_no,
                    progrm_file_nm=view_key,
                ))


if __name__ == "__main__":
    create_tables()
    insert_default_data()
