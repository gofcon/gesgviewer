"""시나리오 선도 검증 — JSP: ValidSceFwdList.jsp"""
from ui.views._base_list_view import BaseListView
from services.valid_service import ValidService
from db.models.auth import AppUser

HEADERS = [
    ("base_yymm","기준년월"),("appl_biz_dv","적용업무"),("ir_curve_id","커브ID"),
    ("ir_curve_sce_no","시나리오번호"),("mat_cd","만기"),
    ("spot_rate","현물금리"),("fwd_rate","선도금리"),
    ("adj_spot_rate","조정현물금리"),("adj_fwd_rate","조정선도금리"),
]

class ValidFwdView(BaseListView):
    HEADERS = HEADERS
    VIEW_TITLE = "시나리오 선도 검증"
    def __init__(self, user: AppUser, parent=None):
        super().__init__(user, parent)
    def _build_search_area(self):
        return None
    def _load_data(self, page: int = 1):
        rows, total = ValidService.get_valid_fwd_list(
            self._get_toolbar_yymm(), page=page,
            page_size=self._get_page_size())
        self.table_model.load(rows); self.pager.set_total(total)
