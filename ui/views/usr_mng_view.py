"""사용자 목록 — JSP: UsrMngList.jsp"""
from ui.views._base_crud_view import BaseCrudView
from ui.widgets.form_dialog import FormField
from services.auth_service import AuthService
from db.models.auth import AppUser

HEADERS = [
    ("user_id","사용자ID"),("user_nm","사용자명"),
    ("email","이메일"),("author_code","권한코드"),("use_at","사용여부"),
]
_USE_AT_OPTS = ["Y", "N"]


class UsrMngView(BaseCrudView):
    HEADERS = HEADERS
    VIEW_TITLE = "사용자 목록"
    EDITABLE_KEYS = {"user_nm", "email", "author_code", "use_at"}
    COMBO_COLS = {"use_at": _USE_AT_OPTS}
    ADD_FIELDS = [
        FormField("user_id",     "사용자ID", "text"),
        FormField("user_nm",     "사용자명", "text"),
        FormField("email",       "이메일",   "text", required=False),
        FormField("password",    "비밀번호", "text"),
        FormField("author_code", "권한코드", "text", required=False),
        FormField("use_at",      "사용여부", "combo", options=_USE_AT_OPTS),
    ]

    def __init__(self, user: AppUser, parent=None):
        super().__init__(user, parent)

    def _build_search_area(self):
        return None

    def _load_data(self, page: int = 1):
        rows, total = AuthService.get_user_list(
            user_id="", user_nm="", page=page)
        self.table_model.load(rows)
        self.pager.set_total(total)

    def _save_row(self, data: dict, is_new: bool) -> bool:
        AuthService.save_user(data)
        return True

    def _delete_row(self, row: dict) -> bool:
        AuthService.delete_user(row["user_id"])
        return True
