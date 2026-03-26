"""
ESG 금리 파라미터 관리 시스템 — 앱 진입점
실행: python main.py
패키징: pyinstaller esg_app.spec
"""
import sys
import os

# ── PyInstaller 실행 시 _MEIPASS 기준 경로 처리 ──────────────────
if getattr(sys, "frozen", False):
    # 패키징된 실행파일 내부 경로
    _BASE_DIR = sys._MEIPASS          # noqa: SLF001
    # Qt 플러그인 경로 환경변수 설정 (Linux/Windows 모두 대응)
    os.environ.setdefault(
        "QT_PLUGIN_PATH",
        os.path.join(_BASE_DIR, "PyQt6", "Qt6", "plugins"),
    )
    os.environ.setdefault(
        "QT_QPA_PLATFORM_PLUGIN_PATH",
        os.path.join(_BASE_DIR, "PyQt6", "Qt6", "plugins", "platforms"),
    )
else:
    # 개발 환경: 소스 루트를 Python path에 추가
    _BASE_DIR = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, _BASE_DIR)

# ── 데이터 디렉토리: 실행파일 옆 data/ 에 위치 ──────────────────
if getattr(sys, "frozen", False):
    _EXEC_DIR = os.path.dirname(sys.executable)
else:
    _EXEC_DIR = _BASE_DIR

os.environ.setdefault("ESG_DATA_DIR", os.path.join(_EXEC_DIR, "data"))
os.environ.setdefault("ESG_EXPORT_DIR", os.path.join(_EXEC_DIR, "exports"))

from PyQt6.QtWidgets import QApplication, QMessageBox, QPushButton
from PyQt6.QtGui import QFont, QFontDatabase, QIcon
from PyQt6.QtCore import QObject, QEvent, Qt
from config.settings import APP_TITLE


class _BtnCursorFilter(QObject):
    """전역 이벤트 필터 — 활성 버튼 hover 시 포인터 커서(☞) 표시."""

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if isinstance(watched, QPushButton):
            t = event.type()
            if t == QEvent.Type.Enter:
                # 진입 시 활성 여부에 따라 커서 전환
                watched.setCursor(
                    Qt.CursorShape.PointingHandCursor
                    if watched.isEnabled()
                    else Qt.CursorShape.ArrowCursor
                )
            elif t == QEvent.Type.EnabledChange:
                # 활성/비활성 전환 시 커서 즉시 반영
                if watched.isEnabled():
                    watched.setCursor(Qt.CursorShape.PointingHandCursor)
                else:
                    watched.unsetCursor()
        return False  # 이벤트 소비하지 않음 — 정상 처리 유지

# ── 아이콘 경로: 개발 환경 = 소스 루트/resources, 패키징 = 실행파일 옆 resources
_ICON_PATH = os.path.join(
    os.path.dirname(sys.executable) if getattr(sys, "frozen", False)
    else os.path.dirname(os.path.abspath(__file__)),
    "resources", "icon.png"
)


def main() -> int:
    # ── DB 초기화 (테이블 없으면 자동 생성) ──────────────────────
    try:
        _ensure_db()
    except Exception as exc:
        # GUI 없이 오류 메시지를 보여주기 위해 임시 앱 사용
        _app = QApplication.instance() or QApplication(sys.argv)
        QMessageBox.critical(None, "DB 초기화 오류", str(exc))
        return 1

    # ── Qt 앱 ─────────────────────────────────────────────────────
    app = QApplication.instance() or QApplication(sys.argv)
    app.setApplicationName(APP_TITLE)
    if os.path.exists(_ICON_PATH):
        app.setWindowIcon(QIcon(_ICON_PATH))

    # 버튼 hover 커서 — QApplication 전역 필터로 모든 QPushButton에 적용
    _cursor_filter = _BtnCursorFilter(app)
    app.installEventFilter(_cursor_filter)

    # 기본 폰트 설정 (한글 지원)
    font = QFont()
    for family in ("Malgun Gothic", "NanumGothic", "Apple SD Gothic Neo", "sans-serif"):
        if family in QFontDatabase.families():
            font.setFamily(family)
            break
    font.setPointSize(9)
    app.setFont(font)

    # ── 로그인 ────────────────────────────────────────────────────
    from ui.login_dialog import LoginDialog
    login = LoginDialog()
    if login.exec() != LoginDialog.DialogCode.Accepted or login.user is None:
        return 0

    # ── 메인 윈도우 ───────────────────────────────────────────────
    from ui.main_window import MainWindow
    window = MainWindow(login.user)
    window.show()

    return app.exec()


def _ensure_db() -> None:
    """DB 파일이 없으면 자동 초기화"""
    from config.settings import DB_PATH
    if not os.path.exists(DB_PATH):
        print("[DB] 최초 실행: 데이터베이스를 초기화합니다...")
        from db.init_db import create_tables, insert_default_data
        create_tables()
        insert_default_data()
        print("[DB] 초기화 완료")


if __name__ == "__main__":
    sys.exit(main())
