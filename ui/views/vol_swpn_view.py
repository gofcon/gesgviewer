"""변동성/스왑션 화면 — JSP: VolSwpnList.jsp"""
from ui.views._base_list_view import BaseListView
from db.database import get_session
from db.models.ir_param_model import IrVolSwpn
from db.models.auth import AppUser

HEADERS = [
    ("base_yymm","기준년월"),("ir_curve_id","커브ID"),
    ("swpn_mat_num","스왑션만기"),("swap_ten_num","스왑기간"),("vol","변동성"),
]

class VolSwpnView(BaseListView):
    HEADERS = HEADERS
    VIEW_TITLE = "변동성/스왑션"
    def _load_data(self, page: int = 1):
        with get_session() as session:
            q = session.query(IrVolSwpn)
            ym = self._get_toolbar_yymm()
            if ym: q = q.filter(IrVolSwpn.base_yymm == ym)
            total = q.count()
            ps = self._get_page_size()
            rows_obj = q.offset((page-1)*ps).limit(ps).all()
            rows = [{"base_yymm": r.base_yymm, "ir_curve_id": r.ir_curve_id,
                     "swpn_mat_num": float(r.swpn_mat_num),
                     "swap_ten_num": float(r.swap_ten_num),
                     "vol": float(r.vol) if r.vol else None} for r in rows_obj]
        self.table_model.load(rows); self.pager.set_total(total)
