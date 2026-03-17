"""
재사용 가능한 QAbstractTableModel
jqGrid → QTableView + EsgTableModel 대응
"""
from PyQt6.QtCore import Qt, QAbstractTableModel, QModelIndex, pyqtSignal
from PyQt6.QtWidgets import QStyledItemDelegate, QComboBox


class EsgTableModel(QAbstractTableModel):
    """
    사용법:
        model = EsgTableModel(rows, headers)
        table_view.setModel(model)

    rows    : list[dict]  (서비스 레이어 반환값)
    headers : list[tuple] (column_key, header_label)
    """

    def __init__(self, rows: list[dict], headers: list[tuple], parent=None):
        super().__init__(parent)
        self._headers   = headers          # [(key, label), ...]
        self._rows      = rows
        self._col_aligns: dict[int, Qt.AlignmentFlag] = {}  # 컬럼별 정렬 오버라이드

    # ── QAbstractTableModel 필수 메서드 ─────────────────────────
    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self._rows)

    def columnCount(self, parent=QModelIndex()) -> int:
        return len(self._headers)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        row  = self._rows[index.row()]
        key  = self._headers[index.column()][0]
        val  = row.get(key)

        if role == Qt.ItemDataRole.DisplayRole:
            if val is None:
                return ""
            if isinstance(val, float):
                return f"{val:.6f}"
            return str(val)

        if role == Qt.ItemDataRole.TextAlignmentRole:
            col = index.column()
            if col in self._col_aligns:
                return self._col_aligns[col] | Qt.AlignmentFlag.AlignVCenter
            if isinstance(val, (int, float)):
                return Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
            return Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter

        # 숫자 컬럼 정렬을 위해 원본 값 반환 (프록시 모델이 사용)
        if role == Qt.ItemDataRole.UserRole:
            return val

        return None

    def headerData(self, section: int, orientation: Qt.Orientation,
                   role: int = Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Horizontal:
            if role == Qt.ItemDataRole.DisplayRole:
                return self._headers[section][1]
            if role == Qt.ItemDataRole.TextAlignmentRole:
                return Qt.AlignmentFlag.AlignCenter  # 헤더 항상 가운데
        if role == Qt.ItemDataRole.DisplayRole:
            return str(section + 1)
        return None

    # ── 컬럼 정렬 오버라이드 ─────────────────────────────────────
    def setColumnAlign(self, col: int, align: Qt.AlignmentFlag) -> None:
        self._col_aligns[col] = align
        self.dataChanged.emit(
            self.index(0, col),
            self.index(self.rowCount() - 1, col),
            [Qt.ItemDataRole.TextAlignmentRole])

    # ── 데이터 교체 ──────────────────────────────────────────────
    def load(self, rows: list[dict], headers: list[tuple] | None = None) -> None:
        self.beginResetModel()
        self._rows = rows
        if headers is not None:
            self._headers = headers
        self.endResetModel()

    def get_row(self, row_index: int) -> dict:
        return self._rows[row_index] if 0 <= row_index < len(self._rows) else {}

    def all_rows(self) -> list[dict]:
        return list(self._rows)


# ─── 인라인 편집 + 배치 저장 지원 모델 ──────────────────────────────────
class EsgEditableTableModel(EsgTableModel):
    """
    EsgTableModel 확장 — 인라인 편집 + 배치 저장 지원.

    행 상태:
        'new'      — 추가/복제됨 (초록), DB 미반영, 전체 컬럼 편집 가능
        'modified' — 인라인 수정됨 (주황), DB 미반영
        'deleted'  — 삭제 예정 (빨강), 저장 시 DB DELETE
        없음       — 변경 없음

    배치 저장:
        get_pending() → {'insert': [...], 'update': [...], 'delete': [...]}
        → BaseCrudView._on_save_all() 에서 일괄 DB 반영
    """

    _STATE_COLORS = {
        'new':      '#DCFCE7',   # 연한 초록
        'modified': '#FED7AA',   # 연한 주황
    }

    def __init__(self, rows: list[dict], headers: list[tuple],
                 editable_keys: set, parent=None):
        super().__init__(rows, headers, parent)
        self._editable = editable_keys
        self._row_states: dict[int, str]   = {}   # {row_idx: 'new'|'modified'}
        self._row_originals: dict[int, dict] = {} # 'modified' 행 원본 (PK 변경 감지용)
        self._pending_deletes: list[dict]  = []   # 삭제 예정 행 (그리드에서 즉시 제거됨)
        self._extra_deletions: list[dict]  = []   # PK 변경으로 인한 추가 삭제 목록

    # ── load: 상태 초기화 ───────────────────────────────────────────
    def load(self, rows: list[dict], headers: list[tuple] | None = None) -> None:
        self.beginResetModel()
        self._rows = rows
        if headers is not None:
            self._headers = headers
        self._row_states.clear()
        self._row_originals.clear()
        self._pending_deletes.clear()
        self._extra_deletions.clear()
        self.endResetModel()

    # ── flags: 모든 컬럼 편집 가능 (배치 저장 방식) ─────────────────
    def flags(self, index: QModelIndex):
        base = super().flags(index)
        if not index.isValid():
            return base
        return base | Qt.ItemFlag.ItemIsEditable

    # ── data ────────────────────────────────────────────────────────
    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        row_idx = index.row()
        key = self._headers[index.column()][0]
        state = self._row_states.get(row_idx, '')

        if role == Qt.ItemDataRole.EditRole:
            val = self._rows[row_idx].get(key)
            return "" if val is None else val

        if role == Qt.ItemDataRole.BackgroundRole:
            from PyQt6.QtGui import QColor
            if state in self._STATE_COLORS:
                return QColor(self._STATE_COLORS[state])
            if key in self._editable:
                return QColor("#FEFCE8")   # 편집 가능 셀 — 연한 노란
            return None

        if role == Qt.ItemDataRole.ToolTipRole:
            if state == 'new':      return "신규 행 — 💾 저장 버튼으로 DB에 반영"
            if state == 'modified': return "수정됨 — 💾 저장 버튼으로 DB에 반영"
            if key in self._editable:
                return "더블클릭하여 편집"
            return None

        return super().data(index, role)

    # ── setData: 상태 표시만 (DB 저장 없음) ─────────────────────────
    def setData(self, index: QModelIndex, value,
                role: int = Qt.ItemDataRole.EditRole) -> bool:
        if role != Qt.ItemDataRole.EditRole or not index.isValid():
            return False
        row_idx = index.row()
        row = self._rows[row_idx]
        key = self._headers[index.column()][0]
        # 원본 보존 (처음 수정 시 — 'new' 행은 원본이 없으므로 제외)
        if self._row_states.get(row_idx, '') not in ('new', 'modified'):
            self._row_originals[row_idx] = dict(row)
            self._row_states[row_idx] = 'modified'
        row[key] = value
        self.dataChanged.emit(index, index, [role])
        return True

    # ── 신규 행 삽입 ────────────────────────────────────────────────
    def insert_new_row(self, data: dict, after_row: int = -1) -> int:
        """새 행을 삽입하고 state='new'로 표시. 삽입된 source 인덱스 반환."""
        pos = len(self._rows) if after_row < 0 else after_row + 1
        self.beginInsertRows(QModelIndex(), pos, pos)
        self._rows.insert(pos, dict(data))
        # 기존 상태 인덱스를 pos 이상이면 +1 이동
        self._row_states    = {(i+1 if i >= pos else i): s
                                for i, s in self._row_states.items()}
        self._row_originals = {(i+1 if i >= pos else i): d
                                for i, d in self._row_originals.items()}
        self._row_states[pos] = 'new'
        self.endInsertRows()
        return pos

    # ── 삭제 — 그리드에서 즉시 제거 ────────────────────────────────
    def mark_deleted(self, row_index: int) -> None:
        """'new' 행은 단순 제거. 기존 행은 pending_deletes에 저장 후 즉시 제거."""
        if self._row_states.get(row_index) != 'new':
            # 원본 데이터를 삭제 대상으로 보존
            original = self._row_originals.get(row_index) or self._rows[row_index]
            self._pending_deletes.append(dict(original))
        self._remove_row(row_index)

    # ── 행 데이터 전체 교체 (수정 다이얼로그용) ─────────────────────
    def update_row_data(self, row_index: int, data: dict,
                        force_new: bool = False) -> None:
        """행 데이터를 교체하고 상태를 표시."""
        current = self._row_states.get(row_index, '')
        if force_new:
            new_state = 'new'
        elif current == 'new':
            new_state = 'new'
        else:
            self._row_originals.setdefault(row_index, dict(self._rows[row_index]))
            new_state = 'modified'
        self._rows[row_index] = dict(data)
        self._row_states[row_index] = new_state
        self._refresh_row(row_index)

    # ── PK 변경 시 원본 삭제 등록 ──────────────────────────────────
    def add_extra_deletion(self, row: dict) -> None:
        self._extra_deletions.append(dict(row))

    def get_row_original(self, row_index: int) -> dict:
        """'modified' 행의 원본 데이터 반환. 없으면 빈 dict."""
        return self._row_originals.get(row_index, {})

    # ── 배치 저장 데이터 반환 ───────────────────────────────────────
    def get_pending(self) -> dict:
        """
        {'insert': [...],
         'update': [{'data': ..., 'original': ...}, ...],
         'delete': [...]} 반환.
        update 항목의 'original'은 PK 변경 감지에 사용.
        """
        insert = [self._rows[i]
                  for i, s in self._row_states.items() if s == 'new']
        update = [{'data': self._rows[i],
                   'original': self._row_originals.get(i, {})}
                  for i, s in self._row_states.items() if s == 'modified']
        delete = list(self._pending_deletes) + list(self._extra_deletions)
        return {'insert': insert, 'update': update, 'delete': delete}

    def has_pending(self) -> bool:
        return bool(self._row_states or self._pending_deletes or self._extra_deletions)

    def get_row_state(self, row_index: int) -> str:
        return self._row_states.get(row_index, '')

    # ── 내부 헬퍼 ───────────────────────────────────────────────────
    def _remove_row(self, row_index: int) -> None:
        self.beginRemoveRows(QModelIndex(), row_index, row_index)
        self._rows.pop(row_index)
        self._row_states.pop(row_index, None)
        self._row_originals.pop(row_index, None)
        # 제거된 인덱스 이상 → -1 이동
        self._row_states    = {(i-1 if i > row_index else i): s
                                for i, s in self._row_states.items()}
        self._row_originals = {(i-1 if i > row_index else i): d
                                for i, d in self._row_originals.items()}
        self.endRemoveRows()

    def _refresh_row(self, row_index: int) -> None:
        self.dataChanged.emit(
            self.index(row_index, 0),
            self.index(row_index, self.columnCount() - 1),
            [Qt.ItemDataRole.BackgroundRole, Qt.ItemDataRole.ToolTipRole])


# ─── 콤보박스 인라인 에디터 ─────────────────────────────────────────
class ComboDelegate(QStyledItemDelegate):
    """지정 컬럼에 QComboBox 인라인 에디터를 제공하는 델리게이트."""

    def __init__(self, options: list, parent=None):
        super().__init__(parent)
        self._options = [str(o) for o in options]

    def createEditor(self, parent, option, index):
        cb = QComboBox(parent)
        cb.addItems(self._options)
        return cb

    def setEditorData(self, editor: QComboBox, index: QModelIndex) -> None:
        val = str(index.data(Qt.ItemDataRole.DisplayRole) or "")
        idx = editor.findText(val)
        if idx >= 0:
            editor.setCurrentIndex(idx)

    def setModelData(self, editor: QComboBox, model, index: QModelIndex) -> None:
        model.setData(index, editor.currentText(), Qt.ItemDataRole.EditRole)

    def updateEditorGeometry(self, editor, option, index) -> None:
        editor.setGeometry(option.rect)
