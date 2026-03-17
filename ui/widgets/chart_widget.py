"""
matplotlib 기반 차트 위젯
C3.js/D3.js(JSP) → FigureCanvasQTAgg (PyQt6) 대응
"""
import matplotlib
matplotlib.use("QtAgg")

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT
from PyQt6.QtWidgets import QWidget, QVBoxLayout


class ChartWidget(QWidget):
    """
    사용법:
        chart = ChartWidget()
        chart.plot_line(x_vals, y_series, title="HW 파라미터 추이")
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure, self.ax = plt.subplots(figsize=(8, 4), tight_layout=True)
        self.canvas  = FigureCanvasQTAgg(self.figure)
        self.toolbar = NavigationToolbar2QT(self.canvas, self)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

    def clear(self) -> None:
        self.ax.cla()
        self.canvas.draw()

    def plot_line(self, x_labels: list, y_series: dict[str, list],
                  title: str = "", x_label: str = "", y_label: str = "") -> None:
        """
        꺾은선 그래프
        y_series: {"시리즈명": [값, ...], ...}
        x_labels: X축 레이블 목록 (만기코드, 날짜 등)
        """
        self.ax.cla()
        x_idx = range(len(x_labels))
        for name, vals in y_series.items():
            self.ax.plot(x_idx, vals, marker="o", markersize=3, linewidth=1.2, label=name)

        self.ax.set_xticks(list(x_idx))
        self.ax.set_xticklabels(x_labels, rotation=45, fontsize=7)
        if title:
            self.ax.set_title(title, fontsize=10)
        if x_label:
            self.ax.set_xlabel(x_label, fontsize=8)
        if y_label:
            self.ax.set_ylabel(y_label, fontsize=8)
        if y_series:
            self.ax.legend(fontsize=8)
        self.ax.grid(True, linestyle="--", alpha=0.4)
        self.figure.tight_layout()
        self.canvas.draw()

    def plot_bar(self, x_labels: list, y_series: dict[str, list],
                 title: str = "") -> None:
        """막대 그래프"""
        self.ax.cla()
        n = len(y_series)
        width = 0.8 / max(n, 1)
        x_idx = list(range(len(x_labels)))
        for i, (name, vals) in enumerate(y_series.items()):
            offset = [xi + width * (i - n / 2 + 0.5) for xi in x_idx]
            self.ax.bar(offset, vals, width=width * 0.9, label=name)

        self.ax.set_xticks(x_idx)
        self.ax.set_xticklabels(x_labels, rotation=45, fontsize=7)
        if title:
            self.ax.set_title(title, fontsize=10)
        if y_series:
            self.ax.legend(fontsize=8)
        self.ax.grid(True, axis="y", linestyle="--", alpha=0.4)
        self.figure.tight_layout()
        self.canvas.draw()
