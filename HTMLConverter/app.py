import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QFileDialog,
    QVBoxLayout, QHBoxLayout, QSpinBox, QFormLayout, QLabel
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, QMarginsF
from PyQt5.QtGui import QPageLayout, QPageSize

class HtmlToPdfConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Advanced HTML to PDF Converter")
        self.setGeometry(100, 100, 1000, 800)

        self.web_view = QWebEngineView()

        # Buttons
        self.open_btn = QPushButton("Open HTML")
        self.open_btn.clicked.connect(self.load_html)

        self.export_btn = QPushButton("Export PDF")
        self.export_btn.clicked.connect(self.export_pdf)

        # Controls
        self.width_input = QSpinBox()
        self.width_input.setRange(300, 5000)
        self.width_input.setValue(1200)

        self.height_input = QSpinBox()
        self.height_input.setRange(300, 5000)
        self.height_input.setValue(1600)

        self.margin_input = QSpinBox()
        self.margin_input.setRange(0, 100)
        self.margin_input.setValue(10)

        # Crop controls
        self.crop_x = QSpinBox(); self.crop_y = QSpinBox()
        self.crop_w = QSpinBox(); self.crop_h = QSpinBox()
        for spin in [self.crop_x, self.crop_y, self.crop_w, self.crop_h]:
            spin.setRange(0, 5000)

        form = QFormLayout()
        form.addRow("Viewport Width:", self.width_input)
        form.addRow("Viewport Height:", self.height_input)
        form.addRow("Margins:", self.margin_input)
        form.addRow("Crop X:", self.crop_x)
        form.addRow("Crop Y:", self.crop_y)
        form.addRow("Crop Width:", self.crop_w)
        form.addRow("Crop Height:", self.crop_h)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.open_btn)
        btn_layout.addWidget(self.export_btn)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addLayout(btn_layout)
        layout.addWidget(self.web_view)

        self.setLayout(layout)
        self.current_file = None

    def load_html(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open HTML", "", "HTML Files (*.html *.htm)")
        if path:
            self.current_file = path
            self.web_view.load(QUrl.fromLocalFile(path))

    def export_pdf(self):
        if not self.current_file:
            return

        save_path, _ = QFileDialog.getSaveFileName(self, "Save PDF", "output.pdf", "PDF Files (*.pdf)")
        if not save_path:
            return

        width = self.width_input.value()
        height = self.height_input.value()
        margin = self.margin_input.value()

        # Set viewport size (IMPORTANT for accurate rendering)
        self.web_view.resize(width, height)

        # Apply crop using CSS injection
        crop_x = self.crop_x.value()
        crop_y = self.crop_y.value()
        crop_w = self.crop_w.value()
        crop_h = self.crop_h.value()

        crop_script = """
        document.body.style.overflow = 'hidden';
        document.body.style.position = 'relative';
        document.body.style.left = '-%dpx';
        document.body.style.top = '-%dpx';
        document.body.style.width = '%dpx';
        document.body.style.height = '%dpx';
        """ % (crop_x, crop_y, crop_w if crop_w else width, crop_h if crop_h else height)

        def after_crop():
            margins = QMarginsF(margin, margin, margin, margin)
            layout = QPageLayout(QPageSize(QPageSize.A4), QPageLayout.Portrait, margins)

            self.web_view.page().printToPdf(save_path, layout)
            print("PDF saved:", save_path)

        # Inject crop JS before export
        self.web_view.page().runJavaScript(crop_script, lambda _: after_crop())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = HtmlToPdfConverter()
    win.show()
    sys.exit(app.exec_())
