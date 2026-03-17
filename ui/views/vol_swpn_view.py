"""변동성/스왑션 화면 — JSP: VolSwpnList.jsp"""
from ui.views._base_list_view import BaseListView
from db.database import get_session
from db.models.ir_param_model import VolSwpn
from db.models.auth import AppUser

HEADERS = [
    ("base_yymm","기준년월"),("appl_biz_dv","적용업무"),("ir_curve_id","커브ID"),
    ("opt_mat_cd","옵션만기"),("swpn_mat_cd","스왑션만기"),("vol_val","변동성"),
]

class VolSwpnView(BaseListView):
    HEADERS = HEADERS
    VIEW_TITLE = "변동성/스왑션"
    def _load_data(self, page: int = 1):
        from config.settings import DEFAULT_PAGE_SIZE
        with get_session() as session:
            q = session.query(VolSwpn)
            ym = self._get_toolbar_yymm()
            if ym: q = q.filter(VolSwpn.base_yymm == ym)
            total = q.count()
            rows_obj = q.offset((page-1)*DEFAULT_PAGE_SIZE).limit(DEFAULT_PAGE_SIZE).all()
            rows = [{"base_yymm": r.base_yymm,"appl_biz_dv": r.appl_biz_dv,"ir_curve_id": r.ir_curve_id,
                     "opt_mat_cd": r.opt_mat_cd,"swpn_mat_cd": r.swpn_mat_cd,
                     "vol_val": float(r.vol_val) if r.vol_val else None} for r in rows_obj]
        self.table_model.load(rows); self.pager.set_total(total)
