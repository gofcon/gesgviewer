"""사용자별 권한 관리 — JSP: AuthGroupList.jsp"""
from ui.views._base_list_view import BaseListView
from services.system_service import AuthService
from db.models.auth import AppUser

HEADERS = [
    ("user_id","사용자ID"),("user_nm","사용자명"),
    ("author_code","권한코드"),("use_at","사용여부"),
]

class AuthGroupView(BaseListView):
    HEADERS = HEADERS
    VIEW_TITLE = "사용자별 권한 관리"
    def __init__(self, user: AppUser, parent=None):
        super().__init__(user, parent)
    def _build_search_area(self):
        return None
    def _load_data(self, page: int = 1):
        rows, total = AuthService.get_user_list(
            user_id="", user_nm="", page=page,
            page_size=self._get_page_size())
        self.table_model.load(rows); self.pager.set_total(total)
