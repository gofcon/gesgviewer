"""
스프레드 커브 / AFNS 스프레드 / 기업 부도율 / 검증 모델
Oracle: E_IR_SPRD_CURVE, E_IR_SPRD_AFNS_BIZ, E_RC_CORP_PD_BIZ, E_RC_CORP_PD,
        E_IR_DCNT_RATE, E_IR_VALID_RND, E_IR_VALID_SCE_STO
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime, Numeric


class SprdCurve(SQLModel, table=True):
    """위험스프레드 커브 (E_IR_SPRD_CURVE)"""
    __tablename__ = "E_IR_SPRD_CURVE"

    base_yymm:        str           = Field(primary_key=True)
    ir_curve_id:      str           = Field(primary_key=True)
    ir_typ_dv_cd:     str           = Field(primary_key=True)
    mat_cd:           str           = Field(primary_key=True)
    int_rate:         Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(22, 20)))
    crd_sprd:         Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(22, 20)))
    last_modified_by: Optional[str] = None
    last_update_date: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime, default=datetime.now))


class SprdAfnsBiz(SQLModel, table=True):
    """AFNS 충격 스프레드 (E_IR_SPRD_AFNS_BIZ)"""
    __tablename__ = "E_IR_SPRD_AFNS_BIZ"

    base_yymm:        str           = Field(primary_key=True)
    ir_model_id:      str           = Field(primary_key=True)
    ir_curve_id:      str           = Field(primary_key=True)
    ir_curve_sce_no:  int           = Field(primary_key=True)
    mat_cd:           str           = Field(primary_key=True)
    shk_sprd_cont:    Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(25, 20)))
    last_modified_by: Optional[str] = None
    last_update_date: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime, default=datetime.now))


class RcCorpPdBiz(SQLModel, table=True):
    """기업 부도율 업무 (E_RC_CORP_PD_BIZ)"""
    __tablename__ = "E_RC_CORP_PD_BIZ"

    base_yymm:        str           = Field(primary_key=True)
    appl_biz_dv:      str           = Field(primary_key=True)
    crd_grd_cd:       str           = Field(primary_key=True)
    mat_cd:           str           = Field(primary_key=True)
    cum_pd:           Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(10, 8)))
    fwd_pd:           Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(10, 8)))
    last_modified_by: Optional[str] = None
    last_update_date: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime, default=datetime.now))


class RcCorpPd(SQLModel, table=True):
    """기업 부도율 (E_RC_CORP_PD)"""
    __tablename__ = "E_RC_CORP_PD"

    base_yymm:          str           = Field(primary_key=True)
    crd_eval_agncy_cd:  str           = Field(primary_key=True)
    crd_grd_cd:         str           = Field(primary_key=True)
    mat_cd:             str           = Field(primary_key=True)
    cum_pd:             Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(10, 8)))
    fwd_pd:             Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(10, 8)))
    last_modified_by:   Optional[str] = None
    last_update_date:   Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime, default=datetime.now))


class IrDcntRate(SQLModel, table=True):
    """할인율 (E_IR_DCNT_RATE)"""
    __tablename__ = "E_IR_DCNT_RATE"

    base_yymm:        str           = Field(primary_key=True)
    appl_biz_dv:      str           = Field(primary_key=True)
    ir_curve_id:      str           = Field(primary_key=True)
    ir_curve_sce_no:  int           = Field(primary_key=True)
    mat_cd:           str           = Field(primary_key=True)
    spot_rate:        Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(22, 20)))
    fwd_rate:         Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(22, 20)))
    adj_spot_rate:    Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(22, 20)))
    adj_fwd_rate:     Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(22, 20)))
    last_modified_by: Optional[str] = None
    last_update_date: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime, default=datetime.now))


class IrValidRnd(SQLModel, table=True):
    """랜덤 검증 (E_IR_VALID_RND)"""
    __tablename__ = "E_IR_VALID_RND"

    base_yymm:        str           = Field(primary_key=True)
    ir_model_id:      str           = Field(primary_key=True)
    ir_curve_id:      str           = Field(primary_key=True)
    valid_dv:         str           = Field(primary_key=True)
    valid_seq:        int           = Field(primary_key=True)
    valid_val1:       Optional[Decimal] = Field(default=None, sa_column=Column(Numeric(25, 20)))
    valid_val2:       Optional[Decimal] = Field(default=None, sa_column=Column(Numeric(25, 20)))
    valid_val3:       Optional[Decimal] = Field(default=None, sa_column=Column(Numeric(25, 20)))
    valid_val4:       Optional[Decimal] = Field(default=None, sa_column=Column(Numeric(25, 20)))
    valid_val5:       Optional[Decimal] = Field(default=None, sa_column=Column(Numeric(25, 20)))
    last_modified_by: Optional[str] = None
    last_update_date: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime, default=datetime.now))


class IrValidSceSto(SQLModel, table=True):
    """시나리오 저장 검증 (E_IR_VALID_SCE_STO)"""
    __tablename__ = "E_IR_VALID_SCE_STO"

    base_yymm:        str           = Field(primary_key=True)
    appl_biz_dv:      str           = Field(primary_key=True)
    ir_model_id:      str           = Field(primary_key=True)
    ir_curve_id:      str           = Field(primary_key=True)
    ir_curve_sce_no:  int           = Field(primary_key=True)
    valid_dv:         str           = Field(primary_key=True)
    valid_seq:        int           = Field(primary_key=True)
    valid_val1:       Optional[Decimal] = Field(default=None, sa_column=Column(Numeric(25, 20)))
    valid_val2:       Optional[Decimal] = Field(default=None, sa_column=Column(Numeric(25, 20)))
    valid_val3:       Optional[Decimal] = Field(default=None, sa_column=Column(Numeric(25, 20)))
    valid_val4:       Optional[Decimal] = Field(default=None, sa_column=Column(Numeric(25, 20)))
    valid_val5:       Optional[Decimal] = Field(default=None, sa_column=Column(Numeric(25, 20)))
    last_modified_by: Optional[str] = None
    last_update_date: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime, default=datetime.now))


class SprdAfnsCalc(SQLModel, table=True):
    """AFNS 스프레드 계산 (E_IR_SPRD_AFNS_CALC)"""
    __tablename__ = "E_IR_SPRD_AFNS_CALC"

    base_yymm:        str           = Field(primary_key=True)
    ir_model_id:      str           = Field(primary_key=True)
    ir_curve_id:      str           = Field(primary_key=True)
    ir_curve_sce_no:  int           = Field(primary_key=True)
    mat_cd:           str           = Field(primary_key=True)
    shk_sprd_cont:    Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(25, 20)))
    last_modified_by: Optional[str] = None
    last_update_date: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime, default=datetime.now))


class SprdLp(SQLModel, table=True):
    """LP 스프레드 (E_IR_SPRD_LP)"""
    __tablename__ = "E_IR_SPRD_LP"

    base_yymm:            str           = Field(primary_key=True)
    dcnt_appl_model_cd:   str           = Field(primary_key=True)
    appl_biz_dv:          str           = Field(primary_key=True)
    ir_curve_id:          str           = Field(primary_key=True)
    ir_curve_sce_no:      int           = Field(primary_key=True)
    mat_cd:               str           = Field(primary_key=True)
    liq_prem:             Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(22, 20)))
    last_modified_by:     Optional[str] = None
    last_update_date:     Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime, default=datetime.now))


class SprdLpBiz(SQLModel, table=True):
    """LP 스프레드 비즈 (E_IR_SPRD_LP_BIZ)"""
    __tablename__ = "E_IR_SPRD_LP_BIZ"

    base_yymm:        str           = Field(primary_key=True)
    appl_biz_dv:      str           = Field(primary_key=True)
    ir_curve_id:      str           = Field(primary_key=True)
    ir_curve_sce_no:  int           = Field(primary_key=True)
    mat_cd:           str           = Field(primary_key=True)
    liq_prem:         Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(22, 20)))
    last_modified_by: Optional[str] = None
    last_update_date: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime, default=datetime.now))


class SprdAfnsUsr(SQLModel, table=True):
    """AFNS 스프레드 사용자 입력 (E_IR_SPRD_AFNS_USR)"""
    __tablename__ = "E_IR_SPRD_AFNS_USR"

    base_yymm:        str           = Field(primary_key=True)
    ir_model_id:      str           = Field(primary_key=True)
    ir_curve_id:      str           = Field(primary_key=True)
    mat_cd:           str           = Field(primary_key=True)
    mean_sprd:        Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(25, 20)))
    up_sprd:          Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(25, 20)))
    down_sprd:        Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(25, 20)))
    flat_sprd:        Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(25, 20)))
    steep_sprd:       Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(25, 20)))
    last_modified_by: Optional[str] = None
    last_update_date: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime, default=datetime.now))


class SprdLpUsr(SQLModel, table=True):
    """LP 스프레드 사용자 입력 (E_IR_SPRD_LP_USR)"""
    __tablename__ = "E_IR_SPRD_LP_USR"

    appl_st_yymm:     str           = Field(primary_key=True)
    appl_ed_yymm:     str           = Field(primary_key=True)
    appl_biz_dv:      str           = Field(primary_key=True)
    ir_curve_id:      str           = Field(primary_key=True)
    ir_curve_sce_no:  int           = Field(primary_key=True)
    mat_cd:           str           = Field(primary_key=True)
    liq_prem:         Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(22, 20)))
    last_modified_by: Optional[str] = None
    last_update_date: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime, default=datetime.now))


class RcCorpTm(SQLModel, table=True):
    """기업 전환행렬 (E_RC_CORP_TM)"""
    __tablename__ = "E_RC_CORP_TM"

    base_yymm:          str           = Field(primary_key=True)
    crd_eval_agncy_cd:  str           = Field(primary_key=True)
    from_crd_grd_cd:    str           = Field(primary_key=True)
    to_crd_grd_cd:      str           = Field(primary_key=True)
    trans_prob:         Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(10, 8)))
    last_modified_by:   Optional[str] = None
    last_update_date:   Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime, default=datetime.now))


class RcCorpTmUsr(SQLModel, table=True):
    """기업 전환행렬 사용자 입력 (E_RC_CORP_TM_USR)"""
    __tablename__ = "E_RC_CORP_TM_USR"

    base_yymm:          str           = Field(primary_key=True)
    crd_eval_agncy_cd:  str           = Field(primary_key=True)
    from_crd_grd_cd:    str           = Field(primary_key=True)
    trans_prob_1:       Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(10, 8)))
    trans_prob_2:       Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(10, 8)))
    trans_prob_3:       Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(10, 8)))
    trans_prob_4:       Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(10, 8)))
    trans_prob_5:       Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(10, 8)))
    trans_prob_6:       Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(10, 8)))
    trans_prob_7:       Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(10, 8)))
    last_modified_by:   Optional[str] = None
    last_update_date:   Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime, default=datetime.now))
