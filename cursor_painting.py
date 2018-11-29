import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QFrame, \
                            QGraphicsScene
from PyQt5.QtGui import QPainter, QColor, QPen, QPainterPath, \
                        QImage, QPixmap, QTransform
from PyQt5.QtCore import Qt, QPoint, QThread, QTimer, QRect, pyqtSignal
from PyQt5 import uic
import math
import random
from extra_clases import Point

score_board, QtClass = uic.loadUiType('qtd_score_board.ui')


class ScoreBoard(score_board, QtClass):


    def __init__(self, cliente):
        super().__init__()
        self.setupUi(self)
        self.cliente = cliente
        self.display_x = 281
        self.display_y = 731
        self.setGeometry(256*5, 35*2, \
                        self.display_x, self.display_y)
        self.setFixedSize(self.display_x, self.display_y)
        self.player_labels = [  self.Player1NameDisplay, \
                                self.Player2NameDisplay, \
                                self.Player3NameDisplay, \
                                self.Player4NameDisplay ]
        self.player_scores = [  self.Player1ScoreDisplayer, \
                                self.Player2ScoreDisplayer, \
                                self.Player3ScoreDisplayer, \
                                self.Player4ScoreDisplayer ]
        self.init_GUI()
        self.show()


    def init_GUI(self):
        self.GoalDisplayer.setText(str(self.cliente.win_score))
        for (i, user) in enumerate(self.cliente.users):
            self.player_labels[i].setText(user)
            self.player_labels[i].setStyleSheet( \
                f'font-weight: bolder; color: {self.cliente.users[user]}')
            self.player_scores[i].setText(str(0))



    def update_score(self, event):
        pass




class MainWindow(QWidget):


    send_position = pyqtSignal(dict)


    def __init__(self, cliente):
        super().__init__()
        self.cliente = cliente
        self.users = self.cliente.users
        self.send_position.connect(self.cliente.send)
        self.init_GUI()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.mainloop)
        self.timer.start(1000/self.fps)
        self.is_paused = False

    def init_GUI(self):
        self.fps = self.cliente.fps
        self.goal = self.cliente.win_score
        self.radio = self.cliente.radio
        self.cada_tiempo = random.randint(0, self.cliente.tick_corte)
        self.tiempo_corte = random.randint(0, self.cliente.tiempo_corte)
        self.display_x = 256*5
        self.display_y = 192*5
        self.setGeometry(self.display_y//4, 0+35*2, \
                        self.display_x, self.display_y)

        self.character_color = self.cliente.color
        self.brush_size = 4
        self.color_brushes = { 'red' : Qt.red, \
                            'green' : Qt.green, \
                            'blue' : Qt.blue, \
                            'yellow' : Qt.yellow, \
                            'cyan' : Qt.cyan, \
                            'purple' : Qt.magenta   }
        self.brush_color = self.color_brushes[self.character_color]
        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.black)

        self.character = Character(self)
        self.character.run()
        self.character.cut_track_checker()
        self.character.pickup_power_checker()

        self.other_players = []
        self.spawn_other_players()
        for player in self.other_players:
            player.run()
            player.cut_track_checker()
            player.pickup_power_checker()

        self.powers_in_screen = set()
        self.power = Poder(self)
        self.powers_in_screen.add(self.power)

        self.tracks = set()

        self.show()


    def spawn_other_players(self):
        for user in self.users:
            # print(self.users[user], self.brush_color)
            if self.users[user] != self.character_color:
                player = AI(self, self.users[user])
                self.other_players.append(player)


    def mainloop(self):
        pass



    def update_player_position(self, event):
        for player in self.other_players:
            if event["user"] == player.color:
                player.x = event["info"]["x"]
                player.y = event["info"]["y"]
        print('position updated')


    def keyPressEvent(self, event):
        if event.key() == self.cliente.lft_key:
            self.character.angle += -math.radians(3)
        if event.key() == self.cliente.rgt_key:
            self.character.angle += math.radians(3)
        if event.key() == Qt.Key_Space:
            if self.is_paused is False:
                self.is_paused = True
            else:
                self.is_paused = False


    def paintEvent(self, event):
        qp = QPainter(self)
        qp.drawImage(self.rect(), self.image, self.image.rect())



