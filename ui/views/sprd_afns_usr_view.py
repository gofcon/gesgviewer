"""AFNS 스프레드 사용자 입력 화면"""
from ui.views._base_crud_view import BaseCrudView
from ui.widgets.form_dialog import FormField
from db.database import get_session
from db.utils import upsert, delete_by_pk
from db.models.sprd_curve import SprdAfnsUsr
from db.models.auth import AppUser
from config.settings import DEFAULT_PAGE_SIZE
from services.input_service import IrCurveInputService

HEADERS = [
    ("base_yymm","기준년월"),("ir_model_id","모델ID"),("ir_curve_id","커브ID"),("mat_cd","만기"),
    ("mean_sprd","평균"),("up_sprd","상승"),("down_sprd","하락"),("flat_sprd","평탄"),("steep_sprd","가파름"),
]


class SprdAfnsUsrView(BaseCrudView):
    HEADERS = HEADERS
    VIEW_TITLE = "AFNS 스프레드 사용자 입력"
    EDITABLE_KEYS = {"mean_sprd", "up_sprd", "down_sprd", "flat_sprd", "steep_sprd"}

    def __init__(self, user: AppUser, parent=None):
        curves = IrCurveInputService.get_ir_curve_id_options()
        self.ADD_FIELDS = [
            FormField("base_yymm",   "기준년월", "text"),
            FormField("ir_model_id", "모델ID",   "text"),
            FormField("ir_curve_id", "커브ID",   "combo", options=curves),
            FormField("mat_cd",      "만기",     "text"),
            FormField("mean_sprd",   "평균",     "decimal"),
            FormField("up_sprd",     "상승",     "decimal"),
            FormField("down_sprd",   "하락",     "decimal"),
            FormField("flat_sprd",   "평탄",     "decimal"),
            FormField("steep_sprd",  "가파름",   "decimal"),
        ]
        super().__init__(user, parent)

    def _load_data(self, page: int = 1):
        with get_session() as session:
            q = session.query(SprdAfnsUsr)
            ym = self._get_toolbar_yymm()
            if ym:
                q = q.filter(SprdAfnsUsr.base_yymm == ym)
            total = q.count()
            ps = self._get_page_size()
            rows_obj = q.offset((page - 1) * ps).limit(ps).all()
            rows = [
                {
                    "base_yymm":   r.base_yymm,
                    "ir_model_id": r.ir_model_id,
                    "ir_curve_id": r.ir_curve_id,
                    "mat_cd":      r.mat_cd,
                    "mean_sprd":   float(r.mean_sprd)  if r.mean_sprd  is not None else None,
                    "up_sprd":     float(r.up_sprd)    if r.up_sprd    is not None else None,
                    "down_sprd":   float(r.down_sprd)  if r.down_sprd  is not None else None,
                    "flat_sprd":   float(r.flat_sprd)  if r.flat_sprd  is not None else None,
                    "steep_sprd":  float(r.steep_sprd) if r.steep_sprd is not None else None,
                }
                for r in rows_obj
            ]
        self.table_model.load(rows)
        self.pager.set_total(total)

    def _save_row(self, data: dict, is_new: bool) -> bool:
        with get_session() as session:
            upsert(session, SprdAfnsUsr,
                   (data["base_yymm"], data["ir_model_id"], data["ir_curve_id"], data["mat_cd"]),
                   data)
        return True

    def _delete_row(self, row: dict) -> bool:
        with get_session() as session:
            delete_by_pk(session, SprdAfnsUsr,
                         (row["base_yymm"], row["ir_model_id"], row["ir_curve_id"], row["mat_cd"]))
        return True
