"""배치 스케줄 관리 — JSP: BatchSchdList.jsp"""
from ui.views._base_crud_view import BaseCrudView
from ui.widgets.form_dialog import FormField
from services.common_service import BatchService
from db.models.auth import AppUser

HEADERS = [
    ("batch_schdul_id","스케줄ID"),("batch_opert_id","작업ID"),
    ("execut_cycle","실행주기"),("execut_schdul_de","실행일정"),
    ("execut_schdul_hour","시"),("execut_schdul_mnt","분"),("execut_schdul_secnd","초"),
]


class BatchSchdView(BaseCrudView):
    HEADERS = HEADERS
    VIEW_TITLE = "배치 스케줄 관리"
    EDITABLE_KEYS = {"batch_opert_id", "execut_cycle", "execut_schdul_de",
                     "execut_schdul_hour", "execut_schdul_mnt", "execut_schdul_secnd"}
    ADD_FIELDS = [
        FormField("batch_schdul_id",    "스케줄ID",  "text"),
        FormField("batch_opert_id",     "작업ID",    "text"),
        FormField("execut_cycle",       "실행주기",  "text", required=False),
        FormField("execut_schdul_de",   "실행일정일","text", required=False),
        FormField("execut_schdul_hour", "시",        "text", required=False),
        FormField("execut_schdul_mnt",  "분",        "text", required=False),
        FormField("execut_schdul_secnd","초",        "text", required=False),
    ]

    def __init__(self, user: AppUser, parent=None):
        super().__init__(user, parent)

    def _load_data(self, page: int = 1):
        rows, total = BatchService.get_batch_schdul_list(page=page)
        self.table_model.load(rows)
        self.pager.set_total(total)

    def _save_row(self, data: dict, is_new: bool) -> bool:
        BatchService.save_batch_schdul(data)
        return True

    def _delete_row(self, row: dict) -> bool:
        BatchService.delete_batch_schdul(row["batch_schdul_id"])
        return True
