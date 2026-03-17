"""ESG 작업 정보 — JSP: CoJobList.jsp"""
from ui.views._base_list_view import BaseListView
from services.common_service import CommonService
from db.models.auth import AppUser

HEADERS = [
    ("job_hist_id","이력ID"),("job_id","작업ID"),("base_yymm","기준년월"),
    ("calc_dt","계산일자"),("calc_start_dt","계산시작"),("calc_end_dt","계산종료"),
    ("calc_sttus","상태"),("error_msg","오류메시지"),
]

class CoJobView(BaseListView):
    HEADERS = HEADERS
    VIEW_TITLE = "ESG 작업 정보"
    def _load_data(self, page: int = 1):
        rows, total = CommonService.get_job_hist_list(base_yymm=self._get_toolbar_yymm(), page=page)
        self.table_model.load(rows); self.pager.set_total(total)
