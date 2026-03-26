"""LP 스프레드 사용자 입력 화면"""
from ui.views._base_crud_view import BaseCrudView
from ui.widgets.form_dialog import FormField
from db.database import get_session
from db.utils import upsert, delete_by_pk
from db.models.sprd_curve import SprdLpUsr
from db.models.auth import AppUser
from config.settings import DEFAULT_PAGE_SIZE
from services.input_service import IrCurveInputService

HEADERS = [
    ("appl_st_yymm","적용시작"),("appl_ed_yymm","적용종료"),("appl_biz_dv","적용업무"),
    ("ir_curve_id","커브ID"),("ir_curve_sce_no","시나리오번호"),("mat_cd","만기"),
    ("liq_prem","유동성프리미엄"),
]


class SprdLpUsrView(BaseCrudView):
    HEADERS = HEADERS
    VIEW_TITLE = "LP 스프레드 사용자 입력"
    EDITABLE_KEYS = {"liq_prem"}

    def __init__(self, user: AppUser, parent=None):
        curves = IrCurveInputService.get_ir_curve_id_options()
        self.ADD_FIELDS = [
            FormField("appl_st_yymm",    "적용시작",     "text"),
            FormField("appl_ed_yymm",    "적용종료",     "text"),
            FormField("appl_biz_dv",     "적용업무",     "combo", options=["KICS","IFRS","IBIZ","SAAS"]),
            FormField("ir_curve_id",     "커브ID",       "combo", options=curves),
            FormField("ir_curve_sce_no", "시나리오번호", "number"),
            FormField("mat_cd",          "만기",         "text"),
            FormField("liq_prem",        "유동성프리미엄", "decimal"),
        ]
        super().__init__(user, parent)

    def _load_data(self, page: int = 1):
        with get_session() as session:
            q = session.query(SprdLpUsr)
            total = q.count()
            ps = self._get_page_size()
            rows_obj = q.offset((page - 1) * ps).limit(ps).all()
            rows = [
                {
                    "appl_st_yymm":    r.appl_st_yymm,
                    "appl_ed_yymm":    r.appl_ed_yymm,
                    "appl_biz_dv":     r.appl_biz_dv,
                    "ir_curve_id":     r.ir_curve_id,
                    "ir_curve_sce_no": r.ir_curve_sce_no,
                    "mat_cd":          r.mat_cd,
                    "liq_prem":        float(r.liq_prem) if r.liq_prem is not None else None,
                }
                for r in rows_obj
            ]
        self.table_model.load(rows)
        self.pager.set_total(total)

    def _save_row(self, data: dict, is_new: bool) -> bool:
        with get_session() as session:
            upsert(session, SprdLpUsr,
                   (data["appl_st_yymm"], data["appl_ed_yymm"], data["appl_biz_dv"],
                    data["ir_curve_id"], int(data["ir_curve_sce_no"]), data["mat_cd"]),
                   data)
        return True

    def _delete_row(self, row: dict) -> bool:
        with get_session() as session:
            delete_by_pk(session, SprdLpUsr,
                         (row["appl_st_yymm"], row["appl_ed_yymm"], row["appl_biz_dv"],
                          row["ir_curve_id"], int(row["ir_curve_sce_no"]), row["mat_cd"]))
        return True
