"""공지사항 — JSP: CopBbsList.jsp"""
from PyQt6.QtWidgets import QWidget, QLineEdit, QFormLayout
from ui.views._base_crud_view import BaseCrudView
from ui.widgets.form_dialog import FormField
from services.common_service import ContentService
from db.database import get_session
from db.models.common import CopBbs
from db.models.auth import AppUser
from config.settings import DEFAULT_PAGE_SIZE

HEADERS = [
    ("ntt_id","게시글ID"),("ntt_sj","제목"),
    ("frst_register_nm","작성자"),("frst_regist_pnttm","등록일시"),
]


class CopBbsView(BaseCrudView):
    HEADERS = HEADERS
    VIEW_TITLE = "공지사항"
    EDITABLE_KEYS = {"ntt_sj", "frst_register_nm"}
    ADD_FIELDS = [
        FormField("ntt_sj",          "제목",   "text"),
        FormField("frst_register_nm","작성자", "text", required=False),
    ]

    def __init__(self, user: AppUser, parent=None):
        self._edit_title = QLineEdit()
        self._edit_title.setPlaceholderText("제목 검색")
        super().__init__(user, parent)

    def _build_search_area(self):
        w = QWidget()
        f = QFormLayout(w)
        f.addRow("제목", self._edit_title)
        return w

    def _load_data(self, page: int = 1):
        with get_session() as session:
            q = session.query(CopBbs)
            title = self._edit_title.text().strip()
            if title:
                q = q.filter(CopBbs.ntt_sj.like(f"%{title}%"))
            total = q.count()
            rows_obj = q.order_by(CopBbs.ntt_id.desc())\
                        .offset((page - 1) * DEFAULT_PAGE_SIZE).limit(DEFAULT_PAGE_SIZE).all()
            rows = [{"ntt_id": r.ntt_id, "ntt_sj": r.ntt_sj,
                     "frst_register_nm": r.frst_register_nm,
                     "frst_regist_pnttm": str(r.frst_regist_pnttm) if r.frst_regist_pnttm else ""}
                    for r in rows_obj]
        self.table_model.load(rows)
        self.pager.set_total(total)

    def _save_row(self, data: dict, is_new: bool) -> bool:
        ContentService.save_cop_bbs(data)
        return True

    def _delete_row(self, row: dict) -> bool:
        ContentService.delete_cop_bbs(row["ntt_id"])
        return True
