"""
파라미터 모델 / AFNS 파라미터
Oracle: E_IR_PARAM_MODEL, E_IR_PARAM_AFNS_BIZ
"""
from datetime import datetime
from sqlalchemy import Column, String, Numeric, DateTime
from db.database import Base


class IrParamModel(Base):
    """금리 파라미터 모델 (E_IR_PARAM_MODEL)"""
    __tablename__ = "E_IR_PARAM_MODEL"

    ir_model_id      = Column(String(20),  primary_key=True, comment="금리모델ID")
    ir_curve_id      = Column(String(20),  primary_key=True, comment="금리커브ID")
    ir_model_nm      = Column(String(100),                   comment="금리모델명")
    ir_model_dc      = Column(String(500),                   comment="금리모델설명")
    use_at           = Column(String(1),   default="Y",      comment="사용여부")
    last_modified_by = Column(String(100),                   comment="최종수정자")
    last_update_date = Column(DateTime, default=datetime.now, comment="최종수정일자")


class IrParamAfnsBiz(Base):
    """AFNS 모수생성결과 (E_IR_PARAM_AFNS_BIZ)"""
    __tablename__ = "E_IR_PARAM_AFNS_BIZ"

    base_yymm        = Column(String(6),   primary_key=True, comment="기준년월")
    ir_model_id      = Column(String(20),  primary_key=True, comment="금리모델ID")
    ir_curve_id      = Column(String(20),  primary_key=True, comment="금리커브ID")
    param_typ_cd     = Column(String(20),  primary_key=True, comment="파라미터유형코드")
    param_val        = Column(Numeric(22, 10),               comment="파라미터값")
    last_modified_by = Column(String(100),                   comment="최종수정자")
    last_update_date = Column(DateTime, default=datetime.now, comment="최종수정일자")


class VolSwpn(Base):
    """변동성/스왑션 (E_VOL_SWPN)"""
    __tablename__ = "E_VOL_SWPN"

    base_yymm        = Column(String(6),   primary_key=True, comment="기준년월")
    appl_biz_dv      = Column(String(10),  primary_key=True, comment="적용업무구분")
    ir_curve_id      = Column(String(20),  primary_key=True, comment="금리커브ID")
    opt_mat_cd       = Column(String(10),  primary_key=True, comment="옵션만기코드")
    swpn_mat_cd      = Column(String(10),  primary_key=True, comment="스왑션만기코드")
    vol_val          = Column(Numeric(22, 10),               comment="변동성값")
    last_modified_by = Column(String(100),                   comment="최종수정자")
    last_update_date = Column(DateTime, default=datetime.now, comment="최종수정일자")
