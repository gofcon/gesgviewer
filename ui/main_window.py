"""
메인 윈도우
Spring: EgovMainView.jsp + EgovIncLeftmenu.jsp → QMainWindow + 상단 툴바 내비게이션
"""
from PyQt6.QtWidgets import (QMainWindow, QWidget, QTabWidget, QLabel,
                              QToolBar, QToolButton, QMenu, QMessageBox,
                              QStatusBar, QSizePolicy, QHBoxLayout,
                              QStyle, QApplication)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont
from ui.widgets.year_month_button import YearMonthButton

from config.settings import APP_TITLE, APP_VERSION, WINDOW_WIDTH, WINDOW_HEIGHT
from db.models.auth import AppUser

# ─── 뷰 임포트 (지연 임포트로 순환 참조 방지) ──────────────────
def _lazy_views():
    from ui.views.param_hw_view      import ParamHwCalcView, ParamHwBizView
    from ui.views.param_sw_view      import ParamSwView
    from ui.views.param_model_view   import ParamModelView
    from ui.views.ir_curve_view      import IrCurveView
    from ui.views.ytm_usr_view       import YtmUsrView
    from ui.views.sprd_curve_view    import SprdCurveView
    from ui.views.sprd_afns_view     import SprdAfnsView
    from ui.views.dcnt_rate_view     import DcntRateView
    from ui.views.dcnt_sto_view      import DcntStoView
    from ui.views.corp_pd_view       import CorpPdView
    from ui.views.crd_corp_pd_view   import CrdCorpPdView
    from ui.views.valid_fwd_view     import ValidFwdView
    from ui.views.valid_rnd_view     import ValidRndView
    from ui.views.valid_sce_sto_view import ValidSceStoView
    from ui.views.param_afns_view    import ParamAfnsView
    from ui.views.vol_swpn_view      import VolSwpnView
    from ui.views.co_job_view        import CoJobView
    from ui.views.batch_opert_view   import BatchOpertView
    from ui.views.batch_result_view  import BatchResultView
    from ui.views.batch_schd_view    import BatchSchdView
    from ui.views.auth_group_view    import AuthGroupView
    from ui.views.auth_info_view     import AuthInfoView
    from ui.views.lgn_policy_view    import LgnPolicyView
    from ui.views.mnu_mng_view       import MnuMngView
    from ui.views.pgm_mng_view       import PgmMngView
    from ui.views.usr_mng_view       import UsrMngView
    from ui.views.indiv_base_dt_view import IndivBaseDtView
    from ui.views.cop_bbs_view       import CopBbsView
    return {
        "param_hw_calc": ParamHwCalcView,
        "param_hw_biz":  ParamHwBizView,
        "param_sw":      ParamSwView,
        "param_model":   ParamModelView,
        "ir_curve":      IrCurveView,
        "ytm_usr":       YtmUsrView,
        "sprd_curve":    SprdCurveView,
        "sprd_afns":     SprdAfnsView,
        "dcnt_rate":     DcntRateView,
        "dcnt_sto":      DcntStoView,
        "corp_pd":       CorpPdView,
        "crd_corp_pd":   CrdCorpPdView,
        "valid_fwd":     ValidFwdView,
        "valid_rnd":     ValidRndView,
        "valid_sce_sto": ValidSceStoView,
        "param_afns":    ParamAfnsView,
        "vol_swpn":      VolSwpnView,
        "co_job":        CoJobView,
        "batch_opert":   BatchOpertView,
        "batch_result":  BatchResultView,
        "batch_schd":    BatchSchdView,
        "auth_group":    AuthGroupView,
        "auth_info":     AuthInfoView,
        "lgn_policy":    LgnPolicyView,
        "mnu_mng":       MnuMngView,
        "pgm_mng":       PgmMngView,
        "usr_mng":       UsrMngView,
        "indiv_base_dt": IndivBaseDtView,
        "cop_bbs":       CopBbsView,
    }


