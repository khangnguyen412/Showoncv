import datetime
import random
import playsound
import speech_recognition as lis
from gtts import gTTS
import sqlite3 as lite
import sys
import os

bot_process = ""
text = ""
name = ""
phone = ""
def main():
    def getaudio():
        fil = ""
        with lis.Microphone() as mic:
            print("Trợ lý:  Đang Nghe..")
            bot_listen = lis.Recognizer()
            audio = bot_listen.listen(mic, phrase_time_limit=5)
            try:
                text = bot_listen.recognize_google(audio, language= "vi-VN")
                print("Tôi: " + text)
                if "ngày học" in text:
                    fil = "ngày học"
                    return fil
                elif "chuyên ngành" in text:
                    fil = "chuyên ngành"
                    return fil
                elif "nghiên cứu khoa học" in text:
                    fil = "nghiên cứu khoa học"
                    return fil
                elif "tín chỉ" in text:
                    fil = "bao nhiêu 1 tín chỉ"
                    return fil
                else:
                    return text
            except:
                text = "Trợ lý:Tôi không hiểu!!"
                return text
    # x = getaudio()
    # print(x)

    def selectdb(x):
        try:
            path = os.path.dirname(__file__) + "\\tuvantuyensinh.db"
            con = lite.connect(path)
            with con:
                cur = con.cursor()
                cur.execute("SELECT cauTraLoi FROM tuVanTuyenSinh WHERE tuKhoa = ?", (x,))
                while True:
                    row = cur.fetchone()
                    if row == x:
                        break
                    try:
                        return row[0]
                    except:
                        return "trợ lý không hiểu, bạn có nói lại được không"
        except lite.Error as e:
            print("Error %s" %e.args[0])
            sys.exit()
        finally:
            if con:
                con.close()
    # x = input()
    # bot_process = selectdb(x)
    # print(bot_process)

    def speakoutput(n):
        r1 = random.randint(1, 10000000)
        r2 = random.randint(1, 10000000)
        randfile = str(r2) + "randomtext" + str(r1) + ".mp3"
        print("Trợ lý: " + bot_process)
        tts = gTTS(text=bot_process, lang='vi', slow=False)
        tts.save(randfile)
        playsound.playsound(randfile)
        ##playsound.playsound("ngayhoc.mp3")
        os.remove(randfile)
    # speakoutput(bot_process)

    def upddb():
        z = input('nhập mã từ khóa muốn đổi: ')
        x = input('nhập từ khóa mới: ')
        y = input('nhập câu trả lời mới: ')
        try:
            path = os.path.dirname(__file__) + "\\tuvantuyensinh.db"
            con = lite.connect(path)
            with con:
                cur = con.cursor()
                cur.execute("UPDATE tuVanTuyenSinh SET  tuKhoa = ?, cauTraLoi = ? WHERE maTuKhoa = ?", (x, y, z))
        except lite.Error as e:
            print("Error %s" %e.args[0])
            sys.exit()
        finally:
            if con:
                con.close()
    # upddb()

    def adddb():
        x = input('nhập mã từ khóa: ')
        y = input('nhập từ khóa: ')
        z = input('nhập câu trả lời: ')
        try:
            path = os.path.dirname(__file__) + "\\tuvantuyensinh.db"
            con = lite.connect(path)
            with con:
                cur = con.cursor()
                cur.execute("INSERT INTO tuVanTuyenSinh VALUES( ?, ?, ?)", (x, y, z))
        except lite.Error as e:
                print("Error %s" %e.args[0])
                sys.exit()
        finally:
            if con:
                con.close()
    # adddb()

    def addttsv(x ,y ,z):
        time = datetime.datetime.now()
        try:
            path = os.path.dirname(__file__) + "\\tuvantuyensinh.db"
            con = lite.connect(path)
            with con:
                cur = con.cursor()
                cur.execute("INSERT INTO thongtinsv VALUES( ?, ?, ?, ?)", (x, y, z, time))
        except lite.Error as e:
                print("Error %s" %e.args[0])
                sys.exit()
        finally:
            if con:
                con.close()

    def deldb():
        i = input('nhập mã từ khóa: ')
        try:
            path = os.path.dirname(__file__) + "\\tuvantuyensinh.db"
            con = lite.connect(path)
            with con:
                cur = con.cursor()
                cur.execute("DELETE FROM tuVanTuyenSinh WHERE maTuKhoa = ?", (i,))
        except lite.Error as e:
            print("Error %s" %e.args[0])
            sys.exit()
        finally:
            if con:
                con.close()
    # deldb()

    bot_process = "chào mừng đến với trường đại học văn hiến, có thể cho tôi biết bạn là quản trị viên hay sinh viên được không"
    speakoutput(bot_process)
    x = getaudio()
    if "quản trị viên" in x:
        bot_process = "bạn cần thêm, xóa hay cập nhật dữ liệu"
        speakoutput(bot_process)
        x = getaudio()
        if "Thêm" in x or "thêm" in x:
            bot_process = "mời bạn nhập dữ liệu cần thêm"
            speakoutput(bot_process)
            adddb()
        elif "Xóa" in x or "xóa" in x:
            bot_process = "mời bạn nhập thông tin cần xóa"
            speakoutput(bot_process)
            deldb()
        elif "Cập nhật" in x or "cập nhật" in x:
            bot_process = "mời bạn nhập thông tin cần cập nhật"
            speakoutput(bot_process)
            upddb()
        else:
            bot_process = "hiện tại chưa có chức năng bạn yêu cầu, xin hãy chạy lại"
            speakoutput(bot_process)
    elif "sinh viên" in x:
        bot_process = "có thể cho tôi biết thông tin về bạn được không"
        speakoutput(bot_process)
        print("-------------")
        name = input("Nhập tên bạn ở đây: ")
        print("-------------")
        phone = input("Nhập số điện thoại bạn ở đây: ")
        print("-------------")
        bot_process = "chào " + name
        speakoutput(bot_process)
        print("-------------")
        bot_process = "chúng tôi giúp gì được cho bạn"
        speakoutput(bot_process)
        print("-------------")
        while True:
            x = getaudio()
            if x == "tạm biệt":
                print("-------------")
                bot_process = "tạm biệt và hẹn gặp lại"
                speakoutput(bot_process)
                break
            else:
                bot_process = selectdb(x)
                speakoutput(bot_process)
                addttsv(name, phone, x)
            print("-------------")
main()
