"""
메인 윈도우 — QTabWidget + QSplitter 기반 VS Code 스타일 패널 시스템

패널 조작:
    • 탭 드래그 (같은 패널 내)  → 탭 순서 변경
    • 탭 드래그 (패널 밖으로)   → 다른 패널로 탭 이동
    • 탭 우클릭                 → 닫기 / 다른 탭 모두 닫기 / 오른쪽·아래로 분리
    • 탭의 ✕ 버튼              → 해당 탭 닫기
    • 패널 경계 드래그          → 패널 크기 조절
"""
from PyQt6.QtWidgets import (QMainWindow, QWidget, QTabWidget, QTabBar,
                              QSplitter, QLabel, QToolBar, QToolButton,
                              QMenu, QMessageBox, QStatusBar, QSizePolicy,
                              QHBoxLayout, QVBoxLayout, QStyle, QApplication)
from PyQt6.QtCore import Qt, QSize, QMimeData, QPoint, pyqtSignal
from PyQt6.QtGui import QFont, QDrag, QPixmap, QColor, QPainter

from ui.widgets.year_month_button import YearMonthButton
from config.settings import APP_TITLE, APP_VERSION, WINDOW_WIDTH, WINDOW_HEIGHT
from config.nav_tree import NAV_TREE as _DEFAULT_NAV_TREE
from db.models.auth import AppUser

# ─── 뷰 임포트 (지연 임포트로 순환 참조 방지) ──────────────────────
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
    from ui.views.data_browser_view  import DataBrowserView
    from ui.views.dcnt_rate_usr_view     import DcntRateUsrView
    from ui.views.sprd_afns_usr_view     import SprdAfnsUsrView
    from ui.views.sprd_lp_usr_view       import SprdLpUsrView
    from ui.views.vol_swpn_usr_view      import VolSwpnUsrView
    from ui.views.corp_tm_usr_view       import CorpTmUsrView
    from ui.views.param_afns_usr_view    import ParamAfnsUsrView
    from ui.views.param_hw_usr_view      import ParamHwUsrView
    from ui.views.param_model_usr_view   import ParamModelUsrView
    from ui.views.ir_curve_ytm_view      import IrCurveYtmView
    from ui.views.ir_curve_spot_week_view import IrCurveSpotWeekView
    from ui.views.ir_curve_fwd_view      import IrCurveFwdView
    from ui.views.sprd_afns_calc_view    import SprdAfnsCalcView
    from ui.views.sprd_lp_view           import SprdLpView
    from ui.views.sprd_lp_biz_view       import SprdLpBizView
    from ui.views.param_afns_calc_view   import ParamAfnsCalcView
    from ui.views.param_hw_rnd_view      import ParamHwRndView
    from ui.views.param_model_calc_view  import ParamModelCalcView
    from ui.views.param_model_biz_view   import ParamModelBizView
    from ui.views.param_model_rnd_view   import ParamModelRndView
    from ui.views.dcnt_rate_bu_view      import DcntRateBuView
    from ui.views.dcnt_rate_bu_im_view   import DcntRateBuImView
    from ui.views.dcnt_sce_det_view      import DcntSceDetView
    from ui.views.dcnt_sce_im_view       import DcntSceImView
    from ui.views.ir_curve_sce_biz_view  import IrCurveSceBizView
    from ui.views.dcnt_sce_sto_gnr_view  import DcntSceStoGnrView
    from ui.views.corp_tm_view           import CorpTmView
    from ui.views.valid_param_hw_view    import ValidParamHwView
    from ui.views.qval_sce_view          import QvalSceView
    from ui.views.help_view              import HelpView
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
        "data_browser":  DataBrowserView,
        "dcnt_rate_usr":     DcntRateUsrView,
        "sprd_afns_usr":     SprdAfnsUsrView,
        "sprd_lp_usr":       SprdLpUsrView,
        "vol_swpn_usr":      VolSwpnUsrView,
        "corp_tm_usr":       CorpTmUsrView,
        "param_afns_usr":    ParamAfnsUsrView,
        "param_hw_usr":      ParamHwUsrView,
        "param_model_usr":   ParamModelUsrView,
        "ir_curve_ytm":      IrCurveYtmView,
        "ir_curve_spot_week": IrCurveSpotWeekView,
        "ir_curve_fwd":      IrCurveFwdView,
        "sprd_afns_calc":    SprdAfnsCalcView,
        "sprd_lp":           SprdLpView,
        "sprd_lp_biz":       SprdLpBizView,
        "param_afns_calc":   ParamAfnsCalcView,
        "param_hw_rnd":      ParamHwRndView,
        "param_model_calc":  ParamModelCalcView,
        "param_model_biz":   ParamModelBizView,
        "param_model_rnd":   ParamModelRndView,
        "dcnt_rate_bu":      DcntRateBuView,
        "dcnt_rate_bu_im":   DcntRateBuImView,
        "dcnt_sce_det":      DcntSceDetView,
        "dcnt_sce_im":       DcntSceImView,
        "ir_curve_sce_biz":  IrCurveSceBizView,
        "dcnt_sce_sto_gnr":  DcntSceStoGnrView,
        "corp_tm":           CorpTmView,
        "valid_param_hw":    ValidParamHwView,
        "qval_sce":          QvalSceView,
        "help":              HelpView,
    }


