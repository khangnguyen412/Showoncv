'''
các gói cài đặt thư viện cài đặt:
pip install wheel
pip install pipwin
pipwin refresh
pipwin install pyaudio
pip install pyttsx3
pip install speechrecognition
pyuic5 -x [tên file của qt].ui -o [tên file của python].py
pyuic5 window6_createadmin.ui -o window6_createadmin.py
pyuic5 window5_infouser.ui -o window5_infouser.py
pyuic5 window4_datatable.ui -o window4_datatable.py
pyuic5 window3_choosetable.ui -o window3_choosetable.py
pyuic5 window2_admissions.ui -o window2_admissions.py
pyuic5 window1_startup.ui -o window1_startup.py
Pip install PyQt5designer
Pip install PyQt5 tools
Pip install PyQt5
pip install pyinstaller
pyinstaller -w --add-data "database.db;." script.py
pyinstaller --onefile --windowed --icon=logo.ico --add-data "tuvantuyensinh.db;." tuvantuyensinh.py
pyinstaller --onefile --windowed --icon=logo.ico tuvantuyensinh.py
'''

import glob #xóa file save mp3
import random #lấy số ngẫu nhiên
import time #lấy thời gian(sleep)
import webbrowser #khởi động web
import playsound #thư viện chạy file mp3
import speech_recognition as lis #lấy giọng nói
from gtts import gTTS #lấy giọng nói của chị google
import mysql.connector #kết nối với mysql
import sys #thư viện hệ thống
import os #thư viện tương tác với hệ điều hành
from openpyxl import Workbook #xuất file excel
import re #thư viện xử lý chuỗi

#thư viện của qtdesigner
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QFileDialog
from PyQt5 import QtWidgets
from PyQt5.QtCore import QUrl, QTimer
from PyQt5.QtMultimedia import QMediaPlayer,QMediaContent

#kết nối file qt
from window1_startup import Ui_startup_window
from window2_admissions import Ui_admissions_window
from window3_choosetable import Ui_choosetable_window
from window4_datatable import Ui_datatable_window
from window5_infouser import Ui_userinfo_window
from window6_createadmin import Ui_createadmin_window

