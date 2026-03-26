"""파라미터 모델 난수 화면"""
from ui.views._base_list_view import BaseListView
from db.database import get_session
from db.models.ir_param_model import IrParamModelRnd
from db.models.auth import AppUser
from config.settings import DEFAULT_PAGE_SIZE

HEADERS = [
    ("base_yymm","기준년월"), ("ir_model_id","모델ID"), ("ir_curve_id","커브ID"),
    ("sce_no","시나리오번호"), ("mat_cd","만기"), ("rnd_num","난수값"),
]


class ParamModelRndView(BaseListView):
    HEADERS = HEADERS
    VIEW_TITLE = "파라미터 모델 난수"

    def __init__(self, user: AppUser, parent=None):
        super().__init__(user, parent)

    def _build_search_area(self):
        return None

    def _load_data(self, page: int = 1):
        with get_session() as session:
            q = session.query(IrParamModelRnd)
            ym = self._get_toolbar_yymm()
            if ym:
                q = q.filter(IrParamModelRnd.base_yymm == ym)
            total = q.count()
            ps = self._get_page_size()
            rows_obj = q.offset((page - 1) * ps).limit(ps).all()
            rows = [
                {
                    "base_yymm": r.base_yymm,
                    "ir_model_id": r.ir_model_id,
                    "ir_curve_id": r.ir_curve_id,
                    "sce_no": r.sce_no,
                    "mat_cd": r.mat_cd,
                    "rnd_num": float(r.rnd_num) if r.rnd_num is not None else None,
                }
                for r in rows_obj
            ]
        self.table_model.load(rows)
        self.pager.set_total(total)
