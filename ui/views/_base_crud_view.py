"""
CRUD 기반 뷰 — BaseCrudView
BaseListView 를 상속해 인라인 편집 + 추가/복제/삭제 + 배치 저장 기능 제공.

편집 모델:
    모든 변경(추가/수정/삭제/복제)은 in-memory 모델에만 반영.
    💾 저장 버튼을 눌러야 DB에 일괄 반영.

행 상태 색상:
    초록 — 신규(new): 추가/복제됨, DB 미반영
    주황 — 수정(modified): 인라인 편집됨, DB 미반영
    삭제 — 그리드에서 즉시 제거, pending_deletes 에 보관

서브클래스 정의 필수:
    EDITABLE_KEYS : set[str]        — (참고용) 비PK 컬럼 키
    ADD_FIELDS    : list[FormField] — 추가/수정 다이얼로그 필드
    COMBO_COLS    : dict[str, list] — {col_key: options_list} 인라인 콤보 (선택)
    _save_row(data, is_new) -> bool
    _delete_row(row) -> bool

버튼 레이아웃 (하단 통합 바):
    [➕ 추가] [✏️ 수정] [🗑️ 삭제] [💾 저장]  [◀◀][◀][1][2][3][4][5][▶][▶▶] 총N건  ──  [📤 Import] [📥 Excel] [🔍 조회]
"""
from PyQt6.QtWidgets import (QPushButton, QMessageBox, QMenu,
                              QAbstractItemView)
from PyQt6.QtCore import Qt

from ui.views._base_list_view import BaseListView
from ui.widgets.base_table_model import EsgEditableTableModel, ComboDelegate
from ui.widgets.form_dialog import FormField, EsgAddDialog, EsgEditDialog, EsgRowViewDialog
from utils.import_utils import import_from_excel


