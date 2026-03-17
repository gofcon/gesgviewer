"""
공통 코드 / ESG 메타 / 작업 정보 / 공지사항
"""
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Text, Numeric
from db.database import Base


class CmmnCode(Base):
    """공통분류코드 (COMTCCMMNCLCODE)"""
    __tablename__ = "COMTCCMMNCLCODE"

    cl_code         = Column(String(3),  primary_key=True, comment="분류코드")
    cl_code_nm      = Column(String(60),                   comment="분류코드명")
    cl_code_dc      = Column(String(200),                  comment="분류코드설명")
    use_at          = Column(String(1),                    comment="사용여부")
    frst_regist_pnttm = Column(DateTime)
    frst_register_id  = Column(String(20))
    last_updt_pnttm   = Column(DateTime)
    last_updusr_id    = Column(String(20))


class CoEsgMeta(Base):
    """ESG 메타 정보 (E_CO_ESG_META)"""
    __tablename__ = "E_CO_ESG_META"

    group_id         = Column(String(50),   primary_key=True, comment="그룹ID")
    param_key        = Column(String(100),  primary_key=True, comment="파라미터키")
    param_val        = Column(String(500),                    comment="파라미터값")
    param_desc       = Column(String(500),                    comment="파라미터설명")
    last_modified_by = Column(String(100),                    comment="최종수정자")
    last_update_date = Column(DateTime,     default=datetime.now, comment="최종수정일자")


class CoJobList(Base):
    """ESG 작업 목록 (E_CO_JOB_LIST)"""
    __tablename__ = "E_CO_JOB_LIST"

    job_id           = Column(String(50),  primary_key=True, comment="작업ID")
    job_nm           = Column(String(200),                   comment="작업명")
    job_desc         = Column(String(500),                   comment="작업설명")
    use_at           = Column(String(1),   default="Y",      comment="사용여부")
    last_modified_by = Column(String(100),                   comment="최종수정자")
    last_update_date = Column(DateTime,    default=datetime.now, comment="최종수정일자")


class CoJobHist(Base):
    """ESG 작업 이력 (E_CO_JOB_HIST) — CoJobList.jsp 표시용"""
    __tablename__ = "E_CO_JOB_HIST"

    job_hist_id      = Column(Integer, primary_key=True, autoincrement=True, comment="이력ID")
    job_id           = Column(String(50),                comment="작업ID")
    base_yymm        = Column(String(6),                 comment="기준년월")
    calc_dt          = Column(String(8),                 comment="계산일자")
    calc_start_dt    = Column(DateTime,                  comment="계산시작일시")
    calc_end_dt      = Column(DateTime,                  comment="계산종료일시")
    calc_sttus       = Column(String(10),                comment="계산상태(SUCCESS/ERROR)")
    error_msg        = Column(Text,                      comment="오류메시지")
    last_modified_by = Column(String(100),               comment="최종수정자")
    last_update_date = Column(DateTime,  default=datetime.now, comment="최종수정일자")


class BatchOpert(Base):
    """배치 작업 (COMTNBATCHOPERT)"""
    __tablename__ = "COMTNBATCHOPERT"

    batch_opert_id  = Column(String(20), primary_key=True, comment="배치작업ID")
    batch_opert_nm  = Column(String(60),                   comment="배치작업명")
    batch_progrm    = Column(String(255),                  comment="배치프로그램")
    paramtr         = Column(String(250),                  comment="파라미터")
    use_at          = Column(String(1),   default="Y",     comment="사용여부")
    frst_register_id  = Column(String(20))
    frst_regist_pnttm = Column(DateTime)
    last_updusr_id    = Column(String(20))
    last_updt_pnttm   = Column(DateTime,  default=datetime.now, nullable=False)


