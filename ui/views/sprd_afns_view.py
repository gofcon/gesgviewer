"""AFNS 스프레드 화면 — JSP: SprdAfnsBizList.jsp"""
from ui.views._base_list_view import BaseListView
from db.database import get_session
from db.models.sprd_curve import SprdAfnsBiz
from db.models.auth import AppUser
from config.settings import DEFAULT_PAGE_SIZE

HEADERS = [
    ("base_yymm","기준년월"),("ir_model_id","모델ID"),("ir_curve_id","커브ID"),
    ("param_typ_cd","파라미터유형"),("param_val","파라미터값"),
]

class SprdAfnsView(BaseListView):
    HEADERS = HEADERS
    VIEW_TITLE = "AFNS 스프레드"
    def __init__(self, user: AppUser, parent=None):
        super().__init__(user, parent)
    def _build_search_area(self):
        return None
    def _load_data(self, page: int = 1):
        with get_session() as session:
            q = session.query(SprdAfnsBiz)
            ym = self._get_toolbar_yymm()
            if ym: q = q.filter(SprdAfnsBiz.base_yymm == ym)
            total = q.count()
            ps = self._get_page_size()
            rows_obj = q.offset((page-1)*ps).limit(ps).all()
            rows = [{"base_yymm": r.base_yymm,"ir_model_id": r.ir_model_id,"ir_curve_id": r.ir_curve_id,
                     "param_typ_cd": r.param_typ_cd,"param_val": float(r.param_val) if r.param_val else None} for r in rows_obj]
        self.table_model.load(rows); self.pager.set_total(total)
