# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'NOK_brukere.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
class Ui_NOK_brukere(object):
    def setupUi(self, NOK_brukere):
        NOK_brukere.setObjectName("NOK_brukere")
        NOK_brukere.resize(480, 320)
        NOK_brukere.setAutoFillBackground(False)
        NOK_brukere.setStyleSheet("background-color: rgb(131, 131, 131);")
        self.centralwidget = QtWidgets.QWidget(NOK_brukere)
        self.centralwidget.setObjectName("centralwidget")
        self.checkBox_4 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_4.setGeometry(QtCore.QRect(20, 160, 91, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_4.setFont(font)
        self.checkBox_4.setStyleSheet("background-color: rgb(255, 249, 175);")
        self.checkBox_4.setObjectName("checkBox_4")
        self.graph = QtWidgets.QPushButton(self.centralwidget)
        self.graph.setGeometry(QtCore.QRect(380, 230, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.graph.setFont(font)
        self.graph.setStyleSheet("background-color: rgb(245, 245, 245);")
        self.graph.setObjectName("graph")
        self.back = QtWidgets.QPushButton(self.centralwidget)
        self.back.setGeometry(QtCore.QRect(20, 230, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.back.setFont(font)
        self.back.setStyleSheet("background-color: rgb(245, 245, 245);")
        self.back.setObjectName("back")
        self.checkBox_6 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_6.setGeometry(QtCore.QRect(300, 160, 91, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_6.setFont(font)
        self.checkBox_6.setStyleSheet("background-color: rgb(255, 249, 175);")
        self.checkBox_6.setObjectName("checkBox_6")
        self.checkBox_3 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_3.setGeometry(QtCore.QRect(300, 100, 91, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_3.setFont(font)
        self.checkBox_3.setStyleSheet("background-color: rgb(255, 249, 175);")
        self.checkBox_3.setObjectName("checkBox_3")
        self.stop_dato = QtWidgets.QLabel(self.centralwidget)
        self.stop_dato.setGeometry(QtCore.QRect(20, 50, 111, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.stop_dato.setFont(font)
        self.stop_dato.setStyleSheet("background-color: rgb(207, 207, 207);")
        self.stop_dato.setObjectName("stop_dato")
        self.checkBox_2 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_2.setGeometry(QtCore.QRect(160, 100, 91, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_2.setFont(font)
        self.checkBox_2.setStyleSheet("background-color: rgb(255, 249, 175);")
        self.checkBox_2.setObjectName("checkBox_2")
        self.dateedit1 = QtWidgets.QDateEdit(self.centralwidget)
        self.dateedit1.setGeometry(QtCore.QRect(160, 0, 231, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.dateedit1.setFont(font)
        self.dateedit1.setStyleSheet("background-color: rgb(207, 207, 207);")
        self.dateedit1.setObjectName("dateedit1")
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(20, 100, 91, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.checkBox.setFont(font)
        self.checkBox.setStyleSheet("background-color: rgb(255, 249, 175);")
        self.checkBox.setObjectName("checkBox")
        self.checkBox_5 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_5.setGeometry(QtCore.QRect(160, 160, 91, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_5.setFont(font)
        self.checkBox_5.setStyleSheet("background-color: rgb(255, 249, 175);")
        self.checkBox_5.setObjectName("checkBox_5")
        self.start_dato = QtWidgets.QLabel(self.centralwidget)
        self.start_dato.setGeometry(QtCore.QRect(20, 0, 111, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.start_dato.setFont(font)
        self.start_dato.setStyleSheet("background-color: rgb(207, 207, 207);")
        self.start_dato.setObjectName("start_dato")
        self.dateedit_NOKb2 = QtWidgets.QDateEdit(self.centralwidget)
        self.dateedit_NOKb2.setGeometry(QtCore.QRect(160, 50, 231, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.dateedit_NOKb2.setFont(font)
        self.dateedit_NOKb2.setStyleSheet("background-color: rgb(207, 207, 207);")
        self.dateedit_NOKb2.setObjectName("dateedit_NOKb2")
        NOK_brukere.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(NOK_brukere)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 480, 21))
        self.menubar.setObjectName("menubar")
        NOK_brukere.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(NOK_brukere)
        self.statusbar.setObjectName("statusbar")
        NOK_brukere.setStatusBar(self.statusbar)

        self.retranslateUi(NOK_brukere)
        QtCore.QMetaObject.connectSlotsByName(NOK_brukere)

    def retranslateUi(self, NOK_brukere):
        _translate = QtCore.QCoreApplication.translate
        NOK_brukere.setWindowTitle(_translate("NOK_brukere", "NOK_brukere"))
        self.checkBox_4.setText(_translate("NOK_brukere", "Bruker4"))
        self.graph.setText(_translate("NOK_brukere", "graph"))
        self.back.setText(_translate("NOK_brukere", "back"))
        self.checkBox_6.setText(_translate("NOK_brukere", "Bruker6"))
        self.checkBox_3.setText(_translate("NOK_brukere", "Bruker3"))
        self.stop_dato.setText(_translate("NOK_brukere", "Stop dato"))
        self.checkBox_2.setText(_translate("NOK_brukere", "Bruker2"))
        self.checkBox.setText(_translate("NOK_brukere", "Bruker1"))
        self.checkBox_5.setText(_translate("NOK_brukere", "Bruker5"))
        self.start_dato.setText(_translate("NOK_brukere", "Start dato"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    NOK_brukere = QtWidgets.QMainWindow()
    ui = Ui_NOK_brukere()
    ui.setupUi(NOK_brukere)
    NOK_brukere.show()
    sys.exit(app.exec_())