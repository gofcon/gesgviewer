"""변동성/스왑션 사용자 입력 화면"""
from ui.views._base_crud_view import BaseCrudView
from ui.widgets.form_dialog import FormField
from db.database import get_session
from db.utils import upsert, delete_by_pk
from db.models.ir_param_model import IrVolSwpnUsr
from db.models.auth import AppUser
from config.settings import DEFAULT_PAGE_SIZE
from services.input_service import IrCurveInputService

HEADERS = [
    ("base_date","기준일자"),("ir_curve_id","커브ID"),("swpn_mat","스왑션만기"),
    ("vol_swpn_y1","Y1"),("vol_swpn_y2","Y2"),("vol_swpn_y3","Y3"),
    ("vol_swpn_y5","Y5"),("vol_swpn_y7","Y7"),("vol_swpn_y10","Y10"),
    ("vol_swpn_y15","Y15"),("vol_swpn_y20","Y20"),("vol_swpn_y30","Y30"),
]


class VolSwpnUsrView(BaseCrudView):
    HEADERS = HEADERS
    VIEW_TITLE = "변동성/스왑션 사용자 입력"
    EDITABLE_KEYS = {
        "vol_swpn_y1","vol_swpn_y2","vol_swpn_y3","vol_swpn_y5","vol_swpn_y7",
        "vol_swpn_y10","vol_swpn_y15","vol_swpn_y20","vol_swpn_y30",
    }

    def __init__(self, user: AppUser, parent=None):
        curves = IrCurveInputService.get_ir_curve_id_options()
        self.ADD_FIELDS = [
            FormField("base_date",    "기준일자",   "text"),
            FormField("ir_curve_id",  "커브ID",     "combo", options=curves),
            FormField("swpn_mat",     "스왑션만기", "text"),
            FormField("vol_swpn_y1",  "Y1",         "decimal"),
            FormField("vol_swpn_y2",  "Y2",         "decimal"),
            FormField("vol_swpn_y3",  "Y3",         "decimal"),
            FormField("vol_swpn_y5",  "Y5",         "decimal"),
            FormField("vol_swpn_y7",  "Y7",         "decimal"),
            FormField("vol_swpn_y10", "Y10",        "decimal"),
            FormField("vol_swpn_y15", "Y15",        "decimal"),
            FormField("vol_swpn_y20", "Y20",        "decimal"),
            FormField("vol_swpn_y30", "Y30",        "decimal"),
        ]
        super().__init__(user, parent)

    def _load_data(self, page: int = 1):
        with get_session() as session:
            q = session.query(IrVolSwpnUsr)
            dt = self._get_toolbar_yymm()
            if dt:
                q = q.filter(IrVolSwpnUsr.base_date.like(dt[:6] + "%"))
            total = q.count()
            ps = self._get_page_size()
            rows_obj = q.offset((page - 1) * ps).limit(ps).all()
            rows = [
                {
                    "base_date":    r.base_date,
                    "ir_curve_id":  r.ir_curve_id,
                    "swpn_mat":     r.swpn_mat,
                    "vol_swpn_y1":  float(r.vol_swpn_y1)  if r.vol_swpn_y1  is not None else None,
                    "vol_swpn_y2":  float(r.vol_swpn_y2)  if r.vol_swpn_y2  is not None else None,
                    "vol_swpn_y3":  float(r.vol_swpn_y3)  if r.vol_swpn_y3  is not None else None,
                    "vol_swpn_y5":  float(r.vol_swpn_y5)  if r.vol_swpn_y5  is not None else None,
                    "vol_swpn_y7":  float(r.vol_swpn_y7)  if r.vol_swpn_y7  is not None else None,
                    "vol_swpn_y10": float(r.vol_swpn_y10) if r.vol_swpn_y10 is not None else None,
                    "vol_swpn_y15": float(r.vol_swpn_y15) if r.vol_swpn_y15 is not None else None,
                    "vol_swpn_y20": float(r.vol_swpn_y20) if r.vol_swpn_y20 is not None else None,
                    "vol_swpn_y30": float(r.vol_swpn_y30) if r.vol_swpn_y30 is not None else None,
                }
                for r in rows_obj
            ]
        self.table_model.load(rows)
        self.pager.set_total(total)

    def _save_row(self, data: dict, is_new: bool) -> bool:
        with get_session() as session:
            upsert(session, IrVolSwpnUsr,
                   (data["base_date"], data["ir_curve_id"], data["swpn_mat"]),
                   data)
        return True

    def _delete_row(self, row: dict) -> bool:
        with get_session() as session:
            delete_by_pk(session, IrVolSwpnUsr,
                         (row["base_date"], row["ir_curve_id"], row["swpn_mat"]))
        return True
