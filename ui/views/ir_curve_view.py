"""
금리 커브 + 할인율 화면 (2-패널)
JSP: IrCurveList.jsp
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                              QLabel, QPushButton, QSplitter, QTableView, QAbstractItemView,
                              QLineEdit, QComboBox, QToolButton, QSizePolicy)
from PyQt6.QtCore import Qt, QSortFilterProxyModel
from ui.views._base_list_view import _ResponsiveButtonMixin
from ui.widgets.base_table_model import EsgTableModel
from ui.widgets.pagination_widget import PaginationWidget
from ui.widgets.chart_widget import ChartWidget
from services.base_data_service import IrCurveBaseService
from utils.export_utils import export_to_excel
from db.models.auth import AppUser
from config.settings import DEFAULT_PAGE_SIZE

CURVE_HEADERS = [
    ("base_date","기준일자"),("ir_curve_id","커브ID"),
    ("mat_cd","만기"),("spot_rate","현물금리"),
]


class IrCurveView(_ResponsiveButtonMixin, QWidget):
    # 차트+그리드 뷰: 전체 너비가 이 값 미만이면 버튼을 이모지 전용으로 전환
    _COMPACT_THRESHOLD = 800

    def __init__(self, user: AppUser, parent=None):
        super().__init__(parent)   # _ResponsiveButtonMixin.__init__ → QWidget.__init__
        self.user = user
        self._search_mode: bool = False
        self._build_ui()
        self._load(1)

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
        title = QLabel("<b>금리 커브</b>")
        title.setStyleSheet("font-size:14px; padding:4px 0;")
        btn_search = QPushButton("🔍 조회")
        btn_search.setFixedWidth(80)
        btn_search.clicked.connect(self._on_search_click)
        self._register_responsive_btn(btn_search)
        title_row.addWidget(title)
        title_row.addStretch()
        title_row.addWidget(btn_search)
        root.addLayout(title_row)

        # 스플리터: 왼쪽(필터+테이블+하단바) | 오른쪽(차트)
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setHandleWidth(6)
        splitter.setChildrenCollapsible(False)
        splitter.setStyleSheet(
            "QSplitter::handle:horizontal {"
            "  background:#CBD5E1; border-radius:3px; margin:4px 0; }"
            "QSplitter::handle:horizontal:hover {"
            "  background:#3B82F6; }")
        left = QWidget()
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(4)

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
        for key, label in CURVE_HEADERS:
            self._filter_col_cb.addItem(label, key)
        filter_row.addWidget(self._filter_col_cb)
        btn_clr = QToolButton()
        btn_clr.setText("✕"); btn_clr.setToolTip("필터 초기화"); btn_clr.setFixedSize(22, 22)
        btn_clr.clicked.connect(self._filter_edit.clear)
        filter_row.addWidget(btn_clr)
        left_layout.addLayout(filter_row)

        # ── 테이블 + 프록시 ───────────────────────────────────────────
        self.model = EsgTableModel([], CURVE_HEADERS)
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
        left_layout.addWidget(self.table, stretch=1)

        # ── 하단 통합 바 ───────────────────────────────────────────────
        self.pager = PaginationWidget()
        self.pager.page_changed.connect(self._load)

        left_btn_w = QWidget()
        left_btn_layout = QHBoxLayout(left_btn_w)
        left_btn_layout.setContentsMargins(0, 0, 0, 0); left_btn_layout.setSpacing(4)
        for lbl in ("➕ 추가", "✏️ 수정", "🗑️ 삭제", "💾 저장"):
            b = QPushButton(lbl); b.setFixedWidth(72); b.setEnabled(False)
            left_btn_layout.addWidget(b)
            self._register_responsive_btn(b)
        left_btn_layout.addStretch()
        left_btn_w.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        right_btn_w = QWidget()
        right_btn_layout = QHBoxLayout(right_btn_w)
        right_btn_layout.setContentsMargins(0, 0, 0, 0); right_btn_layout.setSpacing(4)
        right_btn_layout.addStretch()
        b_imp = QPushButton("📤 Import"); b_imp.setFixedWidth(80); b_imp.setEnabled(False)
        right_btn_layout.addWidget(b_imp)
        self._register_responsive_btn(b_imp)
        b_xl = QPushButton("📥 Excel"); b_xl.setFixedWidth(80); b_xl.clicked.connect(self._on_excel)
        right_btn_layout.addWidget(b_xl)
        self._register_responsive_btn(b_xl)
        right_btn_w.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        bottom_bar = QHBoxLayout()
        bottom_bar.setContentsMargins(0, 2, 0, 2); bottom_bar.setSpacing(0)
        bottom_bar.addWidget(left_btn_w, stretch=1)
        bottom_bar.addWidget(self.pager, stretch=0)
        bottom_bar.addWidget(right_btn_w, stretch=1)
        left_layout.addLayout(bottom_bar)

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
            for i, (key, _) in enumerate(CURVE_HEADERS):
                if key == col_data:
                    self.proxy.setFilterKeyColumn(i)
                    break

    def _on_search_click(self) -> None:
        self._search_mode = True
        self.pager.setVisible(False)
        self._load(1)

    def _load(self, page: int = 1) -> None:
        rows, total = IrCurveBaseService.get_ir_curve_list(
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
        # series_map: {ir_curve_id: {mat_cd: spot_rate}}
        series_map: dict[str, dict] = {}
        for r in rows:
            mat = r.get("mat_cd", "")
            seen_mat[mat] = None
            key = r.get("ir_curve_id", "")
            if key not in series_map:
                series_map[key] = {}
            series_map[key][mat] = r.get("spot_rate") or 0
        x_labels = list(seen_mat)
        # 각 시리즈를 x_labels 순서에 맞게 정렬 (없는 만기는 0 처리)
        y_series = {k: [v.get(m, 0) for m in x_labels] for k, v in series_map.items()}
        self.chart.plot_line(
            x_labels, y_series,
            title="금리 커브 (현물금리)", x_label="만기", y_label="금리")

    def _on_excel(self) -> None:
        export_to_excel(self.model.all_rows(),
                        [h[1] for h in CURVE_HEADERS], [h[0] for h in CURVE_HEADERS],
                        "금리커브")
