import socket
import threading
import json
import random
from lobby import Lobby
from PyQt5.QtCore import pyqtSignal, QObject
from menu_principal_backend import VentanaInicio
from PyQt5.QtWidgets import QApplication


class Cliente(QObject):

    update_lobby_chat = pyqtSignal(dict)
    update_mm_display = pyqtSignal(dict)

    def __init__(self, port, host):
        super().__init__()
        print('Creando cliente')
        self.port = port
        self.host = host
        self.menu_principal = VentanaInicio(self)
        self.update_mm_display.connect(self.menu_principal.update_display)
        self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.connect_to_server()
            self.listen()
        except ConnectionError:
            print('Conexion terminada')
            self.socket_cliente.close()
            exit()


    def connect_to_server(self):
        self.socket_cliente.connect((self.host, self.port))
        print('Cliente conectado a servidor')


    def listen(self):
        thread = threading.Thread(target=self.listen_thread, daemon=True)
        thread.start()


    def send(self, msg):
        json_msg = json.dumps(msg)
        msg_to_send = json_msg.encode()
        self.socket_cliente.send(msg_to_send)


    def listen_thread(self):
        while True:
            data = self.socket_cliente.recv(2**16)
            decoded_data = data.decode()
            decoded_data = decoded_data.replace('\'', '\"')
            data = json.loads(decoded_data)
            self.manipulate_msg(data)


    def manipulate_msg(self, msg):
        if msg["type"] == "chat":
            chat_entry = {  "username" : msg["username"], \
                            "data" : msg["data"]    }
            self.update_lobby_chat.emit(chat_entry)
        elif msg["type"] == "display_update":
            self.user = msg["username"]
            display_entry = {   "place" : msg["place"], \
                                "info" : msg["info"]    }
            self.update_mm_display.emit(display_entry)


    def close_mm(self, event):
        if event is True:
            self.lobby = Lobby(self)
            self.update_lobby_chat.connect(self.lobby.update_chatbox)


if __name__ == '__main__':
    app = QApplication([])
    port = 3245
    host = '192.168.0.3'
    client = Cliente(port, host)
    app.exec_()
