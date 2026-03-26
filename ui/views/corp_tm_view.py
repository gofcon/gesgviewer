"""기업 전환행렬 화면"""
from ui.views._base_list_view import BaseListView
from db.database import get_session
from db.models.sprd_curve import RcCorpTm
from db.models.auth import AppUser
from config.settings import DEFAULT_PAGE_SIZE

HEADERS = [
    ("base_yymm","기준년월"), ("crd_eval_agncy_cd","평가기관"),
    ("from_crd_grd_cd","출발등급"), ("to_crd_grd_cd","도착등급"),
    ("trans_prob","전환확률"),
]


class CorpTmView(BaseListView):
    HEADERS = HEADERS
    VIEW_TITLE = "기업 전환행렬"

    def __init__(self, user: AppUser, parent=None):
        super().__init__(user, parent)

    def _build_search_area(self):
        return None

    def _load_data(self, page: int = 1):
        with get_session() as session:
            q = session.query(RcCorpTm)
            ym = self._get_toolbar_yymm()
            if ym:
                q = q.filter(RcCorpTm.base_yymm == ym)
            total = q.count()
            ps = self._get_page_size()
            rows_obj = q.offset((page - 1) * ps).limit(ps).all()
            rows = [
                {
                    "base_yymm": r.base_yymm,
                    "crd_eval_agncy_cd": r.crd_eval_agncy_cd,
                    "from_crd_grd_cd": r.from_crd_grd_cd,
                    "to_crd_grd_cd": r.to_crd_grd_cd,
                    "trans_prob": float(r.trans_prob) if r.trans_prob is not None else None,
                }
                for r in rows_obj
            ]
        self.table_model.load(rows)
        self.pager.set_total(total)
