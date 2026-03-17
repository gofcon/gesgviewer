"""
앱 전역 설정
- 개발 환경: 소스 트리 내 data/, exports/ 사용
- 패키징 환경: main.py가 ESG_DATA_DIR / ESG_EXPORT_DIR 환경변수를 설정
"""
import os
import sys

# ─── 기본 루트 경로 ─────────────────────────────────────────────
if getattr(sys, "frozen", False):
    # PyInstaller 패키징 실행파일: 실행파일이 위치한 폴더 기준
    BASE_DIR = os.path.dirname(sys.executable)
else:
    # 개발 환경: 프로젝트 루트 기준
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ───────────────────────────────────────────────
# DB 설정
# ───────────────────────────────────────────────
_data_dir = os.environ.get("ESG_DATA_DIR", os.path.join(BASE_DIR, "data"))
DB_PATH   = os.path.join(_data_dir, "esg.db")
DB_URL    = f"sqlite:///{DB_PATH}"

# ───────────────────────────────────────────────
# 앱 설정
# ───────────────────────────────────────────────
APP_TITLE   = "ESG 금리 파라미터 관리 시스템"
APP_VERSION = "1.0.0"
WINDOW_WIDTH  = 1400
WINDOW_HEIGHT = 900

# ───────────────────────────────────────────────
# 페이징 기본값
# ───────────────────────────────────────────────
DEFAULT_PAGE_SIZE = 20

# ───────────────────────────────────────────────
# Excel 내보내기 저장 경로
# ───────────────────────────────────────────────
EXPORT_DIR = os.environ.get("ESG_EXPORT_DIR", os.path.join(BASE_DIR, "exports"))
