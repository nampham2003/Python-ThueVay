from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem, QComboBox
from DB_Connect import create_connection

class QLTK_w(QMainWindow):
    def __init__(self, widget):
        super(QLTK_w, self).__init__()
        self.widget = widget
        self.load_ui()
        self.themtk.clicked.connect(self.qltk)
        self.suatk.clicked.connect(self.sua_qltk)
        self.xoatk.clicked.connect(self.xoa_qltk)
        self.thoat.clicked.connect(self.ve_trang_chu)
        self.table_QLTK.cellClicked.connect(self.load_selected_row)
        self.timkiem.clicked.connect(self.tim_kiem)
        self.user_cbx.currentIndexChanged.connect(self.load_user_from_combobox)  # ComboBox selection
        self.selected_user = None  # Track selected user for editing/deleting
        self.load_data()
        self.load_user_combobox()
        
    def ve_trang_chu(self):
        self.widget.setCurrentIndex(1)  # Chuyển đến TrangChu

    def load_ui(self):
        uic.loadUi('QLTK.ui', self)

    def qltk(self):
        un = self.TK_text.text()
        psw = self.MK_text.text()

        db = create_connection()
        if db is None:
            return

        query = db.cursor()
        try:
            sql_insert_01 = "INSERT INTO login (user, pass) VALUES (%s, %s)"
            query.execute(sql_insert_01, (un, psw))
            db.commit()
            QMessageBox.information(self, "Thêm người dùng", "Người dùng mới đã được thêm thành công")
            self.load_data()
            self.load_user_combobox()  # Reload ComboBox after insertion
            self.clear_inputs()

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Lỗi cơ sở dữ liệu", f"Lỗi: {err}")
        finally:
            query.close()
            db.close()

    def sua_qltk(self):
        un = self.TK_text.text()
        psw = self.MK_text.text()

        if not self.selected_user:
            QMessageBox.warning(self, "Chỉnh sửa", "Hãy chọn tài khoản để chỉnh sửa.")
            return

        db = create_connection()
        if db is None:
            return

        query = db.cursor()
        try:
            # Cập nhật thông tin người dùng
            sql_update_01 = "UPDATE login SET user = %s, pass = %s WHERE user = %s"
            query.execute(sql_update_01, (un, psw, self.selected_user))
            db.commit()
            QMessageBox.information(self, "Chỉnh sửa", "Thông tin người dùng đã được cập nhật thành công")
            self.load_data()
            self.load_user_combobox()  # Reload ComboBox after updating
            self.clear_inputs()

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Lỗi cơ sở dữ liệu", f"Lỗi: {err}")
        finally:
            query.close()
            db.close()

    def xoa_qltk(self):
        if not self.selected_user:
            QMessageBox.warning(self, "Xóa", "Hãy chọn tài khoản để xóa.")
            return

        reply = QMessageBox.question(self, "Xóa tài khoản", 
                                     f"Bạn có chắc muốn xóa tài khoản '{self.selected_user}' không?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.No:
            return

        db = create_connection()
        if db is None:
            return

        query = db.cursor()
        try:
            # Xóa thông tin người dùng
            sql_delete_01 = "DELETE FROM login WHERE user = %s"
            query.execute(sql_delete_01, (self.selected_user,))
            db.commit()
            QMessageBox.information(self, "Xóa", "Tài khoản đã được xóa thành công")
            self.load_data()
            self.load_user_combobox()  # Reload ComboBox after deletion
            self.clear_inputs()

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Lỗi cơ sở dữ liệu", f"Lỗi: {err}")
        finally:
            query.close()
            db.close()

    def load_selected_row(self, row, column):
        # Lấy dữ liệu từ dòng đã chọn và điền vào các trường nhập liệu
        self.selected_user = self.table_QLTK.item(row, 0).text()
        self.TK_text.setText(self.table_QLTK.item(row, 0).text())
        self.MK_text.setText(self.table_QLTK.item(row, 1).text())
        # Đồng bộ QComboBox với lựa chọn trên bảng
        index = self.user_cbx.findText(self.selected_user)
        if index >= 0:
            self.user_cbx.setCurrentIndex(index)

    def load_data(self, search_term=None):
        db = create_connection()
        if db is None:
            return

        query = db.cursor()
        try:
            if search_term:
                query.execute("SELECT user, pass FROM login WHERE user LIKE %s", (f'%{search_term}%',))
            else:
                query.execute("SELECT user, pass FROM login")

            rows = query.fetchall()
            
            self.table_QLTK.setRowCount(len(rows))
            self.table_QLTK.setColumnCount(2)
            self.table_QLTK.setHorizontalHeaderLabels(["Tài khoản", "Mật khẩu"])

            for row_num, row_data in enumerate(rows):
                for col_num, col_data in enumerate(row_data):
                    self.table_QLTK.setItem(row_num, col_num, QTableWidgetItem(str(col_data)))

            self.selected_user = None  # Reset selection

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Lỗi cơ sở dữ liệu", f"Lỗi: {err}")
        finally:
            query.close()
            db.close()

    def clear_inputs(self):
        # Xóa nội dung trong các trường nhập liệu
        self.TK_text.clear()
        self.MK_text.clear()
        self.selected_user = None
        self.user_cbx.setCurrentIndex(-1)  # Reset QComboBox selection

    def tim_kiem(self):
        search_term = self.TK_text.text()
        self.load_data(search_term)

    def load_user_combobox(self):
        db = create_connection()
        if db is None:
            return

        query = db.cursor()
        try:
            query.execute("SELECT user FROM login")
            users = query.fetchall()

            self.user_cbx.clear()
            self.user_cbx.addItem("Chọn tài khoản")
            for user in users:
                self.user_cbx.addItem(user[0])

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Lỗi cơ sở dữ liệu", f"Lỗi: {err}")
        finally:
            query.close()
            db.close()

    def load_user_from_combobox(self):
        # Khi người dùng chọn từ ComboBox, cập nhật các trường nhập liệu
        selected_user = self.user_cbx.currentText()
        if selected_user == "Chọn tài khoản" or not selected_user:
            self.clear_inputs()
            return

        db = create_connection()
        if db is None:
            return

        query = db.cursor()
        try:
            query.execute("SELECT user, pass FROM login WHERE user = %s", (selected_user,))
            user_data = query.fetchone()

            if user_data:
                self.TK_text.setText(user_data[0])
                self.MK_text.setText(user_data[1])
                self.selected_user = user_data[0]  # Set selected user

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Lỗi cơ sở dữ liệu", f"Lỗi: {err}")
        finally:
            query.close()
            db.close()
