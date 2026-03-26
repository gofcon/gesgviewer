"""ESG 작업 정보 — JSP: CoJobList.jsp"""
from ui.views._base_list_view import BaseListView
from services.config_service import ConfigService
from db.models.auth import AppUser

HEADERS = [
    ("job_id","작업ID"),("base_yymm","기준년월"),("calc_date","계산일자"),
    ("job_nm","작업명"),("calc_start","계산시작"),("calc_end","계산종료"),
    ("calc_elps","경과시간"),("calc_scd","계산상태"),
]

class CoJobView(BaseListView):
    HEADERS = HEADERS
    VIEW_TITLE = "ESG 작업 정보"
    def _load_data(self, page: int = 1):
        rows, total = ConfigService.get_job_info_list(
            base_yymm=self._get_toolbar_yymm(), page=page,
            page_size=self._get_page_size())
        self.table_model.load(rows); self.pager.set_total(total)
