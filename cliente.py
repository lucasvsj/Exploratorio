import socket
import threading
import json
import pickle
import random
from lobby import Lobby
from PyQt5.QtCore import pyqtSignal, QObject
from menu_principal_backend import VentanaInicio
from PyQt5.QtWidgets import QApplication
from cursor_painting import *


class Cliente(QObject):

    update_lobby_chat = pyqtSignal(dict)
    update_lobby_player_list = pyqtSignal(dict)
    init_lobby_countdown = pyqtSignal(bool)
    update_lobby_countdown = pyqtSignal(int)
    update_lobby_host_widgets = pyqtSignal(dict)
    update_msg_color_update = pyqtSignal(bool)
    update_mm_display = pyqtSignal(dict)
    update_ai_position = pyqtSignal(dict)

    def __init__(self, port, host):
        super().__init__()
        print('Creando cliente')
        self.port = port
        self.host = host
        self.menu_principal = VentanaInicio(self)
        self.update_mm_display.connect(self.menu_principal.update_display)
        self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.isHost = False
        self.color = None
        self.poderes = [False for i in range(6)]
        self.is_in_game = False
        self.user = None
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
        if msg["type"] == "position_update":
            msg_to_str = f'{msg["type"]};{msg["user"]};{msg["info"]}'
            msg_to_send = pickle.dumps(msg_to_str)
        else:
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
        if isinstance(msg, dict):
            if msg["type"] == "chat":
                chat_entry = {  "username" : msg["username"], \
                                "data" : msg["data"]    }
                self.update_lobby_chat.emit(chat_entry)
            elif msg["type"] == "display_update":
                if msg["place"] in ["log_in", "sign_in"]:
                    self.user = msg["username"]
                    display_entry = {   "place" : msg["place"], \
                                        "info" : msg["info"]    }
                    self.update_mm_display.emit(display_entry)
                elif msg["place"] == "lobby":
                    pass
            elif msg["type"] == "users_update":
                if self.user:
                    if list(msg["info"].keys())[0] == self.user:
                        self.isHost = True
                self.update_lobby_player_list.emit(msg["info"])
                self.update_msg_color_update.emit(False)
            elif msg["type"] == "update_countdown":
                if msg["info"] == 5:
                    self.init_lobby_countdown.emit(True)
                else:
                    self.update_lobby_countdown.emit(msg["info"])
            elif msg["type"] == "parameters_update":
                if msg["parameter"] == "fps":
                    self.fps = msg["info"]
                    self.update_lobby_host_widgets.emit(msg)
                elif msg["parameter"] == "win_score":
                    self.win_score = msg["info"]
                    self.update_lobby_host_widgets.emit(msg)
                elif msg["parameter"] == "win_score":
                    self.win_score = msg["info"]
                    self.update_lobby_host_widgets.emit(msg)
                elif msg["parameter"] == "radio":
                    self.radio = msg["info"]
                    self.update_lobby_host_widgets.emit(msg)
                elif msg["parameter"] == "tick_corte":
                    self.tick_corte = msg["info"]
                    self.update_lobby_host_widgets.emit(msg)
                elif msg["parameter"] == "tiempo_corte":
                    self.tiempo_corte = msg["info"]
                    self.update_lobby_host_widgets.emit(msg)
                elif msg["parameter"] == "usain":
                    self.poderes[0] = msg["info"]
                    self.update_lobby_host_widgets.emit(msg)
                elif msg["parameter"] == "limpiessa":
                    self.poderes[1] = msg["info"]
                    self.update_lobby_host_widgets.emit(msg)
                elif msg["parameter"] == "jaime":
                    self.poderes[2] = msg["info"]
                    self.update_lobby_host_widgets.emit(msg)
                elif msg["parameter"] == "cervessa":
                    self.poderes[3] = msg["info"]
                    self.update_lobby_host_widgets.emit(msg)
                elif msg["parameter"] == "felipe":
                    self.poderes[4] = msg["info"]
                    self.update_lobby_host_widgets.emit(msg)
                elif msg["parameter"] == "nebcoins":
                    self.poderes[5] = msg["info"]
                    self.update_lobby_host_widgets.emit(msg)
        else:
            data = msg.split(';')
            dict_to_send = {    "user" : data[1], \
                                "info" : data[2]    }
            self.update_ai_position.emit(dict_to_send)
            print('position sended')


    def close_mm(self, event):
        if event is True:
            self.lobby = Lobby(self)
            self.update_lobby_chat.connect(self.lobby.update_chatbox)
            self.update_lobby_player_list.connect(self.lobby.update_playerlist)
            self.init_lobby_countdown.connect(self.lobby.init_countdown)
            self.update_lobby_countdown.connect(self.lobby.update_countdown)
            self.update_lobby_host_widgets.connect(\
                                                self.lobby.update_host_widgets)
            self.update_msg_color_update.connect(self.lobby.update_msg_color)


    def set_users(self, event):
        self.users = event
        self.color = self.users[self.user]


    def set_inputs(self, event):
        self.lft_key = event[0]
        self.rgt_key = event[1]


    def close_lobby(self, event):
        if event is True:
            self.game = MainWindow(self)
            self.score_board = ScoreBoard(self)
            self.update_ai_position.connect(self.game.update_player_position)


if __name__ == '__main__':
    app = QApplication([])
    port = 3245
    host = 'localhost'
    client = Cliente(port, host)
    app.exec_()
