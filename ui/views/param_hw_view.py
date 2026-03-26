"""
Hull-White 파라미터 화면 — HW Calc / HW Biz (각각 독립 뷰)
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
                              QLabel, QPushButton, QTableView, QAbstractItemView,
                              QSizePolicy, QLineEdit, QComboBox, QToolButton)
from PyQt6.QtCore import Qt, QSortFilterProxyModel
from ui.views._base_list_view import BaseListView, _ResponsiveButtonMixin
from ui.widgets.base_table_model import EsgTableModel
from ui.widgets.chart_widget import ChartWidget
from ui.widgets.pagination_widget import PaginationWidget
from services.base_data_service import ParamHwService
from utils.export_utils import export_to_excel
from db.models.auth import AppUser
from config.settings import DEFAULT_PAGE_SIZE


class ParamHwCalcView(_ResponsiveButtonMixin, QWidget):
    """HW Calc 파라미터 (테이블 + 차트)"""
    VIEW_TITLE = "HW Calc 파라미터"
    # 차트+그리드 뷰: 전체 너비가 이 값 미만이면 버튼을 이모지 전용으로 전환
    _COMPACT_THRESHOLD = 800

    HEADERS = [
        ("base_yymm",    "기준년월"),
        ("ir_model_id",  "모델ID"),
        ("ir_curve_id",  "커브ID"),
        ("mat_cd",       "만기"),
        ("param_typ_cd", "파라미터유형"),
        ("param_val",    "파라미터값"),
    ]

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

        # 제목 행 (오른쪽 끝 = 조회 버튼) — BaseListView 동일 스타일
        title_row = QHBoxLayout()
        title_row.setContentsMargins(0, 0, 0, 0)
        title = QLabel(f"<b>{self.VIEW_TITLE}</b>")
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

        # 왼쪽 컨테이너: 테이블 + 하단 통합 바 (pagination을 그리드 영역에만 한정)
        left_container = QWidget()
        left_vbox = QVBoxLayout(left_container)
        left_vbox.setContentsMargins(0, 0, 0, 0)
        left_vbox.setSpacing(4)

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
        for key, label in self.HEADERS:
            self._filter_col_cb.addItem(label, key)
        filter_row.addWidget(self._filter_col_cb)
        btn_clr = QToolButton()
        btn_clr.setText("✕"); btn_clr.setToolTip("필터 초기화"); btn_clr.setFixedSize(22, 22)
        btn_clr.clicked.connect(self._filter_edit.clear)
        filter_row.addWidget(btn_clr)
        left_vbox.addLayout(filter_row)

        # ── 테이블 + 프록시 ───────────────────────────────────────────
        self.table_model = EsgTableModel([], self.HEADERS)
        self.proxy = QSortFilterProxyModel()
        self.proxy.setSourceModel(self.table_model)
        self.proxy.setSortRole(Qt.ItemDataRole.UserRole)
        self.proxy.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.proxy.setFilterKeyColumn(-1)
        self._filter_edit.textChanged.connect(self.proxy.setFilterFixedString)
        self._filter_col_cb.currentIndexChanged.connect(self._on_filter_col_changed)

        self.table_view = QTableView()
        self.table_view.setModel(self.proxy)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_view.setAlternatingRowColors(True)
        self.table_view.horizontalHeader().setStretchLastSection(True)
        self.table_view.setSortingEnabled(True)
        self.table_view.horizontalHeader().setSortIndicatorShown(True)
        self.table_view.verticalHeader().setDefaultSectionSize(22)
        self.table_view.verticalHeader().setVisible(False)
        left_vbox.addWidget(self.table_view, stretch=1)

        # 하단 통합 바 — 그리드 영역 안에 배치
        self.pager = PaginationWidget()
        self.pager.page_changed.connect(self._load_data)

        left_w = QWidget()
        left_layout = QHBoxLayout(left_w)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(4)
        for label in ("➕ 추가", "✏️ 수정", "🗑️ 삭제", "💾 저장"):
            btn = QPushButton(label)
            btn.setFixedWidth(72)
            btn.setEnabled(False)
            left_layout.addWidget(btn)
            self._register_responsive_btn(btn)
        left_layout.addStretch()
        left_w.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        right_w = QWidget()
        right_layout = QHBoxLayout(right_w)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(4)
        right_layout.addStretch()
        btn_import = QPushButton("📤 Import")
        btn_import.setFixedWidth(80)
        btn_import.setEnabled(False)
        right_layout.addWidget(btn_import)
        self._register_responsive_btn(btn_import)
        btn_excel = QPushButton("📥 Excel")
        btn_excel.setFixedWidth(80)
        btn_excel.clicked.connect(self._on_excel)
        right_layout.addWidget(btn_excel)
        self._register_responsive_btn(btn_excel)
        right_w.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        bottom_bar = QHBoxLayout()
        bottom_bar.setContentsMargins(0, 2, 0, 2)
        bottom_bar.setSpacing(0)
        bottom_bar.addWidget(left_w,     stretch=1)
        bottom_bar.addWidget(self.pager, stretch=0)
        bottom_bar.addWidget(right_w,    stretch=1)
        left_vbox.addLayout(bottom_bar)

        splitter.addWidget(left_container)
        self.chart = ChartWidget()
        splitter.addWidget(self.chart)
        splitter.setSizes([600, 400])
        root.addWidget(splitter, stretch=1)

        self._load_data(1)

    def _on_filter_col_changed(self, idx: int) -> None:
        col_data = self._filter_col_cb.itemData(idx)
        if col_data == -1:
            self.proxy.setFilterKeyColumn(-1)
        else:
            for i, (key, _) in enumerate(self.HEADERS):
                if key == col_data:
                    self.proxy.setFilterKeyColumn(i)
                    break

    def _on_search_click(self) -> None:
        self._search_mode = True
        self.pager.setVisible(False)
        self._load_data(1)

    def _load_data(self, page: int = 1) -> None:
        base_ym = self._get_toolbar_yymm()
        rows, total = ParamHwService.get_param_hw_calc_list(
            base_yymm=base_ym, page=page, page_size=self._get_page_size())
        self.table_model.load(rows)
        self.pager.set_total(total)
        self._update_chart(base_ym)

    def _update_chart(self, base_ym: str) -> None:
        rows = ParamHwService.get_param_hw_chart_list(base_yymm=base_ym)
        if not rows:
            self.chart.clear()
            return
        # x축: 고유 만기(삽입 순서 유지)
        seen_mat: dict[str, None] = {}
        # series_map: {param_typ_cd: {mat_cd: param_val}}
        series_map: dict[str, dict] = {}
        for r in rows:
            mat = r["mat_cd"]
            seen_mat[mat] = None
            key = r["param_typ_cd"]
            if key not in series_map:
                series_map[key] = {}
            series_map[key][mat] = r["param_val"] or 0
        x_labels = list(seen_mat)
        # 각 시리즈를 x_labels 순서에 맞게 정렬 (없는 만기는 0 처리)
        y_series = {k: [v.get(m, 0) for m in x_labels] for k, v in series_map.items()}
        self.chart.plot_line(
            x_labels, y_series, title="HW 파라미터 (만기별)", x_label="만기")

    def _on_excel(self) -> None:
        rows = self.table_model.all_rows()
        headers = [h[1] for h in self.HEADERS]
        keys    = [h[0] for h in self.HEADERS]
        export_to_excel(rows, headers, keys, "HW_Calc_파라미터")


class ParamHwBizView(BaseListView):
    """HW Biz 적용 파라미터"""
    VIEW_TITLE = "HW Biz 적용 파라미터"
    HEADERS = [
        ("base_yymm",    "기준년월"),
        ("appl_biz_dv",  "적용업무"),
        ("ir_model_id",  "모델ID"),
        ("ir_curve_id",  "커브ID"),
        ("mat_cd",       "만기"),
        ("param_typ_cd", "파라미터유형"),
        ("param_val",    "파라미터값"),
    ]

    def _load_data(self, page: int = 1) -> None:
        rows, total = ParamHwService.get_param_hw_biz_list(
            base_yymm=self._get_toolbar_yymm(), page=page)
        self.table_model.load(rows)
        self.pager.set_total(total)


# 하위 호환 별칭 (기존 import 오류 방지)
ParamHwView = ParamHwCalcView
