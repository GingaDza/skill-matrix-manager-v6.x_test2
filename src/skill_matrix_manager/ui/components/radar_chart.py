from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QRect, QPoint
from PyQt5.QtGui import QPainter, QPen, QColor, QPainterPath
import math

class RadarChartWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.target_values = {}
        self.current_values = {}
        self.animated_values = {}
        self.animation = None
        self.setMinimumSize(400, 400)

    def set_target_values(self, values):
        """目標値の設定"""
        self.target_values = values
        self.update()

    def set_current_values(self, values):
        """現在値の設定"""
        self.current_values = values
        self.animated_values = values.copy()
        self.update()

    def animate_to_values(self, new_values):
        """新しい値へアニメーション"""
        if self.animation:
            self.animation.stop()

        # アニメーションの開始値と終了値を設定
        start_values = self.animated_values.copy()
        self.target_animation_values = new_values

        # アニメーションタイマーの設定
        self.animation_progress = 0
        self.animation = QTimer(self)
        self.animation.timeout.connect(self._update_animation)
        self.animation.start(16)  # 約60FPS

    def _update_animation(self):
        """アニメーションの更新"""
        self.animation_progress += 0.05
        if self.animation_progress >= 1:
            self.animation.stop()
            self.animated_values = self.target_animation_values.copy()
            self.update()
            return

        # イージング関数を使用して補間
        t = self.animation_progress
        t = 1 - math.pow(1 - t, 3)  # cubic ease-out

        # 値の補間
        for skill in self.animated_values:
            start = float(self.current_values[skill])
            end = float(self.target_animation_values[skill])
            self.animated_values[skill] = start + (end - start) * t

        self.update()

    def paintEvent(self, event):
        """レーダーチャートの描画"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # チャートの中心と半径
        center_x = self.width() / 2
        center_y = self.height() / 2
        radius = min(center_x, center_y) * 0.8

        # 軸の数（スキルの数）
        num_skills = len(self.target_values)
        if num_skills < 3:
            return

        # 目標値のチャート描画
        self._draw_chart(painter, self.target_values, center_x, center_y, radius,
                        QColor(255, 200, 200, 128), QColor(255, 100, 100))

        # 現在値のチャート描画
        self._draw_chart(painter, self.animated_values, center_x, center_y, radius,
                        QColor(200, 200, 255, 128), QColor(100, 100, 255))

        # 軸とラベルの描画
        self._draw_axes(painter, int(center_x), int(center_y), int(radius))

    def _draw_chart(self, painter, values, cx, cy, radius, fill_color, line_color):
        """チャートの描画"""
        num_skills = len(values)
        path = QPainterPath()
        first_point = True

        for i, (skill, value) in enumerate(values.items()):
            angle = i * (2 * math.pi / num_skills) - math.pi / 2
            x = cx + radius * (float(value) / 5) * math.cos(angle)
            y = cy + radius * (float(value) / 5) * math.sin(angle)
            
            if first_point:
                path.moveTo(x, y)
                first_point = False
            else:
                path.lineTo(x, y)

        path.closeSubpath()

        # 塗りつぶし
        painter.setBrush(fill_color)
        painter.setPen(Qt.NoPen)
        painter.drawPath(path)

        # 輪郭線
        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(line_color, 2))
        painter.drawPath(path)

    def _draw_axes(self, painter, cx, cy, radius):
        """軸とラベルの描画"""
        num_skills = len(self.target_values)
        painter.setPen(QPen(Qt.gray, 1))

        # 同心円の描画
        for i in range(1, 6):
            r = int(radius * i / 5)
            painter.drawEllipse(cx - r, cy - r, r * 2, r * 2)

        # 軸とラベルの描画
        for i, skill in enumerate(self.target_values.keys()):
            angle = i * (2 * math.pi / num_skills) - math.pi / 2
            end_x = int(cx + radius * math.cos(angle))
            end_y = int(cy + radius * math.sin(angle))
            
            # 軸線の描画
            painter.drawLine(cx, cy, end_x, end_y)
            
            # ラベルの描画
            label_x = int(cx + (radius + 20) * math.cos(angle))
            label_y = int(cy + (radius + 20) * math.sin(angle))
            
            painter.save()
            painter.translate(label_x, label_y)
            painter.rotate(angle * 180 / math.pi + 90)
            painter.drawText(-50, -5, 100, 10, Qt.AlignCenter, skill)
            painter.restore()