# ── 내비게이션 트리: DB 우선, 없으면 기본값 폴백 ────────────────────
def _load_nav_tree() -> list:
    """LETTNMENUINFO에서 메뉴 트리 로드. 없으면 기본값 반환 + DB 자동 시드."""
    try:
        from services.system_service import ContentService
        tree = ContentService.get_nav_tree()
        if tree:
            return tree
        # DB가 비어 있으면 기본값으로 시드 후 반환
        ContentService.seed_nav_tree(_DEFAULT_NAV_TREE)
    except Exception as exc:
        print(f"[MainWindow] 메뉴 DB 로드 실패 → 기본값 사용: {exc}")
    return _DEFAULT_NAV_TREE


_BBS_KEY  = "cop_bbs"
_MIME_TAB = "application/x-gesgviewer-tab"   # 탭 드래그 MIME 타입


# ─── 커스텀 탭 바 — 패널 간 탭 이동 드래그 지원 ──────────────────────
class _TabBar(QTabBar):
    """
    QTabBar 확장.
      • setMovable(True) → 같은 패널 내 탭 순서 변경 (Qt 내장)
      • 탭 바 바깥으로 드래그 → _start_inter_panel_drag → 다른 패널로 이동
    """

    _DRAG_THRESHOLD = 12  # 드래그 인식 최소 이동 거리(px)

    def __init__(self, panel: "QTabWidget", parent=None):
        super().__init__(parent)
        self.setMovable(True)
        self._panel     = panel
        self._press_pos: QPoint | None = None
        self._press_idx: int           = -1
        self._out_drag:  bool          = False

    # ── 마우스 이벤트 ───────────────────────────────────────────────
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._press_pos = event.pos()
            self._press_idx = self.tabAt(event.pos())
            self._out_drag  = False
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if (self._press_pos is not None
                and self._press_idx >= 0
                and not self._out_drag
                and (event.pos() - self._press_pos).manhattanLength()
                    > self._DRAG_THRESHOLD):
            # 탭 바 경계 밖으로 나가면 패널 간 드래그 시작
            if not self.rect().contains(event.pos()):
                self._out_drag = True
                self._start_inter_panel_drag(self._press_idx)
                return
        if not self._out_drag:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self._press_pos = None
        self._press_idx = -1
        self._out_drag  = False
        super().mouseReleaseEvent(event)

    # ── 패널 간 드래그 ──────────────────────────────────────────────
    def _start_inter_panel_drag(self, idx: int) -> None:
        panel  = self._panel
        widget = panel.widget(idx)
        if widget is None:
            self._out_drag = False
            return

        title = panel.tabText(idx)
        key   = widget.property("_view_key") or ""
        area  = panel._area

        # 소스에서 탭 제거 후 드래그 상태 보관
        panel.removeTab(idx)
        widget.hide()
        area._drag_state = {
            "widget": widget,
            "title":  title,
            "key":    key,
            "source": panel,
        }
        # 소스가 비었으면 정리 요청
        if panel.count() == 0:
            area._on_panel_empty(panel)

        # 드래그 픽맵 — 알약 모양 레이블
        pm = QPixmap(max(100, min(len(title) * 9 + 24, 200)), 26)
        pm.fill(Qt.GlobalColor.transparent)
        p = QPainter(pm)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setBrush(QColor("#E0E7FF"))
        p.setPen(QColor("#6366F1"))
        p.drawRoundedRect(0, 0, pm.width() - 1, 25, 5, 5)
        p.setPen(QColor("#312E81"))
        p.drawText(pm.rect(), Qt.AlignmentFlag.AlignCenter,
                   title[:22] + ("…" if len(title) > 22 else ""))
        p.end()

        drag = QDrag(self)
        mime = QMimeData()
        mime.setData(_MIME_TAB, key.encode("utf-8"))
        drag.setMimeData(mime)
        drag.setPixmap(pm)
        drag.setHotSpot(QPoint(pm.width() // 2, 13))

        result = drag.exec(Qt.DropAction.MoveAction)

        # 드롭 실패 → 원래(또는 첫 번째) 패널로 복귀
        if result != Qt.DropAction.MoveAction and area._drag_state:
            state  = area._drag_state
            target = (state["source"]
                      if state["source"] in area._panels
                      else area._panels[0])
            target.add_view(state["title"], state["widget"], state["key"])
            area._drag_state = None

        self._out_drag = False


# ─── 탭 패널 ──────────────────────────────────────────────────────────
class _TabPanel(QTabWidget):
    """
    VS Code 스타일 탭 패널.
      • 탭 닫기 버튼 (✕)
      • 탭 순서 드래그 (같은 패널)
      • 패널 간 탭 이동 드래그 수신 (dropEvent)
      • 우클릭 컨텍스트 메뉴 — 닫기 / 분리
    """

    panel_empty = pyqtSignal(object)   # _EditorArea 에 빈 패널 정리 요청

    def __init__(self, area: "_EditorArea", parent=None):
        super().__init__(parent)
        self._area = area

        # 커스텀 탭 바 설치 (addTab 전에 호출해야 함)
        tb = _TabBar(self)
        self.setTabBar(tb)

        self.setTabsClosable(True)
        self.setDocumentMode(True)    # VS Code 플랫 스타일
        self.setAcceptDrops(True)

        # 내부 콘텐츠 위젯의 minimumSizeHint 가 스플리터 조절을 막지 않도록
        # 명시적 최소 크기를 0 으로 지정
        self.setMinimumSize(0, 0)

        self.tabCloseRequested.connect(self._on_close)
        tb.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        tb.customContextMenuRequested.connect(self._on_ctx_menu)

    # ── minimumSizeHint 오버라이드 ──────────────────────────────────
    def minimumSizeHint(self) -> QSize:
        """스플리터가 패널을 자유롭게 축소할 수 있도록 작은 고정 최소 크기 반환."""
        return QSize(60, 60)

    # ── 뷰 추가 ────────────────────────────────────────────────────
    def add_view(self, title: str, widget: QWidget, key: str) -> None:
        widget.setProperty("_view_key", key)
        idx = self.addTab(widget, title)
        self.setCurrentIndex(idx)
        widget.show()

    def find_key(self, key: str) -> int:
        """key 에 해당하는 탭 인덱스 반환. 없으면 -1."""
        for i in range(self.count()):
            w = self.widget(i)
            if w and w.property("_view_key") == key:
                return i
        return -1

    # ── 탭 닫기 ────────────────────────────────────────────────────
    def _on_close(self, idx: int) -> None:
        w   = self.widget(idx)
        key = (w.property("_view_key") or "") if w else ""
        self.removeTab(idx)
        if key:
            self._area._view_cache.pop(key, None)
        if self.count() == 0:
            self.panel_empty.emit(self)

    # ── 우클릭 메뉴 ────────────────────────────────────────────────
    def _on_ctx_menu(self, pos: QPoint) -> None:
        tb  = self.tabBar()
        idx = tb.tabAt(pos)
        if idx < 0:
            return
        menu = QMenu(self)
        menu.addAction("닫기",               lambda: self._on_close(idx))
        menu.addAction("다른 탭 모두 닫기",  lambda: self._close_others(idx))
        menu.addSeparator()
        menu.addAction("오른쪽으로 분리",
                       lambda: self._area.split_tab(
                           self, idx, Qt.Orientation.Horizontal))
        menu.addAction("아래로 분리",
                       lambda: self._area.split_tab(
                           self, idx, Qt.Orientation.Vertical))
        menu.exec(tb.mapToGlobal(pos))

    def _close_others(self, keep: int) -> None:
        for i in reversed(range(self.count())):
            if i == keep:
                continue
            w   = self.widget(i)
            key = (w.property("_view_key") or "") if w else ""
            self.removeTab(i)
            if key:
                self._area._view_cache.pop(key, None)
        if self.count() == 0:
            self.panel_empty.emit(self)

    # ── 드롭 수신 (다른 패널에서 탭 드래그) ──────────────────────
    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat(_MIME_TAB):
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat(_MIME_TAB):
            event.acceptProposedAction()

    def dropEvent(self, event):
        if not event.mimeData().hasFormat(_MIME_TAB):
            event.ignore()
            return
        state = self._area._drag_state
        if not state:
            event.ignore()
            return
        widget              = state["widget"]
        title               = state["title"]
        key                 = state["key"]
        self._area._drag_state = None
        self.add_view(title, widget, key)
        event.setDropAction(Qt.DropAction.MoveAction)
        event.accept()


# ─── 에디터 영역 ───────────────────────────────────────────────────────
class _EditorArea(QWidget):
    """
    QSplitter + _TabPanel 로 구성된 VS Code 스타일 에디터 영역.
    패널 분리, 빈 패널 정리, 탭 드래그 상태 관리를 담당한다.
    """

    def __init__(self, view_cache: dict, parent=None):
        super().__init__(parent)
        self._view_cache              = view_cache
        self._panels: list[_TabPanel] = []
        self._drag_state: dict | None = None

        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)

        self._root = self._new_splitter(Qt.Orientation.Horizontal)
        lay.addWidget(self._root)

        first = self._new_panel()
        self._root.addWidget(first)

    # ── 스플리터 팩토리 ────────────────────────────────────────────
    @staticmethod
    def _new_splitter(orientation: Qt.Orientation,
                      parent: QWidget | None = None) -> QSplitter:
        """공통 스플리터 설정 적용 후 반환."""
        sp = QSplitter(orientation, parent)
        sp.setChildrenCollapsible(False)   # 패널이 완전히 사라지지 않도록
        sp.setHandleWidth(4)               # 드래그 핸들 두께
        return sp

    # ── 내부 패널 팩토리 ───────────────────────────────────────────
    def _new_panel(self) -> _TabPanel:
        panel = _TabPanel(self)
        panel.panel_empty.connect(self._on_panel_empty)
        self._panels.append(panel)
        return panel

    # ── 뷰 열기 ────────────────────────────────────────────────────
    def open_view(self, title: str, widget: QWidget, key: str) -> None:
        """현재 활성 패널에 탭으로 추가."""
        self._active_panel().add_view(title, widget, key)

    def find_and_raise(self, key: str) -> bool:
        """이미 열린 뷰를 찾아 활성화. 있으면 True 반환."""
        for panel in self._panels:
            idx = panel.find_key(key)
            if idx >= 0:
                panel.setCurrentIndex(idx)
                panel.setFocus()
                return True
        return False

    def _active_panel(self) -> _TabPanel:
        """포커스된 패널. 없으면 첫 번째 패널 (없으면 새로 생성)."""
        fw = QApplication.focusWidget()
        while fw:
            if isinstance(fw, _TabPanel) and fw in self._panels:
                return fw
            fw = fw.parent() if fw else None
        if self._panels:
            return self._panels[0]
        # 모든 패널이 제거된 극단적 상황
        p = self._new_panel()
        self._root.addWidget(p)
        return p

    # ── 탭 분리 ────────────────────────────────────────────────────
    def split_tab(self, source: _TabPanel, idx: int,
                  orientation: Qt.Orientation) -> None:
        """source 의 idx 탭을 분리해 새 패널에 배치."""
        widget = source.widget(idx)
        if widget is None:
            return
        title = source.tabText(idx)
        key   = widget.property("_view_key") or ""

        source.removeTab(idx)

        new_panel = self._new_panel()

        sp = source.parent()
        if isinstance(sp, QSplitter) and sp.orientation() == orientation:
            # 같은 방향 스플리터 — 소스 옆에 바로 삽입
            pos = sp.indexOf(source)
            sp.insertWidget(pos + 1, new_panel)
        else:
            # 방향이 다름 — 새 스플리터로 감싸기
            new_sp = self._new_splitter(orientation)
            if isinstance(sp, QSplitter):
                pos = sp.indexOf(source)
                sp.insertWidget(pos, new_sp)   # new_sp 를 source 자리에 삽입
            else:
                # sp 가 스플리터가 아닌 경우 (레이아웃 직접 교체)
                lay = self.layout()
                lay.removeWidget(self._root)
                new_sp.setParent(self)
                lay.addWidget(new_sp)
                self._root = new_sp
            new_sp.addWidget(source)           # Qt 가 source 를 new_sp 로 reparent
            new_sp.addWidget(new_panel)

        new_panel.add_view(title, widget, key)
        new_panel.show()

        if source.count() == 0:
            self._on_panel_empty(source)

    # ── 빈 패널 정리 ───────────────────────────────────────────────
    def _on_panel_empty(self, panel: _TabPanel) -> None:
        """마지막 1개 패널은 유지. 그 외 빈 패널과 불필요 스플리터 정리."""
        if len(self._panels) <= 1:
            return
        if panel not in self._panels:
            return

        self._panels.remove(panel)
        sp = panel.parent()

        # 패널을 스플리터에서 제거
        panel.setParent(None)   # type: ignore[arg-type]
        panel.deleteLater()

        # 스플리터에 자식이 1개만 남으면 위로 올려 불필요 스플리터 제거
        if (isinstance(sp, QSplitter)
                and sp is not self._root
                and sp.count() == 1):
            remaining   = sp.widget(0)
            grandparent = sp.parent()
            if isinstance(grandparent, QSplitter):
                pos = grandparent.indexOf(sp)
                grandparent.insertWidget(pos, remaining)   # Qt 가 reparent
            sp.deleteLater()


# ─── 메인 윈도우 ──────────────────────────────────────────────────────
class MainWindow(QMainWindow):
    def __init__(self, user: AppUser):
        super().__init__()
        self.user = user
        self._view_cache:   dict[str, QWidget] = {}
        self._view_classes: dict[str, type]    = {}
        self._nav_toolbar   = None          # 툴바 참조 (재구성용)
        self._build_ui()
        self._load_views()

    # ─── UI 구성 ──────────────────────────────────────────────────
    def _build_ui(self) -> None:
        self.setWindowTitle(f"{APP_TITLE}  v{APP_VERSION}")
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

        # 에디터 영역을 중앙 위젯으로 설정
        self._editor = _EditorArea(self._view_cache, self)
        self.setCentralWidget(self._editor)

        # 전역 스타일 (탭 바 + 스플리터 구분선)
        self.setStyleSheet(
            "QTabWidget::pane { border: none; border-top: 1px solid #E2E8F0; }"
            "QTabBar { background: #F1F5F9; }"
            "QTabBar::tab {"
            "  background: #F1F5F9;"
            "  color: #64748B;"
            "  padding: 5px 14px;"
            "  font-size: 13px;"
            "  border-right: 1px solid #E2E8F0;"
            "  min-width: 80px;"
            "}"
            "QTabBar::tab:selected {"
            "  background: #FFFFFF;"
            "  color: #0F172A;"
            "  font-weight: bold;"
            "  border-top: 2px solid #6366F1;"
            "}"
            "QTabBar::tab:hover:!selected {"
            "  background: #E2E8F0;"
            "  color: #0F172A;"
            "}"
            "QTabBar::close-button:hover {"
            "  background: #FCA5A5;"
            "  border-radius: 2px;"
            "}"
            "QSplitter::handle { background: #CBD5E1; }"
            "QSplitter::handle:horizontal { width: 4px; }"
            "QSplitter::handle:vertical   { height: 4px; }"
            "QSplitter::handle:hover { background: #6366F1; }"
        )

        # ── 대시보드 초기 탭 ──────────────────────────────────────
        welcome = QLabel(
            f"<h2 style='color:#1E293B;'>환영합니다, {self.user.user_nm}님</h2>"
            "<p style='color:#475569;'>상단 메뉴에서 화면을 선택하세요.</p>"
            "<hr style='border:1px solid #E2E8F0;'>"
            "<p style='color:#94A3B8; font-size:12px;'>"
            "💡 패널 조작 방법<br>"
            "　• <b>탭 드래그 (같은 패널)</b> → 탭 순서 변경<br>"
            "　• <b>탭 드래그 (패널 밖으로)</b> → 다른 패널로 탭 이동<br>"
            "　• <b>탭 우클릭</b> → 닫기 / 오른쪽·아래로 분리<br>"
            "　• <b>탭의 ✕ 버튼</b> → 탭 닫기<br>"
            "　• <b>패널 경계 드래그</b> → 패널 크기 조절"
            "</p>"
        )
        welcome.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome.setContentsMargins(40, 40, 40, 40)
        self._editor.open_view("🏠 Dashboard", welcome, "__dashboard__")
        self._view_cache["__dashboard__"] = welcome

        # ── 상단 내비게이션 툴바 ──────────────────────────────────
        self._build_nav_toolbar()

        # ── 상태바 ────────────────────────────────────────────────
        status = QStatusBar()
        self.setStatusBar(status)
        status.showMessage(
            f"  로그인: {self.user.user_nm} ({self.user.user_id})  |  {APP_TITLE}"
        )

    def _build_nav_toolbar(self) -> None:
        """
        툴바 레이아웃:
        [환경설정▾][사용자입력▾][산출결과▾][결과검증▾][시스템관리▾][공지사항][도움말▾]  ─spacer─  [기준년월][로그아웃]
        메뉴 구조는 DB(LETTNMENUINFO)에서 읽어 동적으로 구성한다.
        """
        nav_tree = _load_nav_tree()

        toolbar = QToolBar("메인 툴바")
        toolbar.setMovable(False)
        toolbar.setIconSize(QSize(16, 16))
        toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextOnly)
        toolbar.setStyleSheet(
            "QToolBar { spacing: 2px; padding: 2px 4px; }"
            "QToolButton { padding: 4px 10px; font-size: 13px;"
            "  border: none; border-radius: 3px; }"
            "QToolButton:hover { background: #E2E8F0; }"
            "QToolButton:pressed { background: #CBD5E1; }"
            "QToolButton::menu-indicator { image: none; width: 0px; }"
            "QToolButton#btn_logout {"
            "  border: 1px solid #DC2626; border-radius: 3px; padding: 4px 6px; }"
            "QToolButton#btn_logout:hover { background: #FEE2E2; }"
        )

        _menu_style = (
            "QMenu { padding: 4px 0px; font-size: 13px; }"
            "QMenu::item { padding: 5px 24px 5px 20px; }"
            "QMenu::item:selected { background: #E2E8F0; color: #0F172A; }"
            "QMenu::item:disabled {"
            "  color: #475569; font-size: 11px; font-weight: bold;"
            "  background: transparent; padding: 6px 8px 2px 12px; }"
            "QMenu::separator { height: 1px; background: #E2E8F0; margin: 4px 6px; }"
        )

        for cat_name, sub_groups in nav_tree:
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
                if grp_idx > 0:
                    menu.addSeparator()
                hdr = menu.addAction(sub_name)
                hdr.setEnabled(False)
                for label, key in items:
                    action = menu.addAction(label)
                    action.triggered.connect(
                        lambda checked, k=key: self._handle_nav(k)
                    )

            btn.setMenu(menu)
            toolbar.addWidget(btn)

        # ── 중간 spacer ─────────────────────────────────────────────
        spacer = QWidget()
        spacer.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )
        toolbar.addWidget(spacer)

        # ── 오른쪽: 기준년월 + 로그아웃 ─────────────────────────────
        from datetime import date
        from services.system_service import AuthService

        right_box    = QWidget()
        right_layout = QHBoxLayout(right_box)
        right_layout.setContentsMargins(0, 0, 6, 0)
        right_layout.setSpacing(0)

        lbl_yymm = QLabel("기준년월")
        lbl_yymm.setStyleSheet("font-size: 12px; color: #475569;")
        right_layout.addWidget(lbl_yymm)
        right_layout.addSpacing(6)

        saved_yymm = AuthService.get_base_yymm(self.user.user_id)
        self.edit_base_yymm = YearMonthButton(
            saved_yymm or date.today().strftime("%Y%m")
        )
        right_layout.addWidget(self.edit_base_yymm)
        right_layout.addSpacing(6)

        btn_logout = QToolButton()
        btn_logout.setObjectName("btn_logout")
        btn_logout.setToolTip("로그아웃")
        btn_logout.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        btn_logout.setIcon(
            QApplication.style().standardIcon(
                QStyle.StandardPixmap.SP_DialogCloseButton)
        )
        btn_logout.setIconSize(QSize(18, 18))
        btn_logout.clicked.connect(self._on_logout)
        right_layout.addWidget(btn_logout)

        toolbar.addWidget(right_box)
        self.addToolBar(toolbar)
        self._nav_toolbar = toolbar   # 재구성 시 제거 가능하도록 참조 보관

    def get_base_yymm(self) -> str:
        """툴바 기준년월 값 반환 (각 뷰에서 호출). 재구성 중에는 빈 문자열 반환."""
        if self.edit_base_yymm is None:
            return ""
        return self.edit_base_yymm.text()

    def reload_nav_toolbar(self) -> None:
        """메뉴 DB 변경 후 툴바를 다시 빌드한다.
        기존 툴바를 제거하고 DB에서 새 트리를 읽어 재구성.
        현재 열려 있는 탭은 그대로 유지된다.
        """
        if self._nav_toolbar is not None:
            self.removeToolBar(self._nav_toolbar)
            self._nav_toolbar.deleteLater()
            self._nav_toolbar = None
        # edit_base_yymm 참조 초기화 (재구성 시 새로 생성됨)
        self.edit_base_yymm = None
        self._build_nav_toolbar()

    def _load_views(self) -> None:
        self._view_classes = _lazy_views()

    # ─── 슬롯 ─────────────────────────────────────────────────────
    def _handle_nav(self, key: str) -> None:
        if key == "__about__":
            self._on_about()
        elif key in ("__help__", "help"):
            # 도움말 → 전용 탭으로 열기 (이미 열려있으면 포커스)
            self._show_view("help")
        else:
            self._show_view(key)

    def _show_view(self, view_key: str) -> None:
        """뷰 탭 열기 — 이미 열려있으면 해당 탭을 활성화."""
        # 이미 열린 탭이면 앞으로 가져옴
        if self._editor.find_and_raise(view_key):
            return

        cls = self._view_classes.get(view_key)
        if cls is None:
            return

        widget = cls(self.user)
        title  = getattr(cls, "VIEW_TITLE", view_key)
        self._view_cache[view_key] = widget
        self._editor.open_view(title, widget, view_key)

    # ─── 기타 슬롯 ───────────────────────────────────────────────
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
