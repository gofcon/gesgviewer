"""배치 작업 관리 — JSP: BatchOperList.jsp"""
from ui.views._base_list_view import BaseListView
from services.common_service import BatchService
from db.models.auth import AppUser

HEADERS = [
    ("batch_opert_id","작업ID"),("batch_opert_nm","작업명"),
    ("batch_progrm","프로그램"),("paramtr","파라미터"),("use_at","사용여부"),
]

class BatchOpertView(BaseListView):
    HEADERS = HEADERS
    VIEW_TITLE = "배치 작업 관리"
    def __init__(self, user: AppUser, parent=None):
        super().__init__(user, parent)
    def _build_search_area(self):
        return None
    def _load_data(self, page: int = 1):
        rows, total = BatchService.get_batch_opert_list(
            batch_opert_nm="", batch_progrm="", page=page)
        self.table_model.load(rows); self.pager.set_total(total)
