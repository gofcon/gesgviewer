"""
Hull-White 파라미터 모델
Oracle: E_IR_PARAM_HW_CALC, E_IR_PARAM_HW_BIZ
"""
from datetime import datetime
from sqlalchemy import Column, String, Numeric, DateTime
from db.database import Base


class IrParamHwCalc(Base):
    """HW 파라미터 계산 결과 (E_IR_PARAM_HW_CALC)"""
    __tablename__ = "E_IR_PARAM_HW_CALC"

    base_yymm        = Column(String(6),   primary_key=True, comment="기준년월")
    ir_model_id      = Column(String(20),  primary_key=True, comment="금리모델ID")
    ir_curve_id      = Column(String(20),  primary_key=True, comment="금리커브ID")
    mat_cd           = Column(String(10),  primary_key=True, comment="만기코드")
    param_typ_cd     = Column(String(20),  primary_key=True, comment="파라미터유형코드")
    param_val        = Column(Numeric(22, 10),               comment="파라미터값")
    last_modified_by = Column(String(100),                   comment="최종수정자")
    last_update_date = Column(DateTime, default=datetime.now, comment="최종수정일자")


class IrParamHwBiz(Base):
    """HW 파라미터 업무 적용 (E_IR_PARAM_HW_BIZ)"""
    __tablename__ = "E_IR_PARAM_HW_BIZ"

    base_yymm        = Column(String(6),   primary_key=True, comment="기준년월")
    appl_biz_dv      = Column(String(10),  primary_key=True, comment="적용업무구분")
    ir_model_id      = Column(String(20),  primary_key=True, comment="금리모델ID")
    ir_curve_id      = Column(String(20),  primary_key=True, comment="금리커브ID")
    mat_cd           = Column(String(10),  primary_key=True, comment="만기코드")
    param_typ_cd     = Column(String(20),  primary_key=True, comment="파라미터유형코드")
    param_val        = Column(Numeric(22, 10),               comment="파라미터값")
    last_modified_by = Column(String(100),                   comment="최종수정자")
    last_update_date = Column(DateTime, default=datetime.now, comment="최종수정일자")