class BatchResult(Base):
    """배치 결과 (COMTNBATCHRESULT)"""
    __tablename__ = "COMTNBATCHRESULT"

    batch_result_id   = Column(String(20), primary_key=True, comment="배치결과ID")
    batch_schdul_id   = Column(String(20), nullable=False,   comment="배치일정ID")
    batch_opert_id    = Column(String(20), nullable=False,   comment="배치작업ID")
    paramtr           = Column(String(250),                  comment="파라미터")
    sttus             = Column(String(2),                    comment="상태")
    error_info        = Column(String(2000),                 comment="오류정보")
    execut_begin_tm   = Column(String(14),                   comment="실행시작시각")
    execut_end_tm     = Column(String(14),                   comment="실행종료시각")
    last_updt_pnttm   = Column(DateTime)
    last_updusr_id    = Column(String(20))
    frst_regist_pnttm = Column(DateTime, nullable=False, default=datetime.now)
    frst_register_id  = Column(String(20))


class BatchSchdul(Base):
    """배치 스케줄 (COMTNBATCHSCHDUL)"""
    __tablename__ = "COMTNBATCHSCHDUL"

    batch_schdul_id      = Column(String(20), primary_key=True, comment="배치일정ID")
    batch_opert_id       = Column(String(20), nullable=False,   comment="배치작업ID")
    execut_cycle         = Column(String(2),                    comment="실행주기")
    execut_schdul_de     = Column(String(20),                   comment="실행일정일")
    execut_schdul_hour   = Column(String(2),                    comment="실행일정시")
    execut_schdul_mnt    = Column(String(2),                    comment="실행일정분")
    execut_schdul_secnd  = Column(String(2),                    comment="실행일정초")
    frst_register_id     = Column(String(20))
    frst_regist_pnttm    = Column(DateTime)
    last_updusr_id       = Column(String(20))
    last_updt_pnttm      = Column(DateTime, nullable=False, default=datetime.now)


class CopBbs(Base):
    """공지사항 게시글 (LETTNBBS 간소화)"""
    __tablename__ = "LETTNBBS"

    ntt_id           = Column(Integer, primary_key=True, autoincrement=True, comment="게시글ID")
    bbs_id           = Column(String(20),  nullable=False, comment="게시판ID")
    ntt_sj           = Column(String(255), nullable=False, comment="게시글제목")
    ntt_cn           = Column(Text,                        comment="게시글내용")
    frst_register_id = Column(String(20),                  comment="최초등록자ID")
    frst_register_nm = Column(String(60),                  comment="최초등록자명")
    frst_regist_pnttm= Column(DateTime,    default=datetime.now, comment="최초등록시점")
    last_updusr_id   = Column(String(20),                  comment="최종수정자ID")
    last_updt_pnttm  = Column(DateTime,                    comment="최종수정시점")


class MnuMng(Base):
    """메뉴 목록 (LETTNMENUINFO 간소화)"""
    __tablename__ = "LETTNMENUINFO"

    menu_no          = Column(Integer, primary_key=True, autoincrement=True, comment="메뉴번호")
    menu_ordr        = Column(Integer, comment="메뉴순서")
    menu_nm          = Column(String(100), comment="메뉴명")
    upper_menu_no    = Column(Integer, comment="상위메뉴번호")
    progrm_file_nm   = Column(String(200), comment="프로그램파일명")
    relate_image_nm  = Column(String(100), comment="관련이미지명")
    relate_image_path= Column(String(200), comment="관련이미지경로")
    menu_dc          = Column(String(500), comment="메뉴설명")


class PgmMng(Base):
    """프로그램 관리 (LETTNPROGRMLIST 간소화)"""
    __tablename__ = "LETTNPROGRMLIST"

    progrm_file_nm  = Column(String(200), primary_key=True, comment="프로그램파일명")
    progrm_stre_path= Column(String(200),                   comment="프로그램저장경로")
    progrm_dc       = Column(String(500),                   comment="프로그램설명")
    url             = Column(String(200),                   comment="URL")
    use_at          = Column(String(1), default="Y",        comment="사용여부")
