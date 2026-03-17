"""
신규 행 추가 전용 입력 다이얼로그
  FormField  — 필드 정의 (dataclass)
  EsgAddDialog — QFormLayout 기반 자동 생성 다이얼로그
"""
from dataclasses import dataclass, field

from PyQt6.QtWidgets import (QDialog, QFormLayout, QVBoxLayout, QHBoxLayout,
                              QPushButton, QLineEdit, QComboBox, QMessageBox,
                              QDoubleSpinBox, QWidget, QLabel, QFrame)
from PyQt6.QtCore import Qt


@dataclass
class FormField:
    key: str
    label: str
    widget: str                              # "text" | "number" | "decimal" | "combo"
    required: bool = True
    options: list = field(default_factory=list)   # combo 항목 (str or (value, label))


class EsgAddDialog(QDialog):
    """신규 행 추가 전용 최소 입력 다이얼로그."""

    def __init__(self, fields: list, parent=None):
        super().__init__(parent)
        self.setWindowTitle("신규 추가")
        self.setMinimumWidth(380)
        self._fields = fields
        self._widgets: dict[str, QWidget] = {}
        self._build_ui()

    # ── UI 구성 ──────────────────────────────────────────────────────
    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(16, 12, 16, 12)
        root.setSpacing(12)

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form.setSpacing(6)

        for f in self._fields:
            w = self._make_widget(f)
            self._widgets[f.key] = w
            label_text = f"{f.label} *" if f.required else f.label
            form.addRow(label_text, w)
        root.addLayout(form)

        btn_row = QHBoxLayout()
        btn_ok = QPushButton("저장")
        btn_cancel = QPushButton("취소")
        btn_ok.setDefault(True)
        btn_ok.setFixedWidth(80)
        btn_cancel.setFixedWidth(80)
        btn_ok.clicked.connect(self._on_ok)
        btn_cancel.clicked.connect(self.reject)
        btn_row.addStretch()
        btn_row.addWidget(btn_ok)
        btn_row.addWidget(btn_cancel)
        root.addLayout(btn_row)

    def _make_widget(self, f: FormField) -> QWidget:
        if f.widget == "combo":
            cb = QComboBox()
            for opt in f.options:
                if isinstance(opt, tuple):
                    cb.addItem(str(opt[1]), opt[0])
                else:
                    cb.addItem(str(opt), opt)
            return cb
        elif f.widget == "decimal":
            sb = QDoubleSpinBox()
            sb.setDecimals(6)
            sb.setRange(-999999.0, 999999.0)
            sb.setSingleStep(0.0001)
            return sb
        elif f.widget == "number":
            sb = QDoubleSpinBox()
            sb.setDecimals(0)
            sb.setRange(-999999, 999999)
            sb.setSingleStep(1)
            return sb
        else:   # "text"
            return QLineEdit()

    # ── 슬롯 ──────────────────────────────────────────────────────────
    def _on_ok(self) -> None:
        data = self.get_data()
        for f in self._fields:
            if f.required:
                v = data.get(f.key)
                if v is None or str(v).strip() == "":
                    QMessageBox.warning(self, "입력 오류",
                                        f"'{f.label}'은(는) 필수 입력입니다.")
                    return
        self.accept()

    # ── 데이터 읽기 ───────────────────────────────────────────────────
    def get_data(self) -> dict:
        result = {}
        for f in self._fields:
            w = self._widgets[f.key]
            if isinstance(w, QComboBox):
                result[f.key] = w.currentData()
            elif isinstance(w, QDoubleSpinBox):
                val = w.value()
                result[f.key] = int(val) if f.widget == "number" else val
            else:
                result[f.key] = w.text().strip()
        return result


# ─── 수정 다이얼로그 (EsgAddDialog 확장) ──────────────────────────────────
class EsgEditDialog(EsgAddDialog):
    """
    기존 행 수정 전용 다이얼로그.
    • initial   : 현재 행 데이터 (초기값으로 채움)
    • readonly_keys : 비활성화할 키 집합 (PK 컬럼 등)
    """

    def __init__(self, fields: list, initial: dict,
                 readonly_keys: set | None = None, parent=None):
        super().__init__(fields, parent)
        self.setWindowTitle("수정")
        self._readonly_keys = readonly_keys or set()
        self._fill_initial(initial)
        self._apply_readonly()

    def _fill_initial(self, initial: dict) -> None:
        """위젯에 현재 행 값 채우기."""
        for key, w in self._widgets.items():
            val = initial.get(key)
            if val is None:
                continue
            if isinstance(w, QComboBox):
                idx = w.findData(val)
                if idx < 0:
                    idx = w.findText(str(val))
                if idx >= 0:
                    w.setCurrentIndex(idx)
            elif isinstance(w, QDoubleSpinBox):
                try:
                    w.setValue(float(val))
                except (ValueError, TypeError):
                    pass
            else:
                w.setText(str(val))

    def _apply_readonly(self) -> None:
        """읽기 전용 키 위젯 비활성화 (PK 컬럼 수정 방지)."""
        for key in self._readonly_keys:
            w = self._widgets.get(key)
            if w is None:
                continue
            w.setEnabled(False)
            if isinstance(w, QLineEdit):
                w.setStyleSheet(
                    "QLineEdit { background:#F1F5F9; color:#64748B; border:1px solid #CBD5E1; }")
            elif isinstance(w, QComboBox):
                w.setStyleSheet(
                    "QComboBox { background:#F1F5F9; color:#64748B; }")
            elif isinstance(w, QDoubleSpinBox):
                w.setStyleSheet(
                    "QDoubleSpinBox { background:#F1F5F9; color:#64748B; }")


# ─── 상세 보기 다이얼로그 (읽기 전용) ─────────────────────────────────────
class EsgRowViewDialog(QDialog):
    """
    선택된 행의 모든 필드를 읽기 전용으로 표시하는 다이얼로그.
    headers : list[(key, label)]  — HEADERS 형식
    """

    def __init__(self, row: dict, headers: list[tuple],
                 title: str = "상세 보기", parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumWidth(420)
        self._build_ui(row, headers)

    def _build_ui(self, row: dict, headers: list[tuple]) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(16, 14, 16, 14)
        root.setSpacing(10)

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form.setSpacing(6)
        form.setHorizontalSpacing(12)

        for key, label in headers:
            val = row.get(key)
            display = str(val) if val is not None else ""
            lbl = QLabel(display)
            lbl.setTextInteractionFlags(
                Qt.TextInteractionFlag.TextSelectableByMouse)
            lbl.setStyleSheet(
                "QLabel { padding:3px 6px; background:#F8FAFC;"
                "         border:1px solid #E2E8F0; border-radius:3px; }")
            lbl.setMinimumWidth(180)
            form.addRow(f"<b>{label}</b>", lbl)

        root.addLayout(form)

        # 구분선
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("color: #E2E8F0;")
        root.addWidget(line)

        btn_row = QHBoxLayout()
        btn_close = QPushButton("닫기")
        btn_close.setFixedWidth(80)
        btn_close.setDefault(True)
        btn_close.clicked.connect(self.accept)
        btn_row.addStretch()
        btn_row.addWidget(btn_close)
        root.addLayout(btn_row)
