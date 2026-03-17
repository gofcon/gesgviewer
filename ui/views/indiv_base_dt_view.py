"""개인 기준일자 — JSP: IndivBaseDtList.jsp"""
from ui.views._base_crud_view import BaseCrudView
from ui.widgets.form_dialog import FormField
from services.auth_service import AuthService
from db.models.auth import AppUser

HEADERS = [("user_id","사용자ID"),("base_yymm","기준년월"),("last_modified_by","최종수정자")]


class IndivBaseDtView(BaseCrudView):
    HEADERS = HEADERS
    VIEW_TITLE = "개인 기준일자"
    EDITABLE_KEYS = {"last_modified_by"}
    ADD_FIELDS = [
        FormField("user_id",          "사용자ID",   "text"),
        FormField("base_yymm",        "기준년월",   "text"),
        FormField("last_modified_by", "최종수정자", "text", required=False),
    ]

    def __init__(self, user: AppUser, parent=None):
        super().__init__(user, parent)

    def _load_data(self, page: int = 1):
        rows, total = AuthService.get_indiv_base_dt_list(page=page)
        self.table_model.load(rows)
        self.pager.set_total(total)

    def _save_row(self, data: dict, is_new: bool) -> bool:
        AuthService.save_indiv_base_dt(data)
        return True

    def _delete_row(self, row: dict) -> bool:
        AuthService.delete_indiv_base_dt(row["user_id"], row["base_yymm"])
        return True
