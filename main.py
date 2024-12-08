from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QStackedWidget
import sys

from Login import Login_w
from TrangChu import TrangChu_w
from  QLTK import QLTK_w
from DanhMuc import DanhMuc_w
from kho import Kho_w

def main():
    app = QApplication(sys.argv)
    widget = QStackedWidget()

    login_f = Login_w(widget)
    trang_chu_f = TrangChu_w(widget)
    qltk_f = QLTK_w(widget)
    danh_muc_f = DanhMuc_w()
    kho_f = Kho_w()

    widget.addWidget(login_f)      # Index 0
    widget.addWidget(trang_chu_f)  # Index 1
    widget.addWidget(qltk_f)       # Index 2
    widget.addWidget(danh_muc_f)   # Index 3
    widget.addWidget(kho_f)        # Index 4

    widget.setCurrentIndex(0)
    widget.setFixedHeight(600)
    widget.setFixedWidth(800)
    widget.show()

    sys.exit(app.exec_())  # Note: exec_() is used in PyQt5

if __name__ == '__main__':
    main()
