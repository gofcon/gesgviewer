"""시나리오 저장 검증 — JSP: ValidSceStoList.jsp"""
from ui.views._base_list_view import BaseListView
from services.common_service import ValidService
from db.models.auth import AppUser

HEADERS = [
    ("base_yymm","기준년월"),("appl_biz_dv","적용업무"),("ir_curve_id","커브ID"),
    ("ir_curve_sce_no","시나리오번호"),("valid_typ_cd","검증유형"),("valid_val","검증값"),
]

class ValidSceStoView(BaseListView):
    HEADERS = HEADERS
    VIEW_TITLE = "시나리오 저장 검증"
    def __init__(self, user: AppUser, parent=None):
        super().__init__(user, parent)
    def _build_search_area(self):
        return None
    def _load_data(self, page: int = 1):
        rows, total = ValidService.get_valid_sce_sto_list(self._get_toolbar_yymm(), page=page)
        self.table_model.load(rows); self.pager.set_total(total)
