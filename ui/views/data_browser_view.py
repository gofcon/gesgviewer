"""
데이터 브라우저 — SQLite 테이블 동적 조회 + 무한 스크롤

BaseListView 를 상속하되 페이저 대신 무한 스크롤을 사용한다.

제목행 레이아웃:
  [데이터 브라우저]  [테이블: combo]  |  [총 N건]  [stretch]  [🔍 조회]

조회 흐름:
  1. 테이블 콤보 선택 → 컬럼/헤더 갱신 후 기준년월 없이 첫 배치 자동 로드
  2. 🔍 조회 버튼 클릭 (또는 Enter) → 툴바 기준년월 LIKE 조건 포함 쿼리
  3. 스크롤 하단 80% 도달 → 다음 배치 자동 로드 (동일 조건 유지)
  4. 실시간 필터 텍스트 입력 → 미로드 행 전부 먼저 로드 후 in-memory 필터 적용

기준년월 조건:
  컬럼명에 'YYMM' 이 포함되면 자동 탐지.
  없는 테이블은 조건 없이 전체 조회.
  기준년월 값은 메인 툴바의 _get_toolbar_yymm() 에서 참조.
"""
from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QLabel,
                              QComboBox, QSizePolicy)

from ui.views._base_list_view import BaseListView
from ui.widgets.base_table_model import EsgTableModel
from services.data_browser_service import DataBrowserService
from db.models.auth import AppUser
from config.settings import DEFAULT_PAGE_SIZE


