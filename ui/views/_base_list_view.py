"""
모든 목록 뷰의 공통 기반 클래스
jqGrid 패턴 → QTableView + PaginationWidget 패턴으로 통일

기능:
  • 헤더 클릭 정렬 (오름차순 → 내림차순 → 원래 순서)
  • 테이블 하단 실시간 필터 바 (전체 컬럼 or 특정 컬럼 선택 가능)
  • 숫자 컬럼도 정렬 순서가 올바름 (UserRole 기반 lessThan 비교)
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
                              QTableView, QPushButton, QAbstractItemView,
                              QSizePolicy, QLabel, QLineEdit, QComboBox,
                              QToolButton, QHeaderView, QMenu, QMessageBox)
from PyQt6.QtCore import Qt, QSortFilterProxyModel, QModelIndex
from ui.widgets.base_table_model import EsgTableModel
from ui.widgets.pagination_widget import PaginationWidget
from utils.export_utils import export_to_excel
from db.models.auth import AppUser
from config.settings import DEFAULT_PAGE_SIZE


# ─── 숫자/문자 혼합 정렬을 올바르게 처리하는 프록시 모델 ───────────
class _SortFilterProxy(QSortFilterProxyModel):
    """
    • UserRole 원본 값으로 숫자 컬럼 정렬 (문자열 비교 방지)
    • setFilterKeyColumn(-1) → 모든 컬럼에서 필터링
    • 대소문자 구분 없는 필터링
    """

    def lessThan(self, left: QModelIndex, right: QModelIndex) -> bool:
        lv = left.data(Qt.ItemDataRole.UserRole)
        rv = right.data(Qt.ItemDataRole.UserRole)
        # 둘 다 숫자면 숫자 비교
        if isinstance(lv, (int, float)) and isinstance(rv, (int, float)):
            return lv < rv
        # 그 외 문자열 비교 (None → 빈 문자열)
        return str(lv or "") < str(rv or "")


class _ResponsiveButtonMixin:
    """좁은 패널에서 버튼을 이모지 전용으로 전환하는 믹스인.

    BaseListView 와 차트+그리드 복합 뷰(DcntRateView 등)가 공통으로 사용.
    다중 상속 시 MRO 기반 cooperative __init__ 을 사용하므로
    super().__init__() 호출 순서만 지키면 자동 초기화됨.
    """

    # 이 너비(px) 이하로 좁아지면 버튼을 이모지 전용으로 전환.
    # 차트+그리드 복합 뷰는 서브클래스에서 더 큰 값으로 오버라이드.
    _COMPACT_THRESHOLD = 560

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # [(QPushButton, full_text, emoji, label, original_width), ...]
        self._responsive_btns: list[tuple] = []
        self._is_compact: bool = False

    def _register_responsive_btn(self, btn: QPushButton) -> None:
        """버튼을 반응형 목록에 등록. 'emoji 한글' 형태의 텍스트를 분리해 저장."""
        full_text = btn.text()
        parts     = full_text.split(" ", 1)
        emoji     = parts[0]                         # 첫 토큰 = 이모지
        label     = parts[1] if len(parts) > 1 else full_text
        orig_w    = btn.maximumWidth()
        if orig_w >= 16_777_215:                     # setFixedWidth 미사용
            orig_w = 80
        self._responsive_btns.append((btn, full_text, emoji, label, orig_w))

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self._update_button_mode()

    def _update_button_mode(self) -> None:
        """패널 너비에 따라 버튼을 이모지 전용 ↔ 전체 텍스트 모드로 전환."""
        compact = self.width() < self._COMPACT_THRESHOLD
        if compact == self._is_compact:
            return
        self._is_compact = compact
        for btn, full_text, emoji, label, orig_w in self._responsive_btns:
            if compact:
                btn.setText(emoji)
                btn.setFixedWidth(34)
                btn.setToolTip(label)      # 호버 시 한글 레이블 표시
            else:
                btn.setText(full_text)
                btn.setFixedWidth(orig_w)
                btn.setToolTip("")


class BaseListView(_ResponsiveButtonMixin, QWidget):
    """
    서브클래스에서 반드시 구현:
        HEADERS     : list[tuple[str, str]]  — [(컬럼키, 헤더명), ...]
        VIEW_TITLE  : str                    — 화면 제목
        _load_data(page)                     — 데이터 조회 후 self.table_model.load() 호출
    선택적 오버라이드:
        _build_search_area()                 — 검색 조건 영역 반환 (QWidget)
        _build_extra_buttons()               — 추가 버튼 목록 반환 [QPushButton, ...]
    """

    HEADERS: list[tuple[str, str]] = []
    VIEW_TITLE: str = "목록"
    # 컬럼 너비 설정 (CSS flex 유사)
    # {'key': 80}          → Interactive 초기 80px (드래그 조절 가능)
    # {'key': 'content'}  → ResizeToContents (내용 맞춤)
    # {'key': 'stretch'}  → Stretch (남은 공간 분배)
    # 미지정 컬럼          → Interactive (사용자 드래그 조절)
    # COLUMN_WIDTHS = {}   → 기본값: 전체 ResizeToContents + 마지막 Stretch
    COLUMN_WIDTHS: dict[str, int | str] = {}

    def _make_table_model(self):
        """서브클래스에서 오버라이드하면 다른 모델 사용 가능 (예: EsgEditableTableModel)."""
        return EsgTableModel([], self.HEADERS)

    def __init__(self, user: AppUser, parent=None):
        super().__init__(parent)   # _ResponsiveButtonMixin.__init__ → QWidget.__init__
        self.user = user
        self.table_model = self._make_table_model()

        # ── 검색 모드 플래그 ─────────────────────────────────────
        # False: 조회 전 (yymm 없음, 페이지네이션, 클라이언트 필터)
        # True : 조회 후 (yymm 적용, 전체 로드, 스크롤)
        self._search_mode: bool = False

        # ── 정렬·필터 프록시 ─────────────────────────────────────
        self.proxy_model = _SortFilterProxy()
        self.proxy_model.setSourceModel(self.table_model)
        self.proxy_model.setSortRole(Qt.ItemDataRole.UserRole)
        self.proxy_model.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.proxy_model.setFilterKeyColumn(-1)   # -1 = 전체 컬럼

        self._build_ui()
        self._load_data(1)

    # ─── UI 구성 ──────────────────────────────────────────────────
    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(12, 8, 12, 8)
        root.setSpacing(8)

        # 제목 행 (오른쪽 끝 = 조회 버튼)
        title_row = QHBoxLayout()
        title_row.setContentsMargins(0, 0, 0, 0)
        title = QLabel(f"<b>{self.VIEW_TITLE}</b>")
        title.setStyleSheet("font-size: 14px; padding: 4px 0;")
        self._btn_search = QPushButton("🔍 조회")
        self._btn_search.setFixedWidth(80)
        self._btn_search.clicked.connect(self._on_search_click)
        self._register_responsive_btn(self._btn_search)
        title_row.addWidget(title)
        for w in self._build_title_extra():   # 서브클래스 추가 위젯 (예: DataBrowserView 테이블 콤보)
            title_row.addWidget(w)
        title_row.addStretch()
        title_row.addWidget(self._btn_search)
        root.addLayout(title_row)

        # 검색 영역 (서브클래스 제공)
        search_widget = self._build_search_area()
        if search_widget:
            grp = QGroupBox("검색 조건")
            grp_layout = QVBoxLayout(grp)
            grp_layout.setContentsMargins(8, 4, 8, 4)
            grp_layout.addWidget(search_widget)
            root.addWidget(grp)


        # ── 필터 바 ────────────────────────────────────────────────
        filter_row = QHBoxLayout()
        filter_row.setSpacing(4)

        lbl_filter = QLabel("필터")
        lbl_filter.setStyleSheet("font-size: 11px; color: #64748B;")
        lbl_filter.setFixedWidth(28)
        filter_row.addWidget(lbl_filter)

        self._filter_edit = QLineEdit()
        self._filter_edit.setPlaceholderText("입력하면 현재 그리드에서 필터링…")
        self._filter_edit.setStyleSheet(
            "QLineEdit { border:1px solid #CBD5E1; border-radius:3px;"
            "            padding:2px 6px; font-size:12px; }"
        )
        self._filter_edit.textChanged.connect(self._on_filter_text_changed)
        filter_row.addWidget(self._filter_edit, stretch=1)

        self._filter_col_cb = QComboBox()
        self._filter_col_cb.setStyleSheet("font-size: 12px;")
        self._filter_col_cb.setFixedWidth(110)
        self._filter_col_cb.addItem("전체 컬럼", -1)
        for key, label in self.HEADERS:
            self._filter_col_cb.addItem(label, key)
        self._filter_col_cb.currentIndexChanged.connect(self._on_filter_col_changed)
        filter_row.addWidget(self._filter_col_cb)

        btn_clear = QToolButton()
        btn_clear.setText("✕")
        btn_clear.setToolTip("필터 초기화")
        btn_clear.setFixedSize(22, 22)
        btn_clear.clicked.connect(self._filter_edit.clear)
        filter_row.addWidget(btn_clear)
        root.addLayout(filter_row)

        # 테이블 (프록시 모델 사용)
        self.table_view = QTableView()
        self.table_view.setModel(self.proxy_model)
        self.table_view.setSortingEnabled(True)                          # 헤더 클릭 정렬
        self.table_view.horizontalHeader().setSortIndicatorShown(True)   # 정렬 화살표 표시
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_view.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table_view.setEditTriggers(
            QAbstractItemView.EditTrigger.DoubleClicked |
            QAbstractItemView.EditTrigger.EditKeyPressed)
        self.table_view.setAlternatingRowColors(True)
        self.table_view.verticalHeader().setDefaultSectionSize(22)
        self.table_view.verticalHeader().setVisible(False)
        self._apply_column_widths()
        # 헤더 우클릭 → 정렬 메뉴
        hdr = self.table_view.horizontalHeader()
        hdr.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        hdr.customContextMenuRequested.connect(self._on_header_context_menu)
        self.table_view.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        # 행 선택 색상 명시 (시스템 테마에 관계없이 보이게)
        self.table_view.setStyleSheet("""
            QTableView::item:selected {
                background-color: #DBEAFE;
                color: #1E293B;
            }
            QTableView::item:selected:!active {
                background-color: #E2E8F0;
                color: #334155;
            }
        """)
        root.addWidget(self.table_view, stretch=1)

        # ── 하단 통합 바: [left_btns+stretch] [pager] [stretch+right_btns+Excel] ──
        # left_w / right_w 동일 stretch=1 → pager 완전 가운데 정렬
        self.pager = PaginationWidget()
        self.pager.page_changed.connect(self._on_page_changed)

        left_w = QWidget()
        left_layout = QHBoxLayout(left_w)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(4)
        for btn in self._build_bottom_left_buttons():
            left_layout.addWidget(btn)
            self._register_responsive_btn(btn)
        left_layout.addStretch()
        left_w.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        right_w = QWidget()
        right_layout = QHBoxLayout(right_w)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(4)
        right_layout.addStretch()
        for btn in self._build_bottom_right_buttons():
            right_layout.addWidget(btn)
            self._register_responsive_btn(btn)
        btn_excel = QPushButton("📥 Excel")
        btn_excel.setFixedWidth(80)
        btn_excel.clicked.connect(self._on_excel)
        right_layout.addWidget(btn_excel)
        self._register_responsive_btn(btn_excel)
        right_w.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        bottom_bar = QHBoxLayout()
        bottom_bar.setContentsMargins(0, 2, 0, 2)
        bottom_bar.setSpacing(0)
        bottom_bar.addWidget(left_w,    stretch=1)
        bottom_bar.addWidget(self.pager, stretch=0)
        bottom_bar.addWidget(right_w,   stretch=1)
        root.addLayout(bottom_bar)

    # ─── 컬럼 너비 적용 ──────────────────────────────────────────
    def _apply_column_widths(self) -> None:
        header = self.table_view.horizontalHeader()
        header.setStretchLastSection(False)

        if not self.COLUMN_WIDTHS:
            # 기본값: 전체 ResizeToContents + 마지막 컬럼 Stretch
            header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
            if self.HEADERS:
                header.setSectionResizeMode(
                    len(self.HEADERS) - 1, QHeaderView.ResizeMode.Stretch)
            return

        # 기본 모드: Interactive (사용자 드래그)
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)

        for i, (key, _) in enumerate(self.HEADERS):
            spec = self.COLUMN_WIDTHS.get(key)
            if spec is None:
                pass  # Interactive 유지
            elif spec == 'content':
                header.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)
            elif spec == 'stretch':
                header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)
            else:
                # 초기 너비 지정 + 드래그 조절 가능
                header.setSectionResizeMode(i, QHeaderView.ResizeMode.Interactive)
                header.resizeSection(i, int(spec))

    # ─── 헤더 컨텍스트 메뉴 (정렬) ───────────────────────────────
    def _on_header_context_menu(self, pos) -> None:
        col = self.table_view.horizontalHeader().logicalIndexAt(pos)
        if col < 0:
            return
        menu = QMenu(self)
        menu.addAction("◀  왼쪽 정렬",   lambda: self._set_col_align(col, Qt.AlignmentFlag.AlignLeft))
        menu.addAction("≡  가운데 정렬", lambda: self._set_col_align(col, Qt.AlignmentFlag.AlignHCenter))
        menu.addAction("▶  오른쪽 정렬", lambda: self._set_col_align(col, Qt.AlignmentFlag.AlignRight))
        menu.exec(self.table_view.horizontalHeader().mapToGlobal(pos))

    def _set_col_align(self, col: int, align: Qt.AlignmentFlag) -> None:
        self.table_model.setColumnAlign(col, align)

    # ─── 서브클래스 오버라이드 포인트 ────────────────────────────
    def _get_toolbar_yymm(self) -> str:
        """메인 툴바의 기준년월 반환 (YYYYMM).

        조회 버튼을 누르기 전(초기 모드)에는 빈 문자열을 반환해
        yymm 필터 없이 전체 데이터를 로드한다.
        조회 버튼 클릭 후(검색 모드)에는 현재 툴바 값을 반환한다.
        """
        if not self._search_mode:
            return ""
        win = self.window()
        return win.get_base_yymm() if hasattr(win, "get_base_yymm") else ""

    def _get_page_size(self) -> int:
        """현재 모드에 따른 페이지 크기.

        조회 전: DEFAULT_PAGE_SIZE (페이지네이션)
        조회 후: 999_999 (전체 로드 → 스크롤)
        서브클래스 _load_data() 에서 page_size 인자로 사용한다.
        """
        return 999_999 if self._search_mode else DEFAULT_PAGE_SIZE

    def _build_title_extra(self) -> list:
        """제목 라벨 오른쪽에 추가할 위젯 목록 반환.
        서브클래스에서 오버라이드해 제목행에 커스텀 위젯을 삽입할 수 있다.
        """
        return []

    def _build_search_area(self) -> QWidget | None:
        """검색 조건 위젯 반환. 없으면 None."""
        return None

    def _build_bottom_left_buttons(self) -> list[QPushButton]:
        """페이지 바 왼쪽 버튼 목록 반환.
        조회 전용 화면: 레이아웃 통일을 위해 disabled 버튼 표시.
        CRUD 화면(BaseCrudView): 오버라이드해 활성 버튼 반환.
        """
        btns = []
        for label in ("➕ 추가", "✏️ 수정", "🗑️ 삭제", "💾 저장"):
            btn = QPushButton(label)
            btn.setFixedWidth(72)
            btn.setEnabled(False)
            btns.append(btn)
        return btns

    def _build_bottom_right_buttons(self) -> list[QPushButton]:
        """Excel·조회 버튼 앞(오른쪽) 버튼 목록 반환.
        조회 전용 화면: disabled Import 버튼 표시.
        CRUD 화면(BaseCrudView): 오버라이드해 활성 버튼 반환.
        """
        btn_import = QPushButton("📤 Import")
        btn_import.setFixedWidth(80)
        btn_import.setEnabled(False)
        return [btn_import]

    def _get_search_text(self) -> str:
        """필터 입력창의 현재 텍스트 반환.

        서브클래스에서 _load_data() 안에 서버사이드 조건으로 활용 가능:
            keyword = self._get_search_text()
            if keyword:
                query = query.filter(Model.col.contains(keyword))
        """
        return self._filter_edit.text().strip()

    def _update_search_tooltip(self) -> None:
        """조회 버튼 툴팁을 현재 활성 조회 조건(기준년월 + 필터텍스트)으로 갱신."""
        yymm = self._get_toolbar_yymm()
        text = self._get_search_text()
        parts: list[str] = []
        if yymm:
            parts.append(f"기준년월: {yymm}")
        if text:
            parts.append(f"필터: {text}")
        if parts:
            tip = "📋 현재 조회 조건\n" + "\n".join(f"  • {p}" for p in parts)
        else:
            tip = "📋 조회 조건 없음 (전체 데이터)"
        self._btn_search.setToolTip(tip)

    def _update_button_mode(self) -> None:
        """반응형 모드 전환 후 조회 버튼의 동적 툴팁을 복원."""
        super()._update_button_mode()
        # compact 모드에서 믹스인이 툴팁을 '조회'로 덮어쓰므로
        # 항상 동적 조건 툴팁으로 다시 설정한다.
        if hasattr(self, "_btn_search"):
            self._update_search_tooltip()

    def showEvent(self, event) -> None:
        """탭 전환 또는 첫 표시 시 기준년월이 반영된 최신 툴팁으로 갱신."""
        super().showEvent(event)
        self._update_search_tooltip()

    def _on_search_click(self) -> None:
        """조회 버튼 핸들러.

        첫 클릭 시 검색 모드로 전환:
          • _get_toolbar_yymm() 이 실제 yymm 반환
          • _get_page_size() 가 999_999 반환 (전체 로드)
          • PaginationWidget 숨김 (스크롤 모드)
        서브클래스에서 오버라이드 가능 (예: 미저장 경고).
        """
        self._search_mode = True
        self._update_search_tooltip()
        self.pager.setVisible(False)
        self._load_data(1)

    def _on_page_changed(self, page: int) -> None:
        """페이지 이동 핸들러. 서브클래스에서 오버라이드 가능."""
        self._load_data(page)

    def _load_data(self, page: int = 1) -> None:
        """데이터 로드 (반드시 override)"""
        raise NotImplementedError

    # ─── 프록시 모델 유틸 ─────────────────────────────────────────
    def _get_selected_source_row(self) -> dict:
        """
        현재 선택된 행의 소스 데이터 반환.
        프록시 인덱스 → 소스 인덱스 변환 포함.
        """
        idx = self.table_view.currentIndex()
        if not idx.isValid():
            return {}
        src_idx = self.proxy_model.mapToSource(idx)
        return self.table_model.get_row(src_idx.row())

    # ─── 필터 슬롯 ────────────────────────────────────────────────
    def _on_filter_text_changed(self, text: str) -> None:
        self.proxy_model.setFilterFixedString(text)
        self._update_search_tooltip()   # 필터 변경 즉시 버튼 툴팁 동기화

    def _on_filter_col_changed(self, index: int) -> None:
        """전체 컬럼(-1) 또는 특정 컬럼(0-based) 선택"""
        col_key = self._filter_col_cb.itemData(index)
        if col_key == -1:
            self.proxy_model.setFilterKeyColumn(-1)
        else:
            # HEADERS에서 key → 컬럼 인덱스 찾기
            for i, (key, _) in enumerate(self.HEADERS):
                if key == col_key:
                    self.proxy_model.setFilterKeyColumn(i)
                    break

    # ─── Excel ────────────────────────────────────────────────────
    def _on_excel(self) -> None:
        rows = self.table_model.all_rows()
        headers = [h[1] for h in self.HEADERS]
        keys    = [h[0] for h in self.HEADERS]
        if rows:
            export_to_excel(rows, headers, keys, self.VIEW_TITLE)
        else:
            QMessageBox.information(self, "Excel", "내보낼 데이터가 없습니다.")
