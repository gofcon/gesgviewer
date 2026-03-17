"""위험스프레드 커브 화면 — JSP: SprdCurveList.jsp"""
from ui.views._base_list_view import BaseListView
from services.common_service import SprdService
from db.models.auth import AppUser

HEADERS = [
    ("base_yymm","기준년월"),("ir_curve_id","커브ID"),
    ("ir_typ_cd","금리유형"),("mat_cd","만기"),("sprd_val","스프레드"),
]

class SprdCurveView(BaseListView):
    HEADERS = HEADERS
    VIEW_TITLE = "위험스프레드 커브"
    def _load_data(self, page: int = 1):
        rows, total = SprdService.get_sprd_curve_list(
            base_yymm=self._get_toolbar_yymm(), page=page)
        self.table_model.load(rows); self.pager.set_total(total)
