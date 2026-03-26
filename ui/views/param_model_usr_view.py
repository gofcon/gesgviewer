"""파라미터 모델 사용자 입력 화면"""
from ui.views._base_crud_view import BaseCrudView
from ui.widgets.form_dialog import FormField
from db.database import get_session
from db.utils import upsert, delete_by_pk
from db.models.ir_param_model import IrParamModelUsr
from db.models.auth import AppUser
from config.settings import DEFAULT_PAGE_SIZE
from services.input_service import IrCurveInputService

HEADERS = [
    ("appl_st_yymm","적용시작"),("appl_ed_yymm","적용종료"),("ir_model_id","모델ID"),
    ("ir_curve_id","커브ID"),("param_typ_cd","파라미터유형"),("param_val","파라미터값"),
]


class ParamModelUsrView(BaseCrudView):
    HEADERS = HEADERS
    VIEW_TITLE = "파라미터 모델 사용자 입력"
    EDITABLE_KEYS = {"param_val"}

    def __init__(self, user: AppUser, parent=None):
        curves = IrCurveInputService.get_ir_curve_id_options()
        self.ADD_FIELDS = [
            FormField("appl_st_yymm", "적용시작",     "text"),
            FormField("appl_ed_yymm", "적용종료",     "text"),
            FormField("ir_model_id",  "모델ID",       "text"),
            FormField("ir_curve_id",  "커브ID",       "combo", options=curves),
            FormField("param_typ_cd", "파라미터유형", "text"),
            FormField("param_val",    "파라미터값",   "decimal"),
        ]
        super().__init__(user, parent)

    def _load_data(self, page: int = 1):
        with get_session() as session:
            q = session.query(IrParamModelUsr)
            total = q.count()
            ps = self._get_page_size()
            rows_obj = q.offset((page - 1) * ps).limit(ps).all()
            rows = [
                {
                    "appl_st_yymm": r.appl_st_yymm,
                    "appl_ed_yymm": r.appl_ed_yymm,
                    "ir_model_id":  r.ir_model_id,
                    "ir_curve_id":  r.ir_curve_id,
                    "param_typ_cd": r.param_typ_cd,
                    "param_val":    float(r.param_val) if r.param_val is not None else None,
                }
                for r in rows_obj
            ]
        self.table_model.load(rows)
        self.pager.set_total(total)

    def _save_row(self, data: dict, is_new: bool) -> bool:
        with get_session() as session:
            upsert(session, IrParamModelUsr,
                   (data["appl_st_yymm"], data["appl_ed_yymm"], data["ir_model_id"],
                    data["ir_curve_id"], data["param_typ_cd"]),
                   data)
        return True

    def _delete_row(self, row: dict) -> bool:
        with get_session() as session:
            delete_by_pk(session, IrParamModelUsr,
                         (row["appl_st_yymm"], row["appl_ed_yymm"], row["ir_model_id"],
                          row["ir_curve_id"], row["param_typ_cd"]))
        return True
