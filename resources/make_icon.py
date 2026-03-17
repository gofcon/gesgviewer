"""
ESG 앱 아이콘 생성 유틸리티

실행 (소스 루트에서):
    python resources/make_icon.py

결과:
    resources/icon.png  — 런타임 로딩용 (256×256)
    resources/icon.ico  — PyInstaller EXE 아이콘용 (Windows)
"""
import sys
import os

# 소스 루트를 path에 추가 (PyQt6 임포트용)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPixmap, QPainter, QColor, QFont, QBrush, QPen, QLinearGradient
from PyQt6.QtCore import Qt, QRect, QRectF


def make_icon(size: int = 256) -> QPixmap:
    """ESG 로고 아이콘을 PyQt6 QPainter 로 그려 QPixmap 반환"""
    px = QPixmap(size, size)
    px.fill(Qt.GlobalColor.transparent)

    p = QPainter(px)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)

    m = size // 10                              # 여백
    body = QRectF(m, m, size - 2*m, size - 2*m)

    # ── 배경: 파란 원 ──────────────────────────────────────────
    grad = QLinearGradient(0, 0, size, size)
    grad.setColorAt(0.0, QColor("#1E40AF"))     # 진파랑
    grad.setColorAt(1.0, QColor("#3B82F6"))     # 밝은 파랑
    p.setBrush(QBrush(grad))
    p.setPen(Qt.PenStyle.NoPen)
    p.drawEllipse(body)

    # ── 텍스트 "ESG" ───────────────────────────────────────────
    font = QFont("Arial", size // 4, QFont.Weight.Bold)
    p.setFont(font)
    p.setPen(QPen(QColor("white")))
    p.drawText(QRect(0, 0, size, size), Qt.AlignmentFlag.AlignCenter, "ESG")

    p.end()
    return px


if __name__ == "__main__":
    app = QApplication.instance() or QApplication(sys.argv)

    out_dir = os.path.dirname(os.path.abspath(__file__))

    # PNG — 런타임 로딩용
    png_path = os.path.join(out_dir, "icon.png")
    px = make_icon(256)
    if px.save(png_path, "PNG"):
        print(f"[생성] {png_path}")
    else:
        print(f"[실패] PNG 저장 오류: {png_path}")

    # ICO — PyInstaller EXE 아이콘 (Windows 작업표시줄)
    ico_path = os.path.join(out_dir, "icon.ico")
    px_ico = make_icon(256)
    if px_ico.save(ico_path, "ICO"):
        print(f"[생성] {ico_path}")
    else:
        print(f"[참고] ICO 저장 실패 (Linux에서는 정상 — PNG 사용)")

    print("완료! main.py 에서 icon.png 가 자동 로딩됩니다.")
