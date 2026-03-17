"""메뉴 목록 관리 — JSP: MnuMngList.jsp"""
from ui.views._base_crud_view import BaseCrudView
from ui.widgets.form_dialog import FormField
from services.common_service import ContentService
from db.database import get_session
from db.models.common import MnuMng
from db.models.auth import AppUser
from config.settings import DEFAULT_PAGE_SIZE

HEADERS = [
    ("menu_no","메뉴번호"),("menu_ordr","순서"),("menu_nm","메뉴명"),
    ("upper_menu_no","상위메뉴"),("progrm_file_nm","프로그램파일"),("menu_dc","설명"),
]


class MnuMngView(BaseCrudView):
    HEADERS = HEADERS
    VIEW_TITLE = "메뉴 목록 관리"
    EDITABLE_KEYS = {"menu_ordr", "menu_nm", "upper_menu_no", "progrm_file_nm", "menu_dc"}
    ADD_FIELDS = [
        FormField("menu_ordr",       "순서",       "number", required=False),
        FormField("menu_nm",         "메뉴명",     "text"),
        FormField("upper_menu_no",   "상위메뉴번호", "number", required=False),
        FormField("progrm_file_nm",  "프로그램파일", "text", required=False),
        FormField("menu_dc",         "설명",       "text", required=False),
    ]

    def __init__(self, user: AppUser, parent=None):
        super().__init__(user, parent)

    def _build_search_area(self):
        return None

    def _load_data(self, page: int = 1):
        with get_session() as session:
            q = session.query(MnuMng)
            total = q.count()
            rows_obj = q.order_by(MnuMng.menu_ordr)\
                        .offset((page - 1) * DEFAULT_PAGE_SIZE).limit(DEFAULT_PAGE_SIZE).all()
            rows = [{"menu_no": r.menu_no, "menu_ordr": r.menu_ordr, "menu_nm": r.menu_nm,
                     "upper_menu_no": r.upper_menu_no, "progrm_file_nm": r.progrm_file_nm,
                     "menu_dc": r.menu_dc} for r in rows_obj]
        self.table_model.load(rows)
        self.pager.set_total(total)

    def _save_row(self, data: dict, is_new: bool) -> bool:
        ContentService.save_mnu_mng(data)
        return True

    def _delete_row(self, row: dict) -> bool:
        ContentService.delete_mnu_mng(row["menu_no"])
        return True
