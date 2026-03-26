"""Q값 시나리오 검증 화면"""
from ui.views._base_list_view import BaseListView
from db.database import get_session
from db.models.ir_param_model import IrQvalSce
from db.models.auth import AppUser
from config.settings import DEFAULT_PAGE_SIZE

HEADERS = [
    ("base_yymm","기준년월"), ("appl_biz_dv","적용업무"), ("ir_model_id","모델ID"),
    ("ir_curve_id","커브ID"), ("ir_curve_sce_no","시나리오번호"),
    ("qval_dv","Q값구분"), ("qval_seq","순번"),
    ("qval1","Q값1"), ("qval2","Q값2"), ("qval3","Q값3"),
    ("qval5","Q값5"), ("qval10","Q값10"), ("qval15","Q값15"),
]


class QvalSceView(BaseListView):
    HEADERS = HEADERS
    VIEW_TITLE = "Q값 시나리오 검증"

    def __init__(self, user: AppUser, parent=None):
        super().__init__(user, parent)

    def _build_search_area(self):
        return None

    def _load_data(self, page: int = 1):
        with get_session() as session:
            q = session.query(IrQvalSce)
            ym = self._get_toolbar_yymm()
            if ym:
                q = q.filter(IrQvalSce.base_yymm == ym)
            total = q.count()
            ps = self._get_page_size()
            rows_obj = q.offset((page - 1) * ps).limit(ps).all()
            rows = [
                {
                    "base_yymm": r.base_yymm,
                    "appl_biz_dv": r.appl_biz_dv,
                    "ir_model_id": r.ir_model_id,
                    "ir_curve_id": r.ir_curve_id,
                    "ir_curve_sce_no": r.ir_curve_sce_no,
                    "qval_dv": r.qval_dv,
                    "qval_seq": r.qval_seq,
                    "qval1": float(r.qval1) if r.qval1 is not None else None,
                    "qval2": float(r.qval2) if r.qval2 is not None else None,
                    "qval3": float(r.qval3) if r.qval3 is not None else None,
                    "qval5": float(r.qval5) if r.qval5 is not None else None,
                    "qval10": float(r.qval10) if r.qval10 is not None else None,
                    "qval15": float(r.qval15) if r.qval15 is not None else None,
                }
                for r in rows_obj
            ]
        self.table_model.load(rows)
        self.pager.set_total(total)
