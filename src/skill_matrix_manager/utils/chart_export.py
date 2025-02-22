from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QSize, QRectF, QPoint
from PyQt5.QtGui import QPainter, QImage, QPdfWriter
from PyQt5.QtPrintSupport import QPrinter
import json
from pathlib import Path
from datetime import datetime

class ChartExporter:
    def __init__(self, chart_widget):
        self.chart_widget = chart_widget
        self.export_dir = Path("exports")
        self.export_dir.mkdir(exist_ok=True)

    def export_as_image(self, filename=None):
        if filename is None:
            filename = f"chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        
        filepath = self.export_dir / filename
        
        # ウィジェットの内容を画像として取得
        size = self.chart_widget.size()
        image = QImage(size, QImage.Format_ARGB32)
        image.fill(Qt.white)
        
        painter = QPainter(image)
        self.chart_widget.render(painter, QPoint(0, 0))
        painter.end()
        
        # 画像を保存
        success = image.save(str(filepath))
        return str(filepath) if success else None

    def export_as_pdf(self, filename=None):
        if filename is None:
            filename = f"chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            
        filepath = self.export_dir / filename
        
        # PDFプリンターの設定
        printer = QPrinter(QPrinter.HighResolution)
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setOutputFileName(str(filepath))
        printer.setPageSize(QPrinter.A4)
        
        # チャートのサイズを取得
        size = self.chart_widget.size()
        
        # PDFへの描画
        painter = QPainter()
        if painter.begin(printer):
            # チャートをページの中央に配置
            margin = 50  # マージン
            scale = min(
                (printer.width() - 2 * margin) / size.width(),
                (printer.height() - 2 * margin) / size.height()
            )
            
            painter.translate(printer.width() / 2, printer.height() / 2)
            painter.scale(scale, scale)
            painter.translate(-size.width() / 2, -size.height() / 2)
            
            self.chart_widget.render(painter)
            painter.end()
            return str(filepath)
        return None

    def export_data_as_json(self, data, filename=None):
        if filename is None:
            filename = f"chart_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
        filepath = self.export_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        return str(filepath)
