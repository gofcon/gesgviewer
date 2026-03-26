"""할인율 사용자 입력 화면"""
from ui.views._base_crud_view import BaseCrudView
from ui.widgets.form_dialog import FormField
from db.database import get_session
from db.utils import upsert, delete_by_pk
from db.models.dcnt_rate import IrDcntRateUsr
from db.models.auth import AppUser
from config.settings import DEFAULT_PAGE_SIZE
from services.input_service import IrCurveInputService

HEADERS = [
    ("base_yymm","기준년월"),("appl_biz_dv","적용업무"),("ir_curve_id","커브ID"),
    ("ir_curve_sce_no","시나리오번호"),("mat_cd","만기"),
    ("spot_rate","현물금리"),("fwd_rate","선도금리"),
    ("adj_spot_rate","조정현물"),("adj_fwd_rate","조정선도"),
]


class DcntRateUsrView(BaseCrudView):
    HEADERS = HEADERS
    VIEW_TITLE = "할인율 사용자 입력"
    EDITABLE_KEYS = {"spot_rate", "fwd_rate", "adj_spot_rate", "adj_fwd_rate"}

    def __init__(self, user: AppUser, parent=None):
        curves = IrCurveInputService.get_ir_curve_id_options()
        self.ADD_FIELDS = [
            FormField("base_yymm",       "기준년월",     "text"),
            FormField("appl_biz_dv",     "적용업무",     "combo", options=["KICS","IFRS","IBIZ","SAAS"]),
            FormField("ir_curve_id",     "커브ID",       "combo", options=curves),
            FormField("ir_curve_sce_no", "시나리오번호", "number"),
            FormField("mat_cd",          "만기",         "text"),
            FormField("spot_rate",       "현물금리",     "decimal"),
            FormField("fwd_rate",        "선도금리",     "decimal"),
            FormField("adj_spot_rate",   "조정현물",     "decimal"),
            FormField("adj_fwd_rate",    "조정선도",     "decimal"),
        ]
        super().__init__(user, parent)

    def _load_data(self, page: int = 1):
        with get_session() as session:
            q = session.query(IrDcntRateUsr)
            ym = self._get_toolbar_yymm()
            if ym:
                q = q.filter(IrDcntRateUsr.base_yymm == ym)
            total = q.count()
            ps = self._get_page_size()
            rows_obj = q.offset((page - 1) * ps).limit(ps).all()
            rows = [
                {
                    "base_yymm":       r.base_yymm,
                    "appl_biz_dv":     r.appl_biz_dv,
                    "ir_curve_id":     r.ir_curve_id,
                    "ir_curve_sce_no": r.ir_curve_sce_no,
                    "mat_cd":          r.mat_cd,
                    "spot_rate":       float(r.spot_rate)     if r.spot_rate     is not None else None,
                    "fwd_rate":        float(r.fwd_rate)      if r.fwd_rate      is not None else None,
                    "adj_spot_rate":   float(r.adj_spot_rate) if r.adj_spot_rate is not None else None,
                    "adj_fwd_rate":    float(r.adj_fwd_rate)  if r.adj_fwd_rate  is not None else None,
                }
                for r in rows_obj
            ]
        self.table_model.load(rows)
        self.pager.set_total(total)

    def _save_row(self, data: dict, is_new: bool) -> bool:
        with get_session() as session:
            upsert(session, IrDcntRateUsr,
                   (data["base_yymm"], data["appl_biz_dv"], data["ir_curve_id"],
                    int(data["ir_curve_sce_no"]), data["mat_cd"]),
                   data)
        return True

    def _delete_row(self, row: dict) -> bool:
        with get_session() as session:
            delete_by_pk(session, IrDcntRateUsr,
                         (row["base_yymm"], row["appl_biz_dv"], row["ir_curve_id"],
                          int(row["ir_curve_sce_no"]), row["mat_cd"]))
        return True
