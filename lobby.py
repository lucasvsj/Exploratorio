import sys
import random
import PyQt5.QtWidgets as widgets
import PyQt5.QtCore as core
import PyQt5.QtGui as gui
from PyQt5.QtMultimedia import QSound
from PyQt5 import uic

ventana_principal, QtClass = uic.loadUiType('qtd_lobby.ui')


class Lobby(ventana_principal, QtClass):


    send_msg = core.pyqtSignal(dict)


    def __init__(self, cliente):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(890, 700)
        self.init_widgets()
        self.cliente = cliente
        self.send_msg.connect(self.cliente.send)
        self.users = {}
        self.chat_str = ""
        self.show()


    def init_widgets(self):
        self.AllDisplayer.setAutoFillBackground(True)
        pallete = self.palette()
        pallete.setColor(self.backgroundRole(), core.Qt.black)
        self.AllDisplayer.setPalette(pallete)
        self.EnviarButton.clicked.connect(self.get_msg)


    def get_msg(self):
        if self.ChatInput.text() != '':
            msg = { "type" : "chat", \
                    "username" : self.cliente.user, \
                    "data" : self.ChatInput.text()}
            self.ChatInput.setText('')
            self.send_msg.emit(msg)


    def update_playerlist(self, users):
        for user in users.keys():
            if user not in self.users.keys():
                self.users[user] = users[user]
                item = widgets.QListWidgetItem()
                label_user = widgets.QLabel(user)
                widget = widgets.QWidget()
                layout = widgets.QHBoxLayout()
                layout.addWidget(label_user)
                color = f'font-weight: bolder; color: {users[user]}'
                label_user.setStyleSheet(color)
                if user == list(self.users.keys())[0]:
                    label_host = widgets.QLabel()
                    pixmap = gui.QPixmap('sprites/crown.png')
                    pixmap = pixmap.scaled(pixmap.width()* \
                                            (16*1.5/pixmap.width()), \
                                            pixmap.height()*\
                                            (16*1.5/pixmap.height()))
                    label_host.setPixmap(pixmap)
                    layout.addWidget(label_host)
                widget.setLayout(layout)
                item.setSizeHint(widget.sizeHint())
                self.PlayerList.addItem(item)
                self.PlayerList.setItemWidget(item, widget)


    def update_chatbox(self, msg):
        self.chat_str += f'{msg["username"]}: {msg["data"]}\n'
        self.ChatDisplayer.setText(self.chat_str)


if __name__ == '__main__':
    # app = widgets.QApplication([])
    # init_window = Lobby('hola')
    # app.exec_()
    pass
