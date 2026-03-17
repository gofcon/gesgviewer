"""YTM 사용자 입력 화면 — JSP: YtmUsrList.jsp"""
from ui.views._base_crud_view import BaseCrudView
from ui.widgets.form_dialog import FormField
from services.ir_curve_service import IrCurveService
from db.models.auth import AppUser

HEADERS = [
    ("base_date","기준일자"),("ir_curve_id","커브ID"),
    ("mat_cd","만기"),("ytm_rate","YTM금리"),
]


class YtmUsrView(BaseCrudView):
    HEADERS = HEADERS
    VIEW_TITLE = "YTM 사용자 입력"
    EDITABLE_KEYS = {"ytm_rate"}
    COLUMN_WIDTHS = {
        'base_date':   100,       # 기준일자 고정
        'ir_curve_id': 'stretch', # 커브ID 내용 맞춤
        'mat_cd':       'stretch',        # 만기코드 고정
        'ytm_rate':    'stretch', # YTM금리 나머지 공간
    }

    def __init__(self, user: AppUser, parent=None):
        curves = IrCurveService.get_ir_curve_id_options()
        self.ADD_FIELDS = [
            FormField("base_date",   "기준일자", "text"),
            FormField("ir_curve_id", "커브ID",   "combo", options=curves),
            FormField("mat_cd",      "만기코드", "text"),
            FormField("ytm_rate",    "YTM금리",  "decimal"),
        ]
        super().__init__(user, parent)

    def _load_data(self, page: int = 1):
        rows, total = IrCurveService.get_ytm_usr_list(
            base_yymm=self._get_toolbar_yymm(), page=page)
        self.table_model.load(rows)
        self.pager.set_total(total)

    def _save_row(self, data: dict, is_new: bool) -> bool:
        IrCurveService.save_ytm_usr(data)
        return True

    def _delete_row(self, row: dict) -> bool:
        IrCurveService.delete_ytm_usr(row["base_date"], row["ir_curve_id"], row["mat_cd"])
        return True
