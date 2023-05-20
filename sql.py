#chạy thư viện
import mysql.connector

#kết nối db
db = mysql.connector.connect(user='root', password='khang123', host='127.0.0.1', port='3306', database='tvts')
# db = mysql.connector.connect(user='root', password='', host='192.168.1.1', port='3306', database='tvts')

code ='show tables'

#thực hiện database
cursor = db.cursor()
cursor.execute(code)

#xuất dữ liệu
result = cursor.fetchall()
print(result)

# đóng database
cursor.close()
db.close()

# con = self.condb()
# print('đã kết nối thành công')
# try:
#     cur = con.cursor()
#     cur.execute("select hovaten, sdt, cauhoi, cautraloi, thoigianhoi from TTTS")
#     data = cur.fetchall()
#     self.uic4.data.setRowCount(len(data))
#     self.uic4.data.setColumnCount(5)
#     for rownumber, rowdata in enumerate(data):
#         for colnumber, data in enumerate(rowdata):
#             self.uic4.data.setItem(rownumber, colnumber, QtWidgets.QTableWidgetItem(str(data)))
# except:
#     return con.rollback()
# finally:
#     self.discondb()
#     print('đã ngắt kết nối')

# def deldb(self):
#     con = self.condb()
#     print('đã kết nối thành công')
#     try:
#         cur = con.cursor()
#         cur.execute("DELETE FROM TTTS", ())
#         con.commit()
#     except:
#         con.rollback()
#     finally:
#         self.discondb()
#         print('đã ngắt kết nối')

