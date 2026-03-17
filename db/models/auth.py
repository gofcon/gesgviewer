"""
인증 / 사용자 / 권한 모델
Oracle: LETTNEMPLYRINFO → AppUser (신규)
        LETTNAUTHORINFO  → AuthInfo
        LETTNBASEDATE    → IndivBaseDt
"""
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text
from db.database import Base


class AppUser(Base):
    """로그인용 사용자 (신규 테이블)"""
    __tablename__ = "APP_USER"

    user_id     = Column(String(20),  primary_key=True, comment="사용자ID")
    user_nm     = Column(String(60),  nullable=False,   comment="사용자명")
    password    = Column(String(128), nullable=False,   comment="비밀번호(bcrypt)")
    email       = Column(String(100),                   comment="이메일")
    author_code = Column(String(30),                    comment="권한코드")
    use_at      = Column(String(1),   default="Y",      comment="사용여부")
    reg_dt      = Column(DateTime,    default=datetime.now, comment="등록일시")


class AuthInfo(Base):
    """권한 정보 (LETTNAUTHORINFO)"""
    __tablename__ = "LETTNAUTHORINFO"

    author_code    = Column(String(30), primary_key=True, comment="권한코드")
    author_nm      = Column(String(60), nullable=False,   comment="권한명")
    author_dc      = Column(String(200),                  comment="권한설명")
    author_creat_de= Column(String(20), nullable=False,   comment="권한생성일")


class AuthGroupInfo(Base):
    """그룹 정보 (LETTNAUTHORGROUPINFO)"""
    __tablename__ = "LETTNAUTHORGROUPINFO"

    group_id      = Column(String(20), primary_key=True, comment="그룹ID")
    group_nm      = Column(String(60), nullable=False,   comment="그룹명")
    group_creat_de= Column(String(20), nullable=False,   comment="그룹생성일")
    group_dc      = Column(String(100),                  comment="그룹설명")


class IndivBaseDt(Base):
    """유저별 기준년월 (LETTNBASEDATE)"""
    __tablename__ = "LETTNBASEDATE"

    user_id           = Column(String(100), primary_key=True, comment="유저ID")
    base_yymm         = Column(String(6),   primary_key=True, comment="기준년월")
    last_modified_by  = Column(String(100),                   comment="최종수정자")
    last_update_date  = Column(DateTime,                      comment="최종수정일자")


class LoginPolicy(Base):
    """로그인 정책 (LETTNLGNPOLICY)"""
    __tablename__ = "LETTNLGNPOLICY"

    emplyr_id = Column(String(20), primary_key=True, comment="업무사용자ID")
    ip_info   = Column(String(200),                  comment="IP정보")
    lmtt_at   = Column(String(1),  default="N",      comment="제한여부")
    reg_date  = Column(DateTime,   default=datetime.now, comment="등록일자")