# ── 내비게이션 트리 정의 (카테고리 → 서브그룹 → 뷰 아이템) ────────
# 특수 키: "__about__" → 정보 다이얼로그, "__help__" → 도움말 다이얼로그
NAV_TREE = [
    ("환경설정", [
        ("ESG 작업정보", [
            ("ESG 작업 정보", "co_job"),
        ]),
        ("배치관리", [
            ("배치 작업 관리",   "batch_opert"),
            ("배치 결과 관리",   "batch_result"),
            ("배치 스케줄 관리", "batch_schd"),
        ]),
    ]),
    ("사용자 입력", [
        ("금리 파라미터", [
            ("HW Calc 파라미터",             "param_hw_calc"),
            ("HW Biz 적용 파라미터",          "param_hw_biz"),
            ("AFNS 모수생성결과",             "param_afns"),
            ("파라미터 모델",                 "param_model"),
            ("Smith-Wilson 사용자 파라미터",  "param_sw"),
            ("변동성/스왑션",                 "vol_swpn"),
        ]),
        ("금리 커브", [
            ("금리 커브",       "ir_curve"),
            ("YTM 사용자 입력", "ytm_usr"),
        ]),
        ("스프레드", [
            ("위험스프레드 커브", "sprd_curve"),
            ("AFNS 스프레드",    "sprd_afns"),
        ]),
    ]),
    ("산출결과", [
        ("할인율", [
            ("할인율 비즈",          "dcnt_rate"),
            ("할인율 시나리오 저장",  "dcnt_sto"),
        ]),
        ("채무불이행 위험", [
            ("기업 부도율",          "corp_pd"),
            ("신용등급 기업 부도율",  "crd_corp_pd"),
        ]),
    ]),
    ("결과 검증", [
        ("검증", [
            ("시나리오 선도 검증", "valid_fwd"),
            ("시나리오 랜덤 검증", "valid_rnd"),
            ("시나리오 저장 검증", "valid_sce_sto"),
        ]),
    ]),
    ("시스템 관리", [
        ("시스템 관리", [
            ("사용자 목록",         "usr_mng"),
            ("사용자별 권한 관리",  "auth_group"),
            ("사용자 권한 목록",    "auth_info"),
            ("로그인 정책",         "lgn_policy"),
            ("메뉴 목록 관리",      "mnu_mng"),
            ("프로그램 관리",       "pgm_mng"),
            ("개인 기준일자",       "indiv_base_dt"),
        ]),
    ]),
    ("도움말", [
        ("도움말", [
            ("도움말", "__help__"),
            ("정보",   "__about__"),
        ]),
    ]),
]

# 공지사항 — 서브그룹 없이 직접 이동 (별도 단독 버튼)
_BBS_KEY = "cop_bbs"


