"""
스프레드 커브 / AFNS 스프레드 / 기업 부도율 / 검증 모델
"""
from datetime import datetime
from sqlalchemy import Column, String, Numeric, DateTime, Integer
from db.database import Base


class SprdCurve(Base):
    """위험스프레드 커브 (E_SPRD_CURVE)"""
    __tablename__ = "E_SPRD_CURVE"

    base_yymm        = Column(String(6),   primary_key=True, comment="기준년월")
    ir_curve_id      = Column(String(20),  primary_key=True, comment="금리커브ID")
    ir_typ_cd        = Column(String(10),  primary_key=True, comment="금리유형코드")
    mat_cd           = Column(String(10),  primary_key=True, comment="만기코드")
    sprd_val         = Column(Numeric(22, 10),               comment="스프레드값")
    last_modified_by = Column(String(100),                   comment="최종수정자")
    last_update_date = Column(DateTime, default=datetime.now, comment="최종수정일자")


class SprdAfnsBiz(Base):
    """AFNS 스프레드 (E_SPRD_AFNS_BIZ)"""
    __tablename__ = "E_SPRD_AFNS_BIZ"

    base_yymm        = Column(String(6),   primary_key=True, comment="기준년월")
    ir_model_id      = Column(String(20),  primary_key=True, comment="금리모델ID")
    ir_curve_id      = Column(String(20),  primary_key=True, comment="금리커브ID")
    param_typ_cd     = Column(String(20),  primary_key=True, comment="파라미터유형코드")
    param_val        = Column(Numeric(22, 10),               comment="파라미터값")
    last_modified_by = Column(String(100),                   comment="최종수정자")
    last_update_date = Column(DateTime, default=datetime.now, comment="최종수정일자")


class CorpPd(Base):
    """기업 부도율 (E_CORP_PD)"""
    __tablename__ = "E_CORP_PD"

    base_yymm        = Column(String(6),   primary_key=True, comment="기준년월")
    appl_biz_dv      = Column(String(10),  primary_key=True, comment="적용업무구분")
    crd_grd_cd       = Column(String(10),  primary_key=True, comment="신용등급코드")
    mat_cd           = Column(String(10),  primary_key=True, comment="만기코드")
    cum_pd           = Column(Numeric(22, 10),               comment="누적부도율")
    fwd_pd           = Column(Numeric(22, 10),               comment="선도부도율")
    last_modified_by = Column(String(100),                   comment="최종수정자")
    last_update_date = Column(DateTime, default=datetime.now, comment="최종수정일자")


class CrdCorpPd(Base):
    """신용등급 기업 부도율 (E_CRD_CORP_PD)"""
    __tablename__ = "E_CRD_CORP_PD"

    base_yymm        = Column(String(6),   primary_key=True, comment="기준년월")
    appl_biz_dv      = Column(String(10),  primary_key=True, comment="적용업무구분")
    crd_grd_cd       = Column(String(10),  primary_key=True, comment="신용등급코드")
    mat_cd           = Column(String(10),  primary_key=True, comment="만기코드")
    cum_pd           = Column(Numeric(22, 10),               comment="누적부도율")
    fwd_pd           = Column(Numeric(22, 10),               comment="선도부도율")
    last_modified_by = Column(String(100),                   comment="최종수정자")
    last_update_date = Column(DateTime, default=datetime.now, comment="최종수정일자")


class ValidSceFwd(Base):
    """시나리오 선도 검증 (E_VALID_SCE_FWD)"""
    __tablename__ = "E_VALID_SCE_FWD"

    base_yymm        = Column(String(6),   primary_key=True, comment="기준년월")
    appl_biz_dv      = Column(String(10),  primary_key=True, comment="적용업무구분")
    ir_curve_id      = Column(String(20),  primary_key=True, comment="금리커브ID")
    ir_curve_sce_no  = Column(Integer,     primary_key=True, comment="시나리오번호")
    mat_cd           = Column(String(10),  primary_key=True, comment="만기코드")
    valid_val        = Column(Numeric(22, 10),               comment="검증값")
    last_modified_by = Column(String(100),                   comment="최종수정자")
    last_update_date = Column(DateTime, default=datetime.now, comment="최종수정일자")


class ValidRnd(Base):
    """랜덤 검증 (E_VALID_RND)"""
    __tablename__ = "E_VALID_RND"

    base_yymm        = Column(String(6),   primary_key=True, comment="기준년월")
    appl_biz_dv      = Column(String(10),  primary_key=True, comment="적용업무구분")
    ir_curve_id      = Column(String(20),  primary_key=True, comment="금리커브ID")
    ir_curve_sce_no  = Column(Integer,     primary_key=True, comment="시나리오번호")
    rnd_seq          = Column(Integer,     primary_key=True, comment="난수순번")
    rnd_val          = Column(Numeric(22, 10),               comment="난수값")
    last_modified_by = Column(String(100),                   comment="최종수정자")
    last_update_date = Column(DateTime, default=datetime.now, comment="최종수정일자")


class ValidSceSto(Base):
    """시나리오 저장 검증 (E_VALID_SCE_STO)"""
    __tablename__ = "E_VALID_SCE_STO"

    base_yymm        = Column(String(6),   primary_key=True, comment="기준년월")
    appl_biz_dv      = Column(String(10),  primary_key=True, comment="적용업무구분")
    ir_curve_id      = Column(String(20),  primary_key=True, comment="금리커브ID")
    ir_curve_sce_no  = Column(Integer,     primary_key=True, comment="시나리오번호")
    valid_typ_cd     = Column(String(20),  primary_key=True, comment="검증유형코드")
    valid_val        = Column(Numeric(22, 10),               comment="검증값")
    last_modified_by = Column(String(100),                   comment="최종수정자")
    last_update_date = Column(DateTime, default=datetime.now, comment="최종수정일자")
