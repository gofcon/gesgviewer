"""
Smith-Wilson 파라미터 모델
Oracle: E_IR_PARAM_SW_USR, E_IR_PARAM_SW
"""
from datetime import datetime
from sqlalchemy import Column, String, Numeric, DateTime, Integer
from db.database import Base


class IrParamSwUsr(Base):
    """SW 사용자 입력 파라미터 (E_IR_PARAM_SW_USR)"""
    __tablename__ = "E_IR_PARAM_SW_USR"

    appl_st_yymm     = Column(String(6),   primary_key=True, comment="적용시작년월")
    appl_ed_yymm     = Column(String(6),   nullable=False,   comment="적용종료년월")
    appl_biz_dv      = Column(String(10),  primary_key=True, comment="적용업무구분")
    ir_curve_id      = Column(String(20),  primary_key=True, comment="금리커브ID")
    ir_curve_sce_no  = Column(Integer,     primary_key=True, comment="금리커브시나리오번호")
    ir_curve_sce_nm  = Column(String(100),                   comment="금리커브시나리오명")
    cur_cd           = Column(String(3),                     comment="통화코드")
    freq             = Column(Integer,                       comment="이자지급횟수(년)")
    llp              = Column(Integer,                       comment="최종유동성만기(년)")
    ltfr             = Column(Numeric(22, 20),               comment="장기선도금리")
    ltfr_cp          = Column(Integer,                       comment="장기선도금리수렴연도(년)")
    liq_prem         = Column(Numeric(22, 20),               comment="유동성프리미엄")
    liq_prem_appl_dv = Column(String(1),                     comment="유동성프리미엄적용구분")
    shk_sprd_sce_no  = Column(Integer,                       comment="충격스프레드시나리오번호")
    sw_alpha_ytm     = Column(Numeric(22, 20),               comment="SW_ALPHA(YTM)")
    sto_sce_gen_yn   = Column(String(1),                     comment="확률시나리오생성여부")
    fwd_mat_cd       = Column(String(6),                     comment="선도금리만기코드")
    mult_int_rate    = Column(Numeric(22, 20),               comment="금리배수비율")
    add_sprd         = Column(Numeric(22, 20),               comment="가산스프레드")
    pvt_rate_mat_cd  = Column(String(6),                     comment="PIVOT금리만기코드")
    mult_pvt_rate    = Column(Numeric(22, 20),               comment="PIVOT금리배수비율")
    last_modified_by = Column(String(100),                   comment="최종수정자")
    last_update_date = Column(DateTime, nullable=False, default=datetime.now, comment="최종수정일자")


class IrParamSw(Base):
    """SW 산출 파라미터 (E_IR_PARAM_SW)"""
    __tablename__ = "E_IR_PARAM_SW"

    base_yymm        = Column(String(6),   primary_key=True, comment="기준년월")
    appl_biz_dv      = Column(String(10),  primary_key=True, comment="적용업무구분")
    ir_curve_id      = Column(String(20),  primary_key=True, comment="금리커브ID")
    ir_curve_sce_no  = Column(Integer,     primary_key=True, comment="금리커브시나리오번호")
    ir_curve_sce_nm  = Column(String(100),                   comment="금리커브시나리오명")
    cur_cd           = Column(String(3),                     comment="통화코드")
    freq             = Column(Integer,                       comment="이자지급횟수(년)")
    llp              = Column(Integer,                       comment="최종유동성만기(년)")
    ltfr             = Column(Numeric(22, 20),               comment="장기선도금리")
    ltfr_cp          = Column(Integer,                       comment="장기선도금리수렴연도(년)")
    liq_prem         = Column(Numeric(22, 20),               comment="유동성프리미엄")
    liq_prem_appl_dv = Column(String(1),                     comment="유동성프리미엄적용구분")
    shk_sprd_sce_no  = Column(Integer,                       comment="충격스프레드시나리오번호")
    sw_alpha_ytm     = Column(Numeric(22, 20),               comment="SW_ALPHA(YTM)")
    sto_sce_gen_yn   = Column(String(1),                     comment="확률시나리오생성여부")
    fwd_mat_cd       = Column(String(6),                     comment="선도금리만기코드")
    mult_int_rate    = Column(Numeric(22, 20),               comment="금리배수비율")
    add_sprd         = Column(Numeric(22, 20),               comment="가산스프레드")
    pvt_rate_mat_cd  = Column(String(6),                     comment="PIVOT금리만기코드")
    mult_pvt_rate    = Column(Numeric(22, 20),               comment="PIVOT금리배수비율")
    last_modified_by = Column(String(100),                   comment="최종수정자")
    last_update_date = Column(DateTime, nullable=False, default=datetime.now, comment="최종수정일자")
