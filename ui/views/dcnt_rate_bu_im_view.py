"""할인율 BU 내부모형 화면"""
from ui.views._base_list_view import BaseListView
from db.database import get_session
from db.models.dcnt_rate import IrDcntRateBuIm
from db.models.auth import AppUser
from config.settings import DEFAULT_PAGE_SIZE

HEADERS = [
    ("base_yymm","기준년월"), ("appl_biz_dv","적용업무"), ("ir_model_id","모델ID"),
    ("ir_curve_id","커브ID"), ("ir_curve_sce_no","시나리오번호"), ("mat_cd","만기"),
    ("spot_rate_disc","현물할인"), ("spot_rate_cont","현물연속"),
    ("liq_prem","유동성프리미엄"), ("adj_spot_rate_disc","조정현물할인"),
    ("adj_spot_rate_cont","조정현물연속"), ("add_sprd","추가스프레드"),
]


class DcntRateBuImView(BaseListView):
    HEADERS = HEADERS
    VIEW_TITLE = "할인율 BU 내부모형"

    def __init__(self, user: AppUser, parent=None):
        super().__init__(user, parent)

    def _build_search_area(self):
        return None

    def _load_data(self, page: int = 1):
        with get_session() as session:
            q = session.query(IrDcntRateBuIm)
            ym = self._get_toolbar_yymm()
            if ym:
                q = q.filter(IrDcntRateBuIm.base_yymm == ym)
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
                    "mat_cd": r.mat_cd,
                    "spot_rate_disc": float(r.spot_rate_disc) if r.spot_rate_disc is not None else None,
                    "spot_rate_cont": float(r.spot_rate_cont) if r.spot_rate_cont is not None else None,
                    "liq_prem": float(r.liq_prem) if r.liq_prem is not None else None,
                    "adj_spot_rate_disc": float(r.adj_spot_rate_disc) if r.adj_spot_rate_disc is not None else None,
                    "adj_spot_rate_cont": float(r.adj_spot_rate_cont) if r.adj_spot_rate_cont is not None else None,
                    "add_sprd": float(r.add_sprd) if r.add_sprd is not None else None,
                }
                for r in rows_obj
            ]
        self.table_model.load(rows)
        self.pager.set_total(total)
