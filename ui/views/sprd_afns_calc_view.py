"""AFNS 스프레드 계산 화면"""
from ui.views._base_list_view import BaseListView
from db.database import get_session
from db.models.sprd_curve import SprdAfnsCalc
from db.models.auth import AppUser
from config.settings import DEFAULT_PAGE_SIZE

HEADERS = [
    ("base_yymm","기준년월"), ("ir_model_id","모델ID"), ("ir_curve_id","커브ID"),
    ("ir_curve_sce_no","시나리오번호"), ("mat_cd","만기"),
    ("shk_sprd_cont","연속충격스프레드"),
]


class SprdAfnsCalcView(BaseListView):
    HEADERS = HEADERS
    VIEW_TITLE = "AFNS 스프레드 계산"

    def __init__(self, user: AppUser, parent=None):
        super().__init__(user, parent)

    def _build_search_area(self):
        return None

    def _load_data(self, page: int = 1):
        with get_session() as session:
            q = session.query(SprdAfnsCalc)
            ym = self._get_toolbar_yymm()
            if ym:
                q = q.filter(SprdAfnsCalc.base_yymm == ym)
            total = q.count()
            ps = self._get_page_size()
            rows_obj = q.offset((page - 1) * ps).limit(ps).all()
            rows = [
                {
                    "base_yymm": r.base_yymm,
                    "ir_model_id": r.ir_model_id,
                    "ir_curve_id": r.ir_curve_id,
                    "ir_curve_sce_no": r.ir_curve_sce_no,
                    "mat_cd": r.mat_cd,
                    "shk_sprd_cont": float(r.shk_sprd_cont) if r.shk_sprd_cont is not None else None,
                }
                for r in rows_obj
            ]
        self.table_model.load(rows)
        self.pager.set_total(total)
