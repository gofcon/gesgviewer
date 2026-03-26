"""메뉴 목록 관리 — JSP: MnuMngList.jsp
DB(LETTNMENUINFO) 에 저장된 3레벨 메뉴 구조를 CRUD 로 관리.
저장 후 [메뉴 적용] 버튼으로 상단 툴바를 즉시 재구성할 수 있다.
"""
from PyQt6.QtWidgets import QPushButton, QMessageBox

from ui.views._base_crud_view import BaseCrudView
from ui.widgets.form_dialog import FormField
from services.system_service import ContentService
from db.database import get_session
from db.models.common import MnuMng
from db.models.auth import AppUser
from config.settings import DEFAULT_PAGE_SIZE


# ── HEADERS: 화면 표시 컬럼 ──────────────────────────────────────────
HEADERS = [
    ("menu_no",        "메뉴번호"),
    ("level",          "수준"),        # 계산 컬럼 (1=카테고리, 2=그룹, 3=항목)
    ("menu_ordr",      "순서"),
    ("menu_nm",        "메뉴명"),
    ("upper_menu_nm",  "상위메뉴명"),   # 계산 컬럼
    ("progrm_file_nm", "뷰 키"),
    ("menu_dc",        "설명"),
]


class MnuMngView(BaseCrudView):
    HEADERS      = HEADERS
    VIEW_TITLE   = "메뉴 목록 관리"
    EDITABLE_KEYS = {"menu_ordr", "menu_nm", "upper_menu_no",
                     "progrm_file_nm", "menu_dc"}
    ADD_FIELDS = [
        FormField("menu_ordr",       "순서",         "number", required=False),
        FormField("menu_nm",         "메뉴명",       "text"),
        FormField("upper_menu_no",   "상위메뉴번호", "number", required=False),
        FormField("progrm_file_nm",  "뷰 키",        "text", required=False),
        FormField("menu_dc",         "설명",         "text", required=False),
    ]

    def __init__(self, user: AppUser, parent=None):
        super().__init__(user, parent)

    # ── 하단 오른쪽 버튼 확장 ─────────────────────────────────────
    def _build_bottom_right_buttons(self) -> list:
        """Import 버튼 앞에 '기본값 초기화' · '메뉴 적용' 버튼 추가."""
        buttons = super()._build_bottom_right_buttons()

        btn_reset = QPushButton("🔄 기본값 초기화")
        btn_reset.setFixedWidth(120)
        btn_reset.setToolTip("하드코딩된 기본 메뉴 트리로 DB를 덮어씁니다.")
        btn_reset.clicked.connect(self._on_reset_to_default)

        btn_apply = QPushButton("✅ 메뉴 적용")
        btn_apply.setFixedWidth(96)
        btn_apply.setToolTip("DB 저장 내용을 상단 툴바에 즉시 반영합니다.")
        btn_apply.clicked.connect(self._on_apply_menu)

        # Import 버튼 앞에 삽입
        buttons[:0] = [btn_reset, btn_apply]
        return buttons

    # ── 검색 영역 없음 ─────────────────────────────────────────────
    def _build_search_area(self):
        return None

    # ── 데이터 로드 ────────────────────────────────────────────────
    def _load_data(self, page: int = 1):
        with get_session() as session:
            # level/upper_menu_nm 계산을 위해 전체 조회
            all_rows = session.query(MnuMng).order_by(MnuMng.menu_ordr).all()
            total    = len(all_rows)
            ps       = self._get_page_size()
            paged    = all_rows[(page - 1) * ps:
                                page * ps]
            by_id    = {r.menu_no: r for r in all_rows}
            rows: list[dict] = []
            for r in paged:
                parent = by_id.get(r.upper_menu_no)
                if parent is None:
                    level = 1
                elif by_id.get(parent.upper_menu_no) is None:
                    level = 2
                else:
                    level = 3
                rows.append({
                    "menu_no":        r.menu_no,
                    "level":          level,
                    "menu_ordr":      r.menu_ordr,
                    "menu_nm":        r.menu_nm,
                    "upper_menu_nm":  parent.menu_nm if parent else "",
                    "upper_menu_no":  r.upper_menu_no,   # 저장용
                    "progrm_file_nm": r.progrm_file_nm,
                    "menu_dc":        r.menu_dc,
                })
        self.table_model.load(rows)
        self.pager.set_total(total)

    # ── CRUD 저장/삭제 ─────────────────────────────────────────────
    def _save_row(self, data: dict, is_new: bool) -> bool:
        ContentService.save_mnu_mng(data)
        return True

    def _delete_row(self, row: dict) -> bool:
        ContentService.delete_mnu_mng(row["menu_no"])
        return True

    # ── 기본값 초기화 ──────────────────────────────────────────────
    def _on_reset_to_default(self) -> None:
        reply = QMessageBox.question(
            self, "기본값 초기화",
            "현재 메뉴 DB를 삭제하고 기본 메뉴 트리로 초기화합니다.\n"
            "계속하시겠습니까?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply != QMessageBox.StandardButton.Yes:
            return
        try:
            from config.nav_tree import NAV_TREE
            ContentService.seed_nav_tree(NAV_TREE, overwrite=True)
            QMessageBox.information(
                self, "완료",
                "기본 메뉴 트리로 초기화했습니다.\n[✅ 메뉴 적용] 버튼으로 툴바를 갱신하세요.",
            )
            self._load_data(1)
        except Exception as exc:
            QMessageBox.warning(self, "오류", f"초기화 실패: {exc}")

    # ── 메뉴 적용 (툴바 즉시 재구성) ──────────────────────────────
    def _on_apply_menu(self) -> None:
        win = self.window()
        if hasattr(win, "reload_nav_toolbar"):
            win.reload_nav_toolbar()
            QMessageBox.information(self, "메뉴 적용",
                                    "상단 메뉴 툴바를 새로 불러왔습니다.")
        else:
            QMessageBox.information(self, "메뉴 적용",
                                    "앱을 재시작하면 변경된 메뉴가 반영됩니다.")
