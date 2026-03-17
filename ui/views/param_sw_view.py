"""
Smith-Wilson 사용자 파라미터 화면
JSP: SwUsrList.jsp — jqGrid + CRUD
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy,
                              QFormLayout, QLabel, QComboBox, QPushButton,
                              QDialog, QDialogButtonBox, QMessageBox, QDoubleSpinBox,
                              QLineEdit, QSpinBox, QTableView, QAbstractItemView,
                              QToolButton)
from PyQt6.QtCore import Qt, QSortFilterProxyModel
from ui.widgets.base_table_model import EsgTableModel
from ui.widgets.pagination_widget import PaginationWidget
from services.param_sw_service import ParamSwService
from utils.export_utils import export_to_excel
from db.models.auth import AppUser

HEADERS = [
    ("appl_st_yymm","적용시작년월"),("appl_ed_yymm","적용종료년월"),
    ("appl_biz_dv","적용업무"), ("ir_curve_id","커브ID"),
    ("ir_curve_sce_no","시나리오번호"), ("ir_curve_sce_nm","시나리오명"),
    ("cur_cd","통화"), ("freq","이자지급횟수"), ("llp","최종유동성만기"),
    ("ltfr","장기선도금리"), ("ltfr_cp","수렴연도"), ("liq_prem","유동성프리미엄"),
    ("sw_alpha_ytm","SW_ALPHA"), ("sto_sce_gen_yn","확률시나리오생성"),
    ("last_modified_by","최종수정자"), ("last_update_date","최종수정일"),
]


class ParamSwView(QWidget):
    def __init__(self, user: AppUser, parent=None):
        super().__init__(parent)
        self.user = user
        self._build_ui()
        self._load(1)

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(12, 8, 12, 8)
        root.setSpacing(8)

        # 제목 행 (오른쪽 끝 = 조회 버튼)
        title_row = QHBoxLayout()
        title_row.setContentsMargins(0, 0, 0, 0)
        title = QLabel("<b>Smith-Wilson 사용자 파라미터</b>")
        title.setStyleSheet("font-size:14px; padding:4px 0;")
        btn_search = QPushButton("🔍 조회")
        btn_search.setFixedWidth(80)
        btn_search.clicked.connect(lambda: self._load(1))
        title_row.addWidget(title)
        title_row.addStretch()
        title_row.addWidget(btn_search)
        root.addLayout(title_row)

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
        root.addLayout(filter_row)

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
        root.addWidget(self.table, stretch=1)

        # 하단 통합 바 (추가/수정/삭제 활성, 저장 비활성)
        self.pager = PaginationWidget()
        self.pager.page_changed.connect(self._load)

        left_btn_w = QWidget()
        left_btn_layout = QHBoxLayout(left_btn_w)
        left_btn_layout.setContentsMargins(0, 0, 0, 0)
        left_btn_layout.setSpacing(4)
        btn_add  = QPushButton("➕ 추가"); btn_add.setFixedWidth(72);  btn_add.clicked.connect(self._on_add)
        btn_edit = QPushButton("✏️ 수정"); btn_edit.setFixedWidth(72); btn_edit.clicked.connect(self._on_edit)
        btn_del  = QPushButton("🗑️ 삭제"); btn_del.setFixedWidth(72);  btn_del.clicked.connect(self._on_delete)
        btn_save = QPushButton("💾 저장"); btn_save.setFixedWidth(72);  btn_save.setEnabled(False)
        for btn in (btn_add, btn_edit, btn_del, btn_save):
            left_btn_layout.addWidget(btn)
        left_btn_layout.addStretch()
        left_btn_w.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        right_btn_w = QWidget()
        right_btn_layout = QHBoxLayout(right_btn_w)
        right_btn_layout.setContentsMargins(0, 0, 0, 0)
        right_btn_layout.setSpacing(4)
        right_btn_layout.addStretch()
        btn_import = QPushButton("📤 Import"); btn_import.setFixedWidth(80); btn_import.setEnabled(False)
        right_btn_layout.addWidget(btn_import)
        btn_excel = QPushButton("📥 Excel"); btn_excel.setFixedWidth(80); btn_excel.clicked.connect(self._on_excel)
        right_btn_layout.addWidget(btn_excel)
        right_btn_w.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        bottom_bar = QHBoxLayout()
        bottom_bar.setContentsMargins(0, 2, 0, 2)
        bottom_bar.setSpacing(0)
        bottom_bar.addWidget(left_btn_w,  stretch=1)
        bottom_bar.addWidget(self.pager,  stretch=0)
        bottom_bar.addWidget(right_btn_w, stretch=1)
        root.addLayout(bottom_bar)

    def _get_toolbar_yymm(self) -> str:
        win = self.window()
        return win.get_base_yymm() if hasattr(win, "get_base_yymm") else ""

    def _load(self, page: int = 1) -> None:
        rows, total = ParamSwService.get_sw_usr_list(
            appl_st_yymm=self._get_toolbar_yymm(),
            page=page)
        self.model.load(rows)
        self.pager.set_total(total)

    def _on_filter_col_changed(self, idx: int) -> None:
        col_data = self._filter_col_cb.itemData(idx)
        if col_data == -1:
            self.proxy.setFilterKeyColumn(-1)
        else:
            for i, (key, _) in enumerate(HEADERS):
                if key == col_data:
                    self.proxy.setFilterKeyColumn(i)
                    break

    def _on_add(self) -> None:
        dlg = SwUsrEditDialog(self)
        if dlg.exec():
            ParamSwService.save_sw_usr(dlg.get_data())
            self._load(1)

    def _on_edit(self) -> None:
        proxy_idx = self.table.currentIndex()
        if not proxy_idx.isValid():
            QMessageBox.information(self, "수정", "수정할 행을 선택하세요.")
            return
        src_row = self.proxy.mapToSource(proxy_idx).row()
        row = self.model.get_row(src_row)
        dlg = SwUsrEditDialog(self, row)
        if dlg.exec():
            ParamSwService.save_sw_usr(dlg.get_data())
            self._load(1)

    def _on_delete(self) -> None:
        proxy_idx = self.table.currentIndex()
        if not proxy_idx.isValid():
            QMessageBox.information(self, "삭제", "삭제할 행을 선택하세요.")
            return
        src_row = self.proxy.mapToSource(proxy_idx).row()
        row = self.model.get_row(src_row)
        reply = QMessageBox.question(self, "삭제 확인", "선택한 행을 삭제하시겠습니까?")
        if reply == QMessageBox.StandardButton.Yes:
            ParamSwService.delete_sw_usr(
                row["appl_st_yymm"], row["appl_biz_dv"],
                row["ir_curve_id"], row["ir_curve_sce_no"])
            self._load(1)

    def _on_excel(self) -> None:
        export_to_excel(self.model.all_rows(),
                        [h[1] for h in HEADERS], [h[0] for h in HEADERS],
                        "SW_사용자_파라미터")


class SwUsrEditDialog(QDialog):
    def __init__(self, parent=None, data: dict | None = None):
        super().__init__(parent)
        self._data = data or {}
        self.setWindowTitle("SW 파라미터 편집")
        self.setMinimumWidth(420)
        self._build()

    def _build(self) -> None:
        layout = QVBoxLayout(self)
        form = QFormLayout()

        def le(key, ph=""): e = QLineEdit(str(self._data.get(key, ""))); e.setPlaceholderText(ph); return e
        def sb(key, mn=0, mx=9999): w = QSpinBox(); w.setRange(mn,mx); w.setValue(int(self._data.get(key,0) or 0)); return w
        def dsb(key, dec=6): w = QDoubleSpinBox(); w.setDecimals(dec); w.setRange(-99,99); w.setValue(float(self._data.get(key,0) or 0)); return w

        self.f_st_ym   = le("appl_st_yymm", "YYYYMM")
        self.f_ed_ym   = le("appl_ed_yymm", "YYYYMM")
        self.f_biz_dv  = QComboBox(); self.f_biz_dv.addItems(["KICS","IFRS","IBIZ","SAAS"])
        if self._data.get("appl_biz_dv"):
            self.f_biz_dv.setCurrentText(self._data["appl_biz_dv"])
        self.f_curve   = le("ir_curve_id")
        self.f_sce_no  = sb("ir_curve_sce_no", 1, 9999)
        self.f_sce_nm  = le("ir_curve_sce_nm")
        self.f_cur_cd  = le("cur_cd", "KRW")
        self.f_freq    = sb("freq", 1, 12)
        self.f_llp     = sb("llp", 1, 100)
        self.f_ltfr    = dsb("ltfr")
        self.f_ltfr_cp = sb("ltfr_cp", 1, 200)
        self.f_liq_prem= dsb("liq_prem")
        self.f_sw_alpha= dsb("sw_alpha_ytm")

        form.addRow("적용시작년월*", self.f_st_ym)
        form.addRow("적용종료년월*", self.f_ed_ym)
        form.addRow("적용업무구분*", self.f_biz_dv)
        form.addRow("금리커브ID*",   self.f_curve)
        form.addRow("시나리오번호*", self.f_sce_no)
        form.addRow("시나리오명",    self.f_sce_nm)
        form.addRow("통화코드",      self.f_cur_cd)
        form.addRow("이자지급횟수",  self.f_freq)
        form.addRow("최종유동성만기",self.f_llp)
        form.addRow("장기선도금리",  self.f_ltfr)
        form.addRow("수렴연도",      self.f_ltfr_cp)
        form.addRow("유동성프리미엄",self.f_liq_prem)
        form.addRow("SW_ALPHA",      self.f_sw_alpha)
        layout.addLayout(form)

        btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok |
                                QDialogButtonBox.StandardButton.Cancel)
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)
        layout.addWidget(btns)

    def get_data(self) -> dict:
        return {
            "appl_st_yymm":    self.f_st_ym.text().strip(),
            "appl_ed_yymm":    self.f_ed_ym.text().strip(),
            "appl_biz_dv":     self.f_biz_dv.currentText(),
            "ir_curve_id":     self.f_curve.text().strip(),
            "ir_curve_sce_no": self.f_sce_no.value(),
            "ir_curve_sce_nm": self.f_sce_nm.text().strip(),
            "cur_cd":          self.f_cur_cd.text().strip(),
            "freq":            self.f_freq.value(),
            "llp":             self.f_llp.value(),
            "ltfr":            self.f_ltfr.value(),
            "ltfr_cp":         self.f_ltfr_cp.value(),
            "liq_prem":        self.f_liq_prem.value(),
            "sw_alpha_ytm":    self.f_sw_alpha.value(),
        }