class BaseCrudView(BaseListView):

    EDITABLE_KEYS: set = set()
    ADD_FIELDS: list  = []
    COMBO_COLS: dict  = {}        # {col_key: [option1, option2, ...]}

    def __init__(self, user, parent=None):
        super().__init__(user, parent)
        # 인라인 콤보 델리게이트 설정
        for col_key, options in self.COMBO_COLS.items():
            for i, (key, _) in enumerate(self.HEADERS):
                if key == col_key:
                    self.table_view.setItemDelegateForColumn(
                        i, ComboDelegate(options, self.table_view))
                    break
        # 우클릭 컨텍스트 메뉴
        self.table_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table_view.customContextMenuRequested.connect(self._on_context_menu)

    # ── 팩토리 ──────────────────────────────────────────────────────
    def _make_table_model(self):
        return EsgEditableTableModel([], self.HEADERS, self.EDITABLE_KEYS)

    # ── CRUD 버튼 (하단 바 왼쪽) ─────────────────────────────────────
    def _build_bottom_left_buttons(self) -> list:
        btn_add  = QPushButton("➕ 추가")
        btn_edit = QPushButton("✏️ 수정")
        btn_del  = QPushButton("🗑️ 삭제")
        btn_save = QPushButton("💾 저장")
        for btn in [btn_add, btn_edit, btn_del, btn_save]:
            btn.setFixedWidth(72)
        btn_add.clicked.connect(self._on_add)
        btn_edit.clicked.connect(self._on_edit_selected)
        btn_del.clicked.connect(self._on_delete)
        btn_save.clicked.connect(self._on_save_all)
        return [btn_add, btn_edit, btn_del, btn_save]

    # ── Import 버튼 (하단 바 오른쪽) ─────────────────────────────────
    def _build_bottom_right_buttons(self) -> list:
        btn_import = QPushButton("📤 Import")
        btn_import.setFixedWidth(80)
        btn_import.clicked.connect(self._on_import)
        return [btn_import]

    # ── 조회/페이지 이동 — 미저장 경고 ──────────────────────────────
    def _on_search_click(self) -> None:
        if self._check_pending_and_confirm():
            # 검색 모드 전환 + pager 숨김 (BaseListView 핵심 로직 포함)
            self._search_mode = True
            self._update_search_tooltip()
            self.pager.setVisible(False)
            self._load_data(1)

    def _on_page_changed(self, page: int) -> None:
        if self._check_pending_and_confirm():
            self._load_data(page)

    def _check_pending_and_confirm(self) -> bool:
        if not self.table_model.has_pending():
            return True
        reply = QMessageBox.question(
            self, "미저장 변경",
            "저장하지 않은 변경 사항이 있습니다.\n계속하면 모두 취소됩니다.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        return reply == QMessageBox.StandardButton.Yes

    # ── 추가 ────────────────────────────────────────────────────────
    def _on_add(self) -> None:
        fields = self.ADD_FIELDS
        if not fields:
            return
        dlg = EsgAddDialog(fields, parent=self)
        if dlg.exec() != EsgAddDialog.DialogCode.Accepted:
            return
        data = dlg.get_data()
        new_src_row = self.table_model.insert_new_row(data)
        # 새 행으로 스크롤 + 선택
        src_idx   = self.table_model.index(new_src_row, 0)
        proxy_idx = self.proxy_model.mapFromSource(src_idx)
        if proxy_idx.isValid():
            self.table_view.scrollTo(proxy_idx,
                                     QAbstractItemView.ScrollHint.EnsureVisible)
            self.table_view.setCurrentIndex(proxy_idx)

    # ── 삭제 ────────────────────────────────────────────────────────
    def _on_delete(self) -> None:
        src_row = self._get_selected_source_index()
        if src_row < 0:
            QMessageBox.warning(self, "삭제", "삭제할 행을 선택하세요.")
            return
        self.table_model.mark_deleted(src_row)

    def _on_delete_row(self, src_row: int) -> None:
        """컨텍스트 메뉴에서 특정 source 행을 삭제 표시."""
        self.table_model.mark_deleted(src_row)

    # ── 💾 저장 (일괄 DB 반영) ──────────────────────────────────────
    def _on_save_all(self) -> None:
        pending = self.table_model.get_pending()
        if not (pending['insert'] or pending['update'] or pending['delete']):
            QMessageBox.information(self, "저장", "저장할 변경 사항이 없습니다.")
            return
        ok = err = 0
        errors: list[str] = []
        # 수정 업데이트에서 PK 키 비교에 사용 (루프 외부에서 한 번만 계산)
        pk_keys = {key for key, _ in self.HEADERS} - self.EDITABLE_KEYS
        # 삭제 먼저 (PK 충돌 방지)
        for row in pending['delete']:
            try:
                self._delete_row(row)
                ok += 1
            except Exception as exc:
                err += 1
                errors.append(f"삭제 실패: {exc}")
        # 신규 삽입
        for row in pending['insert']:
            try:
                self._save_row(row, is_new=True)
                ok += 1
            except Exception as exc:
                err += 1
                errors.append(f"추가 실패: {exc}")
        # 수정 업데이트 — PK 변경 시 delete+insert 처리
        for item in pending['update']:
            data     = item['data']
            original = item['original']
            pk_changed = original and any(
                str(original.get(k, '')) != str(data.get(k, ''))
                for k in pk_keys if k in original
            )
            try:
                if pk_changed:
                    self._delete_row(original)
                    self._save_row(data, is_new=True)
                else:
                    self._save_row(data, is_new=False)
                ok += 1
            except Exception as exc:
                err += 1
                errors.append(f"수정 실패: {exc}")
        msg = f"저장 완료: 성공 {ok}건"
        if err:
            msg += f",  실패 {err}건\n\n" + "\n".join(errors[:5])
            QMessageBox.warning(self, "저장", msg)
        else:
            QMessageBox.information(self, "저장", msg)
        if ok > 0:
            self._load_data(self.pager.current_page)

    # ── Import (즉시 DB 저장 유지) ──────────────────────────────────
    def _on_import(self) -> None:
        if self.table_model.has_pending():
            QMessageBox.warning(
                self, "Import",
                "미저장 변경이 있습니다.\n💾 저장 후 Import 하세요.")
            return
        rows = import_from_excel(self, self.HEADERS)
        if not rows:
            return
        reply = QMessageBox.question(
            self, "Import 확인",
            f"{len(rows)}건을 가져오시겠습니까?\n"
            "이미 존재하는 키는 덮어쓰기(UPDATE)됩니다.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply != QMessageBox.StandardButton.Yes:
            return
        ok = err = 0
        for row in rows:
            try:
                self._save_row(row, is_new=True)
                ok += 1
            except Exception:
                err += 1
        msg = f"완료: 성공 {ok}건"
        if err:
            msg += f",  실패 {err}건"
        QMessageBox.information(self, "Import 완료", msg)
        self._load_data(1)

    # ── 컨텍스트 메뉴 ──────────────────────────────────────────────
    def _on_context_menu(self, pos) -> None:
        idx = self.table_view.indexAt(pos)
        if not idx.isValid():
            return
        self.table_view.setCurrentIndex(idx)
        src_idx = self.proxy_model.mapToSource(idx)
        src_row = src_idx.row()
        row = self.table_model.get_row(src_row)
        if not row:
            return

        menu = QMenu(self)
        menu.addAction("➕  추가", self._on_add)
        menu.addAction("👁  보기", lambda: self._on_view_row(row))
        menu.addSeparator()
        act_edit = menu.addAction("✏️  수정",
                                  lambda: self._on_edit_row(row, src_row))
        act_dup  = menu.addAction("📋  복제",
                                  lambda: self._on_duplicate(src_row))
        act_edit.setEnabled(bool(self.ADD_FIELDS))
        act_dup.setEnabled(True)  # 복제는 항상 가능
        menu.addAction("🗑️  삭제", lambda: self._on_delete_row(src_row))

        menu.exec(self.table_view.viewport().mapToGlobal(pos))

    # ── 보기 ────────────────────────────────────────────────────────
    def _on_view_row(self, row: dict) -> None:
        dlg = EsgRowViewDialog(
            row, self.HEADERS,
            title=f"{self.VIEW_TITLE} — 상세 보기",
            parent=self)
        dlg.exec()

    # ── 수정 버튼 핸들러 ────────────────────────────────────────────
    def _on_edit_selected(self) -> None:
        """수정 버튼 — 현재 선택된 행을 수정 다이얼로그로 편집."""
        src_row = self._get_selected_source_index()
        if src_row < 0:
            QMessageBox.warning(self, "수정", "수정할 행을 선택하세요.")
            return
        row = self.table_model.get_row(src_row)
        self._on_edit_row(row, src_row)

    # ── 수정 (다이얼로그 + PK 변경 허용) ────────────────────────────
    def _on_edit_row(self, row: dict, src_row: int) -> None:
        fields = self.ADD_FIELDS
        if not fields:
            return
        # 모든 필드 편집 가능 (PK 포함)
        dlg = EsgEditDialog(fields, initial=row, readonly_keys=set(), parent=self)
        if dlg.exec() != EsgEditDialog.DialogCode.Accepted:
            return
        new_data = dlg.get_data()
        # PK 변경 감지
        pk_keys = {key for key, _ in self.HEADERS} - self.EDITABLE_KEYS
        pk_changed = any(
            str(row.get(k, '')) != str(new_data.get(k, ''))
            for k in pk_keys if k in new_data
        )
        state = self.table_model.get_row_state(src_row)
        if pk_changed and state != 'new':
            # 기존 PK → 삭제 목록 추가, 현재 행 → 'new'로 전환
            self.table_model.add_extra_deletion(row)
            self.table_model.update_row_data(src_row, new_data, force_new=True)
        else:
            self.table_model.update_row_data(src_row, new_data)

    # ── 복제 ────────────────────────────────────────────────────────
    def _on_duplicate(self, src_row: int) -> None:
        row_data = dict(self.table_model.get_row(src_row))
        new_src_row = self.table_model.insert_new_row(row_data, after_row=src_row)
        # 프록시 인덱스로 변환 후 스크롤 + 첫 셀 편집 모드
        src_model_idx = self.table_model.index(new_src_row, 0)
        proxy_idx = self.proxy_model.mapFromSource(src_model_idx)
        if not proxy_idx.isValid():
            # 필터에 걸린 경우 — 필터 초기화 후 재시도
            self._filter_edit.clear()
            proxy_idx = self.proxy_model.mapFromSource(src_model_idx)
        if proxy_idx.isValid():
            self.table_view.scrollTo(proxy_idx,
                                     QAbstractItemView.ScrollHint.EnsureVisible)
            self.table_view.setCurrentIndex(proxy_idx)
            self.table_view.edit(proxy_idx)   # 첫 컬럼 편집 모드 진입

    # ── 유틸 ────────────────────────────────────────────────────────
    def _get_selected_source_index(self) -> int:
        """현재 선택된 행의 source 모델 인덱스 반환. 없으면 -1."""
        idx = self.table_view.currentIndex()
        if not idx.isValid():
            return -1
        return self.proxy_model.mapToSource(idx).row()

    # ── 서브클래스 필수 구현 ────────────────────────────────────────
    def _save_row(self, data: dict, is_new: bool) -> bool:
        raise NotImplementedError

    def _delete_row(self, row: dict) -> bool:
        raise NotImplementedError
