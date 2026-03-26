"""기업 전환행렬 사용자 입력 화면"""
from ui.views._base_crud_view import BaseCrudView
from ui.widgets.form_dialog import FormField
from db.database import get_session
from db.utils import upsert, delete_by_pk
from db.models.sprd_curve import RcCorpTmUsr
from db.models.auth import AppUser
from config.settings import DEFAULT_PAGE_SIZE

HEADERS = [
    ("base_yymm","기준년월"),("crd_eval_agncy_cd","평가기관"),("from_crd_grd_cd","출발등급"),
    ("trans_prob_1","확률1"),("trans_prob_2","확률2"),("trans_prob_3","확률3"),
    ("trans_prob_4","확률4"),("trans_prob_5","확률5"),("trans_prob_6","확률6"),("trans_prob_7","확률7"),
]


class CorpTmUsrView(BaseCrudView):
    HEADERS = HEADERS
    VIEW_TITLE = "기업 전환행렬 사용자 입력"
    EDITABLE_KEYS = {
        "trans_prob_1","trans_prob_2","trans_prob_3","trans_prob_4",
        "trans_prob_5","trans_prob_6","trans_prob_7",
    }

    def __init__(self, user: AppUser, parent=None):
        self.ADD_FIELDS = [
            FormField("base_yymm",        "기준년월", "text"),
            FormField("crd_eval_agncy_cd", "평가기관", "text"),
            FormField("from_crd_grd_cd",   "출발등급", "text"),
            FormField("trans_prob_1",      "확률1",   "decimal"),
            FormField("trans_prob_2",      "확률2",   "decimal"),
            FormField("trans_prob_3",      "확률3",   "decimal"),
            FormField("trans_prob_4",      "확률4",   "decimal"),
            FormField("trans_prob_5",      "확률5",   "decimal"),
            FormField("trans_prob_6",      "확률6",   "decimal"),
            FormField("trans_prob_7",      "확률7",   "decimal"),
        ]
        super().__init__(user, parent)

    def _load_data(self, page: int = 1):
        with get_session() as session:
            q = session.query(RcCorpTmUsr)
            ym = self._get_toolbar_yymm()
            if ym:
                q = q.filter(RcCorpTmUsr.base_yymm == ym)
            total = q.count()
            ps = self._get_page_size()
            rows_obj = q.offset((page - 1) * ps).limit(ps).all()
            rows = [
                {
                    "base_yymm":         r.base_yymm,
                    "crd_eval_agncy_cd": r.crd_eval_agncy_cd,
                    "from_crd_grd_cd":   r.from_crd_grd_cd,
                    "trans_prob_1":      float(r.trans_prob_1) if r.trans_prob_1 is not None else None,
                    "trans_prob_2":      float(r.trans_prob_2) if r.trans_prob_2 is not None else None,
                    "trans_prob_3":      float(r.trans_prob_3) if r.trans_prob_3 is not None else None,
                    "trans_prob_4":      float(r.trans_prob_4) if r.trans_prob_4 is not None else None,
                    "trans_prob_5":      float(r.trans_prob_5) if r.trans_prob_5 is not None else None,
                    "trans_prob_6":      float(r.trans_prob_6) if r.trans_prob_6 is not None else None,
                    "trans_prob_7":      float(r.trans_prob_7) if r.trans_prob_7 is not None else None,
                }
                for r in rows_obj
            ]
        self.table_model.load(rows)
        self.pager.set_total(total)

    def _save_row(self, data: dict, is_new: bool) -> bool:
        with get_session() as session:
            upsert(session, RcCorpTmUsr,
                   (data["base_yymm"], data["crd_eval_agncy_cd"], data["from_crd_grd_cd"]),
                   data)
        return True

    def _delete_row(self, row: dict) -> bool:
        with get_session() as session:
            delete_by_pk(session, RcCorpTmUsr,
                         (row["base_yymm"], row["crd_eval_agncy_cd"], row["from_crd_grd_cd"]))
        return True
