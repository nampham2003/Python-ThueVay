from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow

class Kho_w(QMainWindow):
    def __init__(self):
        super(Kho_w, self).__init__()
        self.load_ui()

    def load_ui(self):
        uic.loadUi('Kho.ui', self)
