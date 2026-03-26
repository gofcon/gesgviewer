"""
시스템관리 + 도움말 서비스
1. 시스템관리: AuthService (사용자/권한/정책)
2. 도움말    : ContentService (공지사항/메뉴/프로그램)
"""
import bcrypt
from datetime import datetime
from db.database import get_session
from db.models.auth import AppUser, AuthInfo, AuthGroupInfo, IndivBaseDt, LoginPolicy
from db.models.common import CopBbs, MnuMng, PgmMng
from db.utils import paginate, upsert, delete_by_pk


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
            rows, total = paginate(q.order_by(AppUser.user_id), page, page_size)
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
            delete_by_pk(session, AppUser, user_id)

    # ─── 권한 정보 ────────────────────────────────────────────
    @staticmethod
    def get_auth_info_list(author_nm: str = "",
                           page: int = 1, page_size: int = 20) -> tuple[list[dict], int]:
        with get_session() as session:
            q = session.query(AuthInfo)
            if author_nm:
                q = q.filter(AuthInfo.author_nm.like(f"%{author_nm}%"))
            rows, total = paginate(q, page, page_size)
            return ([{
                "author_code": r.author_code, "author_nm": r.author_nm,
                "author_dc": r.author_dc, "author_creat_de": r.author_creat_de,
            } for r in rows], total)

    @staticmethod
    def save_auth_info(data: dict) -> None:
        with get_session() as session:
            upsert(session, AuthInfo, data["author_code"], data)

    @staticmethod
    def delete_auth_info(author_code: str) -> None:
        with get_session() as session:
            delete_by_pk(session, AuthInfo, author_code)

    # ─── 로그인 정책 CRUD ────────────────────────────────────
    @staticmethod
    def save_lgn_policy(data: dict) -> None:
        with get_session() as session:
            upsert(session, LoginPolicy, data["emplyr_id"], data)

    @staticmethod
    def delete_lgn_policy(emplyr_id: str) -> None:
        with get_session() as session:
            delete_by_pk(session, LoginPolicy, emplyr_id)

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
            delete_by_pk(session, IndivBaseDt, (user_id, base_yymm))

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
            rows, total = paginate(q, page, page_size)
            return ([{
                "user_id": r.user_id, "base_yymm": r.base_yymm,
                "last_modified_by": r.last_modified_by,
            } for r in rows], total)


class ContentService:
    """공지사항 / 메뉴 / 프로그램 CRUD"""

    # ─── 공지사항 ────────────────────────────────────────────────
    @staticmethod
    def save_cop_bbs(data: dict) -> None:
        with get_session() as session:
            ntt_id = data.get("ntt_id")
            if ntt_id:
                row = session.get(CopBbs, ntt_id)
                if row:
                    for k, v in data.items():
                        if hasattr(row, k):
                            setattr(row, k, v)
                    row.last_updt_pnttm = datetime.now()
                    session.commit()
                    return
            new_row = CopBbs(
                bbs_id=data.get("bbs_id", "NOTICE"),
                ntt_sj=data.get("ntt_sj", ""),
                ntt_cn=data.get("ntt_cn", ""),
                frst_register_nm=data.get("frst_register_nm", ""),
            )
            session.add(new_row)
            session.commit()

    @staticmethod
    def delete_cop_bbs(ntt_id: int) -> None:
        with get_session() as session:
            delete_by_pk(session, CopBbs, ntt_id)

    # ─── 메뉴 관리 ──────────────────────────────────────────────
    @staticmethod
    def save_mnu_mng(data: dict) -> None:
        with get_session() as session:
            menu_no = data.get("menu_no")
            if menu_no:
                row = session.get(MnuMng, menu_no)
                if row:
                    for k, v in data.items():
                        if hasattr(row, k):
                            setattr(row, k, v)
                    session.commit()
                    return
            new_row = MnuMng(**{k: v for k, v in data.items()
                                if k != "menu_no" and hasattr(MnuMng, k)})
            session.add(new_row)
            session.commit()

    @staticmethod
    def delete_mnu_mng(menu_no: int) -> None:
        with get_session() as session:
            delete_by_pk(session, MnuMng, menu_no)

    # ─── 프로그램 관리 ──────────────────────────────────────────
    @staticmethod
    def save_pgm_mng(data: dict) -> None:
        with get_session() as session:
            upsert(session, PgmMng, data["progrm_file_nm"], data)

    @staticmethod
    def delete_pgm_mng(progrm_file_nm: str) -> None:
        with get_session() as session:
            delete_by_pk(session, PgmMng, progrm_file_nm)

    # ─── 내비게이션 트리 (LETTNMENUINFO) ────────────────────────
    @staticmethod
    def get_nav_tree() -> list | None:
        """DB(LETTNMENUINFO)에서 3레벨 메뉴 트리 로드.
        데이터 없으면 None 반환.
        반환 형식: [(카테고리명, [(그룹명, [(메뉴명, view_key)])])]
        """
        with get_session() as session:
            rows = session.query(MnuMng).order_by(MnuMng.menu_ordr).all()
            if not rows:
                return None
            # 레벨별 분류
            cats   = [r for r in rows if r.upper_menu_no is None]
            result = []
            for cat in sorted(cats, key=lambda r: r.menu_ordr or 0):
                groups_raw = [r for r in rows if r.upper_menu_no == cat.menu_no]
                grp_list = []
                for grp in sorted(groups_raw, key=lambda r: r.menu_ordr or 0):
                    items_raw = [r for r in rows if r.upper_menu_no == grp.menu_no]
                    item_list = [
                        (r.menu_nm or "", r.progrm_file_nm or "")
                        for r in sorted(items_raw, key=lambda r: r.menu_ordr or 0)
                    ]
                    if item_list:
                        grp_list.append((grp.menu_nm or "", item_list))
                if grp_list:
                    result.append((cat.menu_nm or "", grp_list))
            return result if result else None

    @staticmethod
    def seed_nav_tree(nav_tree: list, overwrite: bool = False) -> None:
        """DB(LETTNMENUINFO)에 nav_tree 삽입.
        overwrite=True 이면 기존 데이터 전체 삭제 후 재삽입.
        기존 데이터가 있고 overwrite=False 이면 아무 동작 없음.
        """
        with get_session() as session:
            existing = session.query(MnuMng).count()
            if existing > 0 and not overwrite:
                return
            if overwrite and existing > 0:
                session.query(MnuMng).delete()
                session.flush()
            for cat_ordr, (cat_nm, groups) in enumerate(nav_tree, 1):
                cat = MnuMng(menu_nm=cat_nm, menu_ordr=cat_ordr,
                             upper_menu_no=None)
                session.add(cat)
                session.flush()          # cat.menu_no 확보
                for grp_ordr, (grp_nm, items) in enumerate(groups, 1):
                    grp = MnuMng(menu_nm=grp_nm, menu_ordr=grp_ordr,
                                 upper_menu_no=cat.menu_no)
                    session.add(grp)
                    session.flush()      # grp.menu_no 확보
                    for item_ordr, (item_nm, view_key) in enumerate(items, 1):
                        item = MnuMng(
                            menu_nm=item_nm, menu_ordr=item_ordr,
                            upper_menu_no=grp.menu_no,
                            progrm_file_nm=view_key,
                        )
                        session.add(item)
            session.commit()
