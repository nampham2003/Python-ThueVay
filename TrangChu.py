from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow

class TrangChu_w(QMainWindow):
    def __init__(self, widget):
        super(TrangChu_w, self).__init__()
        self.widget = widget
        self.load_ui()
        self.QLTK.clicked.connect(self.kho_form)

    def load_ui(self):
        uic.loadUi('TrangChu.ui', self)

    def kho_form(self):
        self.widget.setCurrentIndex(2)  # Chuyển đến Kho
