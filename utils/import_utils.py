"""
Excel / CSV 불러오기 유틸
export_utils.py 대칭 — pandas + openpyxl 사용
"""
from PyQt6.QtWidgets import QFileDialog, QMessageBox


def import_from_excel(parent, headers: list[tuple]) -> list[dict] | None:
    """
    .xlsx 또는 .csv 파일을 읽어 list[dict] 로 반환.

    Args:
        parent  : QWidget  — 다이얼로그 부모 위젯
        headers : list[(key, display_label)]  — HEADERS 형식
                  Excel 헤더(display_label) 또는 키(key) 모두 허용

    Returns:
        list[dict]  — rows 형식 (키 기준 dict), 취소/오류 시 None
    """
    try:
        import pandas as pd
    except ImportError:
        QMessageBox.critical(parent, "오류",
                             "pandas 라이브러리가 필요합니다.\npip install pandas openpyxl")
        return None

    # ── 파일 선택 ─────────────────────────────────────────────────
    path, _ = QFileDialog.getOpenFileName(
        parent,
        "Excel / CSV 불러오기",
        "",
        "Excel/CSV 파일 (*.xlsx *.csv);;Excel 파일 (*.xlsx);;CSV 파일 (*.csv)",
    )
    if not path:
        return None

    # ── 파일 읽기 ─────────────────────────────────────────────────
    try:
        if path.lower().endswith(".csv"):
            df = pd.read_csv(path, encoding="utf-8-sig", dtype=str, keep_default_na=False)
        else:
            df = pd.read_excel(path, dtype=str, keep_default_na=False, engine="openpyxl")
    except Exception as exc:
        QMessageBox.critical(parent, "파일 읽기 오류", str(exc))
        return None

    if df.empty:
        QMessageBox.information(parent, "Import", "파일에 데이터가 없습니다.")
        return None

    # ── 컬럼 매핑: display_label → key (key 직접 사용도 허용) ──────
    label_to_key = {label: key for key, label in headers}
    key_set      = {key for key, _ in headers}

    col_map: dict[str, str] = {}
    for col in df.columns:
        col_s = str(col).strip()
        if col_s in label_to_key:
            col_map[col] = label_to_key[col_s]
        elif col_s in key_set:
            col_map[col] = col_s

    if not col_map:
        labels = ", ".join(label for _, label in headers)
        QMessageBox.warning(
            parent, "컬럼 불일치",
            f"파일의 헤더가 테이블 컬럼과 일치하지 않습니다.\n\n"
            f"기대 헤더 예시:\n{labels}",
        )
        return None

    # ── DataFrame → list[dict] ────────────────────────────────────
    df = df.rename(columns=col_map)

    # 빈 문자열을 None 으로 변환
    df = df.replace("", None)

    rows = df[[c for c in df.columns if c in key_set]].to_dict(orient="records")
    return rows if rows else None
