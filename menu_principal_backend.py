import sys
import random
import PyQt5.QtWidgets as widgets
import PyQt5.QtGui as gui
import PyQt5.QtCore as core
from PyQt5.QtMultimedia import QSound
from PyQt5 import uic
import time
from encriptacion import encriptar, desencriptar


ventana_principal, QtClass = uic.loadUiType('qtd_menu_principal.ui')


class VentanaInicio(ventana_principal, QtClass):


    send_info = core.pyqtSignal(dict)
    close_window = core.pyqtSignal(bool)


    def __init__(self, cliente):
        super().__init__()
        self.setupUi(self)
        self.init_widgets()
        self.cliente = cliente
        self.send_info.connect(self.cliente.send)
        self.close_window.connect(self.cliente.close_mm)
        self.WindowSwitcher.setCurrentIndex(0)
        self.soundtrack = QSound('black_core.wav')
        self.soundtrack.play()
        self.show()


    def init_widgets(self):
        self.IngresarButton.clicked.connect(self.next_page)
        self.RegistrarseButton.clicked.connect(self.to_registrar)
        self.CreditosButton.clicked.connect(self.to_creditos)
        self.VolverButtonLogIn.clicked.connect(self.main_page)
        self.VolverButtonSignIn.clicked.connect(self.main_page)
        self.VolverButtonCreditos.clicked.connect(self.main_page)
        self.SiguienteButtonCreditos.clicked.connect(self.main_page)
        self.SiguienteButtonSignIn.clicked.connect(self.sign_in_checker)
        self.SiguienteButtonLogIn.clicked.connect(self.log_in_checker)
        self.SalirButton.clicked.connect(sys.exit)


    def clear_inputs(self):
        self.InputUsuarioLogIn.setText('')
        self.InputClaveLogIn.setText('')
        self.InputUsuarioSignIn.setText('')
        self.ErrorDisplayerLogIn.setText('')
        self.InputClaveSignIn.setText('')
        self.InputConfirmarClaveSignIn.setText('')
        self.ErrorDisplayerSignIn.setText('')


    def to_registrar(self):
        self.WindowSwitcher.setCurrentIndex(2)


    def to_creditos(self):
        self.WindowSwitcher.setCurrentIndex(3)


    def next_page(self):
        page = self.WindowSwitcher.currentIndex()
        if self.WindowSwitcher.count() - 1 < page + 1:
            page = -1
        self.WindowSwitcher.setCurrentIndex(page+1)


    def main_page(self):
        self.WindowSwitcher.setCurrentIndex(0)
        self.clear_inputs()


    def sign_in_checker(self):
        input_usuario = self.InputUsuarioSignIn.text()
        input_clave = self.InputClaveSignIn.text()
        input_clave_confirm = self.InputConfirmarClaveSignIn.text()
        nuevo_usuario = self.InputUsuarioSignIn.text()
        if input_clave != input_clave_confirm:
            self.ErrorDisplayerSignIn.setText('La clave no es la misma')
        else:
            msg = { "type" : "sign_in", \
                    "username" : nuevo_usuario, \
                    "clave" : input_clave}
            self.send_info.emit(msg)


    def log_in_checker(self):
        usuario = self.InputUsuarioLogIn.text()
        clave = self.InputClaveLogIn.text()
        msg = { "type" : "log_in", \
                "username" : usuario, \
                "clave" : clave}
        self.send_info.emit(msg)


    def update_display(self, msg):
        if msg["place"] == "sign_in":
            self.ErrorDisplayerSignIn.setText(msg["info"])
        elif msg["place"] == "log_in":
            self.ErrorDisplayerLogIn.setText(msg["info"])
            if "Bienvenido" in msg["info"]:
                self.close_window.emit(True)
                self.hide()
                self.soundtrack.stop()
            # widgets.qApp.quit()


    def keyPressEvent(self, event):
        if event.key() == core.Qt.Key_Return:
            if self.WindowSwitcher.currentIndex() == 1:
                if  self.InputUsuarioLogIn.text() != '' and \
                    self.InputClaveLogIn.text() != '':
                        self.log_in_checker()
            elif self.WindowSwitcher.currentIndex() == 2:
                if  self.InputUsuarioSignIn.text() != '' and \
                    self.InputClaveSignIn.text() != '' and \
                    self.InputConfirmarClaveSignIn.text() != '':
                        self.sign_in_checker()


    def mouseMoveEvent(self, event):
        pass


if __name__ == '__main__':
    # app = widgets.QApplication([])
    # init_window = VentanaInicio()
    # app.exec_()
    pass