class MainWindow(QMainWindow):
    def __init__(self, user: AppUser):
        super().__init__()
        self.user = user
        self._view_cache:   dict[str, QWidget] = {}
        self._view_classes: dict[str, type]    = {}
        self._build_ui()
        self._load_views()

    # ─── UI 구성 ──────────────────────────────────────────────────
    def _build_ui(self) -> None:
        self.setWindowTitle(f"{APP_TITLE}  v{APP_VERSION}")
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

        # ── 상단 내비게이션 툴바 ──────────────────────────────────
        self._build_nav_toolbar()

        # ── 상태바 ────────────────────────────────────────────────
        status = QStatusBar()
        self.setStatusBar(status)
        status.showMessage(
            f"  로그인: {self.user.user_nm} ({self.user.user_id})  |  {APP_TITLE}"
        )

        # ── 중앙 위젯: 탭 위젯 ────────────────────────────────────
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.setMovable(True)
        self.tab_widget.setStyleSheet(
            "QTabBar::tab { padding: 4px 8px 4px 12px; font-size: 13px; }"
            "QTabBar::tab:selected { font-weight: bold; }"
        )
        self.tab_widget.tabCloseRequested.connect(self._on_tab_close)

        welcome = QLabel(
            f"<h2>환영합니다, {self.user.user_nm}님</h2>"
            "<p>상단 메뉴에서 화면을 선택하세요.</p>"
        )
        welcome.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tab_widget.addTab(welcome, "🏠 Dashboard")
        # 홈 탭은 닫기 버튼 숨김
        self.tab_widget.tabBar().setTabButton(
            0, self.tab_widget.tabBar().ButtonPosition.RightSide, None)

        self.setCentralWidget(self.tab_widget)

    def _build_nav_toolbar(self) -> None:
        """
        툴바 레이아웃:
        [환경설정▾][사용자입력▾][산출결과▾][결과검증▾][시스템관리▾][공지사항][도움말▾]  ─spacer─  [로그아웃]
        """
        toolbar = QToolBar("메인 툴바")
        toolbar.setMovable(False)
        toolbar.setIconSize(QSize(16, 16))
        toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextOnly)
        toolbar.setStyleSheet(
            "QToolBar { spacing: 2px; padding: 2px 4px; }"
            "QToolButton { padding: 4px 10px; font-size: 13px; border: none; border-radius: 3px; }"
            "QToolButton:hover { background: #E2E8F0; }"
            "QToolButton:pressed { background: #CBD5E1; }"
            "QToolButton::menu-indicator { image: none; width: 0px; }"
            "QToolButton#btn_logout {"
            "  border: 1px solid #DC2626; border-radius: 3px;"
            "  padding: 4px 6px;"
            "}"
            "QToolButton#btn_logout:hover { background: #FEE2E2; }"
        )

        # QMenu 는 팝업 시 최상위 윈도우로 분리되므로 각 메뉴에 직접 스타일 적용
        # addSection() 대신 disabled-action 헤더 + addSeparator() 방식 사용
        # → 첫 번째 그룹 위의 border(구분선) 제거 가능
        _menu_style = (
            "QMenu { padding: 4px 0px; font-size: 13px; }"
            "QMenu::item { padding: 5px 24px 5px 20px; }"
            "QMenu::item:selected { background: #E2E8F0; color: #0F172A; }"
            "QMenu::item:disabled {"                          # 섹션 헤더 스타일
            "  color: #475569; font-size: 11px; font-weight: bold;"
            "  background: transparent; padding: 6px 8px 2px 12px;"
            "}"
            "QMenu::separator { height: 1px; background: #E2E8F0; margin: 4px 6px; }"
        )

        # ── 왼쪽: 카테고리 드롭다운 버튼들 ──────────────────────
        # NAV_TREE 순서대로 버튼 생성; '도움말' 앞에 공지사항 단독 버튼 삽입
        for idx, (cat_name, sub_groups) in enumerate(NAV_TREE):
            # 도움말 직전에 공지사항(서브메뉴 없는 단독 버튼) 삽입
            if cat_name == "도움말":
                btn_bbs = QToolButton()
                btn_bbs.setText("공지사항")
                btn_bbs.clicked.connect(lambda: self._handle_nav(_BBS_KEY))
                toolbar.addWidget(btn_bbs)

            btn = QToolButton()
            btn.setText(cat_name)
            btn.setFont(QFont())
            btn.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)

            menu = QMenu(btn)
            menu.setStyleSheet(_menu_style)
            for grp_idx, (sub_name, items) in enumerate(sub_groups):
                # 첫 번째 그룹 앞에는 구분선 없음, 이후 그룹 앞에만 구분선 추가
                if grp_idx > 0:
                    menu.addSeparator()
                # 섹션 헤더: disabled action 으로 표시 (addSection 대체)
                hdr = menu.addAction(sub_name)
                hdr.setEnabled(False)
                for label, key in items:
                    action = menu.addAction(label)
                    action.triggered.connect(
                        lambda checked, k=key: self._handle_nav(k)
                    )

            btn.setMenu(menu)
            toolbar.addWidget(btn)

        # ── 가운데 spacer (오른쪽 영역을 우측으로 밀기) ───────────
        spacer = QWidget()
        spacer.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )
        toolbar.addWidget(spacer)

        # ── 오른쪽: 기준년월 + 로그아웃 (단일 컨테이너 — addSpacing 으로 간격 통일) ──
        from datetime import date
        from services.auth_service import AuthService

        right_box = QWidget()
        right_layout = QHBoxLayout(right_box)
        right_layout.setContentsMargins(0, 0, 6, 0)
        right_layout.setSpacing(0)           # addSpacing 으로 간격 명시 제어

        lbl_yymm = QLabel("기준년월")
        lbl_yymm.setStyleSheet("font-size: 12px; color: #475569;")
        right_layout.addWidget(lbl_yymm)
        right_layout.addSpacing(6)           # 레이블 ↔ 버튼 6px

        saved_yymm = AuthService.get_base_yymm(self.user.user_id)
        self.edit_base_yymm = YearMonthButton(
            saved_yymm or date.today().strftime("%Y%m")
        )
        right_layout.addWidget(self.edit_base_yymm)
        right_layout.addSpacing(6)           # 버튼 ↔ 로그아웃 6px

        btn_logout = QToolButton()
        btn_logout.setObjectName("btn_logout")
        btn_logout.setToolTip("로그아웃")
        btn_logout.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        btn_logout.setIcon(
            QApplication.style().standardIcon(QStyle.StandardPixmap.SP_DialogCloseButton)
        )
        btn_logout.setIconSize(QSize(18, 18))
        btn_logout.clicked.connect(self._on_logout)
        right_layout.addWidget(btn_logout)

        toolbar.addWidget(right_box)

        self.addToolBar(toolbar)

    def get_base_yymm(self) -> str:
        """툴바 기준년월 값 반환 (각 뷰에서 호출)"""
        return self.edit_base_yymm.text()

    def _load_views(self) -> None:
        """뷰 클래스 딕셔너리 로드 (실제 인스턴스는 첫 접근 시 생성)"""
        self._view_classes = _lazy_views()

    # ─── 슬롯 ─────────────────────────────────────────────────────
    def _handle_nav(self, key: str) -> None:
        """메뉴 클릭 → 화면 전환 또는 다이얼로그 표시"""
        if key == "__about__":
            self._on_about()
        elif key == "__help__":
            QMessageBox.information(
                self, "도움말",
                f"<b>{APP_TITLE}</b> 사용 안내<br><br>"
                "• 상단 메뉴에서 원하는 화면을 선택하세요.<br>"
                "• 각 화면에서 조회 조건 입력 후 [조회] 버튼을 클릭하세요.<br>"
                "• 엑셀 내보내기는 [Excel] 버튼을 클릭하세요."
            )
        else:
            self._show_view(key)

    def _show_view(self, view_key: str) -> None:
        # 이미 열린 탭이면 해당 탭으로 전환
        if view_key in self._view_cache:
            widget = self._view_cache[view_key]
            for i in range(self.tab_widget.count()):
                if self.tab_widget.widget(i) is widget:
                    self.tab_widget.setCurrentIndex(i)
                    return

        # 신규 탭 생성
        cls = self._view_classes.get(view_key)
        if cls is None:
            return
        widget = cls(self.user)
        self._view_cache[view_key] = widget
        title = getattr(cls, 'VIEW_TITLE', view_key)
        self.tab_widget.addTab(widget, title)
        self.tab_widget.setCurrentWidget(widget)

    def _on_tab_close(self, index: int) -> None:
        """탭 닫기 — 홈(index=0)은 닫지 않음."""
        if index == 0:
            return
        widget = self.tab_widget.widget(index)
        # 캐시에서 제거
        key_to_remove = next(
            (k for k, w in self._view_cache.items() if w is widget), None)
        if key_to_remove:
            del self._view_cache[key_to_remove]
        self.tab_widget.removeTab(index)

    def _on_logout(self) -> None:
        reply = QMessageBox.question(
            self, "로그아웃", "로그아웃 하시겠습니까?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.close()

    def _on_about(self) -> None:
        QMessageBox.information(
            self, "정보",
            f"<b>{APP_TITLE}</b><br>"
            f"버전: {APP_VERSION}<br><br>"
            "Spring eGovFramework → PyQt6 마이그레이션"
        )
