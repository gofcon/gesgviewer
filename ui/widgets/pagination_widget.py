"""
페이지 네비게이션 위젯 — 슬라이딩 5개 번호 버튼 방식
jqGrid pager → QPaginationWidget 대응
"""
import math
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import pyqtSignal, Qt
from config.settings import DEFAULT_PAGE_SIZE

_PAGE_BTN_COUNT = 5   # 표시할 번호 버튼 수
_BTN_H          = 22  # 버튼 높이 (px)


class PaginationWidget(QWidget):
    """
    시그널: page_changed(page_no: int)

    사용법:
        pager = PaginationWidget()
        pager.set_total(total_rows, page_size=20)
        pager.page_changed.connect(self.load_page)
    """

    page_changed = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._current = 1
        self._total   = 0
        self._size    = DEFAULT_PAGE_SIZE

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)

        def _nav_btn(text: str) -> QPushButton:
            btn = QPushButton(text)
            btn.setFixedSize(26, _BTN_H)
            btn.setStyleSheet(
                "QPushButton { border:1px solid #CBD5E1; border-radius:3px;"
                "              background:transparent; color:#475569; }"
                "QPushButton:hover:enabled { background:#EFF6FF; }"
                "QPushButton:disabled { color:#CBD5E1; border-color:#E2E8F0; }")
            return btn

        self.btn_first = _nav_btn("◀◀")
        self.btn_prev  = _nav_btn("◀")
        self.btn_next  = _nav_btn("▶")
        self.btn_last  = _nav_btn("▶▶")

        self._page_btns: list[QPushButton] = []
        for _ in range(_PAGE_BTN_COUNT):
            btn = QPushButton()
            btn.setFixedSize(28, _BTN_H)
            self._page_btns.append(btn)

        self.lbl_total = QLabel("총 0 건")
        self.lbl_total.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.lbl_total.setStyleSheet("font-size:12px; color:#475569; margin-left:6px;")

        layout.addWidget(self.btn_first)
        layout.addWidget(self.btn_prev)
        for btn in self._page_btns:
            layout.addWidget(btn)
        layout.addWidget(self.btn_next)
        layout.addWidget(self.btn_last)
        layout.addWidget(self.lbl_total)

        self.btn_first.clicked.connect(lambda: self._go(1))
        self.btn_prev.clicked.connect(lambda: self._go(self._current - 1))
        self.btn_next.clicked.connect(lambda: self._go(self._current + 1))
        self.btn_last.clicked.connect(lambda: self._go(self._total_pages()))

        self._refresh()

    def set_total(self, total: int, page_size: int | None = None) -> None:
        self._total = total
        if page_size:
            self._size = page_size
        self._current = 1
        self._refresh()

    def reset(self) -> None:
        self._current = 1
        self._total   = 0
        self._refresh()

    # ── 내부 ─────────────────────────────────────────────────────
    def _total_pages(self) -> int:
        return max(1, math.ceil(self._total / self._size))

    def _go(self, page: int) -> None:
        page = max(1, min(page, self._total_pages()))
        if page != self._current:
            self._current = page
            self._refresh()
            self.page_changed.emit(self._current)

    def _refresh(self) -> None:
        tp = self._total_pages()

        # 슬라이딩 윈도우 계산 (현재 페이지가 중앙에 오도록)
        half  = _PAGE_BTN_COUNT // 2
        start = max(1, self._current - half)
        end   = min(tp, start + _PAGE_BTN_COUNT - 1)
        start = max(1, end - _PAGE_BTN_COUNT + 1)

        for i, btn in enumerate(self._page_btns):
            page_no = start + i
            if page_no <= tp:
                btn.setText(str(page_no))
                btn.setVisible(True)
                is_cur = (page_no == self._current)
                btn.setEnabled(not is_cur)
                if is_cur:
                    btn.setStyleSheet(
                        "QPushButton { background:#3B82F6; color:white;"
                        "border:none; border-radius:3px; font-weight:bold; }")
                else:
                    btn.setStyleSheet(
                        "QPushButton { background:transparent; color:#334155;"
                        "border:1px solid #CBD5E1; border-radius:3px; }"
                        "QPushButton:hover { background:#EFF6FF; }")
                try:
                    btn.clicked.disconnect()
                except (RuntimeError, TypeError):
                    pass
                btn.clicked.connect(lambda _checked, p=page_no: self._go(p))
            else:
                btn.setVisible(False)

        self.lbl_total.setText(f"총 {self._total:,} 건")
        self.btn_first.setEnabled(self._current > 1)
        self.btn_prev.setEnabled(self._current > 1)
        self.btn_next.setEnabled(self._current < tp)
        self.btn_last.setEnabled(self._current < tp)
