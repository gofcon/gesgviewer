"""
공통 코드 / ESG 메타 / 작업 정보 / 공지사항
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime, Numeric, Text


class CmmnCode(SQLModel, table=True):
    """공통분류코드 (COMTCCMMNCLCODE)"""
    __tablename__ = "COMTCCMMNCLCODE"

    cl_code:           str           = Field(primary_key=True)
    cl_code_nm:        Optional[str] = None
    cl_code_dc:        Optional[str] = None
    use_at:            Optional[str] = None
    frst_regist_pnttm: Optional[datetime] = None
    frst_register_id:  Optional[str] = None
    last_updt_pnttm:   Optional[datetime] = None
    last_updusr_id:    Optional[str] = None


class CoEsgMeta(SQLModel, table=True):
    """ESG 메타 정보 (E_CO_ESG_META)"""
    __tablename__ = "E_CO_ESG_META"

    group_id:         str           = Field(primary_key=True)
    param_key:        str           = Field(primary_key=True)
    param_value:      Optional[str] = None
    param_name:       Optional[str] = None
    param_desc:       Optional[str] = None
    use_yn:           Optional[str] = None
    last_modified_by: Optional[str] = None
    last_update_date: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime, default=datetime.now))


class CoJobList(SQLModel, table=True):
    """ESG 작업 목록 (E_CO_JOB_LIST)"""
    __tablename__ = "E_CO_JOB_LIST"

    job_id:           str           = Field(primary_key=True)
    job_nm:           Optional[str] = None
    use_yn:           Optional[str] = None
    last_modified_by: Optional[str] = None
    last_update_date: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime, default=datetime.now))


class CoJobInfo(SQLModel, table=True):
    """ESG 작업 이력 (E_CO_JOB_INFO)"""
    __tablename__ = "E_CO_JOB_INFO"

    job_id:           str           = Field(primary_key=True)
    base_yymm:        str           = Field(primary_key=True)
    calc_date:        str           = Field(primary_key=True)
    job_nm:           Optional[str] = None
    calc_start:       Optional[str] = None
    calc_end:         Optional[str] = None
    calc_elps:        Optional[str] = None
    calc_scd:         Optional[str] = None
    last_modified_by: Optional[str] = None
    last_update_date: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime, default=datetime.now))


class BatchOpert(SQLModel, table=True):
    """배치 작업 (COMTNBATCHOPERT)"""
    __tablename__ = "COMTNBATCHOPERT"

    batch_opert_id:   str           = Field(primary_key=True)
    batch_opert_nm:   Optional[str] = None
    batch_progrm:     Optional[str] = None
    paramtr:          Optional[str] = None
    use_at:           str           = "Y"
    frst_register_id: Optional[str] = None
    frst_regist_pnttm: Optional[datetime] = None
    last_updusr_id:   Optional[str] = None
    last_updt_pnttm:  Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime, nullable=False, default=datetime.now))


class BatchResult(SQLModel, table=True):
    """배치 결과 (COMTNBATCHRESULT)"""
    __tablename__ = "COMTNBATCHRESULT"

    batch_result_id:  str = Field(primary_key=True)
    batch_schdul_id:  str
    batch_opert_id:   str
    paramtr:          Optional[str] = None
    sttus:            Optional[str] = None
    error_info:       Optional[str] = None
    execut_begin_tm:  Optional[str] = None
    execut_end_tm:    Optional[str] = None
    last_updt_pnttm:  Optional[datetime] = None
    last_updusr_id:   Optional[str] = None
    frst_regist_pnttm: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime, nullable=False, default=datetime.now))
    frst_register_id: Optional[str] = None


class BatchSchdul(SQLModel, table=True):
    """배치 스케줄 (COMTNBATCHSCHDUL)"""
    __tablename__ = "COMTNBATCHSCHDUL"

    batch_schdul_id:     str           = Field(primary_key=True)
    batch_opert_id:      str
    execut_cycle:        Optional[str] = None
    execut_schdul_de:    Optional[str] = None
    execut_schdul_hour:  Optional[str] = None
    execut_schdul_mnt:   Optional[str] = None
    execut_schdul_secnd: Optional[str] = None
    frst_register_id:    Optional[str] = None
    frst_regist_pnttm:   Optional[datetime] = None
    last_updusr_id:      Optional[str] = None
    last_updt_pnttm:     Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime, nullable=False, default=datetime.now))


class CopBbs(SQLModel, table=True):
    """공지사항 게시글 (LETTNBBS 간소화)"""
    __tablename__ = "LETTNBBS"

    ntt_id:           Optional[int] = Field(default=None, primary_key=True)
    bbs_id:           str
    ntt_sj:           str
    ntt_cn:           Optional[str] = Field(default=None, sa_column=Column(Text))
    frst_register_id: Optional[str] = None
    frst_register_nm: Optional[str] = None
    frst_regist_pnttm: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime, default=datetime.now))
    last_updusr_id:   Optional[str] = None
    last_updt_pnttm:  Optional[datetime] = None


class MnuMng(SQLModel, table=True):
    """메뉴 목록 (LETTNMENUINFO 간소화)"""
    __tablename__ = "LETTNMENUINFO"

    menu_no:           Optional[int] = Field(default=None, primary_key=True)
    menu_ordr:         Optional[int] = None
    menu_nm:           Optional[str] = None
    upper_menu_no:     Optional[int] = None
    progrm_file_nm:    Optional[str] = None
    relate_image_nm:   Optional[str] = None
    relate_image_path: Optional[str] = None
    menu_dc:           Optional[str] = None


class PgmMng(SQLModel, table=True):
    """프로그램 관리 (LETTNPROGRMLIST 간소화)"""
    __tablename__ = "LETTNPROGRMLIST"

    progrm_file_nm:   str           = Field(primary_key=True)
    progrm_stre_path: Optional[str] = None
    progrm_dc:        Optional[str] = None
    url:              Optional[str] = None
    use_at:           str           = "Y"
