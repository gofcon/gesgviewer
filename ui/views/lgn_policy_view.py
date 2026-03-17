"""로그인 정책 — JSP: LgnPolicyList.jsp"""
from ui.views._base_crud_view import BaseCrudView
from ui.widgets.form_dialog import FormField
from services.auth_service import AuthService
from db.database import get_session
from db.models.auth import LoginPolicy, AppUser
from config.settings import DEFAULT_PAGE_SIZE

HEADERS = [("emplyr_id","사용자ID"),("ip_info","IP정보"),("lmtt_at","제한여부")]
_LMTT_OPTS = ["N", "Y"]


class LgnPolicyView(BaseCrudView):
    HEADERS = HEADERS
    VIEW_TITLE = "로그인 정책"
    EDITABLE_KEYS = {"ip_info", "lmtt_at"}
    COMBO_COLS = {"lmtt_at": _LMTT_OPTS}
    ADD_FIELDS = [
        FormField("emplyr_id", "사용자ID", "text"),
        FormField("ip_info",   "IP정보",   "text", required=False),
        FormField("lmtt_at",   "제한여부", "combo", options=_LMTT_OPTS),
    ]

    def __init__(self, user: AppUser, parent=None):
        super().__init__(user, parent)

    def _load_data(self, page: int = 1):
        with get_session() as session:
            q = session.query(LoginPolicy)
            total = q.count()
            rows_obj = q.offset((page - 1) * DEFAULT_PAGE_SIZE).limit(DEFAULT_PAGE_SIZE).all()
            rows = [{"emplyr_id": r.emplyr_id, "ip_info": r.ip_info,
                     "lmtt_at": r.lmtt_at} for r in rows_obj]
        self.table_model.load(rows)
        self.pager.set_total(total)

    def _save_row(self, data: dict, is_new: bool) -> bool:
        AuthService.save_lgn_policy(data)
        return True

    def _delete_row(self, row: dict) -> bool:
        AuthService.delete_lgn_policy(row["emplyr_id"])
        return True
