"""
할인율 모델
Oracle: E_IR_DCNT_RATE_BIZ, E_IR_DCNT_SCE_STO_BIZ
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime, Numeric


class IrDcntRateBiz(SQLModel, table=True):
    """할인율 비즈 (E_IR_DCNT_RATE_BIZ)"""
    __tablename__ = "E_IR_DCNT_RATE_BIZ"

    base_yymm:        str           = Field(primary_key=True)
    appl_biz_dv:      str           = Field(primary_key=True)
    ir_curve_id:      str           = Field(primary_key=True)
    ir_curve_sce_no:  int           = Field(primary_key=True)
    mat_cd:           str           = Field(primary_key=True)
    spot_rate:        Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(22, 20)))
    fwd_rate:         Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(22, 20)))
    last_modified_by: Optional[str] = None
    last_update_date: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime, default=datetime.now))


class IrDcntSceSto(SQLModel, table=True):
    """할인율 확률시나리오 저장 (E_IR_DCNT_SCE_STO_BIZ)"""
    __tablename__ = "E_IR_DCNT_SCE_STO_BIZ"

    base_yymm:        str           = Field(primary_key=True)
    appl_biz_dv:      str           = Field(primary_key=True)
    ir_model_id:      str           = Field(primary_key=True)
    ir_curve_id:      str           = Field(primary_key=True)
    ir_curve_sce_no:  int           = Field(primary_key=True)
    sce_no:           int           = Field(primary_key=True)
    mat_cd:           str           = Field(primary_key=True)
    spot_rate:        Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(22, 20)))
    fwd_rate:         Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(22, 20)))
    last_modified_by: Optional[str] = None
    last_update_date: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime, default=datetime.now))


class IrDcntRateUsr(SQLModel, table=True):
    """할인율 사용자 입력 (E_IR_DCNT_RATE_USR)"""
    __tablename__ = "E_IR_DCNT_RATE_USR"

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


class IrDcntRateBu(SQLModel, table=True):
    """할인율 BU (E_IR_DCNT_RATE_BU)"""
    __tablename__ = "E_IR_DCNT_RATE_BU"

    base_yymm:           str           = Field(primary_key=True)
    appl_biz_dv:         str           = Field(primary_key=True)
    ir_curve_id:         str           = Field(primary_key=True)
    ir_curve_sce_no:     int           = Field(primary_key=True)
    mat_cd:              str           = Field(primary_key=True)
    spot_rate_disc:      Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(22, 20)))
    spot_rate_cont:      Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(22, 20)))
    liq_prem:            Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(22, 20)))
    adj_spot_rate_disc:  Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(22, 20)))
    adj_spot_rate_cont:  Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(22, 20)))
    add_sprd:            Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(22, 20)))
    last_modified_by:    Optional[str] = None
    last_update_date:    Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime, default=datetime.now))


class IrDcntRateBuIm(SQLModel, table=True):
    """할인율 BU 내부모형 (E_IR_DCNT_RATE_BU_IM)"""
    __tablename__ = "E_IR_DCNT_RATE_BU_IM"

    base_yymm:           str           = Field(primary_key=True)
    appl_biz_dv:         str           = Field(primary_key=True)
    ir_model_id:         str           = Field(primary_key=True)
    ir_curve_id:         str           = Field(primary_key=True)
    ir_curve_sce_no:     int           = Field(primary_key=True)
    mat_cd:              str           = Field(primary_key=True)
    spot_rate_disc:      Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(22, 20)))
    spot_rate_cont:      Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(22, 20)))
    liq_prem:            Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(22, 20)))
    adj_spot_rate_disc:  Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(22, 20)))
    adj_spot_rate_cont:  Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(22, 20)))
    add_sprd:            Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(22, 20)))
    last_modified_by:    Optional[str] = None
    last_update_date:    Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime, default=datetime.now))


class IrDcntSceDet(SQLModel, table=True):
    """확률시나리오 상세(비즈) (E_IR_DCNT_SCE_DET_BIZ)"""
    __tablename__ = "E_IR_DCNT_SCE_DET_BIZ"

    base_yymm:        str           = Field(primary_key=True)
    appl_biz_dv:      str           = Field(primary_key=True)
    ir_model_id:      str           = Field(primary_key=True)
    ir_curve_id:      str           = Field(primary_key=True)
    ir_curve_sce_no:  int           = Field(primary_key=True)
    mat_cd:           str           = Field(primary_key=True)
    spot_rate:        Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(22, 20)))
    fwd_rate:         Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(22, 20)))
    last_modified_by: Optional[str] = None
    last_update_date: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime, default=datetime.now))


class IrDcntSceIm(SQLModel, table=True):
    """확률시나리오 내부모형 (E_IR_DCNT_SCE_IM)"""
    __tablename__ = "E_IR_DCNT_SCE_IM"

    base_yymm:        str           = Field(primary_key=True)
    appl_biz_dv:      str           = Field(primary_key=True)
    ir_model_id:      str           = Field(primary_key=True)
    ir_curve_id:      str           = Field(primary_key=True)
    ir_curve_sce_no:  int           = Field(primary_key=True)
    mat_cd:           str           = Field(primary_key=True)
    spot_rate:        Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(22, 20)))
    fwd_rate:         Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(22, 20)))
    last_modified_by: Optional[str] = None
    last_update_date: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime, default=datetime.now))


class IrDcntSceStoGnr(SQLModel, table=True):
    """확률시나리오 저장(일반) (E_IR_DCNT_SCE_STO_GNR)"""
    __tablename__ = "E_IR_DCNT_SCE_STO_GNR"

    base_yymm:        str           = Field(primary_key=True)
    appl_biz_dv:      str           = Field(primary_key=True)
    ir_model_id:      str           = Field(primary_key=True)
    ir_curve_id:      str           = Field(primary_key=True)
    ir_curve_sce_no:  int           = Field(primary_key=True)
    sce_no:           int           = Field(primary_key=True)
    mat_cd:           str           = Field(primary_key=True)
    spot_rate:        Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(22, 20)))
    fwd_rate:         Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(22, 20)))
    last_modified_by: Optional[str] = None
    last_update_date: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime, default=datetime.now))
