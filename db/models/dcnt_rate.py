"""
할인율 모델
Oracle: E_IR_DCNT_RATE_BIZ, E_IR_DCNT_STO_BIZ
"""
from datetime import datetime
from sqlalchemy import Column, String, Numeric, DateTime, Integer
from db.database import Base


class IrDcntRateBiz(Base):
    """할인율 비즈 (E_IR_DCNT_RATE_BIZ)"""
    __tablename__ = "E_IR_DCNT_RATE_BIZ"

    base_yymm        = Column(String(6),   primary_key=True, comment="기준년월")
    appl_biz_dv      = Column(String(10),  primary_key=True, comment="적용업무구분")
    ir_curve_id      = Column(String(20),  primary_key=True, comment="금리커브ID")
    ir_curve_sce_no  = Column(Integer,     primary_key=True, comment="금리커브시나리오번호")
    mat_cd           = Column(String(10),  primary_key=True, comment="만기코드")
    dcnt_rate        = Column(Numeric(22, 10),               comment="할인율")
    spot_rate        = Column(Numeric(22, 10),               comment="현물금리")
    fwd_rate         = Column(Numeric(22, 10),               comment="선도금리")
    last_modified_by = Column(String(100),                   comment="최종수정자")
    last_update_date = Column(DateTime, default=datetime.now, comment="최종수정일자")


class IrDcntStoBiz(Base):
    """할인율 시나리오 저장 (E_IR_DCNT_STO_BIZ)"""
    __tablename__ = "E_IR_DCNT_STO_BIZ"

    base_yymm        = Column(String(6),   primary_key=True, comment="기준년월")
    appl_biz_dv      = Column(String(10),  primary_key=True, comment="적용업무구분")
    ir_curve_id      = Column(String(20),  primary_key=True, comment="금리커브ID")
    ir_curve_sce_no  = Column(Integer,     primary_key=True, comment="금리커브시나리오번호")
    sce_path_no      = Column(Integer,     primary_key=True, comment="시나리오경로번호")
    mat_cd           = Column(String(10),  primary_key=True, comment="만기코드")
    rate_val         = Column(Numeric(22, 10),               comment="금리값")
    last_modified_by = Column(String(100),                   comment="최종수정자")
    last_update_date = Column(DateTime, default=datetime.now, comment="최종수정일자")
