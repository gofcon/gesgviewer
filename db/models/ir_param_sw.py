"""
Smith-Wilson 파라미터 모델
Oracle: E_IR_PARAM_SW_USR, E_IR_PARAM_SW
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime, Numeric


class IrParamSwUsr(SQLModel, table=True):
    """SW 사용자 입력 파라미터 (E_IR_PARAM_SW_USR)"""
    __tablename__ = "E_IR_PARAM_SW_USR"

    appl_st_yymm:     str           = Field(primary_key=True)
    appl_ed_yymm:     str
    appl_biz_dv:      str           = Field(primary_key=True)
    ir_curve_id:      str           = Field(primary_key=True)
    ir_curve_sce_no:  int           = Field(primary_key=True)
    ir_curve_sce_nm:  Optional[str] = None
    cur_cd:           Optional[str] = None
    freq:             Optional[int] = None
    llp:              Optional[int] = None
    ltfr:             Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(22, 20)))
    ltfr_cp:          Optional[int] = None
    liq_prem:         Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(22, 20)))
    liq_prem_appl_dv: Optional[str] = None
    shk_sprd_sce_no:  Optional[int] = None
    sw_alpha_ytm:     Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(22, 20)))
    sto_sce_gen_yn:   Optional[str] = None
    fwd_mat_cd:       Optional[str] = None
    mult_int_rate:    Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(22, 20)))
    add_sprd:         Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(22, 20)))
    pvt_rate_mat_cd:  Optional[str] = None
    mult_pvt_rate:    Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(22, 20)))
    ytm_add_sprd:     Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(22, 20)))
    last_modified_by: Optional[str] = None
    last_update_date: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime, nullable=False, default=datetime.now))


class IrParamSw(SQLModel, table=True):
    """SW 산출 파라미터 (E_IR_PARAM_SW)"""
    __tablename__ = "E_IR_PARAM_SW"

    base_yymm:        str           = Field(primary_key=True)
    appl_biz_dv:      str           = Field(primary_key=True)
    ir_curve_id:      str           = Field(primary_key=True)
    ir_curve_sce_no:  int           = Field(primary_key=True)
    ir_curve_sce_nm:  Optional[str] = None
    cur_cd:           Optional[str] = None
    freq:             Optional[int] = None
    llp:              Optional[int] = None
    ltfr:             Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(22, 20)))
    ltfr_cp:          Optional[int] = None
    liq_prem:         Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(22, 20)))
    liq_prem_appl_dv: Optional[str] = None
    shk_sprd_sce_no:  Optional[int] = None
    sw_alpha_ytm:     Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(22, 20)))
    sto_sce_gen_yn:   Optional[str] = None
    fwd_mat_cd:       Optional[str] = None
    mult_int_rate:    Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(22, 20)))
    add_sprd:         Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(22, 20)))
    pvt_rate_mat_cd:  Optional[str] = None
    mult_pvt_rate:    Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(22, 20)))
    ytm_add_sprd:     Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(22, 20)))
    last_modified_by: Optional[str] = None
    last_update_date: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime, nullable=False, default=datetime.now))
