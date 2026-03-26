"""금리커브 YTM 화면"""
from ui.views._base_list_view import BaseListView
from db.database import get_session
from db.models.ir_curve import IrCurveYtm
from db.models.auth import AppUser
from config.settings import DEFAULT_PAGE_SIZE

HEADERS = [
    ("base_date","기준일자"), ("ir_curve_id","커브ID"), ("mat_cd","만기"),
    ("ytm","YTM"), ("ticker_nm","티커명"),
]


class IrCurveYtmView(BaseListView):
    HEADERS = HEADERS
    VIEW_TITLE = "금리커브 YTM"

    def __init__(self, user: AppUser, parent=None):
        super().__init__(user, parent)

    def _build_search_area(self):
        return None

    def _load_data(self, page: int = 1):
        with get_session() as session:
            q = session.query(IrCurveYtm)
            dt = self._get_toolbar_yymm()
            if dt:
                q = q.filter(IrCurveYtm.base_date.like(dt[:6] + "%"))
            total = q.count()
            ps = self._get_page_size()
            rows_obj = q.offset((page - 1) * ps).limit(ps).all()
            rows = [
                {
                    "base_date": r.base_date,
                    "ir_curve_id": r.ir_curve_id,
                    "mat_cd": r.mat_cd,
                    "ytm": float(r.ytm) if r.ytm is not None else None,
                    "ticker_nm": r.ticker_nm,
                }
                for r in rows_obj
            ]
        self.table_model.load(rows)
        self.pager.set_total(total)
