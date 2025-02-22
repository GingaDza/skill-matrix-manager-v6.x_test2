from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog
from PyQt5.QtGui import QPainter, QPen, QColor, QFont
from PyQt5.QtCore import Qt, QPointF
from .chart_export import ChartExporter
import math

class RadarChartWidget(QWidget):
    def __init__(self, dual_chart=False, parent=None):
        super().__init__(parent)
        self.dual_chart = dual_chart
        self.data = []
        self.target_data = []
        self.labels = []
        self.exporter = ChartExporter(self)
        self.setMinimumSize(400, 400)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        
        # エクスポートボタンの追加
        export_layout = QVBoxLayout()
        
        export_image_btn = QPushButton("画像として保存")
        export_image_btn.clicked.connect(self._export_as_image)
        export_layout.addWidget(export_image_btn)
        
        export_pdf_btn = QPushButton("PDFとして保存")
        export_pdf_btn.clicked.connect(self._export_as_pdf)
        export_layout.addWidget(export_pdf_btn)
        
        export_data_btn = QPushButton("データとして保存")
        export_data_btn.clicked.connect(self._export_data)
        export_layout.addWidget(export_data_btn)
        
        layout.addLayout(export_layout)

    def set_data(self, data, labels, target_data=None):
        self.data = data
        self.labels = labels
        if target_data:
            self.target_data = target_data
        self.update()

    def _export_as_image(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "チャートを画像として保存",
            "",
            "PNG Images (*.png);;All Files (*)"
        )
        if file_path:
            self.exporter.export_as_image(file_path)

    def _export_as_pdf(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "チャートをPDFとして保存",
            "",
            "PDF Files (*.pdf);;All Files (*)"
        )
        if file_path:
            self.exporter.export_as_pdf(file_path)

    def _export_data(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "チャートデータを保存",
            "",
            "JSON Files (*.json);;All Files (*)"
        )
        if file_path:
            data = {
                "labels": self.labels,
                "data": self.data,
                "target_data": self.target_data if self.dual_chart else None
            }
            self.exporter.export_data_as_json(data, file_path)

    def paintEvent(self, event):
        if not self.data:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # チャートの中心と半径を計算
        center = QPointF(self.width() / 2, self.height() / 2)
        radius = min(self.width(), self.height()) * 0.4

        # 軸を描画
        self._draw_axes(painter, center, radius)
        
        # データを描画
        self._draw_data(painter, center, radius)
        
        if self.dual_chart and self.target_data:
            # 目標データを描画
            self._draw_data(painter, center, radius, True)

    def _draw_axes(self, painter, center, radius):
        n_axes = len(self.labels)
        if n_axes < 3:
            return

        # 軸を描画
        painter.setPen(QPen(Qt.gray, 1))
        for i in range(n_axes):
            angle = i * 2 * math.pi / n_axes - math.pi / 2  # 最初の軸を12時の位置に
            end_point = QPointF(
                center.x() + radius * math.cos(angle),
                center.y() + radius * math.sin(angle)
            )
            painter.drawLine(center.toPoint(), end_point.toPoint())

        # レベルの円を描画
        for level in range(1, 6):  # 1から5までのレベル
            r = radius * level / 5
            painter.drawEllipse(center, r, r)

        # ラベルを描画
        font = painter.font()
        font.setPointSize(10)
        painter.setFont(font)
        
        for i, label in enumerate(self.labels):
            angle = i * 2 * math.pi / n_axes - math.pi / 2
            point = QPointF(
                center.x() + (radius + 20) * math.cos(angle),
                center.y() + (radius + 20) * math.sin(angle)
            )
            
            # ラベルの配置を調整
            flags = Qt.AlignCenter
            rect = painter.fontMetrics().boundingRect(label)
            rect.moveCenter(point.toPoint())
            painter.drawText(rect, flags, label)

    def _draw_data(self, painter, center, radius, is_target=False):
        n_points = len(self.data)
        if n_points < 3:
            return

        # データポイントの座標を計算
        points = []
        data = self.target_data if is_target else self.data
        
        for i, value in enumerate(data):
            angle = i * 2 * math.pi / n_points - math.pi / 2
            normalized_value = value / 5.0  # スキルレベルは1-5を想定
            point = QPointF(
                center.x() + radius * normalized_value * math.cos(angle),
                center.y() + radius * normalized_value * math.sin(angle)
            )
            points.append(point)

        # データラインの描画
        color = QColor(0, 0, 255, 128) if is_target else QColor(255, 0, 0, 128)
        painter.setPen(QPen(color, 2))
        
        # ポリゴンを塗りつぶし
        painter.setBrush(QColor(color.red(), color.green(), color.blue(), 32))
        
        # データポイントを接続
        for i in range(n_points):
            next_i = (i + 1) % n_points
            painter.drawLine(points[i], points[next_i])