class DataBrowserView(BaseListView):
    """SQLite DB 내 임의 테이블을 동적으로 탐색하는 읽기 전용 뷰 (무한 스크롤)."""

    VIEW_TITLE = "데이터 브라우저"
    HEADERS: list[tuple[str, str]] = []   # 선택된 테이블 컬럼으로 동적 갱신

    # 한 번에 로드할 행 수
    _SCROLL_PAGE_SIZE = 200

    def __init__(self, user: AppUser, parent=None):
        # ① 상태 변수 — super().__init__ → _load_data(1) 이전에 초기화
        self._current_table:  str  = ""
        self._yymm_col:       str  = ""   # 기준년월 컬럼명 (없으면 "")
        self._scroll_page:    int  = 0
        self._scroll_total:   int  = 0
        self._scroll_loading: bool = False

        super().__init__(user, parent)
        # ② 스크롤 연결 (조회 후 모드에서만 동작; 조회 전은 pager 사용)
        self.table_view.verticalScrollBar().valueChanged.connect(
            self._on_scroll)

        # ③ 테이블 목록 로드 → 첫 번째 테이블 자동 선택 → 첫 배치 자동 로드
        self._populate_table_combo()

    # ── 제목행 추가 위젯: 테이블 콤보 + 건수 라벨 ───────────────────
    def _build_title_extra(self) -> list:
        """제목 라벨 오른쪽에 테이블 선택 콤보 + 건수 라벨을 삽입."""
        widgets = []

        sep0 = QLabel("  ")   # 타이틀과 약간의 간격
        widgets.append(sep0)

        lbl_tbl = QLabel("테이블:")
        lbl_tbl.setStyleSheet("font-size: 12px;")
        widgets.append(lbl_tbl)

        self._table_combo = QComboBox()
        self._table_combo.setMinimumWidth(220)
        self._table_combo.setMaximumWidth(360)
        self._table_combo.setStyleSheet("font-size: 12px;")
        self._table_combo.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self._table_combo.currentIndexChanged.connect(self._on_table_selected)
        widgets.append(self._table_combo)

        sep1 = QLabel("  |  ")
        sep1.setStyleSheet("color: #CBD5E1; font-size: 12px;")
        widgets.append(sep1)

        lbl_cnt = QLabel("총")
        lbl_cnt.setStyleSheet("font-size: 12px; color: #64748B;")
        widgets.append(lbl_cnt)

        self._lbl_row_count = QLabel("-")
        self._lbl_row_count.setStyleSheet(
            "font-size: 12px; font-weight: bold; color: #1E293B;")
        widgets.append(self._lbl_row_count)

        lbl_geon = QLabel("건")
        lbl_geon.setStyleSheet("font-size: 12px; color: #64748B;")
        widgets.append(lbl_geon)

        return widgets

    # ── 테이블 콤보 초기화 ─────────────────────────────────────────
    def _populate_table_combo(self) -> None:
        tables = DataBrowserService.get_table_list()
        self._table_combo.blockSignals(True)
        self._table_combo.clear()
        self._table_combo.addItem("— 테이블 선택 —", "")
        for tbl in tables:
            self._table_combo.addItem(tbl, tbl)
        self._table_combo.blockSignals(False)
        if tables:
            self._table_combo.setCurrentIndex(1)   # 첫 번째 테이블 자동 선택

    # ── 테이블 선택 이벤트 ─────────────────────────────────────────
    def _on_table_selected(self, index: int) -> None:
        """테이블 변경 시 컬럼/헤더 갱신 후 기준년월 조건 없이 첫 배치 자동 로드."""
        table_name = self._table_combo.itemData(index) or ""
        if not table_name:
            self._current_table  = ""
            self._yymm_col       = ""
            self._scroll_page    = 0
            self._scroll_total   = 0
            self._scroll_loading = False
            self._search_mode    = False   # 조회 전 상태로 리셋
            self.table_model.load([])
            self._lbl_row_count.setText("-")
            return

        self._current_table  = table_name
        self._yymm_col       = ""
        self._scroll_page    = 0
        self._scroll_total   = 0
        self._scroll_loading = False
        self._search_mode    = False   # 테이블 변경 시 조회 전 상태로 리셋
        self.pager.setVisible(True)    # 조회 전: pagination 표시
        self._lbl_row_count.setText("-")

        # 컬럼 목록 → 기준년월 컬럼 탐지 + 헤더·필터 콤보 갱신
        cols = DataBrowserService.get_columns(table_name)
        self._yymm_col = DataBrowserService.detect_yymm_col(cols)
        self._apply_dynamic_headers([(c, c) for c in cols])
        self._load_data(1)   # 기준년월 조건 없이 첫 배치 자동 로드

    # ── 동적 헤더 갱신 ─────────────────────────────────────────────
    def _apply_dynamic_headers(self, headers: list[tuple[str, str]]) -> None:
        """컬럼 목록이 바뀔 때 HEADERS / EsgTableModel / proxy / 필터 콤보 갱신."""
        self.HEADERS = headers

        self.table_model = EsgTableModel([], headers)
        self.proxy_model.setSourceModel(self.table_model)

        self._filter_col_cb.blockSignals(True)
        self._filter_col_cb.clear()
        self._filter_col_cb.addItem("전체 컬럼", -1)
        for key, label in headers:
            self._filter_col_cb.addItem(label, key)
        self._filter_col_cb.setCurrentIndex(0)
        self._filter_col_cb.blockSignals(False)
        self.proxy_model.setFilterKeyColumn(-1)

        self._apply_column_widths()

    # ── 🔍 조회 버튼 오버라이드 ────────────────────────────────────
    def _on_search_click(self) -> None:
        """테이블이 선택된 경우에만 조회. 툴바 기준년월 LIKE 조건 포함."""
        if not self._current_table:
            return
        self._search_mode = True
        self._update_search_tooltip()
        self.pager.setVisible(False)   # 조회 후: pagination → scroll 전환
        self._load_data(1)

    # ── 첫 번째 배치 로드 ──────────────────────────────────────────
    def _load_data(self, page: int = 1) -> None:
        """조회 모드에 따라 페이지네이션(조회 전) 또는 무한 스크롤 첫 배치(조회 후) 로드."""
        if not self._current_table:
            return

        if not self._search_mode:
            # 조회 전: 기준년월 없음, DEFAULT_PAGE_SIZE, pager 사용
            rows, total = DataBrowserService.get_data(
                self._current_table,
                page=page,
                page_size=DEFAULT_PAGE_SIZE,
                yymm_col=self._yymm_col,
                yymm_like="",
            )
            self.table_model.load(rows)
            self._scroll_page    = 0
            self._scroll_total   = 0
            self._scroll_loading = False
            self.pager.set_total(total)
            self._lbl_row_count.setText(f"{total:,}")
        else:
            # 조회 후: 기준년월 포함, _SCROLL_PAGE_SIZE, 무한 스크롤
            rows, total = DataBrowserService.get_data(
                self._current_table,
                page=1,
                page_size=self._SCROLL_PAGE_SIZE,
                yymm_col=self._yymm_col,
                yymm_like=self._get_toolbar_yymm(),
            )
            self.table_model.load(rows)
            self._scroll_page    = 1
            self._scroll_total   = total
            self._scroll_loading = False
            self._refresh_count_label()

    # ── 무한 스크롤: 하단 도달 감지 ───────────────────────────────
    def _on_scroll(self, value: int) -> None:
        """수직 스크롤바 값 변경 → 조회 후 모드에서 하단 80% 이상이면 다음 배치 로드."""
        if not self._search_mode:      # 조회 전: pagination 사용, 스크롤 무시
            return
        if self._scroll_loading:
            return
        if self.table_model.rowCount() >= self._scroll_total:
            return

        sb = self.table_view.verticalScrollBar()
        if sb.maximum() > 0 and value >= sb.maximum() * 0.8:
            self._load_more()

    # ── 다음 배치를 모델 끝에 추가 ────────────────────────────────
    def _load_more(self) -> None:
        """다음 페이지를 DB에서 가져와 table_model 끝에 append_rows."""
        self._scroll_loading = True
        rows, _ = DataBrowserService.get_data(
            self._current_table,
            page=self._scroll_page + 1,
            page_size=self._SCROLL_PAGE_SIZE,
            yymm_col=self._yymm_col,
            yymm_like=self._get_toolbar_yymm(),
        )
        if rows:
            self.table_model.append_rows(rows)
            self._scroll_page += 1
            self._refresh_count_label()
        self._scroll_loading = False

    # ── 필터 입력 오버라이드: 미로드 행 먼저 전부 로드 ─────────────
    def _on_filter_text_changed(self, text: str) -> None:
        """텍스트 입력 시 미로드 행이 있으면 전부 로드한 뒤 in-memory 필터 적용."""
        if text and self._current_table and \
                self.table_model.rowCount() < self._scroll_total:
            self._load_remaining_for_filter()
        super()._on_filter_text_changed(text)

    def _load_remaining_for_filter(self) -> None:
        """아직 lazy-load 되지 않은 나머지 행을 모두 append_rows 로 추가."""
        already_loaded = self.table_model.rowCount()
        rows = DataBrowserService.get_remaining_data(
            self._current_table,
            offset=already_loaded,
            yymm_col=self._yymm_col,
            yymm_like=self._get_toolbar_yymm(),
        )
        if rows:
            self.table_model.append_rows(rows)
            self._scroll_page = self._scroll_total // self._SCROLL_PAGE_SIZE
            self._refresh_count_label()

    # ── 행 수 라벨 갱신 ───────────────────────────────────────────
    def _refresh_count_label(self) -> None:
        """로드됨 / 전체 또는 전체 건수를 라벨에 표시."""
        loaded = self.table_model.rowCount()
        total  = self._scroll_total
        if loaded < total:
            self._lbl_row_count.setText(f"{loaded:,} / {total:,}")
        else:
            self._lbl_row_count.setText(f"{total:,}")
