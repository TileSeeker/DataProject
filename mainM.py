from PyQt5 import QtWidgets, QtCore
import  datetime
import pandas as pd
import matplotlib.pyplot as plt
from PyQt5.QtCore import QDate

from meny import Ui_meny
from NOK_brukere import Ui_NOK_brukere
from NOK_felles import Ui_NOK_felles
from solceller import Ui_solceller
from kwh_brukere import Ui_kwh_brukere
from kwh_felles import Ui_kwh_felles


d = QDate(2020, 1, 1)


class solcelle(QtWidgets.QMainWindow, Ui_solceller):
    def __init__(self, parent=None):
        super(solcelle,self).__init__(parent)
        self.setupUi(self)
        self.dateedit1.setMinimumDate(d)
        self.dateedit_2.setMinimumDate(d)
        self.back.clicked.connect(self.hide)
        self.graph.clicked.connect(self.graph_solar)

    def graph_solar(self):
        start_dato = self.dateedit1.date().toString("dd.MM.yyyy")
        stop_dato = self.dateedit_2.date().toString("dd.MM.yyyy")
        start_dato_ts = int(datetime.datetime.strptime(start_dato, '%d.%m.%Y').timestamp())
        stop_dato_ts = int(datetime.datetime.strptime(stop_dato, '%d.%m.%Y').timestamp())
        data = pd.read_csv("newWeatherData.csv", na_filter=False, dtype={"dt": "int64","generated_solar_power[Wh]":"float64"}, 
                    parse_dates=["dt_iso"]).drop_duplicates(subset=["dt"]).reset_index(drop=True)
        data = data[(data["dt"] >= start_dato_ts) & (data["dt"] <= stop_dato_ts)]
        data = data["generated_solar_power[Wh]"].tolist()
        kWhspart = round(sum(data)*0.001, 3)
        plt.plot(data)
        plt.xlabel("Time(h)")
        plt.ylabel("solarpower(Wh)")
        plt.title(start_dato + "-" + stop_dato + "     kWh saved:" + str(kWhspart))
        mng = plt.get_current_fig_manager()
        mng.window.showMaximized()
        plt.show()

class kwhbruker(QtWidgets.QMainWindow, Ui_kwh_brukere):
    def __init__(self, parent=None):
        super(kwhbruker,self).__init__(parent)
        self.setupUi(self)
        self.dateedit1.setMinimumDate(d)
        self.dateedit_2.setMinimumDate(d)
        self.back.clicked.connect(self.hide)
        self.graph.clicked.connect(self.user_sel)
       
    def user_sel(self):
        if self.checkBox.isChecked() == True:
            self.graph_kwhb("1")
        else:
            pass
        if self.checkBox_2.isChecked() == True:
            self.graph_kwhb("2")
        else:
            pass
        if self.checkBox_3.isChecked() == True:
            self.graph_kwhb("3")
        else:
            pass
        if self.checkBox_4.isChecked() == True:
            self.graph_kwhb("4")
        else:
            pass
        if self.checkBox_5.isChecked() == True:
            self.graph_kwhb("5")
        else:
            pass
        if self.checkBox_6.isChecked() == True:
            self.graph_kwhb("6")
        else:
            pass
    def graph_kwhb(self, value):
        start_dato = self.dateedit1.date().toString("dd.MM.yyyy")
        stop_dato = self.dateedit_2.date().toString("dd.MM.yyyy")        
        start_dato_ts = int(datetime.datetime.strptime(start_dato, '%d.%m.%Y').timestamp())
        stop_dato_ts = int(datetime.datetime.strptime(stop_dato, '%d.%m.%Y').timestamp())
        col = "User"+ value + "_power_consumption"
        data = pd.read_csv("newWeatherData.csv", na_filter=False, dtype={"dt": "int64",col:"float64"}, 
                    parse_dates=["dt_iso"]).drop_duplicates(subset=["dt"]).reset_index(drop=True)
        data = data[(data["dt"] >= start_dato_ts) & (data["dt"] <= stop_dato_ts)]
        data = data[col].tolist()
        kWhbrukt = round(sum(data)*0.001, 3)
        plt.plot(data, label=col + str(kWhbrukt))
        plt.xlabel("Time(h)")
        plt.ylabel("Power consumption(Wh)")
        plt.title(start_dato + "-" + stop_dato)
        plt.legend()
        mng = plt.get_current_fig_manager()
        mng.window.showMaximized()
        plt.show()

class kwhfelles(QtWidgets.QMainWindow, Ui_kwh_felles):
    def __init__(self, parent=None):
        super(kwhfelles,self).__init__(parent)
        self.setupUi(self)
        self.dateedit1.setMinimumDate(d)
        self.dateedit_2.setMinimumDate(d)
        self.back.clicked.connect(self.hide)
        self.graph.clicked.connect(self.graph_whf)

    def graph_whf(self):
        start_dato = self.dateedit1.date().toString("dd.MM.yyyy")
        stop_dato = self.dateedit_2.date().toString("dd.MM.yyyy")
        start_dato_ts = int(datetime.datetime.strptime(start_dato, '%d.%m.%Y').timestamp())
        stop_dato_ts = int(datetime.datetime.strptime(stop_dato, '%d.%m.%Y').timestamp())
        data = pd.read_csv("newWeatherData.csv", na_filter=False, dtype={"dt": "int64","shared_power":"float64"}, 
                    parse_dates=["dt_iso"]).drop_duplicates(subset=["dt"]).reset_index(drop=True)
        data = data[(data["dt"] >= start_dato_ts) & (data["dt"] <= stop_dato_ts)]
        data = data["shared_power"].tolist()
        kWhspart = round(sum(data)*0.001, 3)
        plt.plot(data)
        plt.xlabel("Time(h)")
        plt.ylabel("total(Wh)")
        plt.title(start_dato + "-" + stop_dato + "     kWh used:" + str(kWhspart))
        mng = plt.get_current_fig_manager()
        mng.window.showMaximized()
        plt.show()

