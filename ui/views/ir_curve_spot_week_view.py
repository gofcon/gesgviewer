"""금리커브 현물(주간) 화면"""
from ui.views._base_list_view import BaseListView
from db.database import get_session
from db.models.ir_curve import IrCurveSpotWeek
from db.models.auth import AppUser
from config.settings import DEFAULT_PAGE_SIZE

HEADERS = [
    ("base_date","기준일자"), ("ir_curve_id","커브ID"), ("mat_cd","만기"),
    ("spot_rate","현물금리"), ("day_of_week","요일"), ("biz_day_type","영업일유형"),
]


class IrCurveSpotWeekView(BaseListView):
    HEADERS = HEADERS
    VIEW_TITLE = "금리커브 현물(주간)"

    def __init__(self, user: AppUser, parent=None):
        super().__init__(user, parent)

    def _build_search_area(self):
        return None

    def _load_data(self, page: int = 1):
        with get_session() as session:
            q = session.query(IrCurveSpotWeek)
            dt = self._get_toolbar_yymm()
            if dt:
                q = q.filter(IrCurveSpotWeek.base_date.like(dt[:6] + "%"))
            total = q.count()
            ps = self._get_page_size()
            rows_obj = q.offset((page - 1) * ps).limit(ps).all()
            rows = [
                {
                    "base_date": r.base_date,
                    "ir_curve_id": r.ir_curve_id,
                    "mat_cd": r.mat_cd,
                    "spot_rate": float(r.spot_rate) if r.spot_rate is not None else None,
                    "day_of_week": r.day_of_week,
                    "biz_day_type": r.biz_day_type,
                }
                for r in rows_obj
            ]
        self.table_model.load(rows)
        self.pager.set_total(total)
