"""
금리 커브 / YTM 사용자 입력
Oracle: E_IR_CURVE, E_IR_CURVE_YTM_USR
"""
from datetime import datetime
from sqlalchemy import Column, String, Numeric, DateTime, Integer
from db.database import Base


class IrCurve(Base):
    """금리 커브 (E_IR_CURVE)"""
    __tablename__ = "E_IR_CURVE"

    ir_curve_id      = Column(String(20),  primary_key=True, comment="금리커브ID")
    ir_curve_nm      = Column(String(100),                   comment="금리커브명")
    cur_cd           = Column(String(3),                     comment="통화코드")
    ir_curve_typ_cd  = Column(String(10),                    comment="금리커브유형코드")
    use_at           = Column(String(1),   default="Y",      comment="사용여부")
    last_modified_by = Column(String(100),                   comment="최종수정자")
    last_update_date = Column(DateTime, default=datetime.now, comment="최종수정일자")


class IrCurveSpot(Base):
    """금리 커브 현물 (E_IR_CURVE_SPOT) — IrCurveList.jsp 기준"""
    __tablename__ = "E_IR_CURVE_SPOT"

    base_yymm        = Column(String(6),   primary_key=True, comment="기준년월")
    appl_biz_dv      = Column(String(10),  primary_key=True, comment="적용업무구분")
    ir_curve_id      = Column(String(20),  primary_key=True, comment="금리커브ID")
    mat_cd           = Column(String(10),  primary_key=True, comment="만기코드")
    spot_rate        = Column(Numeric(22, 10),               comment="현물금리")
    dcnt_rate        = Column(Numeric(22, 10),               comment="할인율")
    last_modified_by = Column(String(100),                   comment="최종수정자")
    last_update_date = Column(DateTime, default=datetime.now, comment="최종수정일자")


class IrCurveYtmUsr(Base):
    """YTM 사용자 입력 (E_IR_CURVE_YTM_USR)"""
    __tablename__ = "E_IR_CURVE_YTM_USR"

    base_date        = Column(String(8),   primary_key=True, comment="기준일자")
    ir_curve_id      = Column(String(20),  primary_key=True, comment="금리커브ID")
    mat_cd           = Column(String(10),  primary_key=True, comment="만기코드")
    ytm_rate         = Column(Numeric(22, 10),               comment="YTM금리")
    last_modified_by = Column(String(100),                   comment="최종수정자")
    last_update_date = Column(DateTime, default=datetime.now, comment="최종수정일자")
