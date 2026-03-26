"""배치 결과 관리 — JSP: BatchRsltList.jsp"""
from ui.views._base_list_view import BaseListView
from services.config_service import BatchService
from db.models.auth import AppUser

HEADERS = [
    ("batch_result_id","결과ID"),("batch_schdul_id","스케줄ID"),("batch_opert_id","작업ID"),
    ("paramtr","파라미터"),("sttus","상태"),("error_info","오류정보"),
    ("execut_begin_tm","시작시각"),("execut_end_tm","종료시각"),
]

class BatchResultView(BaseListView):
    HEADERS = HEADERS
    VIEW_TITLE = "배치 결과 관리"
    def __init__(self, user: AppUser, parent=None):
        super().__init__(user, parent)
    def _build_search_area(self):
        return None
    def _load_data(self, page: int = 1):
        rows, total = BatchService.get_batch_result_list(
            sttus="", page=page, page_size=self._get_page_size())
        self.table_model.load(rows); self.pager.set_total(total)
