"""
인증 / 사용자 / 권한 모델
Oracle: LETTNEMPLYRINFO → AppUser (신규)
        LETTNAUTHORINFO  → AuthInfo
        LETTNBASEDATE    → IndivBaseDt
"""
from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime


class AppUser(SQLModel, table=True):
    """로그인용 사용자 (신규 테이블)"""
    __tablename__ = "APP_USER"

    user_id:     str            = Field(primary_key=True)
    user_nm:     str
    password:    str
    email:       Optional[str]  = None
    author_code: Optional[str]  = None
    use_at:      str            = "Y"
    reg_dt:      Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime, default=datetime.now))


class AuthInfo(SQLModel, table=True):
    """권한 정보 (LETTNAUTHORINFO)"""
    __tablename__ = "LETTNAUTHORINFO"

    author_code:     str           = Field(primary_key=True)
    author_nm:       str
    author_dc:       Optional[str] = None
    author_creat_de: str


class AuthGroupInfo(SQLModel, table=True):
    """그룹 정보 (LETTNAUTHORGROUPINFO)"""
    __tablename__ = "LETTNAUTHORGROUPINFO"

    group_id:       str           = Field(primary_key=True)
    group_nm:       str
    group_creat_de: str
    group_dc:       Optional[str] = None


class IndivBaseDt(SQLModel, table=True):
    """유저별 기준년월 (LETTNBASEDATE)"""
    __tablename__ = "LETTNBASEDATE"

    user_id:          str           = Field(primary_key=True)
    base_yymm:        str           = Field(primary_key=True)
    last_modified_by: Optional[str] = None
    last_update_date: Optional[datetime] = None


class LoginPolicy(SQLModel, table=True):
    """로그인 정책 (LETTNLGNPOLICY)"""
    __tablename__ = "LETTNLGNPOLICY"

    emplyr_id: str           = Field(primary_key=True)
    ip_info:   Optional[str] = None
    lmtt_at:   str           = "N"
    reg_date:  Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime, default=datetime.now))
