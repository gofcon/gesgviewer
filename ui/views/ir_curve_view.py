"""
금리 커브 + 할인율 화면 (2-패널)
JSP: IrCurveList.jsp
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                              QLabel, QPushButton, QSplitter, QTableView, QAbstractItemView,
                              QLineEdit, QComboBox, QToolButton, QSizePolicy)
from PyQt6.QtCore import Qt, QSortFilterProxyModel
from ui.widgets.base_table_model import EsgTableModel
from ui.widgets.pagination_widget import PaginationWidget
from ui.widgets.chart_widget import ChartWidget
from services.ir_curve_service import IrCurveService
from utils.export_utils import export_to_excel
from db.models.auth import AppUser

CURVE_HEADERS = [
    ("base_yymm","기준년월"),("appl_biz_dv","적용업무"),("ir_curve_id","커브ID"),
    ("mat_cd","만기"),("spot_rate","현물금리"),("dcnt_rate","할인율"),
]


class IrCurveView(QWidget):
    def __init__(self, user: AppUser, parent=None):
        super().__init__(parent)
        self.user = user
        self._build_ui()
        self._load(1)

    def _get_toolbar_yymm(self) -> str:
        win = self.window()
        return win.get_base_yymm() if hasattr(win, "get_base_yymm") else ""

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
        btn_search.clicked.connect(lambda: self._load(1))
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
        left_btn_layout.addStretch()
        left_btn_w.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        right_btn_w = QWidget()
        right_btn_layout = QHBoxLayout(right_btn_w)
        right_btn_layout.setContentsMargins(0, 0, 0, 0); right_btn_layout.setSpacing(4)
        right_btn_layout.addStretch()
        b_imp = QPushButton("📤 Import"); b_imp.setFixedWidth(80); b_imp.setEnabled(False)
        right_btn_layout.addWidget(b_imp)
        b_xl = QPushButton("📥 Excel"); b_xl.setFixedWidth(80); b_xl.clicked.connect(self._on_excel)
        right_btn_layout.addWidget(b_xl)
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

    def _load(self, page: int = 1) -> None:
        rows, total = IrCurveService.get_ir_curve_list(
            base_yymm=self._get_toolbar_yymm(),
            page=page)
        self.model.load(rows)
        self.pager.set_total(total)
        self._update_chart(rows)

    def _update_chart(self, rows: list[dict]) -> None:
        if not rows:
            self.chart.clear(); return
        from collections import defaultdict
        mat_set: list[str] = []
        series: dict[str, list] = defaultdict(list)
        for r in rows:
            mat = r.get("mat_cd","")
            if mat not in mat_set:
                mat_set.append(mat)
        for r in rows:
            series[r.get("ir_curve_id","")].append(r.get("spot_rate") or 0)
        self.chart.plot_line(mat_set, dict(series), title="금리 커브 (현물금리)", x_label="만기", y_label="금리")

    def _on_excel(self) -> None:
        export_to_excel(self.model.all_rows(),
                        [h[1] for h in CURVE_HEADERS], [h[0] for h in CURVE_HEADERS],
                        "금리커브")
