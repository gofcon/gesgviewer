# ESG PyQt6 그리드 기능 정리

공통 기반 클래스: `BaseListView` / `BaseCrudView` / `EsgTableModel` / `EsgEditableTableModel`

---

## 1. 아키텍처

| 클래스 | 파일 | 역할 |
|---|---|---|
| `BaseListView` | `ui/views/_base_list_view.py` | 조회 전용 뷰 기반 (정렬·필터·페이지·Excel) |
| `BaseCrudView` | `ui/views/_base_crud_view.py` | CRUD 뷰 기반 (추가·수정·삭제·저장·Import) |
| `EsgTableModel` | `ui/widgets/base_table_model.py` | 읽기 전용 테이블 모델 |
| `EsgEditableTableModel` | `ui/widgets/base_table_model.py` | 인라인 편집 + 배치 저장 모델 |

---

## 2. 배치 저장 (Batch Save)

모든 변경은 **in-memory 그리드**에만 반영되고, **💾 저장** 버튼을 눌러야 DB에 일괄 반영됩니다.

### 행 상태 색상

| 상태 | 색상 | 의미 |
|---|---|---|
| `new` | 연한 초록 `#DCFCE7` | 추가/복제됨, DB 미반영 |
| `modified` | 연한 주황 `#FED7AA` | 인라인 수정됨, DB 미반영 |
| *(없음)* | 기본 | 변경 없음 |
| 삭제 | — | 그리드에서 즉시 제거, `pending_deletes`에 보관 후 저장 시 DB DELETE |

### 배치 저장 흐름

```
그리드 편집 → in-memory 누적 → 💾 저장 클릭
→ get_pending() → { insert, update, delete }
→ _delete_row() → _save_row(is_new=True) → _save_row(is_new=False)
→ _load_data() 재조회
```

### PK 변경 처리

- 다이얼로그 수정 또는 인라인 수정으로 PK 변경 시 → **DELETE old + INSERT new** 자동 처리
- `_extra_deletions` 목록에 원본 보관

---

## 3. 버튼 레이아웃

```
[🔍 조회] [➕ 추가] [✏️ 수정] [🗑️ 삭제] [💾 저장]  ──  [📤 Import] [📥 Excel]
```

| 버튼 | 동작 |
|---|---|
| 🔍 조회 | 미저장 변경 경고 후 DB 재조회 |
| ➕ 추가 | 다이얼로그 입력 → 초록 행 삽입 |
| ✏️ 수정 | 선택된 행 다이얼로그 수정 → 주황 행 표시 |
| 🗑️ 삭제 | 그리드에서 즉시 제거 (저장 시 DB DELETE) |
| 💾 저장 | 누적된 변경 일괄 DB 반영 |
| 📤 Import | Excel 파일에서 일괄 import (즉시 DB 반영) |
| 📥 Excel | 현재 그리드 데이터 Excel export |

---

## 4. 우클릭 컨텍스트 메뉴

### 셀 우클릭 (`BaseCrudView`)

| 메뉴 | 동작 |
|---|---|
| ➕ 추가 | 추가 다이얼로그 열기 |
| 👁 보기 | 선택 행 읽기 전용 팝업 |
| ✏️ 수정 | 선택 행 수정 다이얼로그 |
| 📋 복제 | 선택 행 복제 → 아래 줄에 초록 행 삽입 + 첫 셀 편집 모드 |
| 🗑️ 삭제 | 선택 행 즉시 제거 |

### 헤더 우클릭 (`BaseListView`)

| 메뉴 | 동작 |
|---|---|
| ◀ 왼쪽 정렬 | 해당 컬럼 셀 내용 왼쪽 정렬 |
| ≡ 가운데 정렬 | 해당 컬럼 셀 내용 가운데 정렬 |
| ▶ 오른쪽 정렬 | 해당 컬럼 셀 내용 오른쪽 정렬 |

> 헤더 텍스트 자체는 항상 가운데 고정

---

## 5. 컬럼 너비 (`COLUMN_WIDTHS`)

각 뷰 클래스에 `COLUMN_WIDTHS` 딕셔너리를 정의합니다.

```python
COLUMN_WIDTHS = {
    'base_date':   100,       # Interactive: 초기 100px, 드래그 조절 가능
    'ir_curve_id': 'content', # ResizeToContents: 내용에 맞게 자동
    'mat_cd':       80,       # Interactive: 초기 80px, 드래그 조절 가능
    'ytm_rate':   'stretch',  # Stretch: 남은 공간 채움
}
```

| 값 | 모드 | 드래그 |
|---|---|---|
| 숫자 (예: `100`) | Interactive, 초기 너비 지정 | ✅ 가능 |
| `'content'` | ResizeToContents | ❌ 자동 |
| `'stretch'` | Stretch, 남은 공간 채움 | ❌ 자동 |
| 미지정 | Interactive | ✅ 가능 |
| `{}` (기본값) | 전체 ResizeToContents + 마지막 Stretch | — |

---

## 6. 정렬 (Sorting)

- 헤더 클릭: **오름차순 → 내림차순 → 원래 순서** 토글
- 숫자 컬럼도 올바르게 정렬 (`UserRole` 원본 값 기반 비교)
- 단일 컬럼 정렬만 지원 (멀티 컬럼 정렬은 미구현)

---

## 7. 실시간 필터 바

- 텍스트 입력 → 전체 컬럼 또는 선택 컬럼에서 실시간 필터링
- 대소문자 구분 없음
- ✕ 버튼으로 필터 초기화

---

## 8. 페이지 네비게이션

- `PaginationWidget`: ◀◀ ◀ [현재/전체 페이지] ▶ ▶▶
- 페이지 이동 시 미저장 변경 경고 (`BaseCrudView`)
- 기본 페이지 크기: `config/settings.py`의 `DEFAULT_PAGE_SIZE`

---

## 9. 셀 정렬 기본값

| 값 타입 | 기본 정렬 |
|---|---|
| `int`, `float` | 오른쪽 |
| `str`, `None` | 왼쪽 |
| 헤더 | 가운데 (고정) |

헤더 우클릭으로 컬럼별 오버라이드 가능.

---

## 10. 서브클래스 정의 항목

### `BaseCrudView` 필수/선택

```python
class MyView(BaseCrudView):
    HEADERS       = [("col_key", "헤더명"), ...]   # 필수
    VIEW_TITLE    = "화면 제목"                     # 필수
    EDITABLE_KEYS = {"col1", "col2"}               # 비PK 컬럼 (참고용)
    ADD_FIELDS    = [FormField(...), ...]           # 추가/수정 다이얼로그 필드
    COMBO_COLS    = {"col_key": ["옵션1", "옵션2"]} # 인라인 콤보박스
    COLUMN_WIDTHS = {"col_key": 80, ...}           # 컬럼 너비 (선택)

    def _save_row(self, data: dict, is_new: bool) -> bool: ...  # 필수
    def _delete_row(self, row: dict) -> bool: ...               # 필수
    def _load_data(self, page: int) -> None: ...                # 필수
    def _build_search_area(self) -> QWidget | None: ...         # 선택
```

---

## 11. 기타

- **행 번호 컬럼** (vertical header): 숨김 처리
- **행 선택 색상**: `#DBEAFE` (파란색 계열), 비활성 시 `#E2E8F0`
- **교대 행 색상**: `setAlternatingRowColors(True)`
- **행 높이**: 기본 22px