class Mainwindow:
    # *******************window1*********************

    # khởi chạy chương trình
    def __init__(self):
        self.window_startupwin = QMainWindow()
        self.uic_startupwin = Ui_startup_window()
        self.uic_startupwin.setupUi(self.window_startupwin)
        self.uic_startupwin.admissions_consultancy.clicked.connect(self.show_admissionswindow)
        self.uic_startupwin.loggin_admin.clicked.connect(self.show_choosetablewindow)

    # load form đăng nhập
    def show_startupwindow(self):
        self.window_startupwin.show()

    # *******************window2*********************

    # load form tư vấn tuyển sinh
    def show_admissionswindow(self):
        bot_process = "Chào mừng bạn đến với tư vấn tuyển sinh của trường Đại Học Văn Hiến"
        self.speakoutput(bot_process)
        self.window_startupwin.close()
        self.window_admissionswindow = QtWidgets.QMainWindow()
        self.uic_admissionswindow= Ui_admissions_window()
        self.uic_admissionswindow.setupUi(self.window_admissionswindow)
        self.window_admissionswindow.show()
        self.uic_admissionswindow.bot_output.setText(bot_process)
        self.uic_admissionswindow.signup.clicked.connect(self.btn_signup)
        self.uic_admissionswindow.question_send.clicked.connect(self.btn_sendadmissions)
        self.uic_admissionswindow.info_send.clicked.connect(self.btn_sendinfo)
        self.uic_admissionswindow.record.clicked.connect(self.btn_record)
        self.uic_admissionswindow.logout.clicked.connect(self.btn_logout_admissionswindow)
        self.uic_admissionswindow.refresh_button.clicked.connect(self.btn_resetwindow)
        self.loaddatahintquestion()

    # nút đăng ký
    def btn_signup(self):
        webbrowser.open('https://dangky.vhu.edu.vn/#/ChucNang/GhiDanh')

    # nút gửi
    def btn_sendadmissions(self):
        tensv = self.uic_admissionswindow.name_input.text()
        sdt = self.uic_admissionswindow.numberphone_input.text()
        checksdt = len(self.uic_admissionswindow.numberphone_input.text())
        self.timestop()
        if tensv == "" or sdt == "":
            bot_process = "bạn cho mình xin họ và tên và số điện thoại nhé"
            self.speakoutput(bot_process)
        elif tensv.replace(' ', '').isalpha() == False:
            bot_process = "bạn cho mình xin chính xác họ và tên"
            self.speakoutput(bot_process)
        elif sdt.isalnum() == False or checksdt != 10 or sdt.startswith('0') == False:
            bot_process = "bạn cho mình xin chính xác số điện thoại"
            self.speakoutput(bot_process)
        else:
            self.uic_admissionswindow.name_input.setDisabled(True)
            self.uic_admissionswindow.numberphone_input.setDisabled(True)
            self.uic_admissionswindow.info_send.setDisabled(True)
            if self.uic_admissionswindow.question_input.text().isspace() or self.uic_admissionswindow.question_input.text() == "":
                bot_process = "bạn chưa nhập câu hỏi"
                self.speakoutput(bot_process)
                self.uic_admissionswindow.bot_output.setText(bot_process)
            else:
                bot_process = self.get_response(self.uic_admissionswindow.question_input.text())
                self.speakoutput(bot_process)
                self.uic_admissionswindow.bot_output.setText(bot_process)
                ten = self.uic_admissionswindow.name_input.text()
                sdt = self.uic_admissionswindow.numberphone_input.text()
                cauhoi = self.uic_admissionswindow.question_input.text()
                cautl = self.uic_admissionswindow.bot_output.toPlainText()
                self.adddb_userinfowindow(ten, sdt, cauhoi, cautl)
                self.uic_admissionswindow.user_ouput.setText(self.uic_admissionswindow.question_input.text())
                self.loaddatahintquestion()
                self.timestart()

    # nút gửi thông tin
    def btn_sendinfo(self):
        tensv = self.uic_admissionswindow.name_input.text()
        sdt = self.uic_admissionswindow.numberphone_input.text()
        checksdt = len(self.uic_admissionswindow.numberphone_input.text())
        if tensv == "" or sdt == "":
            bot_process = "bạn cho mình xin họ và tên và số điện thoại nhé"
            self.speakoutput(bot_process)
        elif tensv.replace(' ', '').isalpha() == False:
            bot_process = "bạn cho mình xin chính xác họ và tên"
            self.speakoutput(bot_process)
        elif sdt.isalnum() == False or checksdt != 10 or sdt.startswith('0') == False:
            bot_process = "bạn cho mình xin chính xác số điện thoại"
            self.speakoutput(bot_process)
        else:
            self.uic_admissionswindow.name_input.setEnabled(False)
            self.uic_admissionswindow.numberphone_input.setEnabled(False)
            self.uic_admissionswindow.info_send.setEnabled(False)
            bot_process = "Chào " + self.uic_admissionswindow.name_input.text() + ". Chúng tôi giúp gì được cho bạn"
            self.speakoutput(bot_process)
            self.uic_admissionswindow.bot_output.setText(bot_process)
            self.uic_admissionswindow.name_input.setEnabled(False)
            self.uic_admissionswindow.numberphone_input.setEnabled(False)

    # nút ghi âm
    def btn_record(self):
        self.loaddatahintquestion()
        tensv = self.uic_admissionswindow.name_input.text()
        sdt = self.uic_admissionswindow.numberphone_input.text()
        checksdt = len(self.uic_admissionswindow.numberphone_input.text())
        self.timestop()
        if tensv == "" or sdt == "":
            bot_process = "bạn cho mình xin họ và tên và số điện thoại nhé"
            self.speakoutput(bot_process)
        elif tensv.replace(' ', '').isalpha() == False:
            bot_process = "bạn cho mình xin chính xác họ và tên"
            self.speakoutput(bot_process)
        elif sdt.isalnum() == False or checksdt != 10 or sdt.startswith('0') == False:
            bot_process = "bạn cho mình xin chính xác số điện thoại"
            self.speakoutput(bot_process)
        else:
            self.uic_admissionswindow.name_input.setEnabled(False)
            self.uic_admissionswindow.numberphone_input.setEnabled(False)
            self.uic_admissionswindow.info_send.setEnabled(False)
            bot_process = "trợ lý đang nghe..."
            self.speakoutput(bot_process)
            self.uic_admissionswindow.bot_output.setText(bot_process)
            time.sleep(1.25)
            self.cauhoi = self.getaudio()
            self.uic_admissionswindow.user_ouput.setText(self.cauhoi)
            # bot_process = self.selectdb(self.cauhoi, table=self.nameadmissionswindow())
            bot_process = self.get_response(self.cauhoi)
            self.speakoutput(bot_process)
            self.uic_admissionswindow.bot_output.setText(bot_process)
            ten = self.uic_admissionswindow.name_input.text()
            sdt = self.uic_admissionswindow.numberphone_input.text()
            cauhoi = self.cauhoi
            cautl = self.uic_admissionswindow.bot_output.toPlainText()
            self.adddb_userinfowindow(ten, sdt, cauhoi, cautl)
            self.loaddatahintquestion()
            self.timestart()

    # nút quay lại của win 2
    def btn_logout_admissionswindow(self):
        self.window_admissionswindow.close()
        self.window_startupwin.show()

    # nút tải lại
    def btn_resetwindow(self):
        self.timestop()
        text = "Chào mừng bạn đến với tư vấn tuyển sinh của trường Đại Học Văn Hiến"
        self.uic_admissionswindow.name_input.setText("")
        self.uic_admissionswindow.bot_output.setText(text)
        self.uic_admissionswindow.numberphone_input.setText("")
        self.uic_admissionswindow.user_ouput.setText("")
        self.uic_admissionswindow.question_input.setText("")
        self.uic_admissionswindow.name_input.setDisabled(False)
        self.uic_admissionswindow.numberphone_input.setDisabled(False)
        self.uic_admissionswindow.info_send.setDisabled(False)

    # thời gian tự động
    def timestart(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.btn_resetwindow)
        self.timer.start(300000)

    # ngừng đếm thời gian tự động
    def timestop(self):
        self.timestart()
        self.timer.stop()

    # lọc tên bảng cơ sở dữ liệu của admissionswindow
    def cb_tablename_admissionswindow(self):
        if self.uic_admissionswindow.choosetable_box.currentText() == 'Tất cả':
            text = 'Chung'
            return text
        elif self.uic_admissionswindow.choosetable_box.currentText() == 'Du lịch':
            text = 'DLICH'
            return text
        elif self.uic_admissionswindow.choosetable_box.currentText() == 'Công nghệ thông tin':
            text = 'CNTT'
            return text
        else:
            text = 'Chung'
            return text

    # tải câu hỏi gợi ý
    def loaddatahintquestion(self):
        self.uic_admissionswindow.hintquestion.setColumnWidth(0, 400)
        self.uic_admissionswindow.hintquestion.setHorizontalHeaderLabels(["Câu Hỏi Gợi Ý"])
        con = self.condb()
        print('đã kết nối thành công')
        try:
            cur = con.cursor()
            cur.execute("   select distinct cauhoi, cautraloi from TTTS\
                            where cauhoi not like 'Hệ thống chưa nhận diện được giọng nói của bạn xin hãy thử lại!'\
                            having cautraloi != 'trợ lý không hiểu' ORDER BY cauhoi, cautraloi;")
            data = cur.fetchall()
            self.uic_admissionswindow.hintquestion.setRowCount(len(data))
            self.uic_admissionswindow.hintquestion.setColumnCount(1)
            for rownumber, rowdata in enumerate(data):
                for colnumber, data in enumerate(rowdata):
                    self.uic_admissionswindow.hintquestion.setItem(rownumber, colnumber,
                                                                   QtWidgets.QTableWidgetItem(str(data)))
        except:
            return con.rollback()
        finally:
            self.discondb()
            print('đã ngắt kết nối')

    # chọn câu trả lời trong admissionswindow
    def selectdb_admissionswindow(self):
        con = self.condb()
        table = self.cb_tablename_admissionswindow()
        print('đã kết nối thành công')
        try:
            query = "select cauhoi, cautraloi from " + table + ";"
            cur = con.cursor()
            cur.execute(query)
            data = cur.fetchall()
            return data
        except:
            return con.rollback()
        finally:
            self.discondb()
            print('đã ngắt kết nối')

    def message_probability(self, user_message, recognised_words, single_response=False, required_words=[]):
        message_certainty = 0
        has_required_words = True

        # Đếm số từ có trong mỗi tin nhắn được xác định trước
        for word in user_message:
            if word in recognised_words:
                message_certainty += 1

        # Tính toán phần trăm các từ được nhận dạng trong một tin nhắn của người dùng
        percentage = float(message_certainty) / float(len(recognised_words))

        # Kiểm tra xem required_words có trong chuỗi không
        for word in required_words:
            if word not in user_message:
                has_required_words = False
                break

        # Phải có has_required_words hoặc là single_response
        if has_required_words or single_response:
            return int(percentage * 100)
        else:
            return 0

    def check_all_messages(self, message):
        highest_prob_list = {}

        # Đơn giản hóa việc tạo phản hồi / thêm nó vào dict
        def response(bot_response, list_of_words, single_response=False, required_words=[]):
            nonlocal highest_prob_list
            highest_prob_list[bot_response] = self.message_probability(message, list_of_words, single_response,
                                                                       required_words)

        # lấy câu trả lời -------------------------------------------------------------------------------------------------------
        data = self.selectdb_admissionswindow()
        response('trợ lý không hiểu', [''], single_response=True)
        for x in data:
            response(x[1], re.split(r'\s+|[,;?!.-]\s*', x[0]), single_response=True)

        best_match = max(highest_prob_list, key=highest_prob_list.get)
        return best_match

    # lấy câu trả lời
    def get_response(self, user_input):
        split_message = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
        response = self.check_all_messages(split_message)
        return response

    # hàm lấy giọng nói trong admissionswindow
    def getaudio(self):
        with lis.Microphone() as mic:
            print("Trợ lý:  Đang Nghe..")
            bot_listen = lis.Recognizer()
            audio = bot_listen.listen(mic, phrase_time_limit=5)
            try:
                text = bot_listen.recognize_google(audio, language="vi-VN")
                return text
            except:
                text = "Hệ thống chưa nhận diện được giọng nói của bạn xin hãy thử lại!"
                return text

    # thêm ttsv vào dbbase trong admissionswindow
    def adddb_userinfowindow(self, ten, sdt, cauhoi, cautrl):
        con = self.condb()
        print('đã kết nối thành công')
        try:
            query = "insert into TTTS (hovaten, sdt, cauhoi, cautraloi) values ('" + ten + "', '" + sdt + "', '" + cauhoi + "', '" + cautrl + "');"
            cur = con.cursor()
            cur.execute(query)
            con.commit()
        except:
            con.rollback()
        finally:
            self.discondb()
            print('đã ngắt kết nối')

    # *******************window3*********************

    # load form chọn dbase
    def show_choosetablewindow(self):
        tendangnhap = self.uic_startupwin.username_input.text()
        matkhau = self.uic_startupwin.password_input.text()
        username = None
        password = None
        con = self.condb()
        print('đã kết nối thành công')
        try:
            cur = con.cursor()
            cur.execute("select taikhoan, matkhau from quanlyadmin where taikhoan = '"+tendangnhap+"';")
            data = cur.fetchall()
            username = data[0][0]
            password = data[0][1]
        except:
            self.uic_startupwin.note.setText("Sai tên đăng nhập hoặc mật khẩu")
        finally:
            self.discondb()
            print('đã ngắt kết nối')
        if tendangnhap == username and matkhau == password:
            self.uic_startupwin.username_input.setText("")
            self.uic_startupwin.password_input.setText("")
            self.uic_startupwin.note.setText("")
            self.window_startupwin.close()
            self.window_choosetablewindow = QtWidgets.QMainWindow()
            self.uic_choosetablewindow = Ui_choosetable_window()
            self.uic_choosetablewindow.setupUi(self.window_choosetablewindow)
            self.window_choosetablewindow.show()
            self.uic_choosetablewindow.data_table.clicked.connect(self.show_datatablewindow)
            self.uic_choosetablewindow.infouser_table.clicked.connect(self.show_userinfowindow)
            self.uic_choosetablewindow.logout.clicked.connect(self.btn_logout_choosetablewindow)
            self.uic_choosetablewindow.update_button.clicked.connect(self.btn_upddbpass_admin)
            self.uic_choosetablewindow.signup_admin.setDisabled(True)
            self.uic_choosetablewindow.account_input.setText(tendangnhap)
            self.uic_choosetablewindow.password_input.setText(matkhau)
            self.uic_choosetablewindow.account_input.setDisabled(True)
        elif tendangnhap == "admin" and matkhau == "admin":
            self.uic_startupwin.username_input.setText("")
            self.uic_startupwin.password_input.setText("")
            self.uic_startupwin.note.setText("")
            self.window_startupwin.close()
            self.window_choosetablewindow = QtWidgets.QMainWindow()
            self.uic_choosetablewindow = Ui_choosetable_window()
            self.uic_choosetablewindow.setupUi(self.window_choosetablewindow)
            self.window_choosetablewindow.show()
            self.uic_choosetablewindow.data_table.clicked.connect(self.show_datatablewindow)
            self.uic_choosetablewindow.infouser_table.clicked.connect(self.show_userinfowindow)
            self.uic_choosetablewindow.logout.clicked.connect(self.btn_logout_choosetablewindow)
            self.uic_choosetablewindow.signup_admin.clicked.connect(self.show_createadminwindow)
            self.uic_choosetablewindow.account_input.setText(tendangnhap)
            self.uic_choosetablewindow.password_input.setText(matkhau)
            self.uic_choosetablewindow.account_input.setDisabled(True)
            self.uic_choosetablewindow.password_input.setDisabled(True)
            self.uic_choosetablewindow.update_button.setDisabled(True)
        else:
            self.uic_startupwin.note.setText("Sai tên đăng nhập hoặc mật khẩu")

    # window3
    def btn_logout_choosetablewindow(self):
        self.window_choosetablewindow.close()
        self.window_startupwin.show()

    # nút cập nhật mật khẩu
    def btn_upddbpass_admin(self):
        taikhoan = self.uic_choosetablewindow.account_input.text()
        matkhau = self.uic_choosetablewindow.password_input.text()
        con = self.condb()
        print('đã kết nối thành công')
        try:
            query = "update quanlyadmin set matkhau = '"+matkhau+"' where taikhoan = '"+taikhoan+"';"
            cur = con.cursor()
            cur.execute(query)
            con.commit()
        except:
            con.rollback()
        finally:
            self.discondb()
            print('đã ngắt kết nối')
            self.showDialog('cập nhật mật khẩu thành công')

    # *******************window4*********************

    # load bảng câu hỏi tư vấn
    def show_datatablewindow(self):
        self.window_choosetablewindow.close()
        self.window_datatablewindow = QtWidgets.QMainWindow()
        self.uic_datatablewindow = Ui_datatable_window()
        self.window_datatablewindow.show()
        self.uic_datatablewindow.setupUi(self.window_datatablewindow)
        self.uic_datatablewindow.datatable.setHorizontalHeaderLabels(["STT" , "Mã Từ Khóa", "Câu Hỏi", "Câu Trả Lời", "Thời Gian"])
        self.uic_datatablewindow.datatable.setColumnWidth(4, 170)
        self.uic_datatablewindow.datatable.setColumnWidth(3, 450)
        self.uic_datatablewindow.datatable.setColumnWidth(2, 350)
        self.uic_datatablewindow.datatable.setColumnWidth(1, 70)
        self.uic_datatablewindow.datatable.setColumnWidth(0, 10)
        self.uic_datatablewindow.loadtable_button.clicked.connect(self.loadtable)
        self.uic_datatablewindow.logout_button.clicked.connect(self.btn_log_datatablewindow)
        self.uic_datatablewindow.back_button.clicked.connect(self.btn_back_datatablewindow)
        self.uic_datatablewindow.add_button.clicked.connect(self.btn_add)
        self.uic_datatablewindow.update_button.clicked.connect(self.btn_uppdate)
        self.uic_datatablewindow.delete_button.clicked.connect(self.btn_delete)
        self.uic_datatablewindow.search_input.textChanged.connect(self.searchdata)

    # nút tải dữ liệu
    def loadtable(self):
        choosetable = self.cb_tablename_datatablewindow()
        self.loaddb_admissions(choosetable)

    # lọc tên bảng cơ sở dữ liệu của datatablewindow
    def cb_tablename_datatablewindow(self):
        if self.uic_datatablewindow.choosetable_box.currentText() == 'Tất cả':
            text = 'Chung'
            return text
        elif self.uic_datatablewindow.choosetable_box.currentText() == 'Du lịch':
            text = 'DLICH'
            return text
        elif self.uic_datatablewindow.choosetable_box.currentText() == 'Công nghệ thông tin':
            text = 'CNTT'
            return text
        else:
            text = 'Chung'
            return text

    # window4
    def btn_log_datatablewindow(self):
        self.window_datatablewindow.close()
        self.window_startupwin.show()

    # nút quay lại của win4
    def btn_back_datatablewindow(self):
        self.window_datatablewindow.close()
        self.window_choosetablewindow.show()

    # chức năng thêm trong win 4
    def btn_add(self):
        try:
            choosetable = self.cb_tablename_datatablewindow()
            matk = self.uic_datatablewindow.idkeyword_input.text()
            cauhoi = self.uic_datatablewindow.question_input.text()
            cautl = self.uic_datatablewindow.answer_input.text()
            self.adddb_admissionwindows(matk, cauhoi, cautl, choosetable)
            self.loaddb_admissions(choosetable)
        except:
            self.showDialog('lỗi! thêm dữ liệu thất bại')
        finally:
            self.uic_datatablewindow.idkeyword_input.setText("")
            self.uic_datatablewindow.question_input.setText("")
            self.uic_datatablewindow.answer_input.setText("")

    # hàm adddb trong
    def adddb_admissionwindows(self, matk, cauhoi, cautl, table=''):
        con = self.condb()
        print('đã kết nối thành công')
        try:
            query = "INSERT INTO " + table + "(macauhoi, cauhoi, cautraloi) VALUES('" + matk + "', '" + cauhoi + "', '" + cautl + "')"
            cur = con.cursor()
            cur.execute(query)
            con.commit()
        except:
            con.rollback()
        finally:
            self.discondb()
            print('đã ngắt kết nối')
            self.showDialog('thêm dữ liệu tuyển sinh thành công')

    # nút sửa data trên giao diện
    def btn_uppdate(self):
        currentItem = 0
        for currentItem in self.uic_datatablewindow.datatable.selectedItems():
            currentItem.row()
        if (self.uic_datatablewindow.idkeyword_input.text() == ""):
            try:
                self.uic_datatablewindow.id_input.setText(self.uic_datatablewindow.datatable.item(currentItem.row(), 0).text())
                self.uic_datatablewindow.idkeyword_input.setText(self.uic_datatablewindow.datatable.item(currentItem.row(), 1).text())
                self.uic_datatablewindow.question_input.setText(self.uic_datatablewindow.datatable.item(currentItem.row(), 2).text())
                self.uic_datatablewindow.answer_input.setText(self.uic_datatablewindow.datatable.item(currentItem.row(), 3).text())
            except:
                self.showDialog('lỗi! chưa chọn dữ liệu')
        else:
            choosetable = self.cb_tablename_datatablewindow()
            try:
                id = ""
                if self.uic_datatablewindow.id_input.text() == "":
                    self.showDialog('Cảnh báo: không tìm thấy STT để cập nhật')
                else:
                    id = self.uic_datatablewindow.id_input.text()
                matk = self.uic_datatablewindow.idkeyword_input.text()
                cauhoi = self.uic_datatablewindow.question_input.text()
                cautl = self.uic_datatablewindow.answer_input.text()
                self.upddatedb_admissionswindow(cauhoi, cautl, matk, id, choosetable)
                self.showDialog('cập nhật thành công!')
            except:
                self.showDialog('lỗi! cập nhật không thành công')
            finally:
                self.loaddb_admissions(choosetable)
                self.uic_datatablewindow.id_input.setText("")
                self.uic_datatablewindow.idkeyword_input.setText("")
                self.uic_datatablewindow.question_input.setText("")
                self.uic_datatablewindow.answer_input.setText("")

    # chức năng update dữ liệu admissionswindow
    def upddatedb_admissionswindow(self, cauhoi, cautl, matk, id, table=''):
        con = self.condb()
        print('đã kết nối thành công')
        try:
            query = "update " + table + " set macauhoi = '" + matk + "', cauhoi = '" + cauhoi + "', cautraloi = '" + cautl + "', thoigiancapnhat = now() where id = " + id + ";"
            cur = con.cursor()
            cur.execute(query)
            con.commit()
        except:
            con.rollback()
        finally:
            self.discondb()
            print('đã ngắt kết nối')

    # chức năng hỏi trước khi xóa trong win 4
    def btn_delete(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setText("bạn có muốn xóa dữ liệu không??")
        msgBox.setWindowTitle("Thông báo")
        msgBox.setStandardButtons(QMessageBox.Ok| QMessageBox.Cancel)
        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            self.delete_datatablewindow()

    # chức năng xóa bảng trong datatablewindow
    def delete_datatablewindow(self):
        currentItem = 0
        choosetable = self.cb_tablename_datatablewindow()
        for currentItem in self.uic_datatablewindow.datatable.selectedItems():
            currentItem.row()
        try:
            id = self.uic_datatablewindow.datatable.item(currentItem.row(), 0).text()
            self.delselectdb_admissionwindows(id, choosetable)
            self.loaddb_admissions(choosetable)
            self.showDialog('xóa dữ liệu thành công')
        except:
            self.showDialog('lỗi! chưa chọn dữ liệu')

    # chức năng xóa db trong tư vấn tuyển sinh
    def delselectdb_admissionwindows(self, id, table):
        con = self.condb()
        print('đã kết nối thành công')
        try:
            query = "DELETE FROM " + table + " where id = " + id + ";"
            cur = con.cursor()
            cur.execute(query)
            con.commit()
        except:
            con.rollback()
        finally:
            self.discondb()
            print('đã ngắt kết nối')

    # tìm kiếm dữ liệu
    def searchdata(self, i=''):
        table = self.cb_tablename_datatablewindow()
        self.uic_datatablewindow.datatable.resizeColumnToContents(0)
        self.uic_datatablewindow.datatable.resizeColumnToContents(1)
        con = self.condb()
        print('đã kết nối thành công')
        try:
            query = "SELECT id, macauhoi, cauhoi, cautraloi, thoigiancapnhat FROM "+table+" where macauhoi LIKE '%"+i+"%' or cauhoi LIKE '%"+i+"%';"
            cur = con.cursor()
            cur.execute(query)
            data = cur.fetchall()
            self.uic_datatablewindow.datatable.setRowCount(len(data))
            self.uic_datatablewindow.datatable.setColumnCount(5)
            for rownumber, rowdata in enumerate(data):
                for colnumber, data in enumerate(rowdata):
                    self.uic_datatablewindow.datatable.setItem(rownumber, colnumber, QtWidgets.QTableWidgetItem(str(data)))
        except:
            return con.rollback()
        finally:
            self.discondb()
            print('đã ngắt kết nối')

    # load data datatablewindow
    def loaddb_admissions(self, table=''):
        self.uic_datatablewindow.datatable.setColumnWidth(4, 170)
        self.uic_datatablewindow.datatable.setColumnWidth(3, 450)
        self.uic_datatablewindow.datatable.setColumnWidth(2, 350)
        self.uic_datatablewindow.datatable.setColumnWidth(1, 70)
        self.uic_datatablewindow.datatable.setColumnWidth(0, 10)
        self.uic_datatablewindow.datatable.setHorizontalHeaderLabels(
            ["STT", "Mã Từ Khóa", "Câu Hỏi", "Câu Trả Lời", "Thời Gian"])
        con = self.condb()
        print('đã kết nối thành công')
        try:
            query = "select id, macauhoi, cauhoi, cautraloi, thoigiancapnhat from " + table + ";"
            cur = con.cursor()
            cur.execute(query)
            data = cur.fetchall()
            self.uic_datatablewindow.datatable.setRowCount(len(data))
            self.uic_datatablewindow.datatable.setColumnCount(5)
            for rownumber, rowdata in enumerate(data):
                for colnumber, data in enumerate(rowdata):
                    self.uic_datatablewindow.datatable.setItem(rownumber, colnumber,
                                                               QtWidgets.QTableWidgetItem(str(data)))
        except:
            return con.rollback()
        finally:
            self.discondb()
            print('đã ngắt kết nối')

    # *******************window5*********************

    # load bảng câu hỏi thí sinh
    def show_userinfowindow(self):
        self.window_choosetablewindow.close()
        self.window_userinfowindow = QtWidgets.QMainWindow()
        self.uic_userinfowindow = Ui_userinfo_window()
        self.uic_userinfowindow.setupUi(self.window_userinfowindow)
        self.window_userinfowindow.show()
        self.loaddata_userinfowindow()
        self.uic_userinfowindow.search_input.textChanged.connect(self.searchstudent)
        self.uic_userinfowindow.excel_button.clicked.connect(self.btn_exportexcel)
        self.uic_userinfowindow.deleteall_button.clicked.connect(self.btn_deleteall)
        self.uic_userinfowindow.logout_button.clicked.connect(self.btn_logout_userinfowindow)
        self.uic_userinfowindow.back_button.clicked.connect(self.btn_back_userinfowindow)

    # tìm dữ liệu sinh viên
    def searchstudent(self, i=''):
        self.uic_userinfowindow.datatable.setColumnWidth(0, 220)
        self.uic_userinfowindow.datatable.setColumnWidth(1, 220)
        self.uic_userinfowindow.datatable.setColumnWidth(2, 220)
        self.uic_userinfowindow.datatable.setColumnWidth(3, 220)
        self.uic_userinfowindow.datatable.setColumnWidth(4, 220)
        con = self.condb()
        print('đã kết nối thành công')
        try:
            cur = con.cursor()
            cur.execute("select hovaten, sdt, cauhoi, cautraloi, thoigianhoi from TTTS where sdt LIKE '%" + i + "%' or hovaten LIKE '%" + i + "%'")
            data = cur.fetchall()
            self.uic_userinfowindow.datatable.setRowCount(len(data))
            self.uic_userinfowindow.datatable.setColumnCount(5)
            for rownumber, rowdata in enumerate(data):
                for colnumber, data in enumerate(rowdata):
                    self.uic_userinfowindow.datatable.setItem(rownumber, colnumber, QtWidgets.QTableWidgetItem(str(data)))
        except:
            return con.rollback()
        finally:
            self.discondb()
            print('đã ngắt kết nối')

    # nút xuất file exe
    def btn_exportexcel(self):
        columnheader = ["Họ Và Tên", "Số Điện Thoại", "Câu Hỏi", "Câu Trả Lời", "Thời Gian"]
        con = self.condb()
        print('đã kết nối thành công')
        try:
            cur = con.cursor()
            cur.execute("select hovaten, sdt, cauhoi, cautraloi, thoigianhoi from TTTS")
            data = cur.fetchall()
            wb = Workbook()
            ws = wb.active
            ws.append(columnheader)
            for row in data:
                ws.append(row)
            savespot = QFileDialog.getSaveFileName(directory='c:/', filter="Excel Files (*.xlsx)")
            print(savespot[0])
            wb.save(savespot[0])
            self.showDialog('đã xuất dữ liệu thành công')
        except:
            self.showDialog('lỗi! xuất dữ liệu không thành công')
        finally:
            self.discondb()
            print('đã ngắt kết nối')

    # nút xóa tất cả ghi bản thông tin sinh viên
    def btn_deleteall(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setText("bạn có muốn xóa dữ liệu không??")
        msgBox.setWindowTitle("Thông báo")
        msgBox.setStandardButtons(QMessageBox.Ok| QMessageBox.Cancel)
        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            self.delalldb_userinfowindow()

    # chức năng xóa tất cả ghi bản thông tin sinh viên
    def delalldb_userinfowindow(self):
        try:
            self.deletedb_userinfowindow()
            self.clearsavefilemp3()
            self.showDialog('xóa thành công')
        except:
            self.showDialog('lỗi! chưa xóa được dữ liệu')
        finally:
            self.loaddata_userinfowindow()

    # chức năng xóa bảng trong userinfowindow
    def deletedb_userinfowindow(self):
        con = self.condb()
        print('đã kết nối thành công')
        try:
            cur = con.cursor()
            cur.execute("DELETE FROM TTTS", ())
            con.commit()
        except:
            con.rollback()
        finally:
            self.discondb()
            print('đã ngắt kết nối')

    # đăng xuất userinfowindow
    def btn_logout_userinfowindow(self):
        self.window_userinfowindow.close()
        self.window_startupwin.show()

    # nút quay lại của userinfowindow
    def btn_back_userinfowindow(self):
        self.window_userinfowindow.close()
        self.window_choosetablewindow.show()

    # tải dữ liệu từ sql lên userinfowindow
    def loaddata_userinfowindow(self):
        self.uic_userinfowindow.datatable.setColumnWidth(0, 200)
        self.uic_userinfowindow.datatable.setColumnWidth(1, 200)
        self.uic_userinfowindow.datatable.setColumnWidth(2, 200)
        self.uic_userinfowindow.datatable.setColumnWidth(3, 200)
        self.uic_userinfowindow.datatable.setColumnWidth(4, 200)
        self.uic_userinfowindow.datatable.setHorizontalHeaderLabels(
            ["Họ Và Tên", "Số Điện Thoại", "Câu Hỏi", "Câu Trả Lời", "Thời Gian"])
        con = self.condb()
        print('đã kết nối thành công')
        try:
            cur = con.cursor()
            cur.execute("select hovaten, sdt, cauhoi, cautraloi, thoigianhoi from TTTS")
            data = cur.fetchall()
            self.uic_userinfowindow.datatable.setRowCount(len(data))
            self.uic_userinfowindow.datatable.setColumnCount(5)
            for rownumber, rowdata in enumerate(data):
                for colnumber, data in enumerate(rowdata):
                    self.uic_userinfowindow.datatable.setItem(rownumber, colnumber,
                                                              QtWidgets.QTableWidgetItem(str(data)))
        except:
            return con.rollback()
        finally:
            self.discondb()
            print('đã ngắt kết nối')

    # *******************window 6*********************

    # load bảng quản lý quản trị viên
    def show_createadminwindow(self):
        self.window_choosetablewindow.close()
        self.window_createadminwindow = QtWidgets.QMainWindow()
        self.uic_createadminwindow = Ui_createadmin_window()
        self.uic_createadminwindow.setupUi(self.window_createadminwindow)
        self.window_createadminwindow.show()
        self.loaddata_accountnadmin()
        self.uic_createadminwindow.search_input.textChanged.connect(self.searchdata_createadminwindow)
        self.uic_createadminwindow.back_button.clicked.connect(self.btn_back_createadminwindow)
        self.uic_createadminwindow.logout_button.clicked.connect(self.btn_logout_createadminwindow)
        self.uic_createadminwindow.add_button.clicked.connect(self.btn_addadmin)
        self.uic_createadminwindow.update_button.clicked.connect(self.btn_updateadmin)
        self.uic_createadminwindow.delete_button.clicked.connect(self.btn_deleteadmin)

    # chức năng tìm kiếm thông tin quản trị viên
    def searchdata_createadminwindow(self, i=''):
        self.uic_createadminwindow.datatable.setColumnWidth(3, 350)
        self.uic_createadminwindow.datatable.setColumnWidth(2, 350)
        self.uic_createadminwindow.datatable.setColumnWidth(1, 350)
        self.uic_createadminwindow.datatable.setColumnWidth(0, 10)
        con = self.condb()
        print('đã kết nối thành công')
        try:
            query = "select id, hovaten, taikhoan, matkhau from quanlyadmin where hovaten LIKE '%" + i + "%' or taikhoan LIKE '%" + i + "%';"
            cur = con.cursor()
            cur.execute(query)
            data = cur.fetchall()
            self.uic_createadminwindow.datatable.setRowCount(len(data))
            self.uic_createadminwindow.datatable.setColumnCount(4)
            for rownumber, rowdata in enumerate(data):
                for colnumber, data in enumerate(rowdata):
                    self.uic_createadminwindow.datatable.setItem(rownumber, colnumber,
                                                                 QtWidgets.QTableWidgetItem(str(data)))
        except:
            return con.rollback()
        finally:
            self.discondb()
            print('đã ngắt kết nối')

    # nút trở về chọn bảng
    def btn_back_createadminwindow(self):
        self.window_createadminwindow.close()
        self.window_choosetablewindow.show()

    # nút đăng xuất khỏi quản lý tài khoản quản trị viên
    def btn_logout_createadminwindow(self):
        self.window_createadminwindow.close()
        self.window_startupwin.show()

    # nút thêm quản trị viên
    def btn_addadmin(self):
        hovaten = self.uic_createadminwindow.fullname_input.text()
        taikhoan = self.uic_createadminwindow.account_input.text()
        matkhau = self.uic_createadminwindow.password_input.text()
        if taikhoan.isalnum() == True and matkhau.isalnum() == True:
            self.adddb_createadminwindow(hovaten, taikhoan, matkhau)
            self.loaddata_accountnadmin()
            self.uic_createadminwindow.fullname_input.setText("")
            self.uic_createadminwindow.account_input.setText("")
            self.uic_createadminwindow.password_input.setText("")
        else:
            self.showDialog("tên tài khoản và mật khẩu không hơp lệ")

    # chức năng quản trị viên
    def adddb_createadminwindow(self, hovaten, taikhoan, matkhau):
        con = self.condb()
        print('đã kết nối thành công')
        try:
            query = "insert into quanlyadmin (hovaten, taikhoan, matkhau) values ('" + hovaten + "', '" + taikhoan + "', '" + matkhau + "');"
            cur = con.cursor()
            cur.execute(query)
            con.commit()
        except:
            con.rollback()
        finally:
            self.discondb()
            print('đã ngắt kết nối')
            self.showDialog('thêm quản trị viên thành công')

    # nút cập nhật thông tin tài khoản quản trị viên
    def btn_updateadmin(self):
        currentItem = 0
        for currentItem in self.uic_createadminwindow.datatable.selectedItems():
            currentItem.row()
        if (self.uic_createadminwindow.fullname_input.text() == ""):
            try:
                self.uic_createadminwindow.id_input.setText(self.uic_createadminwindow.datatable.item(currentItem.row(), 0).text())
                self.uic_createadminwindow.fullname_input.setText(self.uic_createadminwindow.datatable.item(currentItem.row(), 1).text())
                self.uic_createadminwindow.account_input.setText(self.uic_createadminwindow.datatable.item(currentItem.row(), 2).text())
                self.uic_createadminwindow.password_input.setText(self.uic_createadminwindow.datatable.item(currentItem.row(), 3).text())
            except:
                self.showDialog('lỗi! chưa chọn dữ liệu')
        else:
            try:
                id = ""
                if self.uic_createadminwindow.id_input.text() == "":
                    self.showDialog('Cảnh báo: không tìm thấy STT để cập nhật')
                else:
                    id = self.uic_createadminwindow.id_input.text()
                hoten = self.uic_createadminwindow.fullname_input.text()
                taikhoan = self.uic_createadminwindow.account_input.text()
                matkhau = self.uic_createadminwindow.password_input.text()
                self.upddbadmin_createadminwindow(hoten, taikhoan, matkhau, id)
                self.showDialog('cập nhật thành công')
            except:
                self.showDialog('lỗi! tài khoản chưa được cập nhật')
            finally:
                self.loaddata_accountnadmin()
                self.uic_createadminwindow.id_input.setText("")
                self.uic_createadminwindow.fullname_input.setText("")
                self.uic_createadminwindow.account_input.setText("")
                self.uic_createadminwindow.password_input.setText("")

    # chức năng cập nhật thông tin tài khoản quản trị viên
    def upddbadmin_createadminwindow(self, hoten, taikhoan, matkhau, id):
        con = self.condb()
        print('đã kết nối thành công')
        try:
            query = "update quanlyadmin set hovaten = '" + hoten + "', taikhoan = '" + taikhoan + "', matkhau = '" + matkhau + "' where id = " + id + ";"
            cur = con.cursor()
            cur.execute(query)
            con.commit()
        except:
            con.rollback()
        finally:
            self.discondb()
            print('đã ngắt kết nối')

    # nút xóa tài khoản quản trị viên
    def btn_deleteadmin(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setText("bạn có muốn xóa dữ liệu không??")
        msgBox.setWindowTitle("Thông báo")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            self.function_delectadmin()

    # chức năng xóa tài khoản quản trị viên
    def function_delectadmin(self):
        currentItem = 0
        for currentItem in self.uic_createadminwindow.datatable.selectedItems():
            currentItem.row()
        try:
            id = self.uic_createadminwindow.datatable.item(currentItem.row(), 0).text()
            self.delselectdb_createadminwindow(id)
            self.loaddata_accountnadmin()
            self.showDialog('xóa quản trị viên thành công')
        except:
            self.showDialog('lỗi! chưa chọn quản trị viên')


    # chức năng xóa csdl trên tài khoản quản trị viên
    def delselectdb_createadminwindow(self, id):
        con = self.condb()
        print('đã kết nối thành công')
        try:
            query = "DELETE FROM quanlyadmin where id = " + id + ";"
            cur = con.cursor()
            cur.execute(query)
            con.commit()
        except:
            con.rollback()
        finally:
            self.discondb()
            print('đã ngắt kết nối')

    # tải dữ liệu tài khoản quản trị viên
    def loaddata_accountnadmin(self, ):
        self.uic_createadminwindow.datatable.setColumnWidth(3, 350)
        self.uic_createadminwindow.datatable.setColumnWidth(2, 350)
        self.uic_createadminwindow.datatable.setColumnWidth(1, 350)
        self.uic_createadminwindow.datatable.setColumnWidth(0, 10)
        self.uic_createadminwindow.datatable.setHorizontalHeaderLabels(
            ["STT", "Họ và tên", "Tài khoản", "Mật khẩu"])
        con = self.condb()
        print('đã kết nối thành công')
        try:
            query = "select id, hovaten, taikhoan, matkhau from quanlyadmin;"
            cur = con.cursor()
            cur.execute(query)
            data = cur.fetchall()
            self.uic_createadminwindow.datatable.setRowCount(len(data))
            self.uic_createadminwindow.datatable.setColumnCount(4)
            for rownumber, rowdata in enumerate(data):
                for colnumber, data in enumerate(rowdata):
                    self.uic_createadminwindow.datatable.setItem(rownumber, colnumber,
                                                                 QtWidgets.QTableWidgetItem(str(data)))
        except:
            return con.rollback()
        finally:
            self.discondb()
            print('đã ngắt kết nối')

    # *******************chức năng chung*********************

    # kết nối csdl
    def condb(self):
        db = mysql.connector.connect(user='root', password='khang123', host='localhost', port='3306', database='tvts')
        # db = mysql.connector.connect(user='root', password='khang123', host='192.168.1.8', port='3306', database='tvts')
        return db

    # hủy kết nối csdl
    def discondb(self):
        self.condb().close()

    # chức năng show thông báo
    def showDialog(self, text):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(text)
        msgBox.setWindowTitle("Thông báo")
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec()

    # chức năng chuyển văn bản thành giọng nói
    def speakoutput(self, text):
        r1 = random.randint(1, 10000000)
        r2 = random.randint(1, 10000000)
        randfile = str(r2) + "randomtext" + str(r1) + ".mp3"
        tts = gTTS(text=text, lang='vi', slow=False)
        tts.save("savefilemp3/" + randfile + "")
        self.player = QMediaPlayer()
        fullfile = os.path.join(os.getcwd(), "savefilemp3/" + randfile + "")
        url = QUrl.fromLocalFile(fullfile)
        content = QMediaContent(url)
        self.player.setMedia(content)
        self.player.play()

    # xóa các bản lưu tư vấn của chương trình
    def clearsavefilemp3(self):
        dir = "savefilemp3"
        filelist = glob.glob(os.path.join(dir, "*"))
        for f in filelist:
            os.remove(f)

if __name__== "__main__":
    app = QApplication(sys.argv)
    main_win = Mainwindow()
    main_win.show_startupwindow()
    sys.exit(app.exec())