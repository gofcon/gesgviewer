"""시나리오 랜덤 검증 — JSP: ValidRndList.jsp"""
from ui.views._base_list_view import BaseListView
from services.valid_service import ValidService
from db.models.auth import AppUser

HEADERS = [
    ("base_yymm","기준년월"),("ir_model_id","모델ID"),("ir_curve_id","커브ID"),
    ("valid_dv","검증구분"),("valid_seq","검증순번"),
    ("valid_val1","검증값1"),("valid_val2","검증값2"),("valid_val3","검증값3"),
]

class ValidRndView(BaseListView):
    HEADERS = HEADERS
    VIEW_TITLE = "시나리오 랜덤 검증"
    def __init__(self, user: AppUser, parent=None):
        super().__init__(user, parent)
    def _build_search_area(self):
        return None
    def _load_data(self, page: int = 1):
        rows, total = ValidService.get_valid_rnd_list(
            self._get_toolbar_yymm(), page=page,
            page_size=self._get_page_size())
        self.table_model.load(rows); self.pager.set_total(total)
