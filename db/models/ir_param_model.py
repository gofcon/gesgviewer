"""
파라미터 모델 / AFNS 파라미터 / 변동성
Oracle: E_IR_PARAM_MODEL, E_IR_PARAM_AFNS_BIZ, E_IR_VOL_SWPN
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime, Numeric


class IrParamModel(SQLModel, table=True):
    """금리 파라미터 모델 (E_IR_PARAM_MODEL)"""
    __tablename__ = "E_IR_PARAM_MODEL"

    ir_model_id:      str           = Field(primary_key=True)
    ir_curve_id:      str           = Field(primary_key=True)
    ir_model_nm:      Optional[str] = None
    total_sce_no:     Optional[str] = None
    rnd_seed:         Optional[str] = None
    itr_tol:          Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(22, 20)))
    use_yn:           Optional[str] = None
    last_modified_by: Optional[str] = None
    last_update_date: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime, default=datetime.now))


class IrParamAfnsBiz(SQLModel, table=True):
    """AFNS 모수생성결과 (E_IR_PARAM_AFNS_BIZ)"""
    __tablename__ = "E_IR_PARAM_AFNS_BIZ"

    base_yymm:        str           = Field(primary_key=True)
    ir_model_id:      str           = Field(primary_key=True)
    ir_curve_id:      str           = Field(primary_key=True)
    param_typ_cd:     str           = Field(primary_key=True)
    param_val:        Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(25, 20)))
    last_modified_by: Optional[str] = None
    last_update_date: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime, default=datetime.now))


class IrVolSwpn(SQLModel, table=True):
    """변동성/스왑션 (E_IR_VOL_SWPN)"""
    __tablename__ = "E_IR_VOL_SWPN"

    base_yymm:        str           = Field(primary_key=True)
    ir_curve_id:      str           = Field(primary_key=True)
    swpn_mat_num:     Decimal       = Field(
        sa_column=Column(Numeric(7, 2), primary_key=True, nullable=False))
    swap_ten_num:     Decimal       = Field(
        sa_column=Column(Numeric(7, 2), primary_key=True, nullable=False))
    vol:              Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(25, 20)))
    last_modified_by: Optional[str] = None
    last_update_date: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime, default=datetime.now))


class IrParamAfnsCalc(SQLModel, table=True):
    """AFNS 모수 계산 (E_IR_PARAM_AFNS_CALC)"""
    __tablename__ = "E_IR_PARAM_AFNS_CALC"

    base_yymm:        str           = Field(primary_key=True)
    ir_model_id:      str           = Field(primary_key=True)
    ir_curve_id:      str           = Field(primary_key=True)
    param_typ_cd:     str           = Field(primary_key=True)
    param_val:        Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(25, 20)))
    last_modified_by: Optional[str] = None
    last_update_date: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime, default=datetime.now))


class IrParamAfnsUsr(SQLModel, table=True):
    """AFNS 파라미터 사용자 입력 (E_IR_PARAM_AFNS_USR)"""
    __tablename__ = "E_IR_PARAM_AFNS_USR"

    base_yymm:        str           = Field(primary_key=True)
    ir_model_id:      str           = Field(primary_key=True)
    ir_curve_id:      str           = Field(primary_key=True)
    param_typ_cd:     str           = Field(primary_key=True)
    param_val:        Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(25, 20)))
    last_modified_by: Optional[str] = None
    last_update_date: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime, default=datetime.now))


class IrParamModelCalc(SQLModel, table=True):
    """파라미터 모델 계산 (E_IR_PARAM_MODEL_CALC)"""
    __tablename__ = "E_IR_PARAM_MODEL_CALC"

    base_yymm:        str           = Field(primary_key=True)
    ir_model_id:      str           = Field(primary_key=True)
    ir_curve_id:      str           = Field(primary_key=True)
    param_typ_cd:     str           = Field(primary_key=True)
    param_val:        Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(25, 20)))
    last_modified_by: Optional[str] = None
    last_update_date: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime, default=datetime.now))


class IrParamModelBiz(SQLModel, table=True):
    """파라미터 모델 비즈 (E_IR_PARAM_MODEL_BIZ)"""
    __tablename__ = "E_IR_PARAM_MODEL_BIZ"

    base_yymm:        str           = Field(primary_key=True)
    ir_model_id:      str           = Field(primary_key=True)
    ir_curve_id:      str           = Field(primary_key=True)
    param_typ_cd:     str           = Field(primary_key=True)
    param_val:        Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(25, 20)))
    last_modified_by: Optional[str] = None
    last_update_date: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime, default=datetime.now))


class IrParamModelRnd(SQLModel, table=True):
    """파라미터 모델 난수 (E_IR_PARAM_MODEL_RND)"""
    __tablename__ = "E_IR_PARAM_MODEL_RND"

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


class IrParamModelUsr(SQLModel, table=True):
    """파라미터 모델 사용자 입력 (E_IR_PARAM_MODEL_USR)"""
    __tablename__ = "E_IR_PARAM_MODEL_USR"

    appl_st_yymm:     str           = Field(primary_key=True)
    appl_ed_yymm:     str           = Field(primary_key=True)
    ir_model_id:      str           = Field(primary_key=True)
    ir_curve_id:      str           = Field(primary_key=True)
    param_typ_cd:     str           = Field(primary_key=True)
    param_val:        Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(25, 20)))
    last_modified_by: Optional[str] = None
    last_update_date: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime, default=datetime.now))


class IrVolSwpnUsr(SQLModel, table=True):
    """변동성/스왑션 사용자 입력 (E_IR_VOL_SWPN_USR)"""
    __tablename__ = "E_IR_VOL_SWPN_USR"

    base_date:        str           = Field(primary_key=True)
    ir_curve_id:      str           = Field(primary_key=True)
    swpn_mat:         str           = Field(primary_key=True)
    vol_swpn_y1:      Optional[Decimal] = Field(default=None, sa_column=Column(Numeric(25, 20)))
    vol_swpn_y2:      Optional[Decimal] = Field(default=None, sa_column=Column(Numeric(25, 20)))
    vol_swpn_y3:      Optional[Decimal] = Field(default=None, sa_column=Column(Numeric(25, 20)))
    vol_swpn_y4:      Optional[Decimal] = Field(default=None, sa_column=Column(Numeric(25, 20)))
    vol_swpn_y5:      Optional[Decimal] = Field(default=None, sa_column=Column(Numeric(25, 20)))
    vol_swpn_y7:      Optional[Decimal] = Field(default=None, sa_column=Column(Numeric(25, 20)))
    vol_swpn_y10:     Optional[Decimal] = Field(default=None, sa_column=Column(Numeric(25, 20)))
    vol_swpn_y12:     Optional[Decimal] = Field(default=None, sa_column=Column(Numeric(25, 20)))
    vol_swpn_y15:     Optional[Decimal] = Field(default=None, sa_column=Column(Numeric(25, 20)))
    vol_swpn_y20:     Optional[Decimal] = Field(default=None, sa_column=Column(Numeric(25, 20)))
    vol_swpn_y25:     Optional[Decimal] = Field(default=None, sa_column=Column(Numeric(25, 20)))
    vol_swpn_y30:     Optional[Decimal] = Field(default=None, sa_column=Column(Numeric(25, 20)))
    last_modified_by: Optional[str] = None
    last_update_date: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime, default=datetime.now))


class IrValidParamHw(SQLModel, table=True):
    """HW 파라미터 검증 (E_IR_VALID_PARAM_HW)"""
    __tablename__ = "E_IR_VALID_PARAM_HW"

    base_yymm:        str           = Field(primary_key=True)
    ir_model_id:      str           = Field(primary_key=True)
    ir_curve_id:      str           = Field(primary_key=True)
    swpn_mat_num:     Decimal       = Field(
        sa_column=Column(Numeric(7, 2), primary_key=True, nullable=False))
    swap_ten_num:     Decimal       = Field(
        sa_column=Column(Numeric(7, 2), primary_key=True, nullable=False))
    valid_dv:         str           = Field(primary_key=True)
    valid_val1:       Optional[Decimal] = Field(default=None, sa_column=Column(Numeric(25, 20)))
    valid_val2:       Optional[Decimal] = Field(default=None, sa_column=Column(Numeric(25, 20)))
    valid_val3:       Optional[Decimal] = Field(default=None, sa_column=Column(Numeric(25, 20)))
    valid_val4:       Optional[Decimal] = Field(default=None, sa_column=Column(Numeric(25, 20)))
    valid_val5:       Optional[Decimal] = Field(default=None, sa_column=Column(Numeric(25, 20)))
    last_modified_by: Optional[str] = None
    last_update_date: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime, default=datetime.now))


class IrQvalSce(SQLModel, table=True):
    """Q값 시나리오 검증 (E_IR_QVAL_SCE)"""
    __tablename__ = "E_IR_QVAL_SCE"

    base_yymm:        str           = Field(primary_key=True)
    appl_biz_dv:      str           = Field(primary_key=True)
    ir_model_id:      str           = Field(primary_key=True)
    ir_curve_id:      str           = Field(primary_key=True)
    ir_curve_sce_no:  int           = Field(primary_key=True)
    qval_dv:          str           = Field(primary_key=True)
    qval_seq:         int           = Field(primary_key=True)
    qval1:            Optional[Decimal] = Field(default=None, sa_column=Column(Numeric(25, 20)))
    qval2:            Optional[Decimal] = Field(default=None, sa_column=Column(Numeric(25, 20)))
    qval3:            Optional[Decimal] = Field(default=None, sa_column=Column(Numeric(25, 20)))
    qval4:            Optional[Decimal] = Field(default=None, sa_column=Column(Numeric(25, 20)))
    qval5:            Optional[Decimal] = Field(default=None, sa_column=Column(Numeric(25, 20)))
    qval6:            Optional[Decimal] = Field(default=None, sa_column=Column(Numeric(25, 20)))
    qval7:            Optional[Decimal] = Field(default=None, sa_column=Column(Numeric(25, 20)))
    qval8:            Optional[Decimal] = Field(default=None, sa_column=Column(Numeric(25, 20)))
    qval9:            Optional[Decimal] = Field(default=None, sa_column=Column(Numeric(25, 20)))
    qval10:           Optional[Decimal] = Field(default=None, sa_column=Column(Numeric(25, 20)))
    qval11:           Optional[Decimal] = Field(default=None, sa_column=Column(Numeric(25, 20)))
    qval12:           Optional[Decimal] = Field(default=None, sa_column=Column(Numeric(25, 20)))
    qval13:           Optional[Decimal] = Field(default=None, sa_column=Column(Numeric(25, 20)))
    qval14:           Optional[Decimal] = Field(default=None, sa_column=Column(Numeric(25, 20)))
    qval15:           Optional[Decimal] = Field(default=None, sa_column=Column(Numeric(25, 20)))
    last_modified_by: Optional[str] = None
    last_update_date: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime, default=datetime.now))
