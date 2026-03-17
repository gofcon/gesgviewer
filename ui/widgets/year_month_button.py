"""
기준년월 선택 버튼 위젯

클릭 시 팝업:  연도(SpinBox) + 월(버튼 그리드 4×3) → 확인
QLineEdit 호환: text() / setText(YYYYMM) 인터페이스 제공
"""
from datetime import date

from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QGridLayout,
                              QToolButton, QSpinBox, QLabel, QPushButton,
                              QDialog, QFrame)
from PyQt6.QtCore import Qt, QPoint, pyqtSignal


class _YearMonthPopup(QDialog):
    """내부 팝업: 연도 스핀박스 + 월 버튼 그리드"""
    confirmed = pyqtSignal(str)   # YYYYMM

    def __init__(self, yymm: str, parent=None):
        super().__init__(parent, Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint)
        year  = int(yymm[:4]) if len(yymm) >= 4 else date.today().year
        month = int(yymm[4:6]) if len(yymm) >= 6 else date.today().month
        self._month = month
        self._build_ui(year, month)
        self.adjustSize()

    def _build_ui(self, year: int, month: int) -> None:
        self.setStyleSheet(
            "QDialog  { background:#FFFFFF; border:1px solid #CBD5E1; border-radius:8px; }"
            "QSpinBox  { border:1px solid #CBD5E1; border-radius:4px;"
            "            padding:3px 6px; font-size:13px; }"
            "QSpinBox::up-button   { width:16px; }"
            "QSpinBox::down-button { width:16px; }"
        )
        root = QVBoxLayout(self)
        root.setContentsMargins(12, 10, 12, 10)
        root.setSpacing(8)

        # ── 연도 행 ──────────────────────────────────────────────
        year_row = QHBoxLayout()
        year_row.setSpacing(6)
        lbl = QLabel("연도")
        lbl.setStyleSheet("font-size:12px; font-weight:bold; color:#374151;")
        self._spin = QSpinBox()
        self._spin.setRange(2000, 2099)
        self._spin.setValue(year)
        self._spin.setFixedWidth(90)
        self._spin.setAlignment(Qt.AlignmentFlag.AlignCenter)
        year_row.addWidget(lbl)
        year_row.addStretch()
        year_row.addWidget(self._spin)
        root.addLayout(year_row)

        # ── 구분선 ────────────────────────────────────────────────
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("QFrame { color:#E5E7EB; }")
        root.addWidget(sep)

        # ── 월 버튼 그리드 (4열 × 3행) ─────────────────────────
        grid = QGridLayout()
        grid.setSpacing(4)
        self._month_btns: list[QPushButton] = []
        for i in range(12):
            m = i + 1
            btn = QPushButton(f"{m:02d}월")
            btn.setCheckable(True)
            btn.setChecked(m == month)
            btn.setFixedSize(54, 30)
            btn.setStyleSheet(
                "QPushButton {"
                "  border:1px solid #E2E8F0; border-radius:4px;"
                "  font-size:12px; background:#F8FAFC;"
                "}"
                "QPushButton:hover   { background:#EFF6FF; }"
                "QPushButton:checked {"
                "  background:#1E40AF; color:white; border:1px solid #1E40AF;"
                "}"
            )
            btn.clicked.connect(lambda _, mm=m: self._on_month_click(mm))
            self._month_btns.append(btn)
            grid.addWidget(btn, i // 4, i % 4)
        root.addLayout(grid)

        # ── 확인 버튼 ────────────────────────────────────────────
        btn_ok = QPushButton("확인")
        btn_ok.setFixedHeight(32)
        btn_ok.setStyleSheet(
            "QPushButton {"
            "  background:#1E40AF; color:white;"
            "  border-radius:4px; font-size:13px; font-weight:bold;"
            "}"
            "QPushButton:hover { background:#1D4ED8; }"
        )
        btn_ok.clicked.connect(self._on_ok)
        root.addWidget(btn_ok)

    def _on_month_click(self, month: int) -> None:
        self._month = month
        for i, btn in enumerate(self._month_btns):
            btn.setChecked(i + 1 == month)

    def _on_ok(self) -> None:
        yymm = f"{self._spin.value():04d}{self._month:02d}"
        self.confirmed.emit(yymm)
        self.accept()


class YearMonthButton(QWidget):
    """
    기준년월 선택 버튼 위젯.

    • QLineEdit 호환 인터페이스: text() / setText(YYYYMM)
    • 클릭 시 연도·월 팝업 표시
    • 선택 완료 시 yearMonthChanged(YYYYMM) 시그널 발생
    """
    yearMonthChanged = pyqtSignal(str)   # YYYYMM 문자열

    def __init__(self, yymm: str = "", parent=None):
        super().__init__(parent)
        self._yymm = (
            yymm if (len(yymm) == 6 and yymm.isdigit())
            else date.today().strftime("%Y%m")
        )
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self._btn = QToolButton()
        self._btn.setObjectName("btn_yymm_picker")
        self._btn.setToolTip("기준년월 선택 (클릭)")
        self._btn.setFixedWidth(90)
        self._btn.setStyleSheet(
            "QToolButton {"
            "  border:1px solid #CBD5E1; border-radius:4px;"
            "  padding:3px 8px; font-size:12px;"
            "  background:white; color:#1E293B;"
            "}"
            "QToolButton:hover   { background:#EFF6FF; }"
            "QToolButton:pressed { background:#DBEAFE; }"
        )
        self._refresh_label()
        self._btn.clicked.connect(self._show_popup)
        layout.addWidget(self._btn)

    # ── QLineEdit 호환 인터페이스 ──────────────────────────────
    def text(self) -> str:
        """YYYYMM 반환 (QLineEdit.text() 호환)"""
        return self._yymm

    def setText(self, yymm: str) -> None:
        """YYYYMM 문자열로 값 설정 (QLineEdit.setText() 호환)"""
        if len(yymm) == 6 and yymm.isdigit():
            self._yymm = yymm
            self._refresh_label()

    # ── 내부 ──────────────────────────────────────────────────
    def _refresh_label(self) -> None:
        y, m = self._yymm[:4], self._yymm[4:6]
        self._btn.setText(f"{y}/{m} ▾")

    def _show_popup(self) -> None:
        popup = _YearMonthPopup(self._yymm, self)
        popup.confirmed.connect(self._on_confirmed)
        popup.adjustSize()                        # 팝업 크기 확정
        # 팝업 오른쪽 가장자리를 버튼 오른쪽 가장자리에 맞춤
        btn_br = self._btn.mapToGlobal(QPoint(self._btn.width(), self._btn.height() + 2))
        pos = QPoint(btn_br.x() - popup.width(), btn_br.y())
        popup.move(pos)
        popup.exec()

    def _on_confirmed(self, yymm: str) -> None:
        self._yymm = yymm
        self._refresh_label()
        self.yearMonthChanged.emit(yymm)
