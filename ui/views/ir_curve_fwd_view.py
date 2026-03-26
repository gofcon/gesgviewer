"""금리커브 선도 화면"""
from ui.views._base_list_view import BaseListView
from db.database import get_session
from db.models.ir_curve import IrCurveFwd
from db.models.auth import AppUser
from config.settings import DEFAULT_PAGE_SIZE

HEADERS = [
    ("base_date","기준일자"), ("ir_curve_id","커브ID"), ("fwd_mat_cd","선도만기"),
    ("mat_cd","만기"), ("int_rate","금리"),
]


class IrCurveFwdView(BaseListView):
    HEADERS = HEADERS
    VIEW_TITLE = "금리커브 선도"

    def __init__(self, user: AppUser, parent=None):
        super().__init__(user, parent)

    def _build_search_area(self):
        return None

    def _load_data(self, page: int = 1):
        with get_session() as session:
            q = session.query(IrCurveFwd)
            dt = self._get_toolbar_yymm()
            if dt:
                q = q.filter(IrCurveFwd.base_date.like(dt[:6] + "%"))
            total = q.count()
            ps = self._get_page_size()
            rows_obj = q.offset((page - 1) * ps).limit(ps).all()
            rows = [
                {
                    "base_date": r.base_date,
                    "ir_curve_id": r.ir_curve_id,
                    "fwd_mat_cd": r.fwd_mat_cd,
                    "mat_cd": r.mat_cd,
                    "int_rate": float(r.int_rate) if r.int_rate is not None else None,
                }
                for r in rows_obj
            ]
        self.table_model.load(rows)
        self.pager.set_total(total)
