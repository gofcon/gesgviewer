"""LP 스프레드 비즈 화면"""
from ui.views._base_list_view import BaseListView
from db.database import get_session
from db.models.sprd_curve import SprdLpBiz
from db.models.auth import AppUser
from config.settings import DEFAULT_PAGE_SIZE

HEADERS = [
    ("base_yymm","기준년월"), ("appl_biz_dv","적용업무"), ("ir_curve_id","커브ID"),
    ("ir_curve_sce_no","시나리오번호"), ("mat_cd","만기"),
    ("liq_prem","유동성프리미엄"),
]


class SprdLpBizView(BaseListView):
    HEADERS = HEADERS
    VIEW_TITLE = "LP 스프레드 비즈"

    def __init__(self, user: AppUser, parent=None):
        super().__init__(user, parent)

    def _build_search_area(self):
        return None

    def _load_data(self, page: int = 1):
        with get_session() as session:
            q = session.query(SprdLpBiz)
            ym = self._get_toolbar_yymm()
            if ym:
                q = q.filter(SprdLpBiz.base_yymm == ym)
            total = q.count()
            ps = self._get_page_size()
            rows_obj = q.offset((page - 1) * ps).limit(ps).all()
            rows = [
                {
                    "base_yymm": r.base_yymm,
                    "appl_biz_dv": r.appl_biz_dv,
                    "ir_curve_id": r.ir_curve_id,
                    "ir_curve_sce_no": r.ir_curve_sce_no,
                    "mat_cd": r.mat_cd,
                    "liq_prem": float(r.liq_prem) if r.liq_prem is not None else None,
                }
                for r in rows_obj
            ]
        self.table_model.load(rows)
        self.pager.set_total(total)
