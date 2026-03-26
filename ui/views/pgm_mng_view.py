"""프로그램 관리 — JSP: PgmMngList.jsp"""
from ui.views._base_crud_view import BaseCrudView
from ui.widgets.form_dialog import FormField
from services.system_service import ContentService
from db.database import get_session
from db.models.common import PgmMng
from db.models.auth import AppUser
from config.settings import DEFAULT_PAGE_SIZE

HEADERS = [("progrm_file_nm","파일명"),("progrm_stre_path","경로"),("url","URL"),("use_at","사용여부")]
_USE_AT_OPTS = ["Y", "N"]


class PgmMngView(BaseCrudView):
    HEADERS = HEADERS
    VIEW_TITLE = "프로그램 관리"
    EDITABLE_KEYS = {"progrm_stre_path", "url", "use_at"}
    COMBO_COLS = {"use_at": _USE_AT_OPTS}
    ADD_FIELDS = [
        FormField("progrm_file_nm",  "파일명", "text"),
        FormField("progrm_stre_path","경로",   "text", required=False),
        FormField("url",             "URL",    "text", required=False),
        FormField("use_at",          "사용여부","combo", options=_USE_AT_OPTS),
    ]

    def __init__(self, user: AppUser, parent=None):
        super().__init__(user, parent)

    def _build_search_area(self):
        return None

    def _load_data(self, page: int = 1):
        with get_session() as session:
            q = session.query(PgmMng)
            total = q.count()
            ps = self._get_page_size()
            rows_obj = q.offset((page - 1) * ps).limit(ps).all()
            rows = [{"progrm_file_nm": r.progrm_file_nm, "progrm_stre_path": r.progrm_stre_path,
                     "url": r.url, "use_at": r.use_at} for r in rows_obj]
        self.table_model.load(rows)
        self.pager.set_total(total)

    def _save_row(self, data: dict, is_new: bool) -> bool:
        ContentService.save_pgm_mng(data)
        return True

    def _delete_row(self, row: dict) -> bool:
        ContentService.delete_pgm_mng(row["progrm_file_nm"])
        return True
