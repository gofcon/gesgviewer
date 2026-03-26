"""
할인율 비즈 화면
JSP: DcntRateBizList.jsp — jqGrid + PIVOT 차트
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                              QLabel, QPushButton, QSplitter, QTableView,
                              QAbstractItemView, QSizePolicy,
                              QLineEdit, QComboBox, QToolButton)
from PyQt6.QtCore import Qt, QSortFilterProxyModel
from ui.views._base_list_view import _ResponsiveButtonMixin
from ui.widgets.base_table_model import EsgTableModel
from ui.widgets.pagination_widget import PaginationWidget
from ui.widgets.chart_widget import ChartWidget
from services.result_service import DcntRateService
from utils.export_utils import export_to_excel
from db.models.auth import AppUser
from config.settings import DEFAULT_PAGE_SIZE

HEADERS = [
    ("base_yymm","기준년월"),("appl_biz_dv","적용업무"),("ir_curve_id","커브ID"),
    ("ir_curve_sce_no","시나리오번호"),("mat_cd","만기"),
    ("spot_rate","현물금리"),("fwd_rate","선도금리"),
]


class DcntRateView(_ResponsiveButtonMixin, QWidget):
    # 차트+그리드 뷰: 전체 너비가 이 값 미만이면 버튼을 이모지 전용으로 전환
    _COMPACT_THRESHOLD = 800

    def __init__(self, user: AppUser, parent=None):
        super().__init__(parent)   # _ResponsiveButtonMixin.__init__ → QWidget.__init__
        self.user = user
        self._search_mode: bool = False
        self._build_ui()

    def _get_toolbar_yymm(self) -> str:
        if not self._search_mode:
            return ""
        win = self.window()
        return win.get_base_yymm() if hasattr(win, "get_base_yymm") else ""

    def _get_page_size(self) -> int:
        return 999_999 if self._search_mode else DEFAULT_PAGE_SIZE

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(12, 8, 12, 8)
        root.setSpacing(8)

        # 제목 행 (오른쪽 끝 = 조회 버튼)
        title_row = QHBoxLayout()
        title_row.setContentsMargins(0, 0, 0, 0)
        title = QLabel("<b>할인율 비즈</b>")
        title.setStyleSheet("font-size:14px; padding:4px 0;")
        btn_search = QPushButton("🔍 조회")
        btn_search.setFixedWidth(80)
        btn_search.clicked.connect(self._on_search_click)
        self._register_responsive_btn(btn_search)
        title_row.addWidget(title)
        title_row.addStretch()
        title_row.addWidget(btn_search)
        root.addLayout(title_row)

        # 스플리터: 왼쪽(테이블+하단바) | 오른쪽(차트)
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setHandleWidth(6)
        splitter.setChildrenCollapsible(False)
        splitter.setStyleSheet(
            "QSplitter::handle:horizontal {"
            "  background:#CBD5E1; border-radius:3px; margin:4px 0; }"
            "QSplitter::handle:horizontal:hover {"
            "  background:#3B82F6; }")

        left = QWidget()
        ll = QVBoxLayout(left)
        ll.setContentsMargins(0, 0, 0, 0)
        ll.setSpacing(4)

        # ── 필터 바 ──────────────────────────────────────────────────
        filter_row = QHBoxLayout()
        filter_row.setSpacing(4)
        lbl = QLabel("필터")
        lbl.setStyleSheet("font-size:11px; color:#64748B;")
        lbl.setFixedWidth(28)
        filter_row.addWidget(lbl)
        self._filter_edit = QLineEdit()
        self._filter_edit.setPlaceholderText("입력하면 실시간 필터링…")
        self._filter_edit.setStyleSheet(
            "QLineEdit { border:1px solid #CBD5E1; border-radius:3px; padding:2px 6px; font-size:12px; }")
        filter_row.addWidget(self._filter_edit, stretch=1)
        self._filter_col_cb = QComboBox()
        self._filter_col_cb.setStyleSheet("font-size:12px;")
        self._filter_col_cb.setFixedWidth(110)
        self._filter_col_cb.addItem("전체 컬럼", -1)
        for key, label in HEADERS:
            self._filter_col_cb.addItem(label, key)
        filter_row.addWidget(self._filter_col_cb)
        btn_clr = QToolButton()
        btn_clr.setText("✕"); btn_clr.setToolTip("필터 초기화"); btn_clr.setFixedSize(22, 22)
        btn_clr.clicked.connect(self._filter_edit.clear)
        filter_row.addWidget(btn_clr)
        ll.addLayout(filter_row)

        # ── 테이블 + 프록시 ───────────────────────────────────────────
        self.model = EsgTableModel([], HEADERS)
        self.proxy = QSortFilterProxyModel()
        self.proxy.setSourceModel(self.model)
        self.proxy.setSortRole(Qt.ItemDataRole.UserRole)
        self.proxy.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.proxy.setFilterKeyColumn(-1)
        self._filter_edit.textChanged.connect(self.proxy.setFilterFixedString)
        self._filter_col_cb.currentIndexChanged.connect(self._on_filter_col_changed)

        self.table = QTableView()
        self.table.setModel(self.proxy)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSortingEnabled(True)
        self.table.horizontalHeader().setSortIndicatorShown(True)
        self.table.verticalHeader().setDefaultSectionSize(22)
        ll.addWidget(self.table, stretch=1)

        # 하단 통합 바 — 그리드 영역 안에 배치 (페이저 가운데 정렬)
        self.pager = PaginationWidget()
        self.pager.page_changed.connect(self._load)

        left_btn_w = QWidget()
        left_btn_layout = QHBoxLayout(left_btn_w)
        left_btn_layout.setContentsMargins(0, 0, 0, 0)
        left_btn_layout.setSpacing(4)
        for label in ("➕ 추가", "✏️ 수정", "🗑️ 삭제", "💾 저장"):
            btn = QPushButton(label)
            btn.setFixedWidth(72)
            btn.setEnabled(False)
            left_btn_layout.addWidget(btn)
            self._register_responsive_btn(btn)
        left_btn_layout.addStretch()
        left_btn_w.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        right_btn_w = QWidget()
        right_btn_layout = QHBoxLayout(right_btn_w)
        right_btn_layout.setContentsMargins(0, 0, 0, 0)
        right_btn_layout.setSpacing(4)
        right_btn_layout.addStretch()
        btn_import = QPushButton("📤 Import")
        btn_import.setFixedWidth(80)
        btn_import.setEnabled(False)
        right_btn_layout.addWidget(btn_import)
        self._register_responsive_btn(btn_import)
        btn_excel = QPushButton("📥 Excel")
        btn_excel.setFixedWidth(80)
        btn_excel.clicked.connect(self._on_excel)
        right_btn_layout.addWidget(btn_excel)
        self._register_responsive_btn(btn_excel)
        right_btn_w.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        bottom_bar = QHBoxLayout()
        bottom_bar.setContentsMargins(0, 2, 0, 2)
        bottom_bar.setSpacing(0)
        bottom_bar.addWidget(left_btn_w,  stretch=1)
        bottom_bar.addWidget(self.pager,  stretch=0)
        bottom_bar.addWidget(right_btn_w, stretch=1)
        ll.addLayout(bottom_bar)

        splitter.addWidget(left)
        self.chart = ChartWidget()
        splitter.addWidget(self.chart)
        splitter.setSizes([700, 400])
        root.addWidget(splitter, stretch=1)

    def _on_filter_col_changed(self, idx: int) -> None:
        col_data = self._filter_col_cb.itemData(idx)
        if col_data == -1:
            self.proxy.setFilterKeyColumn(-1)
        else:
            for i, (key, _) in enumerate(HEADERS):
                if key == col_data:
                    self.proxy.setFilterKeyColumn(i)
                    break

    def _on_search_click(self) -> None:
        self._search_mode = True
        self.pager.setVisible(False)
        self._load(1)

    def _load(self, page: int = 1) -> None:
        rows, total = DcntRateService.get_dcnt_rate_biz_list(
            base_yymm=self._get_toolbar_yymm(),
            page=page, page_size=self._get_page_size())
        self.model.load(rows)
        self.pager.set_total(total)
        self._update_chart(rows)

    def _update_chart(self, rows: list[dict]) -> None:
        if not rows:
            self.chart.clear()
            return
        # x축: 고유 만기(삽입 순서 유지)
        seen_mat: dict[str, None] = {}
        # series_map: {시나리오 레이블: {mat_cd: spot_rate}}
        series_map: dict[str, dict] = {}
        for r in rows:
            mat = r.get("mat_cd", "")
            seen_mat[mat] = None
            key = f"시나리오{r.get('ir_curve_sce_no', '')}"
            if key not in series_map:
                series_map[key] = {}
            series_map[key][mat] = r.get("spot_rate") or 0
        x_labels = list(seen_mat)
        # 각 시리즈를 x_labels 순서에 맞게 정렬 (없는 만기는 0 처리)
        y_series = {k: [v.get(m, 0) for m in x_labels] for k, v in series_map.items()}
        self.chart.plot_line(
            x_labels, y_series,
            title="할인율 (만기별)", x_label="만기", y_label="할인율")

    def _on_excel(self) -> None:
        export_to_excel(self.model.all_rows(), [h[1] for h in HEADERS], [h[0] for h in HEADERS], "할인율_비즈")
