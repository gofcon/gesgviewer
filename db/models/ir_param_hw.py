"""
Hull-White 파라미터 모델
Oracle: E_IR_PARAM_HW_CALC, E_IR_PARAM_HW_BIZ
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime, Numeric


class IrParamHwCalc(SQLModel, table=True):
    """HW 파라미터 계산 결과 (E_IR_PARAM_HW_CALC)"""
    __tablename__ = "E_IR_PARAM_HW_CALC"

    base_yymm:        str           = Field(primary_key=True)
    ir_model_id:      str           = Field(primary_key=True)
    ir_curve_id:      str           = Field(primary_key=True)
    mat_cd:           str           = Field(primary_key=True)
    param_typ_cd:     str           = Field(primary_key=True)
    param_val:        Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(22, 10)))
    last_modified_by: Optional[str] = None
    last_update_date: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime, default=datetime.now))


class IrParamHwBiz(SQLModel, table=True):
    """HW 파라미터 업무 적용 (E_IR_PARAM_HW_BIZ)"""
    __tablename__ = "E_IR_PARAM_HW_BIZ"

    base_yymm:        str           = Field(primary_key=True)
    appl_biz_dv:      str           = Field(primary_key=True)
    ir_model_id:      str           = Field(primary_key=True)
    ir_curve_id:      str           = Field(primary_key=True)
    mat_cd:           str           = Field(primary_key=True)
    param_typ_cd:     str           = Field(primary_key=True)
    param_val:        Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(22, 10)))
    last_modified_by: Optional[str] = None
    last_update_date: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime, default=datetime.now))


class IrParamHwRnd(SQLModel, table=True):
    """HW 난수 (E_IR_PARAM_HW_RND)"""
    __tablename__ = "E_IR_PARAM_HW_RND"

    base_yymm:        str           = Field(primary_key=True)
    ir_model_id:      str           = Field(primary_key=True)
    ir_curve_id:      str           = Field(primary_key=True)
    sce_no:           int           = Field(primary_key=True)
    mat_cd:           str           = Field(primary_key=True)
    rnd_num:          Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(22, 20)))
    last_modified_by: Optional[str] = None
    last_update_date: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime, default=datetime.now))


class IrParamHwUsr(SQLModel, table=True):
    """HW 파라미터 사용자 입력 (E_IR_PARAM_HW_USR)"""
    __tablename__ = "E_IR_PARAM_HW_USR"

    base_yymm:        str           = Field(primary_key=True)
    appl_biz_dv:      str           = Field(primary_key=True)
    ir_model_id:      str           = Field(primary_key=True)
    ir_curve_id:      str           = Field(primary_key=True)
    mat_cd:           str           = Field(primary_key=True)
    param_typ_cd:     str           = Field(primary_key=True)
    param_val:        Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(25, 20)))
    last_modified_by: Optional[str] = None
    last_update_date: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime, default=datetime.now))
