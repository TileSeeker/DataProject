from PyQt5 import QtWidgets, QtCore
import  datetime
import pandas as pd
import matplotlib.pyplot as plt

from meny import Ui_meny
from NOK_brukere import Ui_NOK_brukere
from NOK_felles import Ui_NOK_felles
from solceller import Ui_solceller
from kwh_brukere import Ui_kwh_brukere
from kwh_felles import Ui_kwh_felles

class solcelle(QtWidgets.QMainWindow, Ui_solceller):
    def __init__(self, parent=None):
        super(solcelle,self).__init__(parent)
        self.setupUi(self)
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
        plt.title(start_dato + "-" + stop_dato + "     kWh spart:" + str(kWhspart))
        plt.show()

class kwhbruker(QtWidgets.QMainWindow, Ui_kwh_brukere):
    def __init__(self, parent=None):
        super(kwhbruker,self).__init__(parent)
        self.setupUi(self)
        self.back.clicked.connect(self.hide)
        


class kwhfelles(QtWidgets.QMainWindow, Ui_kwh_felles):
    def __init__(self, parent=None):
        super(kwhfelles,self).__init__(parent)
        self.setupUi(self)
        self.back.clicked.connect(self.hide)

class NOKbruker(QtWidgets.QMainWindow, Ui_NOK_brukere):
    def __init__(self, parent=None):
        super(NOKbruker,self).__init__(parent)
        self.setupUi(self)
        self.back.clicked.connect(self.hide)

class NOKfelles(QtWidgets.QMainWindow, Ui_NOK_felles):
    def __init__(self, parent=None):
        super(NOKfelles,self).__init__(parent)
        self.setupUi(self)
        self.back.clicked.connect(self.hide)

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

#   switch_window = QtCore.pyqtSignal(str)     

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = menyM()
    w.show()
    sys.exit(app.exec_())

