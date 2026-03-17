"""
로그인 다이얼로그
Spring: EgovLoginUsr.jsp → LoginDialog
"""
import json
from pathlib import Path

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
                              QLabel, QLineEdit, QPushButton, QMessageBox,
                              QFrame, QCheckBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from services.auth_service import AuthService
from db.models.auth import AppUser

# 사용자 설정 파일 경로 (~/.config/esg/prefs.json)
_PREFS_PATH = Path.home() / ".config" / "esg" / "prefs.json"


def _load_prefs() -> dict:
    """저장된 사용자 설정을 읽어 반환 (파일 없거나 오류 시 빈 dict)"""
    try:
        if _PREFS_PATH.exists():
            with open(_PREFS_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return {}


def _save_prefs(data: dict) -> None:
    """사용자 설정을 파일에 저장"""
    try:
        _PREFS_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(_PREFS_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


class LoginDialog(QDialog):
    """
    exec() 후 self.user 에 로그인된 AppUser 저장
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.user: AppUser | None = None
        self._build_ui()

    def _build_ui(self) -> None:
        self.setWindowTitle("ESG 시스템 로그인")
        self.setFixedSize(380, 310)
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.WindowCloseButtonHint)

        root = QVBoxLayout(self)
        root.setContentsMargins(40, 30, 40, 30)
        root.setSpacing(14)

        # ── 타이틀 ─────────────────────────────────────────────
        title = QLabel("ESG 금리 파라미터 관리")
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        title.setFont(font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root.addWidget(title)

        subtitle = QLabel("Economic Scenario Generator")
        sub_font = QFont()
        sub_font.setPointSize(9)
        subtitle.setFont(sub_font)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: gray;")
        root.addWidget(subtitle)

        # ── 구분선 ─────────────────────────────────────────────
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        root.addWidget(line)

        # ── 폼 ──────────────────────────────────────────────────
        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        self.edit_id = QLineEdit()
        self.edit_id.setPlaceholderText("사용자 ID")
        self.edit_pw = QLineEdit()
        self.edit_pw.setPlaceholderText("비밀번호")
        self.edit_pw.setEchoMode(QLineEdit.EchoMode.Password)
        form.addRow("아이디", self.edit_id)
        form.addRow("비밀번호", self.edit_pw)
        root.addLayout(form)

        # ── 아이디 저장 체크박스 ──────────────────────────────
        chk_row = QHBoxLayout()
        chk_row.addStretch()
        self.chk_save_id = QCheckBox("아이디 저장")
        self.chk_save_id.setStyleSheet("font-size: 12px; color: #475569;")
        chk_row.addWidget(self.chk_save_id)
        root.addLayout(chk_row)

        # ── 저장된 아이디 불러오기 ────────────────────────────
        prefs = _load_prefs()
        saved_id = prefs.get("saved_user_id", "")
        if saved_id:
            self.edit_id.setText(saved_id)
            self.chk_save_id.setChecked(True)
            self.edit_pw.setFocus()
        else:
            self.edit_id.setFocus()

        # ── 버튼 ──────────────────────────────────────────────
        btn_layout = QHBoxLayout()
        self.btn_login = QPushButton("로그인")
        self.btn_login.setDefault(True)
        self.btn_login.setFixedHeight(36)
        self.btn_login.setStyleSheet(
            "QPushButton { background:#2563EB; color:white; border-radius:4px; font-weight:bold; }"
            "QPushButton:hover { background:#1D4ED8; }"
        )
        btn_cancel = QPushButton("취소")
        btn_cancel.setFixedHeight(36)
        btn_layout.addWidget(self.btn_login)
        btn_layout.addWidget(btn_cancel)
        root.addLayout(btn_layout)

        # ── 신호 연결 ──────────────────────────────────────────
        self.btn_login.clicked.connect(self._on_login)
        btn_cancel.clicked.connect(self.reject)
        self.edit_pw.returnPressed.connect(self._on_login)

    def _on_login(self) -> None:
        user_id  = self.edit_id.text().strip()
        password = self.edit_pw.text()          # 비밀번호는 strip 하지 않음
        if not user_id or not password:
            QMessageBox.warning(self, "입력 오류", "아이디와 비밀번호를 입력해주세요.")
            return

        try:
            user = AuthService.login(user_id, password)
        except Exception as exc:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "로그인 오류", f"시스템 오류가 발생했습니다:\n{exc}")
            return

        if user:
            # ── 아이디 저장 / 삭제 처리 ──────────────────────
            prefs = _load_prefs()
            if self.chk_save_id.isChecked():
                prefs["saved_user_id"] = user_id
            else:
                prefs.pop("saved_user_id", None)
            _save_prefs(prefs)

            self.user = user
            self.accept()
        else:
            from config.settings import DB_PATH
            QMessageBox.warning(self, "로그인 실패",
                                "아이디 또는 비밀번호가 올바르지 않습니다.\n\n"
                                f"DB: {DB_PATH}")
            self.edit_pw.clear()
            self.edit_pw.setFocus()
