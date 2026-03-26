"""할인율 시나리오 저장 화면 — JSP: DcntStoBizList.jsp"""
from ui.views._base_list_view import BaseListView
from services.result_service import DcntRateService
from db.models.auth import AppUser

HEADERS = [
    ("base_yymm","기준년월"),("appl_biz_dv","적용업무"),("ir_curve_id","커브ID"),
    ("ir_curve_sce_no","시나리오번호"),("sce_no","경로번호"),
    ("mat_cd","만기"),("spot_rate","현물금리"),("fwd_rate","선도금리"),
]

class DcntStoView(BaseListView):
    HEADERS = HEADERS
    VIEW_TITLE = "할인율 시나리오 저장"
    def _load_data(self, page: int = 1):
        rows, total = DcntRateService.get_dcnt_sto_biz_list(
            base_yymm=self._get_toolbar_yymm(), page=page,
            page_size=self._get_page_size())
        self.table_model.load(rows); self.pager.set_total(total)
