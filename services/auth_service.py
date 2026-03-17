"""
인증 서비스
Spring: AuthGroupList, AuthInfoList, LgnPolicyList, UsrMng 기능 통합
"""
import bcrypt
from sqlalchemy.orm import Session
from db.database import get_session
from db.models.auth import AppUser, AuthInfo, AuthGroupInfo, IndivBaseDt, LoginPolicy


class AuthService:
    # ─── 로그인 ────────────────────────────────────────────────
    @staticmethod
    def login(user_id: str, raw_password: str) -> AppUser | None:
        """ID/PW 검증. 성공 시 AppUser 반환, 실패 시 None"""
        try:
            with get_session() as session:
                user = session.get(AppUser, user_id)
                if user is None:
                    return None
                if user.use_at != "Y":
                    return None
                # bcrypt 검증 — password 컬럼이 str이면 encode(), bytes이면 그대로
                stored = user.password
                stored_bytes = stored if isinstance(stored, bytes) else stored.encode("utf-8")
                raw_bytes    = raw_password.encode("utf-8")
                if bcrypt.checkpw(raw_bytes, stored_bytes):
                    session.expunge(user)
                    return user
                return None
        except Exception as exc:          # noqa: BLE001
            import traceback
            traceback.print_exc()
            print(f"[AuthService.login] 예외 발생: {exc}")
            return None

    # ─── 사용자 관리 ────────────────────────────────────────────
    @staticmethod
    def get_user_list(user_id: str = "", user_nm: str = "",
                      page: int = 1, page_size: int = 20) -> tuple[list[dict], int]:
        with get_session() as session:
            q = session.query(AppUser)
            if user_id:
                q = q.filter(AppUser.user_id.like(f"%{user_id}%"))
            if user_nm:
                q = q.filter(AppUser.user_nm.like(f"%{user_nm}%"))
            total = q.count()
            rows = q.order_by(AppUser.user_id)\
                    .offset((page - 1) * page_size).limit(page_size).all()
            return ([{
                "user_id": r.user_id, "user_nm": r.user_nm,
                "email": r.email, "author_code": r.author_code, "use_at": r.use_at,
            } for r in rows], total)

    @staticmethod
    def save_user(data: dict) -> None:
        with get_session() as session:
            user = session.get(AppUser, data["user_id"])
            if user:
                user.user_nm     = data.get("user_nm", user.user_nm)
                user.email       = data.get("email", user.email)
                user.author_code = data.get("author_code", user.author_code)
                user.use_at      = data.get("use_at", user.use_at)
                if data.get("password"):
                    user.password = bcrypt.hashpw(data["password"].encode(), bcrypt.gensalt()).decode()
            else:
                pw = bcrypt.hashpw(data["password"].encode(), bcrypt.gensalt()).decode()
                session.add(AppUser(**{**data, "password": pw}))
            session.commit()

    @staticmethod
    def delete_user(user_id: str) -> None:
        with get_session() as session:
            user = session.get(AppUser, user_id)
            if user:
                session.delete(user)
                session.commit()

    # ─── 권한 정보 ────────────────────────────────────────────
    @staticmethod
    def get_auth_info_list(author_nm: str = "",
                           page: int = 1, page_size: int = 20) -> tuple[list[dict], int]:
        with get_session() as session:
            q = session.query(AuthInfo)
            if author_nm:
                q = q.filter(AuthInfo.author_nm.like(f"%{author_nm}%"))
            total = q.count()
            rows = q.offset((page - 1) * page_size).limit(page_size).all()
            return ([{
                "author_code": r.author_code, "author_nm": r.author_nm,
                "author_dc": r.author_dc, "author_creat_de": r.author_creat_de,
            } for r in rows], total)

    # ─── 권한 정보 CRUD ────────────────────────────────────────
    @staticmethod
    def save_auth_info(data: dict) -> None:
        with get_session() as session:
            obj = session.get(AuthInfo, data["author_code"])
            if obj:
                for k, v in data.items():
                    if hasattr(obj, k):
                        setattr(obj, k, v)
            else:
                session.add(AuthInfo(**data))
            session.commit()

    @staticmethod
    def delete_auth_info(author_code: str) -> None:
        with get_session() as session:
            obj = session.get(AuthInfo, author_code)
            if obj:
                session.delete(obj)
                session.commit()

    # ─── 로그인 정책 CRUD ────────────────────────────────────
    @staticmethod
    def save_lgn_policy(data: dict) -> None:
        with get_session() as session:
            obj = session.get(LoginPolicy, data["emplyr_id"])
            if obj:
                for k, v in data.items():
                    if hasattr(obj, k):
                        setattr(obj, k, v)
            else:
                session.add(LoginPolicy(**data))
            session.commit()

    @staticmethod
    def delete_lgn_policy(emplyr_id: str) -> None:
        with get_session() as session:
            obj = session.get(LoginPolicy, emplyr_id)
            if obj:
                session.delete(obj)
                session.commit()

    # ─── 개인 기준년월 CRUD ─────────────────────────────────
    @staticmethod
    def save_indiv_base_dt(data: dict) -> None:
        with get_session() as session:
            pk = (data["user_id"], data["base_yymm"])
            obj = session.get(IndivBaseDt, pk)
            if obj:
                for k, v in data.items():
                    if hasattr(obj, k):
                        setattr(obj, k, v)
            else:
                safe_keys = {"user_id", "base_yymm", "last_modified_by"}
                session.add(IndivBaseDt(**{k: v for k, v in data.items() if k in safe_keys}))
            session.commit()

    @staticmethod
    def delete_indiv_base_dt(user_id: str, base_yymm: str) -> None:
        with get_session() as session:
            obj = session.get(IndivBaseDt, (user_id, base_yymm))
            if obj:
                session.delete(obj)
                session.commit()

    # ─── 개인 기준년월 조회 ────────────────────────────────────────────────
    @staticmethod
    def get_base_yymm(user_id: str) -> str:
        """해당 사용자의 가장 최근 기준년월 반환"""
        with get_session() as session:
            row = session.query(IndivBaseDt)\
                         .filter(IndivBaseDt.user_id == user_id)\
                         .order_by(IndivBaseDt.base_yymm.desc()).first()
            return row.base_yymm if row else ""

    @staticmethod
    def get_indiv_base_dt_list(page: int = 1, page_size: int = 20) -> tuple[list[dict], int]:
        with get_session() as session:
            q = session.query(IndivBaseDt)
            total = q.count()
            rows = q.offset((page - 1) * page_size).limit(page_size).all()
            return ([{
                "user_id": r.user_id, "base_yymm": r.base_yymm,
                "last_modified_by": r.last_modified_by,
            } for r in rows], total)
