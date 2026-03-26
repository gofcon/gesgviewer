"""사용자 권한 목록 — JSP: AuthInfoList.jsp"""
from ui.views._base_crud_view import BaseCrudView
from ui.widgets.form_dialog import FormField
from services.system_service import AuthService
from db.models.auth import AppUser

HEADERS = [
    ("author_code","권한코드"),("author_nm","권한명"),
    ("author_dc","권한설명"),("author_creat_de","생성일"),
]


class AuthInfoView(BaseCrudView):
    HEADERS = HEADERS
    VIEW_TITLE = "사용자 권한 목록"
    EDITABLE_KEYS = {"author_nm", "author_dc", "author_creat_de"}
    ADD_FIELDS = [
        FormField("author_code",     "권한코드", "text"),
        FormField("author_nm",       "권한명",   "text"),
        FormField("author_dc",       "권한설명", "text", required=False),
        FormField("author_creat_de", "생성일",   "text"),
    ]

    def __init__(self, user: AppUser, parent=None):
        super().__init__(user, parent)

    def _build_search_area(self):
        return None

    def _load_data(self, page: int = 1):
        rows, total = AuthService.get_auth_info_list(
            author_nm="", page=page,
            page_size=self._get_page_size())
        self.table_model.load(rows)
        self.pager.set_total(total)

    def _save_row(self, data: dict, is_new: bool) -> bool:
        AuthService.save_auth_info(data)
        return True

    def _delete_row(self, row: dict) -> bool:
        AuthService.delete_auth_info(row["author_code"])
        return True
