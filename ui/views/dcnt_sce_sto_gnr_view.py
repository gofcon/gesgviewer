"""확률시나리오 저장(일반) 화면"""
from ui.views._base_list_view import BaseListView
from db.database import get_session
from db.models.dcnt_rate import IrDcntSceStoGnr
from db.models.auth import AppUser
from config.settings import DEFAULT_PAGE_SIZE

HEADERS = [
    ("base_yymm","기준년월"), ("appl_biz_dv","적용업무"), ("ir_model_id","모델ID"),
    ("ir_curve_id","커브ID"), ("ir_curve_sce_no","시나리오번호"),
    ("sce_no","시나리오번호2"), ("mat_cd","만기"),
    ("spot_rate","현물금리"), ("fwd_rate","선도금리"),
]


class DcntSceStoGnrView(BaseListView):
    HEADERS = HEADERS
    VIEW_TITLE = "확률시나리오 저장(일반)"

    def __init__(self, user: AppUser, parent=None):
        super().__init__(user, parent)

    def _build_search_area(self):
        return None

    def _load_data(self, page: int = 1):
        with get_session() as session:
            q = session.query(IrDcntSceStoGnr)
            ym = self._get_toolbar_yymm()
            if ym:
                q = q.filter(IrDcntSceStoGnr.base_yymm == ym)
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
                    "sce_no": r.sce_no,
                    "mat_cd": r.mat_cd,
                    "spot_rate": float(r.spot_rate) if r.spot_rate is not None else None,
                    "fwd_rate": float(r.fwd_rate) if r.fwd_rate is not None else None,
                }
                for r in rows_obj
            ]
        self.table_model.load(rows)
        self.pager.set_total(total)