class NOKbruker(QtWidgets.QMainWindow, Ui_NOK_brukere):
    def __init__(self, parent=None):
        super(NOKbruker,self).__init__(parent)
        self.setupUi(self)
        self.dateedit1.setMinimumDate(d)
        self.dateedit_NOKb2.setMinimumDate(d)
        self.back.clicked.connect(self.hide)
        self.graph.clicked.connect(self.user_sel)
       
    def user_sel(self):
        if self.checkBox.isChecked() == True:
            self.graph_nokb("1")
        else:
            pass
        if self.checkBox_2.isChecked() == True:
            self.graph_nokb("2")
        else:
            pass
        if self.checkBox_3.isChecked() == True:
            self.graph_nokb("3")
        else:
            pass
        if self.checkBox_4.isChecked() == True:
            self.graph_nokb("4")
        else:
            pass
        if self.checkBox_5.isChecked() == True:
            self.graph_nokb("5")
        else:
            pass
        if self.checkBox_6.isChecked() == True:
            self.graph_nokb("6")
        else:
            pass
        

    def graph_nokb(self, value):
        start_dato = self.dateedit1.date().toString("dd.MM.yyyy")
        stop_dato = self.dateedit_NOKb2.date().toString("dd.MM.yyyy")        
        start_dato_ts = int(datetime.datetime.strptime(start_dato, '%d.%m.%Y').timestamp())
        stop_dato_ts = int(datetime.datetime.strptime(stop_dato, '%d.%m.%Y').timestamp())
        col = "User"+ value + "_NOK"
        data = pd.read_csv("newWeatherData.csv", na_filter=False, dtype={"dt": "int64",col:"float64"}, 
                    parse_dates=["dt_iso"]).drop_duplicates(subset=["dt"]).reset_index(drop=True)
        data = data[(data["dt"] >= start_dato_ts) & (data["dt"] <= stop_dato_ts)]
        data = data[col].tolist()
        nokbrukt = round(sum(data), 2)
        plt.plot(data, label = col + str(nokbrukt))
        plt.xlabel("Time(h)")
        plt.ylabel("Cost(NOK)")
        plt.title(start_dato + "-" + stop_dato)
        plt.legend()
        mng = plt.get_current_fig_manager()
        mng.window.showMaximized()
        plt.show()

class NOKfelles(QtWidgets.QMainWindow, Ui_NOK_felles):
    def __init__(self, parent=None):
        super(NOKfelles,self).__init__(parent)
        self.setupUi(self)
        self.dateedit1.setMinimumDate(d)
        self.dateedit_2.setMinimumDate(d)
        self.back.clicked.connect(self.hide)
        self.graph.clicked.connect(self.graph_nokf)

    def graph_nokf(self):
        start_dato = self.dateedit1.date().toString("dd.MM.yyyy")
        stop_dato = self.dateedit_2.date().toString("dd.MM.yyyy")
        start_dato_ts = int(datetime.datetime.strptime(start_dato, '%d.%m.%Y').timestamp())
        stop_dato_ts = int(datetime.datetime.strptime(stop_dato, '%d.%m.%Y').timestamp())
        data = pd.read_csv("newWeatherData.csv", na_filter=False, dtype={"dt": "int64","shared_NOK":"float64"}, 
                    parse_dates=["dt_iso"]).drop_duplicates(subset=["dt"]).reset_index(drop=True)
        data = data[(data["dt"] >= start_dato_ts) & (data["dt"] <= stop_dato_ts)]
        data = data["shared_NOK"].tolist()
        kWhspart = round(sum(data)*0.001, 2)
        plt.plot(data)
        plt.xlabel("Time(h)")
        plt.ylabel("cost(NOK)")
        plt.title(start_dato + "-" + stop_dato + "     NOK cost:" + str(kWhspart))
        mng = plt.get_current_fig_manager()
        mng.window.showMaximized()
        plt.show()


class menyM(QtWidgets.QMainWindow, Ui_meny):
    def __init__(self, parent=None):
        super(menyM,self).__init__(parent)
        self.setupUi(self)
        self.other_window1 = NOKfelles()
        self.nokfelles_button.clicked.connect(self.other_window1.show)
        self.other_window2 = NOKbruker()
        self.nokbrukere_button.clicked.connect(self.other_window2.show)
        self.other_window3 = kwhfelles()
        self.kwhfelles_button.clicked.connect(self.other_window3.show)
        self.other_window4 = kwhbruker()
        self.kwhbrukere_button.clicked.connect(self.other_window4.show)
        self.other_window5 = solcelle()
        self.solcelle_button.clicked.connect(self.other_window5.show)



class Controller:
    def __init__(self):
        pass
   

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = menyM()
    w.show()
    sys.exit(app.exec_())

