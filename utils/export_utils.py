"""
Excel / CSV 내보내기 유틸
JSP: ExcelDownload 기능 → pandas + openpyxl 대응
"""
import os
from datetime import datetime
from PyQt6.QtWidgets import QFileDialog, QMessageBox


def export_to_excel(rows: list[dict], headers: list[str], keys: list[str],
                    default_name: str = "export") -> None:
    """
    rows    : list[dict] — 서비스 레이어 반환값
    headers : list[str]  — 컬럼 헤더 (표시용)
    keys    : list[str]  — 컬럼 키    (rows의 딕셔너리 키)
    """
    try:
        import pandas as pd
    except ImportError:
        QMessageBox.critical(None, "오류", "pandas 라이브러리가 필요합니다.\npip install pandas openpyxl")
        return

    if not rows:
        QMessageBox.information(None, "Excel 내보내기", "내보낼 데이터가 없습니다.")
        return

    from config.settings import EXPORT_DIR
    os.makedirs(EXPORT_DIR, exist_ok=True)

    ts   = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe = default_name.replace("/", "_").replace(" ", "_")
    default_path = os.path.join(EXPORT_DIR, f"{safe}_{ts}.xlsx")

    path, _ = QFileDialog.getSaveFileName(
        None,
        "Excel 파일 저장",
        default_path,
        "Excel 파일 (*.xlsx);;CSV 파일 (*.csv)",
    )
    if not path:
        return

    data = [{h: row.get(k, "") for h, k in zip(headers, keys)} for row in rows]
    df   = pd.DataFrame(data, columns=headers)

    try:
        if path.endswith(".csv"):
            df.to_csv(path, index=False, encoding="utf-8-sig")
        else:
            with pd.ExcelWriter(path, engine="openpyxl") as writer:
                df.to_excel(writer, sheet_name=safe[:31], index=False)
                ws = writer.sheets[safe[:31]]
                # 컬럼 너비 자동 조정
                for col in ws.columns:
                    max_len = max((len(str(cell.value or "")) for cell in col), default=10)
                    ws.column_dimensions[col[0].column_letter].width = min(max_len + 4, 40)
        QMessageBox.information(None, "완료", f"저장 완료:\n{path}")
    except Exception as e:
        QMessageBox.critical(None, "저장 실패", str(e))
