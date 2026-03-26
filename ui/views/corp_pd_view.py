"""기업 부도율 화면 — JSP: CorpPdList.jsp"""
from ui.views._base_list_view import BaseListView
from db.database import get_session
from db.models.sprd_curve import RcCorpPdBiz
from db.models.auth import AppUser
from config.settings import DEFAULT_PAGE_SIZE

HEADERS = [
    ("base_yymm","기준년월"),("appl_biz_dv","적용업무"),("crd_grd_cd","신용등급"),
    ("mat_cd","만기"),("cum_pd","누적부도율"),("fwd_pd","선도부도율"),
]

class CorpPdView(BaseListView):
    HEADERS = HEADERS
    VIEW_TITLE = "기업 부도율"
    def _load_data(self, page: int = 1):
        with get_session() as session:
            q = session.query(RcCorpPdBiz)
            ym = self._get_toolbar_yymm()
            if ym: q = q.filter(RcCorpPdBiz.base_yymm == ym)
            total = q.count()
            ps = self._get_page_size()
            rows_obj = q.offset((page-1)*ps).limit(ps).all()
            rows = [{"base_yymm": r.base_yymm,"appl_biz_dv": r.appl_biz_dv,"crd_grd_cd": r.crd_grd_cd,
                     "mat_cd": r.mat_cd,"cum_pd": float(r.cum_pd) if r.cum_pd else None,
                     "fwd_pd": float(r.fwd_pd) if r.fwd_pd else None} for r in rows_obj]
        self.table_model.load(rows); self.pager.set_total(total)
