"""HW 파라미터 검증 화면"""
from ui.views._base_list_view import BaseListView
from db.database import get_session
from db.models.ir_param_model import IrValidParamHw
from db.models.auth import AppUser
from config.settings import DEFAULT_PAGE_SIZE

HEADERS = [
    ("base_yymm","기준년월"), ("ir_model_id","모델ID"), ("ir_curve_id","커브ID"),
    ("swpn_mat_num","스왑션만기"), ("swap_ten_num","스왑기간"),
    ("valid_dv","검증구분"),
    ("valid_val1","검증값1"), ("valid_val2","검증값2"), ("valid_val3","검증값3"),
    ("valid_val4","검증값4"), ("valid_val5","검증값5"),
]


class ValidParamHwView(BaseListView):
    HEADERS = HEADERS
    VIEW_TITLE = "HW 파라미터 검증"

    def __init__(self, user: AppUser, parent=None):
        super().__init__(user, parent)

    def _build_search_area(self):
        return None

    def _load_data(self, page: int = 1):
        with get_session() as session:
            q = session.query(IrValidParamHw)
            ym = self._get_toolbar_yymm()
            if ym:
                q = q.filter(IrValidParamHw.base_yymm == ym)
            total = q.count()
            ps = self._get_page_size()
            rows_obj = q.offset((page - 1) * ps).limit(ps).all()
            rows = [
                {
                    "base_yymm": r.base_yymm,
                    "ir_model_id": r.ir_model_id,
                    "ir_curve_id": r.ir_curve_id,
                    "swpn_mat_num": float(r.swpn_mat_num) if r.swpn_mat_num is not None else None,
                    "swap_ten_num": float(r.swap_ten_num) if r.swap_ten_num is not None else None,
                    "valid_dv": r.valid_dv,
                    "valid_val1": float(r.valid_val1) if r.valid_val1 is not None else None,
                    "valid_val2": float(r.valid_val2) if r.valid_val2 is not None else None,
                    "valid_val3": float(r.valid_val3) if r.valid_val3 is not None else None,
                    "valid_val4": float(r.valid_val4) if r.valid_val4 is not None else None,
                    "valid_val5": float(r.valid_val5) if r.valid_val5 is not None else None,
                }
                for r in rows_obj
            ]
        self.table_model.load(rows)
        self.pager.set_total(total)
