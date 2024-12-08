from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from DB_Connect import create_connection

class Login_w(QMainWindow):
    def __init__(self, widget):
        super(Login_w, self).__init__()
        self.widget = widget
        self.load_ui()
        self.b1.clicked.connect(self.login)
        self.b2.clicked.connect(self.reg_form)

    def load_ui(self):
        uic.loadUi('Login.ui', self)

    def reg_form(self):
        self.widget.setCurrentIndex(1)  # Chuyển đến TrangChu

    def login(self):
        un = self.user.text()
        psw = self.pw.text()

        db = create_connection()
        if db is None:
            return

        query = db.cursor()
        try:
            query.execute("SELECT * FROM login WHERE user = %s AND pass = %s", (un, psw))
            kt = query.fetchone()
            if kt:
                QMessageBox.information(self, "Kết quả đăng nhập", "Đăng nhập thành công")
                self.widget.setCurrentIndex(1)  # Chuyển đến TrangChu
            else:
                QMessageBox.warning(self, "Kết quả đăng nhập", "Đăng nhập thất bại")

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Lỗi cơ sở dữ liệu", f"Lỗi: {err}")
        finally:
            query.close()
            db.close()
