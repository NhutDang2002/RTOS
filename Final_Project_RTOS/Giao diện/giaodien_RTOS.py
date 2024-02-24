from PyQt5.QtWidgets import *
from PyQt5 import uic
import serial
import sys
import serial.tools.list_ports
import time

global ser


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        uic.loadUi("giaodien_RTOS.ui", self)
        self.button = self.findChild(QPushButton, "pushButton")
        self.dulieu = self.findChild(QLineEdit,"lineEdit")
        self.text = self. findChild(QTextBrowser,"textBrowser")
        self.command = self.findChild(QRadioButton, "radio_command")
        self.icon = self.findChild(QRadioButton, "radio_icon")
        self.thoigian = self.findChild(QCheckBox, "box_thoigian")
        self.nhietdo = self.findChild(QCheckBox, "box_nhietdo")
        self.dich = self.findChild(QCheckBox, "box_dich")
        self.button_COM = self.findChild(QPushButton, "pushButton_2")
        self.box_COM = self.findChild(QComboBox, "comboBox")

        self.command.setChecked(1)
        self.button.clicked.connect(self.clicker)
        self.button_COM.clicked.connect(self.load_COM)
        self.command.clicked.connect(self.check_radio)
        self.icon.clicked.connect(self.check_radio)
        self.dich.stateChanged.connect(self.text_dich)
        self.show()
    
    def text_dich(self):
        if(self.dich.checkState()):
            self.dich.setText("Dich phai")
        else:
            self.dich.setText("Dich trai")
    def check_radio(self):
        print(self.command.isChecked())
        if(self.command.isChecked()):
            self.dulieu.setEnabled(1)
            self.thoigian.setEnabled(1)
            self.nhietdo.setEnabled(1)
            self.dich.setEnabled(1)
        else:
            self.dulieu.setEnabled(0)
            self.thoigian.setEnabled(0)
            self.nhietdo.setEnabled(0)
            self.dich.setEnabled(0)    

    def load_COM(self):
        i = 0
        ports = list(serial.tools.list_ports.comports())
        self.box_COM.clear()
        for p in ports:
            self.box_COM.addItem("")
            self.box_COM.setItemText(i, str(p))
            i +=1
    def clicker(self):
        global ser
        try:
            ser = serial.Serial(self.box_COM.currentText()[0:5],9600)
            a = ""
            self.text.clear()
            if(self.command.isChecked()):
                if(self.thoigian.checkState()):
                    self.text.append("thoi gian")
                if(self.nhietdo.checkState()):
                    self.text.append("nhiet do")
                if(self.nhietdo.checkState()):
                    if(self.thoigian.checkState()):
                        a += "$"
                    else:
                        a += "#"
                else:
                    if(self.thoigian.checkState()):
                        a += "@"
                    else:
                        a += "+"
                if(self.dich.checkState()):
                    a += "^"
                else:
                    a += "!"
                a += self.dulieu.displayText()
                self.text.append(self.dulieu.displayText())
            else:
                a += "% "
                self.text.append("icon")
            ser.write(a.encode("ascii"))
            #self.text.setText(a)
            print("ok")
            time.sleep(0.1)
            ser.close()
        except:
            pass
app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()