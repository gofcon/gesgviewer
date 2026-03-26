"""
금리 커브 / YTM 사용자 입력
Oracle: E_IR_CURVE, E_IR_CURVE_SPOT, E_IR_CURVE_YTM_USR
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime, Numeric


class IrCurve(SQLModel, table=True):
    """금리 커브 (E_IR_CURVE)"""
    __tablename__ = "E_IR_CURVE"

    ir_curve_id:      str           = Field(primary_key=True)
    ir_curve_nm:      Optional[str] = None
    cur_cd:           Optional[str] = None
    appl_meth_dv:     Optional[str] = None
    crd_grd_cd:       Optional[str] = None
    intp_meth_cd:     Optional[str] = None
    use_yn:           Optional[str] = None
    last_modified_by: Optional[str] = None
    last_update_date: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime, default=datetime.now))


class IrCurveSpot(SQLModel, table=True):
    """금리 커브 현물 (E_IR_CURVE_SPOT)"""
    __tablename__ = "E_IR_CURVE_SPOT"

    base_date:        str           = Field(primary_key=True)
    ir_curve_id:      str           = Field(primary_key=True)
    mat_cd:           str           = Field(primary_key=True)
    spot_rate:        Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(22, 20)))
    last_modified_by: Optional[str] = None
    last_update_date: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime, default=datetime.now))


class IrCurveYtmUsr(SQLModel, table=True):
    """YTM 사용자 입력 (E_IR_CURVE_YTM_USR)"""
    __tablename__ = "E_IR_CURVE_YTM_USR"

    base_date:        str           = Field(primary_key=True)
    ir_curve_id:      str           = Field(primary_key=True)
    mat_cd:           str           = Field(primary_key=True)
    ytm:              Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(22, 20)))
    last_modified_by: Optional[str] = None
    last_update_date: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime, default=datetime.now))


class IrCurveYtm(SQLModel, table=True):
    """금리커브 YTM (E_IR_CURVE_YTM)"""
    __tablename__ = "E_IR_CURVE_YTM"

    base_date:        str           = Field(primary_key=True)
    ir_curve_id:      str           = Field(primary_key=True)
    mat_cd:           str           = Field(primary_key=True)
    ytm:              Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(22, 20)))
    ticker_nm:        Optional[str] = None
    last_modified_by: Optional[str] = None
    last_update_date: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime, default=datetime.now))


class IrCurveSpotWeek(SQLModel, table=True):
    """금리커브 현물(주간) (E_IR_CURVE_SPOT_WEEK)"""
    __tablename__ = "E_IR_CURVE_SPOT_WEEK"

    base_date:        str           = Field(primary_key=True)
    ir_curve_id:      str           = Field(primary_key=True)
    mat_cd:           str           = Field(primary_key=True)
    spot_rate:        Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(22, 20)))
    day_of_week:      Optional[str] = None
    biz_day_type:     Optional[str] = None
    last_modified_by: Optional[str] = None
    last_update_date: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime, default=datetime.now))


class IrCurveFwd(SQLModel, table=True):
    """금리커브 선도 (E_IR_CURVE_FWD)"""
    __tablename__ = "E_IR_CURVE_FWD"

    base_date:        str           = Field(primary_key=True)
    ir_curve_id:      str           = Field(primary_key=True)
    fwd_mat_cd:       str           = Field(primary_key=True)
    mat_cd:           str           = Field(primary_key=True)
    int_rate:         Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(22, 20)))
    last_modified_by: Optional[str] = None
    last_update_date: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime, default=datetime.now))


class IrCurveSceBiz(SQLModel, table=True):
    """금리커브 시나리오(비즈) (E_IR_CURVE_SCE_BIZ)"""
    __tablename__ = "E_IR_CURVE_SCE_BIZ"

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
