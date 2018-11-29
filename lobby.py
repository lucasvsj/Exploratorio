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
    give_inputs = core.pyqtSignal(list)
    give_users = core.pyqtSignal(dict)
    close_window = core.pyqtSignal(bool)


    def __init__(self, cliente):
        super().__init__()
        self.setupUi(self)
        self.cliente = cliente
        self.player = None
        self.setFixedSize(890, 700)
        self.init_widgets()
        self.host_widgets_set = False
        self.send_msg.connect(self.cliente.send)
        self.give_inputs.connect(self.cliente.set_inputs)
        self.give_users.connect(self.cliente.set_users)
        self.close_window.connect(self.cliente.close_lobby)
        self.users = {}
        self.chat_str = ""
        self.soundtrack = QSound('adrenaline.wav')
        self.soundtrack.play()

        self.player_list_items = []
        self.color_list = ['red', 'green', 'blue', 'yellow', 'cyan', 'purple']
        self.players_error_labels = [   self.Player1ErrorDisplayer, \
                                        self.Player2ErrorDisplayer, \
                                        self.Player3ErrorDisplayer, \
                                        self.Player4ErrorDisplayer  ]
        self.labels = [  self.Player1Label, \
                        self.Player2Label, \
                        self.Player3Label, \
                        self.Player4Label   ]
        self.color_lists = [ self.Player1ColorList, \
                            self.Player2ColorList, \
                            self.Player3ColorList, \
                            self.Player4ColorList   ]
        self.color_lists_previous_indexes = [   self.Player1ColorList_pi, \
                                                self.Player2ColorList_pi, \
                                                self.Player3ColorList_pi, \
                                                self.Player4ColorList_pi   ]
        self.english_to_spanish = {  "red" : "Rojo", \
                                    "green" : "Verde", \
                                    "blue" : "Azul", \
                                    "yellow" : "Amarillo", \
                                    "cyan" : "Cyan", \
                                    "purple" : "Morado"}
        self.allListsDisabled = False
        self.color_checker = core.QTimer(self)
        self.msg_color_update = False
        self.color_checker.timeout.connect(self.change_color_checker)
        self.color_checker.start(250)


        self.lft_key = None
        self.rgt_key = None
        self.key_inputs = [ [self.InputPlayer1Izq, \
                                self.InputPlayer1Drc], \
                            [self.InputPlayer2Izq, \
                                self.InputPlayer2Drc], \
                            [self.InputPlayer3Izq, \
                                self.InputPlayer3Drc], \
                            [self.InputPlayer4Izq, \
                                self.InputPlayer4Drc]   ]
        self.str_to_key = { 'q' : core.Qt.Key_Q, \
                            'w' : core.Qt.Key_W, \
                            'e' : core.Qt.Key_E, \
                            'r' : core.Qt.Key_R, \
                            't' : core.Qt.Key_T, \
                            'y' : core.Qt.Key_Y, \
                            'u' : core.Qt.Key_U, \
                            'i' : core.Qt.Key_I, \
                            'o' : core.Qt.Key_O, \
                            'p' : core.Qt.Key_P, \
                            'a' : core.Qt.Key_A, \
                            's' : core.Qt.Key_S, \
                            'd' : core.Qt.Key_D, \
                            'f' : core.Qt.Key_F, \
                            'g' : core.Qt.Key_G, \
                            'h' : core.Qt.Key_H, \
                            'j' : core.Qt.Key_J, \
                            'k' : core.Qt.Key_K, \
                            'l' : core.Qt.Key_L, \
                            'ñ' : 209, \
                            'z' : core.Qt.Key_Z, \
                            'x' : core.Qt.Key_X, \
                            'c' : core.Qt.Key_C, \
                            'v' : core.Qt.Key_V, \
                            'b' : core.Qt.Key_B, \
                            'n' : core.Qt.Key_N, \
                            'm' : core.Qt.Key_M     }
        self.input_error_labels = [ [self.Player1IzqKeyErrorLabel, \
                                        self.Player1DrcKeyErrorLabel], \
                                    [self.Player2IzqKeyErrorLabel, \
                                        self.Player2DrcKeyErrorLabel], \
                                    [self.Player3IzqKeyErrorLabel, \
                                        self.Player3DrcKeyErrorLabel], \
                                    [self.Player4IzqKeyErrorLabel, \
                                        self.Player4DrcKeyErrorLabel]   ]
        self.poderes = [False for i in range(6)]
        self.fps = 1
        self.win_score = 0
        self.radio = 0
        self.tick_corte = 0
        self.tiempo_corte = 0
        self.show()


    def init_widgets(self):
        self.Player1ColorList_pi = -1
        self.Player2ColorList_pi = -1
        self.Player3ColorList_pi = -1
        self.Player4ColorList_pi = -1
        self.AllDisplayer.setAutoFillBackground(True)
        pallete = self.palette()
        pallete.setColor(self.backgroundRole(), core.Qt.black)
        self.AllDisplayer.setPalette(pallete)
        self.EnviarButton.clicked.connect(self.get_msg)


    def init_Host_widgets(self):
        self.JugarButton.clicked.connect(self.start_countdown)

        self.FPSInput.setReadOnly(False)
        self.FPSButton.clicked.connect(self.set_fps)
        self.WinScoreInput.setReadOnly(False)
        self.WinScoreButton.clicked.connect(self.set_win_score)
        self.RadioInput.setReadOnly(False)
        self.RadioButton.clicked.connect(self.set_radio)
        self.TickCorteInput.setReadOnly(False)
        self.TickCorteButton.clicked.connect(self.set_tick_corte)
        self.TiempoCorteInput.setReadOnly(False)
        self.TiempoCorteButton.clicked.connect(self.set_tiempo_corte)

        self.UsainInput.setCheckable(True)
        self.UsainButton.clicked.connect(self.set_usain)
        self.LimpiessaInput.setCheckable(True)
        self.LimpiessaButton.clicked.connect(self.set_limpiessa)
        self.JaimeInput.setCheckable(True)
        self.JaimeButton.clicked.connect(self.set_jaime)
        self.CervessaInput.setCheckable(True)
        self.CervessaButton.clicked.connect(self.set_cervessa)
        self.FelipeInput.setCheckable(True)
        self.FelipeButton.clicked.connect(self.set_felipe)
        self.NebcoinsInput.setCheckable(True)
        self.NebcoinsButton.clicked.connect(self.set_nebcoins)


    def update_host_widgets(self, event):
        if self.cliente.isHost is not True:
            print('NO HOST')
            if event["parameter"] == "fps":
                self.FPSInput.setText(str(event["info"]))
            elif event["parameter"] == "win_score":
                self.WinScoreInput.setText(str(event["info"]))
            elif event["parameter"] == "radio":
                self.RadioInput.setText(str(event["info"]))
            elif event["parameter"] == "tick_corte":
                self.TickCorteInput.setText(str(event["info"]))
            elif event["parameter"] == "tiempo_corte":
                self.TiempoCorteInput.setText(str(event["info"]))
            elif event["parameter"] == "usain":
                self.UsainInput.setCheckState(event["info"])
            elif event["parameter"] == "limpiessa":
                self.LimpiessaInput.setCheckState(event["info"])
            elif event["parameter"] == "jaime":
                self.JaimeInput.setCheckState(event["info"])
            elif event["parameter"] == "cervessa":
                self.CervessaInput.setCheckState(event["info"])
            elif event["parameter"] == "felipe":
                self.FelipeInput.setCheckState(event["info"])
            elif event["parameter"] == "nebcoins":
                self.NebcoinsInput.setCheckState(event["info"])



    #Justificado porque esta seguido
    def set_fps(self):
        self.fps = int(self.FPSInput.text())
        msg_to_send = { "type" : "parameters_update", \
                        "parameter" : "fps", \
                        "info" : self.fps}
        self.send_msg.emit(msg_to_send)
    def set_win_score(self):
        self.win_score = int(self.WinScoreInput.text())
        msg_to_send = { "type" : "parameters_update", \
                        "parameter" : "win_score", \
                        "info" : self.win_score}
        self.send_msg.emit(msg_to_send)
    def set_radio(self):
        self.radio = int(self.RadioInput.text())
        msg_to_send = { "type" : "parameters_update", \
                        "parameter" : "radio", \
                        "info" : self.radio}
        self.send_msg.emit(msg_to_send)
    def set_tick_corte(self):
        self.tick_corte = int(self.TickCorteInput.text())
        msg_to_send = { "type" : "parameters_update", \
                        "parameter" : "tick_corte", \
                        "info" : self.tick_corte}
        self.send_msg.emit(msg_to_send)
    def set_tiempo_corte(self):
        self.tiempo_corte = int(self.TiempoCorteInput.text())
        msg_to_send = { "type" : "parameters_update", \
                        "parameter" : "tiempo_corte", \
                        "info" : self.tiempo_corte}
        self.send_msg.emit(msg_to_send)
    def set_usain(self):
        self.poderes[0] = int(self.UsainInput.isChecked())
        msg_to_send = { "type" : "parameters_update", \
                        "parameter" : "usain", \
                        "info" : self.poderes[0]}
        self.send_msg.emit(msg_to_send)
    def set_limpiessa(self):
        self.poderes[1] = int(self.LimpiessaInput.isChecked())
        msg_to_send = { "type" : "parameters_update", \
                        "parameter" : "limpiessa", \
                        "info" : self.poderes[1]}
        self.send_msg.emit(msg_to_send)
    def set_jaime(self):
        self.poderes[2] = int(self.JaimeInput.isChecked())
        msg_to_send = { "type" : "parameters_update", \
                        "parameter" : "jaime", \
                        "info" : self.poderes[2]}
        self.send_msg.emit(msg_to_send)
    def set_cervessa(self):
        self.poderes[3] = int(self.CervessaInput.isChecked())
        msg_to_send = { "type" : "parameters_update", \
                        "parameter" : "cervessa", \
                        "info" : self.poderes[3]}
        self.send_msg.emit(msg_to_send)
    def set_felipe(self):
        self.poderes[4] = int(self.FelipeInput.isChecked())
        msg_to_send = { "type" : "parameters_update", \
                        "parameter" : "felipe", \
                        "info" : self.poderes[4]}
        self.send_msg.emit(msg_to_send)
    def set_nebcoins(self):
        self.poderes[5] = int(self.NebcoinsInput.isChecked())
        msg_to_send = { "type" : "parameters_update", \
                        "parameter" : "nebcoins", \
                        "info" : self.poderes[5]}
        self.send_msg.emit(msg_to_send)


    def keyPressEvent(self, event):
        izq_key = self.key_inputs[self.player-1][0]
        izq_label = self.input_error_labels[self.player-1][0]
        drc_key = self.key_inputs[self.player-1][1]
        drc_label = self.input_error_labels[self.player-1][1]
        if izq_key.text() != '':
            if len(izq_key.text()) == 1:
                try:
                    self.lft_key = self.str_to_key[izq_key.text().lower()]
                except KeyError:
                    izq_label.setText( \
                                    'Ingrese\n' + \
                                    'una\n' + \
                                    'letra\n'   )
                    izq_label.setStyleSheet( \
                        f'font-weight: bolder; color: grey')
                    return
                if self.lft_key == self.rgt_key:
                        izq_label.setText( \
                                        'Tecla\n' + \
                                        'ya esta\n' + \
                                        'usada')
                        izq_label.setStyleSheet( \
                            f'font-weight: bolder; color: grey')
                        self.lft_key = None
                else:
                    izq_label.setText('')
            else:
                izq_label.setText( \
                                'Ingrese\n' + \
                                'una\n' + \
                                'letra\n' + \
                                'no una\n' + \
                                'palabra')
                izq_label.setStyleSheet( \
                    f'font-weight: bolder; color: grey')
        if drc_key.text() != '':
            if len(drc_key.text()) == 1:
                try:
                    self.rgt_key = self.str_to_key[drc_key.text().lower()]
                except KeyError:
                    drc_label.setText( \
                                    'Ingrese\n' + \
                                    'una\n' + \
                                    'letra\n'   )
                    drc_label.setStyleSheet( \
                        f'font-weight: bolder; color: grey')
                    return
                if self.rgt_key == self.lft_key:
                        drc_label.setText( \
                                        'Tecla\n' + \
                                        'ya esta\n' + \
                                        'usada')
                        drc_label.setStyleSheet( \
                            f'font-weight: bolder; color: grey')
                        self.rgt_key = None
                else:
                    drc_label.setText('')
            else:
                drc_label.setText( \
                                'Ingrese\n' + \
                                'una\n' + \
                                'letra\n' + \
                                'no una\n' + \
                                'palabra')
                drc_label.setStyleSheet( \
                    f'font-weight: bolder; color: grey')
        print(self.lft_key, self.rgt_key)

        if event.key() == core.Qt.Key_Return:
            if self.ChatInput.text() != '':
                self.get_msg()


    def get_msg(self):
        if self.ChatInput.text() != '':
            msg = { "type" : "chat", \
                    "username" : self.cliente.user, \
                    "data" : self.ChatInput.text()}
            self.ChatInput.setText('')
            self.send_msg.emit(msg)


    def start_countdown(self):
        msg = { "type" : "display_update", \
                "place" : "lobby", \
                "info" : "start_countdown"}
        self.send_msg.emit(msg)


    def update_playerlist(self, users):
        if self.player is None:
            self.player = len(users)
            self.block_keys_inputs()
            self.update_color_lists()
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
                self.update_player_widgets_color(user, \
                                        list(self.users.keys()).index(user), \
                                        users[user])
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
                # print(widget.layout().itemAt(0).widget().setText('Hola'))
                item.setSizeHint(widget.sizeHint())
                self.player_list_items.append(item)
                self.PlayerList.addItem(item)
                # self.PlayerList.addItem(f'{user}')
                self.PlayerList.setItemWidget(item, widget)
            else:
                self.users[user] = users[user]
                self.update_playerlist_networking(user)
        if self.host_widgets_set is False:
            if self.cliente.isHost:
                self.init_Host_widgets()
                self.host_widgets_set = True
        self.color_list = ['red', 'green', 'blue', 'yellow', 'cyan', 'purple']


    def update_playerlist_networking(self, user):
        player_index = list(self.users.keys()).index(user)
        color = f'font-weight: bolder; color: {self.users[user]}'
        print(player_index)
        self.PlayerList.itemWidget( \
            self.PlayerList.item(player_index)).layout().itemAt( \
                0).widget().setStyleSheet(color)
        self.update_player_widgets_color(user, \
                                list(self.users.keys()).index(user), \
                                self.users[user])




    def update_chatbox(self, msg):
        self.chat_str += f'{msg["username"]}: {msg["data"]}\n'
        self.ChatDisplayer.setText(self.chat_str)


    def init_countdown(self, event):
        if event is True:
            self.gridLayout_9.removeWidget(self.JugarButton)
            self.JugarButton.deleteLater()
            self.JugarButton = None
            self.CountDown = widgets.QLCDNumber(self)
            self.gridLayout_9.addWidget(self.CountDown)
            self.CountDown.display(5)
            self.CountDown.setDigitCount(len("5"))


    def update_countdown(self, event):
        self.CountDown.display(event)
        self.CountDown.setDigitCount(len(str(event)))
        if event == 0:
            self.give_inputs.emit([self.lft_key, self.rgt_key])
            self.give_users.emit(self.users)
            self.close_window.emit(True)
            self.hide()
            self.soundtrack.stop()



    def update_msg_color(self, event):
        self.msg_color_update = event


    def change_color_checker(self):
        if self.player is not None and self.msg_color_update is False:
            player_widget = { \
                        1 : [self.Player1ColorList, self.Player1ColorList_pi], \
                        2 : [self.Player2ColorList, self.Player2ColorList_pi], \
                        3 : [self.Player3ColorList, self.Player3ColorList_pi], \
                        4 : [self.Player4ColorList, self.Player4ColorList_pi]   }
            widget = player_widget[self.player][0]
            last_index = player_widget[self.player][1]
            if widget.currentIndex() != last_index:
                if self.color_list[widget.currentIndex()] not in \
                                                        self.users.values():
                    msg = { "type" : "color_update", \
                            "username" : self.cliente.user, \
                            "info" : self.color_list[widget.currentIndex()]}
                    self.send_msg.emit(msg)
                    self.msg_color_update = True
                else:
                    color_usado = self.color_list[widget.currentIndex()]
                    self.update_error_label(color_usado)


    def update_color_lists(self):
        for i in range(4):
            if i != self.player-1:
                self.color_lists[i].setEnabled(False)


    def update_error_label(self, color):
        self.players_error_labels[self.player-1].setText( \
                                    'El color:\n' + \
                                    f'{self.english_to_spanish[color]}\n' + \
                                    'ya esta ocupado')
        self.players_error_labels[self.player-1].setStyleSheet( \
                                f'font-weight: bolder; color: grey')
        self.color_lists[self.player-1].setCurrentIndex( \
                        self.color_lists_previous_indexes[self.player-1])

    def update_player_widgets_color(self, player, player_index, color):
        self.labels[player_index].setText(player)
        self.labels[player_index].setStyleSheet( \
                                        f'font-weight: bolder; color: {color}')
        self.color_lists[player_index].setCurrentIndex( \
                                            self.color_list.index(color))
        self.color_lists_previous_indexes[player_index] = \
                                    self.color_lists[player_index].currentIndex()
        self.Player1ColorList_pi = self.color_lists_previous_indexes[0]
        self.Player2ColorList_pi = self.color_lists_previous_indexes[1]
        self.Player3ColorList_pi = self.color_lists_previous_indexes[2]
        self.Player4ColorList_pi = self.color_lists_previous_indexes[3]
        self.players_error_labels[self.player-1].setText('')


    def block_keys_inputs(self):
        for i in range(4):
            if i != self.player-1:
                for input in self.key_inputs[i]:
                    input.setReadOnly(True)



if __name__ == '__main__':
    # app = widgets.QApplication([])
    # init_window = Lobby('hola')
    # app.exec_()
    users = {'lucas' : 'rojo', 'pedro' : 'azul'}
    # i_d = {users[char] : char for char in users}
    print('rojo' in users)
