"""파라미터 모델 계산 화면"""
from ui.views._base_list_view import BaseListView
from db.database import get_session
from db.models.ir_param_model import IrParamModelCalc
from db.models.auth import AppUser
from config.settings import DEFAULT_PAGE_SIZE

HEADERS = [
    ("base_yymm","기준년월"), ("ir_model_id","모델ID"), ("ir_curve_id","커브ID"),
    ("param_typ_cd","파라미터유형"), ("param_val","파라미터값"),
]


class ParamModelCalcView(BaseListView):
    HEADERS = HEADERS
    VIEW_TITLE = "파라미터 모델 계산"

    def __init__(self, user: AppUser, parent=None):
        super().__init__(user, parent)

    def _build_search_area(self):
        return None

    def _load_data(self, page: int = 1):
        with get_session() as session:
            q = session.query(IrParamModelCalc)
            ym = self._get_toolbar_yymm()
            if ym:
                q = q.filter(IrParamModelCalc.base_yymm == ym)
            total = q.count()
            ps = self._get_page_size()
            rows_obj = q.offset((page - 1) * ps).limit(ps).all()
            rows = [
                {
                    "base_yymm": r.base_yymm,
                    "ir_model_id": r.ir_model_id,
                    "ir_curve_id": r.ir_curve_id,
                    "param_typ_cd": r.param_typ_cd,
                    "param_val": float(r.param_val) if r.param_val is not None else None,
                }
                for r in rows_obj
            ]
        self.table_model.load(rows)
        self.pager.set_total(total)
