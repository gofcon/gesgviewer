"""
ESG 금리 파라미터 관리 시스템 — 도움말 화면

레이아웃:
  ┌─────────────┬──────────────────────────────────────────┐
  │  목차        │  본문 (QTextBrowser)                      │
  │ (QListWidget)│  HTML 렌더링, 앵커 이동 지원             │
  └─────────────┴──────────────────────────────────────────┘
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                              QSplitter, QListWidget, QListWidgetItem,
                              QTextBrowser, QLabel, QLineEdit, QToolButton,
                              QSizePolicy)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from db.models.auth import AppUser
from config.settings import APP_TITLE, APP_VERSION


# ─── 목차 정의 ─────────────────────────────────────────────────────────
_TOC = [
    ("📋 시스템 개요",          "overview"),
    ("🖥️ 화면 구성",            "ui"),
    ("⚙️ 공통 기능",             "common"),
    ("─── 메뉴별 기능 ───",     None),         # 구분선
    ("🔧 환경설정",              "config"),
    ("✏️ 사용자 입력",           "input"),
    ("📊 기초데이터",            "base"),
    ("📈 산출결과",              "result"),
    ("🔍 결과검증",              "valid"),
    ("🛠️ 시스템 관리",          "sysadmin"),
    ("🗄️ 데이터 탐색",          "data"),
    ("─── 부록 ───",            None),
    ("📌 DB 테이블 구조",        "tables"),
    ("❓ 자주 묻는 질문",        "faq"),
]


# ─── HTML 도움말 본문 ───────────────────────────────────────────────────
def _build_html() -> str:
    css = """
    <style>
      body  { font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif;
              font-size: 13px; color: #1E293B; margin: 0; padding: 0; }
      h1    { font-size: 20px; color: #1E3A5F; border-bottom: 2px solid #3B82F6;
              padding-bottom: 8px; margin-top: 32px; }
      h2    { font-size: 16px; color: #1D4ED8; border-left: 4px solid #3B82F6;
              padding-left: 10px; margin-top: 28px; }
      h3    { font-size: 13px; color: #374151; margin-top: 18px; }
      table { border-collapse: collapse; width: 100%; margin: 10px 0; }
      th    { background: #EFF6FF; color: #1E40AF; font-weight: bold;
              padding: 7px 12px; border: 1px solid #BFDBFE; text-align: left; }
      td    { padding: 6px 12px; border: 1px solid #E2E8F0; }
      tr:nth-child(even) td { background: #F8FAFC; }
      .tip  { background: #F0FDF4; border-left: 4px solid #22C55E;
              padding: 8px 14px; margin: 10px 0; border-radius: 0 4px 4px 0; }
      .warn { background: #FFFBEB; border-left: 4px solid #F59E0B;
              padding: 8px 14px; margin: 10px 0; border-radius: 0 4px 4px 0; }
      .info { background: #EFF6FF; border-left: 4px solid #3B82F6;
              padding: 8px 14px; margin: 10px 0; border-radius: 0 4px 4px 0; }
      code  { background: #F1F5F9; border: 1px solid #CBD5E1;
              padding: 1px 5px; border-radius: 3px; font-family: monospace; }
      ul    { padding-left: 20px; margin: 8px 0; }
      li    { margin: 4px 0; }
      .badge { display: inline-block; padding: 1px 8px; border-radius: 10px;
               font-size: 11px; font-weight: bold; }
      .badge-r { background: #FEE2E2; color: #DC2626; }   /* read-only */
      .badge-c { background: #DCFCE7; color: #16A34A; }   /* crud */
      .badge-s { background: #EDE9FE; color: #7C3AED; }   /* special */
    </style>
    """

    body = f"""
<a name="overview"></a>
<h1>📋 시스템 개요</h1>
<p><b>{APP_TITLE}</b> (버전 {APP_VERSION})는 보험사 IFRS17 / K-ICS 기준의
금리 파라미터(Smith-Wilson, Hull-White, AFNS) 및 할인율을 관리·조회하는
데스크톱 애플리케이션입니다.</p>

<h3>주요 역할</h3>
<table>
  <tr><th>구분</th><th>내용</th></tr>
  <tr><td>사용자 입력</td><td>금리 YTM, 스프레드, SW/HW/AFNS 파라미터 등 사용자 직접 입력</td></tr>
  <tr><td>기초데이터 조회</td><td>금리 커브, 스프레드, 변동성, 모수 등 계산·저장된 데이터 조회</td></tr>
  <tr><td>산출결과 조회</td><td>할인율, 금리시나리오, 기업부도율 등 배치 산출 결과 확인</td></tr>
  <tr><td>결과검증</td><td>선도/랜덤/저장 시나리오 및 HW 파라미터 검증</td></tr>
  <tr><td>시스템관리</td><td>사용자·권한·메뉴·배치 관리</td></tr>
</table>

<div class="info">
  <b>기술 스택</b>: Python 3.12 · PyQt6 · SQLAlchemy (SQLite) · pandas · openpyxl · matplotlib
</div>

<hr>
<a name="ui"></a>
<h1>🖥️ 화면 구성</h1>

<h2>전체 레이아웃</h2>
<pre style="background:#F8FAFC;padding:12px;border:1px solid #E2E8F0;border-radius:4px;font-family:monospace;font-size:12px;">
┌─────────────────────────────────────────────────────────────────────┐
│ [환경설정▾][사용자입력▾][기초데이터▾]...  [기준년월]  [×로그아웃] │  ← 상단 메뉴 툴바
├─────────────────────────────────────────────────────────────────────┤
│  ┌───────────────┐ ┌─────────────────────────────────────────────┐ │
│  │ Tab1 │ Tab2 ✕│ │ Tab3 │ Tab4 ✕                              │ │  ← 탭 패널 (분할 가능)
│  │───────────────│ │─────────────────────────────────────────────│ │
│  │               │ │                                             │ │
│  │  화면 내용    │ │  화면 내용                                  │ │
│  │               │ │                                             │ │
│  └───────────────┘ └─────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────────┤
│  로그인: 사용자명 (ID)  |  ESG 금리 파라미터 관리 시스템          │  ← 상태바
└─────────────────────────────────────────────────────────────────────┘
</pre>

<h2>탭 패널 조작</h2>
<table>
  <tr><th>동작</th><th>효과</th></tr>
  <tr><td>탭 드래그 (같은 패널 내)</td><td>탭 순서 변경</td></tr>
  <tr><td>탭 드래그 (패널 밖으로)</td><td>드롭한 패널로 탭 이동</td></tr>
  <tr><td>탭 우클릭</td><td>닫기 / 다른 탭 모두 닫기 / 오른쪽·아래로 분리</td></tr>
  <tr><td>탭의 ✕ 버튼</td><td>해당 탭 닫기</td></tr>
  <tr><td>패널 경계 드래그</td><td>패널 너비/높이 조절</td></tr>
</table>

<h2>상단 툴바</h2>
<ul>
  <li><b>메뉴 버튼 (▾)</b> — 클릭 시 드롭다운 메뉴 표시</li>
  <li><b>공지사항</b> — 게시판 화면 열기</li>
  <li><b>기준년월</b> — 클릭하면 연/월 선택 팝업 표시. 각 화면의 조회 기준년월로 사용</li>
  <li><b>× 로그아웃</b> — 앱 종료 (로그아웃)</li>
</ul>

<hr>
<a name="common"></a>
<h1>⚙️ 공통 기능</h1>

<h2>조회 화면 공통 요소</h2>
<table>
  <tr><th>요소</th><th>위치</th><th>설명</th></tr>
  <tr><td>필터 입력창</td><td>테이블 상단</td><td>입력 즉시 그리드 행 필터링 (실시간)</td></tr>
  <tr><td>컬럼 선택 콤보</td><td>필터 옆</td><td>특정 컬럼만 필터 대상으로 지정</td></tr>
  <tr><td>✕ 버튼</td><td>필터 옆</td><td>필터 초기화</td></tr>
  <tr><td>컬럼 헤더 클릭</td><td>그리드 상단</td><td>해당 컬럼 오름차순/내림차순 정렬</td></tr>
  <tr><td>페이지네이션</td><td>하단 중앙</td><td>◀◀ ◀ [1][2][3]… ▶ ▶▶ 형식, 총 건수 표시</td></tr>
  <tr><td>📥 Excel 버튼</td><td>하단 우측</td><td>현재 페이지 데이터를 엑셀로 저장</td></tr>
  <tr><td>🔍 조회 버튼</td><td>상단 우측</td><td>기준년월 변경 후 재조회</td></tr>
</table>

<h2>CRUD 화면 추가 요소</h2>
<div class="info">
  사용자 입력 메뉴 화면은 아래 CRUD 버튼을 제공합니다.
</div>
<table>
  <tr><th>버튼</th><th>동작</th></tr>
  <tr><td>➕ 추가</td><td>신규 행 입력 다이얼로그 표시. OK 후 그리드에 <span style="color:#16A34A">초록색</span>으로 추가 (미저장)</td></tr>
  <tr><td>✏️ 수정</td><td>선택 행 편집 다이얼로그 표시. OK 후 <span style="color:#D97706">주황색</span>으로 변경 (미저장)</td></tr>
  <tr><td>🗑️ 삭제</td><td>선택 행을 그리드에서 즉시 제거 (미저장 — 취소선 표시)</td></tr>
  <tr><td>💾 저장</td><td>추가/수정/삭제 변경 사항을 DB에 일괄 반영</td></tr>
  <tr><td>📤 Import</td><td>Excel 파일에서 데이터 일괄 가져오기 (upsert)</td></tr>
</table>
<div class="tip">
  <b>💡 미저장 경고</b>: 변경 사항이 있는 상태에서 페이지 이동 또는 조회 버튼을 클릭하면
  "저장하지 않은 변경 사항이 있습니다" 경고가 표시됩니다.
</div>

<h2>컨텍스트 메뉴 (우클릭)</h2>
<table>
  <tr><th>항목</th><th>설명</th></tr>
  <tr><td>➕ 추가</td><td>추가 다이얼로그 열기</td></tr>
  <tr><td>👁 보기</td><td>선택 행 전체 필드 상세 보기</td></tr>
  <tr><td>✏️ 수정</td><td>선택 행 편집</td></tr>
  <tr><td>📋 복제</td><td>선택 행을 아래에 복사 후 첫 번째 셀 편집 모드 진입</td></tr>
  <tr><td>🗑️ 삭제</td><td>선택 행 삭제 표시</td></tr>
</table>

<h2>Excel Import 형식</h2>
<ul>
  <li>첫 번째 행은 <b>헤더(한글 컬럼명)</b>이어야 합니다.</li>
  <li>화면의 컬럼 순서와 동일하게 작성하세요.</li>
  <li>이미 존재하는 PK는 <b>UPDATE</b>, 없는 PK는 <b>INSERT</b> 됩니다.</li>
</ul>

<hr>
<a name="config"></a>
<h1>🔧 환경설정</h1>

<h2>ESG 작업 정보</h2>
<p>배치 작업(계산 배치)의 실행 이력을 조회합니다.
<code>E_CO_JOB_INFO</code> 테이블 기반. 기준년월·계산일자·시작/종료 시간 확인 가능.</p>

<h2>배치관리</h2>
<table>
  <tr><th>화면</th><th>테이블</th><th>설명</th></tr>
  <tr><td>배치 작업 관리</td><td>COMTNBATCHOPERT</td><td>배치 작업 ID/명칭/프로그램 등록·관리</td></tr>
  <tr><td>배치 결과 관리</td><td>COMTNBATCHRESULT</td><td>배치 실행 결과(성공/실패/소요시간) 조회</td></tr>
  <tr><td>배치 스케줄 관리</td><td>COMTNBATCHSCHDUL</td><td>배치 실행 주기(cron) 설정</td></tr>
</table>

<hr>
<a name="input"></a>
<h1>✏️ 사용자 입력</h1>
<div class="info">
  사용자가 직접 입력하는 <code>_USR</code> 계열 테이블을 관리합니다.
  모든 화면이 <b>CRUD(추가·수정·삭제·저장)</b> 기능을 제공합니다.
</div>

<h2>금리정보</h2>
<table>
  <tr><th>화면</th><th>테이블</th><th>PK</th></tr>
  <tr><td>YTM 사용자 입력</td><td>E_IR_CURVE_YTM_USR</td><td>기준일자 · 커브ID · 만기코드</td></tr>
  <tr><td>할인율 사용자 입력</td><td>E_IR_DCNT_RATE_USR</td><td>기준년월 · 적용업무 · 커브ID · 시나리오번호 · 만기</td></tr>
</table>

<h2>금리스프레드</h2>
<table>
  <tr><th>화면</th><th>테이블</th><th>PK</th></tr>
  <tr><td>AFNS 스프레드 사용자 입력</td><td>E_IR_SPRD_AFNS_USR</td><td>기준년월 · 모델ID · 커브ID · 만기</td></tr>
  <tr><td>LP 스프레드 사용자 입력</td><td>E_IR_SPRD_LP_USR</td><td>적용시작/종료년월 · 적용업무 · 커브ID · 시나리오번호 · 만기</td></tr>
</table>

<h2>Swap 변동성</h2>
<table>
  <tr><th>화면</th><th>테이블</th><th>설명</th></tr>
  <tr><td>변동성/스왑션 사용자 입력</td><td>E_IR_VOL_SWPN_USR</td><td>만기 Y1~Y30 변동성 입력</td></tr>
</table>

<h2>기업 부도율</h2>
<table>
  <tr><th>화면</th><th>테이블</th><th>설명</th></tr>
  <tr><td>기업 전환행렬 사용자 입력</td><td>E_RC_CORP_TM_USR</td><td>신용등급 전환확률 7개 컬럼 입력</td></tr>
</table>

<h2>매개변수</h2>
<table>
  <tr><th>화면</th><th>테이블</th><th>설명</th></tr>
  <tr><td>Smith-Wilson 사용자 파라미터</td><td>E_IR_PARAM_SW_USR</td><td>LLP, LTFR, 유동성 프리미엄, SW Alpha 등</td></tr>
  <tr><td>AFNS 파라미터 사용자 입력</td><td>E_IR_PARAM_AFNS_USR</td><td>param_typ_cd별 파라미터값</td></tr>
  <tr><td>HW 파라미터 사용자 입력</td><td>E_IR_PARAM_HW_USR</td><td>적용업무 · 만기 · 파라미터 유형별 값</td></tr>
  <tr><td>파라미터 모델 사용자 입력</td><td>E_IR_PARAM_MODEL_USR</td><td>적용시작/종료년월 기준 파라미터값</td></tr>
</table>

<div class="tip">
  <b>💡 Smith-Wilson 파라미터 필드 설명</b><br>
  • <b>LLP</b> (Last Liquid Point): 최종 유동성 만기 (년)<br>
  • <b>LTFR</b> (Long-Term Forward Rate): 장기선도금리<br>
  • <b>수렴연도</b>: UFR 수렴 연도<br>
  • <b>유동성 프리미엄</b>: 국채 대비 보험부채 유동성 조정<br>
  • <b>SW Alpha</b>: Smith-Wilson 수렴속도 파라미터
</div>

<hr>
<a name="base"></a>
<h1>📊 기초데이터</h1>
<div class="info">
  배치 계산 또는 시장 데이터 수집으로 생성된 기초 데이터입니다. <b>읽기 전용(조회만)</b> 화면입니다.
</div>

<h2>금리정보</h2>
<table>
  <tr><th>화면</th><th>테이블</th><th>설명</th></tr>
  <tr><td>금리 커브</td><td>E_IR_CURVE_SPOT</td><td>현물금리 커브 (기준일자 · 커브ID · 만기별 spot_rate) + 차트</td></tr>
  <tr><td>금리커브 YTM</td><td>E_IR_CURVE_YTM</td><td>만기수익률(Yield to Maturity) 데이터</td></tr>
  <tr><td>금리커브 현물(주간)</td><td>E_IR_CURVE_SPOT_WEEK</td><td>주간 현물금리 (요일/영업일구분 포함)</td></tr>
  <tr><td>금리커브 선도</td><td>E_IR_CURVE_FWD</td><td>선도금리 (fwd_mat_cd · mat_cd · int_rate)</td></tr>
</table>

<h2>금리스프레드</h2>
<table>
  <tr><th>화면</th><th>테이블</th><th>설명</th></tr>
  <tr><td>AFNS 스프레드</td><td>E_IR_SPRD_AFNS_BIZ</td><td>AFNS 모형 스프레드 (충격/수준/기울기)</td></tr>
  <tr><td>AFNS 스프레드 계산</td><td>E_IR_SPRD_AFNS_CALC</td><td>AFNS 스프레드 계산 결과</td></tr>
  <tr><td>위험스프레드 커브</td><td>E_IR_SPRD_CURVE</td><td>국채/회사채 위험스프레드 (int_rate, crd_sprd)</td></tr>
  <tr><td>LP 스프레드</td><td>E_IR_SPRD_LP</td><td>유동성프리미엄 스프레드 (모델 · 적용업무)</td></tr>
  <tr><td>LP 스프레드 비즈</td><td>E_IR_SPRD_LP_BIZ</td><td>유동성프리미엄 비즈 적용값</td></tr>
</table>

<h2>Swap 변동성</h2>
<table>
  <tr><th>화면</th><th>테이블</th><th>설명</th></tr>
  <tr><td>변동성/스왑션</td><td>E_IR_VOL_SWPN</td><td>스왑션 변동성 (swpn_mat_num · swap_ten_num)</td></tr>
</table>

<h2>매개변수</h2>
<table>
  <tr><th>화면</th><th>테이블</th><th>설명</th></tr>
  <tr><td>HW Calc 파라미터</td><td>E_IR_PARAM_HW_CALC</td><td>Hull-White 모수 계산 결과 + 차트</td></tr>
  <tr><td>HW Biz 적용 파라미터</td><td>E_IR_PARAM_HW_BIZ</td><td>비즈 적용 HW 모수</td></tr>
  <tr><td>AFNS 모수생성결과</td><td>E_IR_PARAM_AFNS_BIZ</td><td>AFNS 모수 생성 최종 결과</td></tr>
  <tr><td>AFNS 모수 계산</td><td>E_IR_PARAM_AFNS_CALC</td><td>AFNS 중간 계산 결과</td></tr>
  <tr><td>파라미터 모델</td><td>E_IR_PARAM_MODEL</td><td>금리모형 파라미터 (IrParamModel)</td></tr>
  <tr><td>파라미터 모델 계산</td><td>E_IR_PARAM_MODEL_CALC</td><td>모형 파라미터 계산 결과</td></tr>
  <tr><td>파라미터 모델 비즈</td><td>E_IR_PARAM_MODEL_BIZ</td><td>비즈 적용 모형 파라미터</td></tr>
  <tr><td>HW 난수</td><td>E_IR_PARAM_HW_RND</td><td>HW 시뮬레이션 난수</td></tr>
  <tr><td>파라미터 모델 난수</td><td>E_IR_PARAM_MODEL_RND</td><td>모형 시뮬레이션 난수</td></tr>
</table>

<hr>
<a name="result"></a>
<h1>📈 산출결과</h1>
<div class="info">
  배치 계산으로 생성된 최종 산출 결과입니다. 읽기 전용입니다.
</div>

<h2>할인율</h2>
<table>
  <tr><th>화면</th><th>테이블</th><th>설명</th></tr>
  <tr><td>할인율 비즈</td><td>E_IR_DCNT_RATE_BIZ</td><td>비즈 적용 할인율 (spot_rate, fwd_rate) + 차트</td></tr>
  <tr><td>할인율 BU</td><td>E_IR_DCNT_RATE_BU</td><td>BU 기준 할인율 (원가/시가/유동성프리미엄)</td></tr>
  <tr><td>할인율 BU 내부모형</td><td>E_IR_DCNT_RATE_BU_IM</td><td>내부모형 기준 BU 할인율</td></tr>
</table>

<h2>금리시나리오</h2>
<table>
  <tr><th>화면</th><th>테이블</th><th>설명</th></tr>
  <tr><td>확률시나리오 저장(비즈)</td><td>E_IR_DCNT_SCE_STO_BIZ</td><td>비즈용 확률론적 시나리오 저장</td></tr>
  <tr><td>확률시나리오 저장(일반)</td><td>E_IR_DCNT_SCE_STO_GNR</td><td>일반 확률론적 시나리오 (sce_no 추가)</td></tr>
  <tr><td>확률시나리오 상세(비즈)</td><td>E_IR_DCNT_SCE_DET_BIZ</td><td>시나리오별 spot/fwd rate 상세</td></tr>
  <tr><td>확률시나리오 내부모형</td><td>E_IR_DCNT_SCE_IM</td><td>내부모형 기준 시나리오</td></tr>
  <tr><td>금리커브 시나리오(비즈)</td><td>E_IR_CURVE_SCE_BIZ</td><td>시나리오별 금리커브</td></tr>
</table>

<h2>기업 부도율</h2>
<table>
  <tr><th>화면</th><th>테이블</th><th>설명</th></tr>
  <tr><td>기업 전환행렬</td><td>E_RC_CORP_TM</td><td>등급 간 전환확률 행렬</td></tr>
  <tr><td>기업 부도율</td><td>E_RC_CORP_PD_BIZ</td><td>등급별 부도확률 (비즈 기준)</td></tr>
  <tr><td>신용등급 기업 부도율</td><td>E_RC_CORP_PD</td><td>신용평가기관별 부도확률</td></tr>
</table>

<hr>
<a name="valid"></a>
<h1>🔍 결과검증</h1>
<div class="info">
  산출 결과의 정합성을 검증하는 화면들입니다. 읽기 전용입니다.
</div>
<table>
  <tr><th>화면</th><th>테이블</th><th>설명</th></tr>
  <tr><td>시나리오 선도 검증</td><td>E_IR_DCNT_RATE</td><td>선도금리 기반 검증 데이터</td></tr>
  <tr><td>시나리오 랜덤 검증</td><td>E_IR_VALID_RND</td><td>난수 기반 시나리오 검증</td></tr>
  <tr><td>시나리오 저장 검증</td><td>E_IR_VALID_SCE_STO</td><td>저장 시나리오 검증</td></tr>
  <tr><td>HW 파라미터 검증</td><td>E_IR_VALID_PARAM_HW</td><td>HW 모수 검증값 (swpn_mat_num · swap_ten_num)</td></tr>
  <tr><td>Q값 시나리오 검증</td><td>E_IR_QVAL_SCE</td><td>qval1~qval15 검증 지표</td></tr>
</table>

<hr>
<a name="sysadmin"></a>
<h1>🛠️ 시스템 관리</h1>

<h2>사용자 관리</h2>
<table>
  <tr><th>화면</th><th>테이블</th><th>설명</th></tr>
  <tr><td>사용자 목록</td><td>APP_USER</td><td>사용자 등록·수정·삭제. 비밀번호는 bcrypt 암호화</td></tr>
  <tr><td>사용자별 권한 관리</td><td>LETTNAUTHORGROUPINFO</td><td>그룹(권한) 생성·편집</td></tr>
  <tr><td>사용자 권한 목록</td><td>LETTNAUTHORINFO</td><td>권한 코드 관리</td></tr>
  <tr><td>로그인 정책</td><td>LETTNLGNPOLICY</td><td>IP 제한 · 로그인 제한 여부 설정</td></tr>
</table>

<h2>메뉴 관리</h2>
<table>
  <tr><th>화면</th><th>테이블</th><th>설명</th></tr>
  <tr><td>메뉴 목록 관리</td><td>LETTNMENUINFO</td><td>상단 내비게이션 트리 직접 편집</td></tr>
</table>
<div class="warn">
  <b>⚠️ 메뉴 목록 관리 주의사항</b><br>
  • <b>수준(level)</b> 1=카테고리, 2=그룹, 3=항목(leaf) 구조를 유지하세요.<br>
  • <b>뷰 키</b>는 <code>_lazy_views()</code>에 등록된 키와 정확히 일치해야 화면이 열립니다.<br>
  • 편집 후 <b>[✅ 메뉴 적용]</b> 버튼을 눌러야 즉시 반영됩니다 (재시작 불필요).<br>
  • <b>[🔄 기본값 초기화]</b>를 누르면 시스템 기본 메뉴로 복원됩니다.
</div>

<h2>기타 시스템</h2>
<table>
  <tr><th>화면</th><th>테이블</th><th>설명</th></tr>
  <tr><td>프로그램 관리</td><td>LETTNPROGRMLIST</td><td>프로그램 파일·URL 관리</td></tr>
  <tr><td>개인 기준일자</td><td>LETTNBASEDATE</td><td>사용자별 기본 기준년월 설정</td></tr>
</table>

<hr>
<a name="data"></a>
<h1>🗄️ 데이터 탐색</h1>
<p><b>데이터 브라우저</b>는 DB의 모든 테이블을 직접 탐색할 수 있는 개발자·관리자용 화면입니다.</p>
<ul>
  <li>왼쪽 패널에서 테이블 선택 → 오른쪽 그리드에 해당 테이블 내용 표시</li>
  <li>테이블 검색 기능 제공</li>
  <li>페이지네이션 및 Excel 내보내기 지원</li>
</ul>

<hr>
<a name="tables"></a>
<h1>📌 DB 테이블 구조</h1>
<h2>주요 테이블 접두사 규칙</h2>
<table>
  <tr><th>접두사</th><th>구분</th><th>예시</th></tr>
  <tr><td><code>E_IR_</code></td><td>금리 관련 테이블</td><td>E_IR_CURVE_SPOT, E_IR_DCNT_RATE_BIZ</td></tr>
  <tr><td><code>E_IR_..._USR</code></td><td>사용자 입력 테이블</td><td>E_IR_PARAM_SW_USR, E_IR_DCNT_RATE_USR</td></tr>
  <tr><td><code>E_IR_..._BIZ</code></td><td>비즈(업무) 적용 결과</td><td>E_IR_DCNT_RATE_BIZ, E_IR_SPRD_AFNS_BIZ</td></tr>
  <tr><td><code>E_IR_..._CALC</code></td><td>계산 중간/결과</td><td>E_IR_PARAM_HW_CALC, E_IR_SPRD_AFNS_CALC</td></tr>
  <tr><td><code>E_RC_</code></td><td>신용 위험 테이블</td><td>E_RC_CORP_PD, E_RC_CORP_TM</td></tr>
  <tr><td><code>E_CO_</code></td><td>공통 메타/작업</td><td>E_CO_ESG_META, E_CO_JOB_INFO</td></tr>
  <tr><td><code>LETTN</code></td><td>eGov 시스템 테이블</td><td>LETTNMENUINFO, LETTNAUTHORINFO</td></tr>
  <tr><td><code>COMTN</code></td><td>eGov 배치 테이블</td><td>COMTNBATCHOPERT, COMTNBATCHSCHDUL</td></tr>
  <tr><td><code>APP_</code></td><td>신규 앱 테이블</td><td>APP_USER</td></tr>
</table>

<h2>PK 구조 패턴</h2>
<table>
  <tr><th>패턴</th><th>설명</th></tr>
  <tr><td><code>base_yymm</code></td><td>기준년월 (YYYYMM 형식)</td></tr>
  <tr><td><code>base_date</code></td><td>기준일자 (YYYYMMDD 형식)</td></tr>
  <tr><td><code>ir_curve_id</code></td><td>금리 커브 ID (예: KRW_GOV)</td></tr>
  <tr><td><code>ir_model_id</code></td><td>금리 모형 ID (예: HW1F, SW, AFNS)</td></tr>
  <tr><td><code>mat_cd</code></td><td>만기 코드 (예: 1Y, 3Y, 5Y, 10Y)</td></tr>
  <tr><td><code>appl_biz_dv</code></td><td>적용업무 구분 (KICS, IFRS, IBIZ, SAAS)</td></tr>
  <tr><td><code>ir_curve_sce_no</code></td><td>금리커브 시나리오 번호 (Integer)</td></tr>
</table>

<hr>
<a name="faq"></a>
<h1>❓ 자주 묻는 질문</h1>

<h3>Q. 조회 버튼을 눌러도 데이터가 나오지 않습니다.</h3>
<p>상단 툴바의 <b>기준년월</b>이 DB 데이터와 일치하는지 확인하세요.
기준년월은 YYYYMM 형식이며, 각 화면은 이 값을 기준으로 필터링합니다.</p>

<h3>Q. 저장 버튼을 눌렀는데 "저장할 변경 사항이 없습니다"가 뜹니다.</h3>
<p>CRUD 화면에서 ➕추가 / ✏️수정 / 🗑️삭제 버튼으로 변경을 먼저 수행한 후 💾저장을 눌러야 합니다.
그리드 셀 직접 편집 후에도 저장 가능합니다.</p>

<h3>Q. 메뉴를 추가했는데 화면이 열리지 않습니다.</h3>
<p>메뉴 목록 관리에서 <b>뷰 키</b>가 <code>_lazy_views()</code>에 등록된 키와 정확히 일치해야 합니다.
등록되지 않은 뷰 키를 입력하면 탭이 열리지 않습니다.</p>

<h3>Q. Excel Import 시 일부 행만 실패합니다.</h3>
<p>PK가 중복되거나 필수 컬럼이 빈 경우 해당 행만 실패합니다.
Import 완료 메시지에서 "성공/실패 건수"를 확인할 수 있습니다.</p>

<h3>Q. DB 파일 위치는 어디인가요?</h3>
<p>개발 환경: <code>&lt;프로젝트루트&gt;/data/esg.db</code><br>
패키징 실행: <code>&lt;실행파일 폴더&gt;/data/esg.db</code></p>

<h3>Q. 비밀번호를 잊어버렸습니다.</h3>
<p>프로젝트 루트의 <code>reset_admin.py</code>를 실행하면 admin 계정 비밀번호를
<code>admin</code>으로 초기화할 수 있습니다.</p>
"""
    return f"<html><head>{css}</head><body style='padding:20px 28px;'>{body}</body></html>"


# ─── HelpView 위젯 ─────────────────────────────────────────────────────
class HelpView(QWidget):
    VIEW_TITLE = "📖 도움말"

    def __init__(self, user: AppUser, parent=None):
        super().__init__(parent)
        self.user = user
        self._build_ui()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setHandleWidth(4)
        splitter.setChildrenCollapsible(False)

        # ── 왼쪽: 목차 ──────────────────────────────────────────────
        left = QWidget()
        left.setMinimumWidth(170)
        left.setMaximumWidth(250)
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(0)

        # 목차 헤더
        toc_header = QLabel("  목차")
        toc_header.setFixedHeight(36)
        toc_header.setStyleSheet(
            "background:#1E3A5F; color:white; font-size:13px; font-weight:bold;")
        left_layout.addWidget(toc_header)

        # 검색
        search_row = QHBoxLayout()
        search_row.setContentsMargins(4, 4, 4, 4)
        search_row.setSpacing(2)
        self._search = QLineEdit()
        self._search.setPlaceholderText("검색…")
        self._search.setStyleSheet(
            "QLineEdit { border:1px solid #CBD5E1; border-radius:3px;"
            "  padding:2px 6px; font-size:12px; }")
        search_row.addWidget(self._search)
        btn_clr = QToolButton()
        btn_clr.setText("✕")
        btn_clr.setFixedSize(22, 22)
        btn_clr.setStyleSheet("font-size:10px;")
        btn_clr.clicked.connect(self._search.clear)
        search_row.addWidget(btn_clr)
        left_layout.addLayout(search_row)

        # 목차 리스트
        self._toc_list = QListWidget()
        self._toc_list.setStyleSheet(
            "QListWidget { border:none; background:#F8FAFC; font-size:12px; }"
            "QListWidget::item { padding:5px 10px; border-bottom:1px solid #F1F5F9; }"
            "QListWidget::item:selected { background:#DBEAFE; color:#1D4ED8; }"
            "QListWidget::item:hover    { background:#EFF6FF; }"
        )
        for label, anchor in _TOC:
            item = QListWidgetItem(label)
            if anchor is None:
                # 구분선 항목
                item.setFlags(Qt.ItemFlag.NoItemFlags)
                item.setForeground(Qt.GlobalColor.gray)
                font = QFont()
                font.setPointSize(9)
                item.setFont(font)
            else:
                item.setData(Qt.ItemDataRole.UserRole, anchor)
            self._toc_list.addItem(item)
        self._toc_list.itemClicked.connect(self._on_toc_click)
        left_layout.addWidget(self._toc_list, stretch=1)

        splitter.addWidget(left)

        # ── 오른쪽: 본문 ─────────────────────────────────────────────
        right = QWidget()
        right_layout = QVBoxLayout(right)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        self._browser = QTextBrowser()
        self._browser.setOpenExternalLinks(True)
        self._browser.setStyleSheet(
            "QTextBrowser { border:none; background:#FFFFFF; }")
        self._browser.setHtml(_build_html())
        right_layout.addWidget(self._browser)

        splitter.addWidget(right)
        splitter.setSizes([200, 900])
        root.addWidget(splitter)

        # 검색어 연결
        self._search.textChanged.connect(self._on_search)

    # ── 슬롯 ────────────────────────────────────────────────────────
    def _on_toc_click(self, item: QListWidgetItem) -> None:
        anchor = item.data(Qt.ItemDataRole.UserRole)
        if anchor:
            self._browser.scrollToAnchor(anchor)

    def _on_search(self, text: str) -> None:
        """목차 항목 필터링."""
        for i in range(self._toc_list.count()):
            item = self._toc_list.item(i)
            anchor = item.data(Qt.ItemDataRole.UserRole)
            if anchor is None:
                item.setHidden(bool(text))
                continue
            item.setHidden(bool(text) and text.lower() not in item.text().lower())
