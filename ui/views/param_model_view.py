"""파라미터 모델 화면 — JSP: ParamModelList.jsp"""
from ui.views._base_crud_view import BaseCrudView
from ui.widgets.form_dialog import FormField
from services.param_sw_service import ParamSwService
from services.ir_curve_service import IrCurveService
from db.models.auth import AppUser

HEADERS = [
    ("ir_model_id","모델ID"),("ir_curve_id","커브ID"),
    ("ir_model_nm","모델명"),("ir_model_dc","설명"),("use_at","사용여부"),
]
_USE_AT_OPTS = ["Y", "N"]


class ParamModelView(BaseCrudView):
    HEADERS = HEADERS
    VIEW_TITLE = "파라미터 모델"
    EDITABLE_KEYS = {"ir_model_nm", "ir_model_dc", "use_at"}
    COMBO_COLS = {"use_at": _USE_AT_OPTS}

    def __init__(self, user: AppUser, parent=None):
        curves = IrCurveService.get_ir_curve_id_options()
        self.ADD_FIELDS = [
            FormField("ir_model_id", "모델ID",   "text"),
            FormField("ir_curve_id", "커브ID",   "combo", options=curves),
            FormField("ir_model_nm", "모델명",   "text"),
            FormField("ir_model_dc", "설명",     "text",  required=False),
            FormField("use_at",      "사용여부", "combo", options=_USE_AT_OPTS),
        ]
        super().__init__(user, parent)

    def _load_data(self, page: int = 1):
        rows, total = ParamSwService.get_param_model_list(page=page)
        self.table_model.load(rows)
        self.pager.set_total(total)

    def _save_row(self, data: dict, is_new: bool) -> bool:
        ParamSwService.save_param_model(data)
        return True

    def _delete_row(self, row: dict) -> bool:
        ParamSwService.delete_param_model(row["ir_model_id"], row["ir_curve_id"])
        return True