class Character(QWidget):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.color = self.parent.character_color
        self.label = QLabel(self.parent)
        self._angle = math.radians(0)
        self.radio = self.parent.radio
        self.anim_angle = 0
        self.velocidad = 1
        self.update_Pixmap()
        self._x = 0
        self._y = 0
        self.isAlive = True
        self.drawing = True

        self.fps = self.parent.fps
        self.sum_intervals = 0
        self.seconds_passed = 0

        self.cada_tiempo = self.parent.cada_tiempo
        self.tiempo_corte = self.parent.tiempo_corte

        self.centro = Point(self.x+self.pixmap.width()/2, \
                            self.y+self.pixmap.height()/2)
        self.distancia_hitbox = 8
        self.hitbox_poderes = 10
        self.has_power = False
        self.x = random.randint(32*6, self.parent.display_x-32*6)
        self.y = random.randint(32*6, self.parent.display_y-32*6)
        position = { "x" : self.x, "y" : self.y }
        msg_to_send = { "type" : "position_update", \
                        "user" : self.color, \
                        "info" : position}
        self.parent.send_position.emit(msg_to_send)


    @property
    def x(self):
        return self._x


    @x.setter
    def x(self, value):
        self._x = value
        self.label.move(self.x, self.y)


    @property
    def y(self):
        return self._y


    @y.setter
    def y(self, value):
        self._y = value
        self.label.move(self.x, self.y)


    @property
    def angle(self):
        return self._angle


    @angle.setter
    def angle(self, value):
        self._angle = value
        self.update_Pixmap()


    def update_Pixmap(self, dead=None):
        if dead is True:
            self.pixmap = QPixmap(f'sprites/{self.color}_ball_dead.png')
        else:
            self.pixmap = QPixmap(f'sprites/{self.color}_ball.png')
        self.label.setMinimumSize(self.pixmap.width(), self.pixmap.height())
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFixedSize(self.pixmap.width(), self.pixmap.height())
        self.label.setPixmap(self.pixmap)


    def pos(self):
        return QPoint(self.x+8, self.y+8)


    def run(self):
        self.timer = QTimer(self.parent)
        self.timer.timeout.connect(self.animation)
        self.timer.start(1000/self.parent.fps)



    def cut_track_checker(self):
        self.time_checker = QTimer(self.parent)
        self.time_checker.timeout.connect(self.cut_track)
        self.time_checker.start(1000)


    def pickup_power_checker(self):
        self.power_timer = QTimer(self.parent)
        self.power_timer.timeout.connect(self.pickup_power)
        self.power_timer.start(1000/self.parent.fps)


    def pickup_power(self):
        if self.has_power is False:
            for power in self.parent.powers_in_screen:
                distancia = \
                        math.sqrt(  abs(self.centro.x - power.centro.x)**2 + \
                                    abs(self.centro.y - power.centro.y)**2    )
                if distancia <= self.hitbox_poderes:
                    power.taken(self)
                    print(self.velocidad)
                    self.has_power = True


    def cut_track(self):
        if self.isAlive is True:
            if self.drawing:
                if self.seconds_passed == self.cada_tiempo:
                    self.drawing = False
                    self.seconds_passed = 0
                else:
                    self.seconds_passed += self.time_checker.interval()/1000
            else:
                if self.seconds_passed == self.tiempo_corte:
                    self.drawing = True
                    self.seconds_passed = 0
                else:
                    self.seconds_passed += self.time_checker.interval()/1000
        else:
            self.update_Pixmap(True)


    def animation(self):
        if self.isAlive is True:
            if self.parent.is_paused is False:
                self.x += self.radio*self.velocidad*\
                            math.cos(self.angle*self.velocidad)
                self.y += self.radio*\
                            self.velocidad*math.sin(self.angle*self.velocidad)
                self.manipulate_position()
                self.centro = Point(self.x+self.pixmap.width()/2, \
                                    self.y+self.pixmap.height()/2)
                painter = QPainter(self.parent.image)
                painter.setPen(QPen(self.parent.brush_color, \
                                    self.parent.brush_size, \
                                    Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                if self.drawing is True:
                    point_to_save = \
                        Point(self.centro.x-17*math.cos(self.angle), \
                            self.centro.y-17*math.sin(self.angle))
                    painter.drawLine(self.centro.x-17*math.cos(self.angle), \
                                    self.centro.y-17*math.sin(self.angle), \
                                    self.centro.x-16*math.cos(self.angle), \
                                    self.centro.y-16*math.sin(self.angle)   )
                    self.parent.tracks.add(point_to_save)
                self.parent.update()
                if  self.x < 0 or self.parent.display_x < self.x+16 or \
                    self.y < 0 or self.parent.display_y < self.y+16:
                    self.isAlive = False
                for point in self.parent.tracks:
                    distancia = math.sqrt(  abs(self.centro.x - point.x)**2 + \
                                    abs(self.centro.y - point.y)**2    )
                    if distancia <= self.distancia_hitbox:
                        self.isAlive = False
        else:
            self.timer.stop()
            self.points_to_give = 1


    def manipulate_position(self):
        position = { "x" : self.x, "y" : self.y }
        msg_to_send = { "type" : "position_update", \
                        "user" : self.color, \
                        "info" : position}
        self.parent.send_position.emit(msg_to_send)


class AI(Character):


    def __init__(self, parent, color):
        super().__init__(parent)
        self.color = color
        self.update_Pixmap()


    def animation(self):
        if self.isAlive:
            self.centro = Point(self.x+self.pixmap.width()/2, \
                                self.y+self.pixmap.height()/2)
            painter = QPainter(self.parent.image)
            painter.setPen(QPen(self.parent.color_brushes[self.color], \
                                self.parent.brush_size, \
                                Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            if self.drawing:
                # painter.drawLine(   self.centro.x-17*math.cos(self.angle), \
                                    # self.centro.y-17*math.sin(self.angle), \
                                    # self.centro.x-16*math.cos(self.angle), \
                                    # self.centro.y-16*math.sin(self.angle)   )
                painter.drawLine(   self.x-1, self.y-1, \
                                    self.x, self.y)
                # self.parent.tracks.add(point_to_save)
            self.parent.update()
            if  self.x < 0 or self.parent.display_x < self.x+16 or \
                self.y < 0 or self.parent.display_y < self.y+16:
                self.isAlive = False
            for point in self.parent.tracks:
                distancia = math.sqrt(   abs(self.centro.x - point.x)**2 + \
                                abs(self.centro.y - point.y)**2    )
                if distancia <= self.distancia_hitbox:
                    self.isAlive = False
        else:
            self.timer.stop()


class Poder(QWidget):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.label = QLabel(self.parent)
        self.name = ''
        self._x = 0
        self._y = 0
        self.update_Pixmap()
        self.x = 200
        self.y = 200
        self.centro = Point(self.x+self.pixmap.width()/2, \
                            self.y+self.pixmap.height()/2)


    @property
    def x(self):
        return self._x


    @x.setter
    def x(self, value):
        self._x = value
        self.label.move(self.x, self.y)


    @property
    def y(self):
        return self._y


    @y.setter
    def y(self, value):
        self._y = value
        self.label.move(self.x, self.y)


    def update_Pixmap(self, dead=None):
        self.pixmap = QPixmap(f'sprites/usain_nebolt.png')
        self.pixmap = self.pixmap.scaled( \
                        self.pixmap.width()*(16/self.width()),\
                        self.pixmap.height()*(16/self.height()))
        self.label.setMinimumSize(self.pixmap.width(), self.pixmap.height())
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFixedSize(self.pixmap.width(), self.pixmap.height())
        self.label.setPixmap(self.pixmap)


    def taken(self, player):
        player.velocidad = player.velocidad*2
        self.label.deleteLater()
        self.label = None
        pass




if __name__ == '__main__':
    def hook(type, value, traceback):
        print(type)
        print(traceback)
    sys.__excepthook__ = hook
    app = QApplication([])
    window = ScoreBoard('lol')
    sys.exit(app.exec_())
    for angle in range(181):
        print(3*math.cos(math.radians(angle)))
