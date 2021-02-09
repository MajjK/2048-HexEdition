from menuWindow import Ui_StartWindow
from multiWindow import Ui_MultiWindow
from scoresWindow import Ui_ScoresWindow
from mainWindow import Ui_MainWindow
from multiMode import multiMode
from agent import agent
from game import game
import thread
import xml.etree.ElementTree as et
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import numpy as np
import os.path
import socket
import json
import time
import sys
import re
# pyside2-uic Hex2048.ui > mainWindow.py


class mainWindow(QMainWindow, Ui_MainWindow, QWidget):
    def __init__(self, init, nickname, connection, parent=None):
        self.parent = parent
        self.player = nickname
        self.socket = connection
        self.game = None
        self.multi = None
        self.in_game = False
        self.ai = False
        self.in_progress = False
        self.hexpolygons = []
        self.hextexts = []

        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.threadpool = QThreadPool()
        self.setWindowTitle("2048 - HexEdition")
        self.scene = QGraphicsScene(self)
        self.graphics_view.setScene(self.scene)
        self.white_brush = QBrush(Qt.white)
        self.red_brush = QBrush(Qt.red)
        self.blue_brush = QBrush(Qt.blue)
        self.pen = QPen(Qt.black)
        self.pen.setWidth(2)
        self.create_hex_map()
        self.show()

        self.label_player.setText(self.player)
        self.tr_button.clicked.connect(self.tr_function)
        self.r_button.clicked.connect(self.r_function)
        self.br_button.clicked.connect(self.br_function)
        self.bl_button.clicked.connect(self.bl_function)
        self.l_button.clicked.connect(self.l_function)
        self.tl_button.clicked.connect(self.tl_function)
        self.save_game_button.clicked.connect(self.save_game_function)
        self.menu_button.clicked.connect(self.menu_function)
        self.tr_keyboard = QShortcut(QKeySequence(Qt.Key_Up, Qt.Key_Right), self.tr_button, self.tr_function)
        self.r_keyboard = QShortcut(QKeySequence(Qt.Key_Right), self.r_button, self.r_function)
        self.br_keyboard = QShortcut(QKeySequence(Qt.Key_Down, Qt.Key_Right), self.br_button, self.br_function)
        self.bl_keyboard = QShortcut(QKeySequence(Qt.Key_Down, Qt.Key_Left), self.bl_button, self.bl_function)
        self.l_keyboard = QShortcut(QKeySequence(Qt.Key_Left), self.l_button, self.l_function)
        self.tl_keyboard = QShortcut(QKeySequence(Qt.Key_Up, Qt.Key_Left), self.tl_button, self.tl_function)
        if init == 'New':
            self.player_2 = 'Player 2'
            self.new_game_function()
        elif init == 'Load':
            self.load_function()
        elif init == 'Ai':
            self.player_2 = 'AI'
            self.play_ai_function()
        elif init == 'Client':
            self.setWindowTitle("2048 - HexEdition - Client")
            self.multi = multiMode('Client', self)
            self.player = self.multi.nickname_transmission(nickname)
            self.player_2 = nickname
            self.client_function()
        elif init == 'Server':
            self.setWindowTitle("2048 - HexEdition - Server")
            self.multi = multiMode('Server', self)
            self.player_2 = self.multi.nickname_transmission(self.player)
            self.server_function()

    def new_game_function(self):
        self.in_game = True
        self.game = game(0, self.multi, self.player)
        self.update_hex_map()

    def load_function(self):
        if os.path.exists('game_history.xml'):
            self.create_worker(self.replay, self.update_hex_map)
            print("Game Loaded Successfully")
        else:
            print("Cant find game_history.xml")
            print("Create your game history!")
            self.close()
            self.parent.show()

    def play_ai_function(self):
        self.in_game = True
        self.ai = True
        self.game = game(1, self.multi, self.player)
        self.update_hex_map()

    def client_function(self):
        self.in_game = True
        self.game = game(0, self.multi.mode, self.player)
        self.game.agents.append(self.multi.get_agent())
        self.game.agents.append(self.multi.get_agent())
        self.update_hex_map()
        self.create_worker(self.multi.get_move_and_agent, self.update_map_thread_finished)

    def server_function(self):
        self.in_game = True
        self.game = game(0, self.multi.mode, self.player)
        self.multi.send_agent(self.game.agents[0])
        time.sleep(0.5)
        self.multi.send_agent(self.game.agents[1])
        self.update_hex_map()

    def tr_function(self):
        if self.in_game and not self.in_progress:
            self.game.play_turn(1)
            self.update_hex_map()
            if self.ai and not self.game.finished:
                self.start_ai_turn()
            if self.multi is not None:
                self.start_multi_turn(1)
        else:
            pass

    def r_function(self):
        if self.in_game and not self.in_progress:
            self.game.play_turn(2)
            self.update_hex_map()
            if self.ai and not self.game.finished:
                self.start_ai_turn()
            elif self.multi is not None:
                self.start_multi_turn(2)
        else:
            pass

    def br_function(self):
        if self.in_game and not self.in_progress:
            self.game.play_turn(3)
            self.update_hex_map()
            if self.ai and not self.game.finished:
                self.start_ai_turn()
            elif self.multi is not None:
                self.start_multi_turn(3)
        else:
            pass

    def bl_function(self):
        if self.in_game and not self.in_progress:
            self.game.play_turn(4)
            self.update_hex_map()
            if self.ai and not self.game.finished:
                self.start_ai_turn()
            elif self.multi is not None:
                self.start_multi_turn(4)
        else:
            pass

    def l_function(self):
        if self.in_game and not self.in_progress:
            self.game.play_turn(5)
            self.update_hex_map()
            if self.ai and not self.game.finished:
                self.start_ai_turn()
            elif self.multi is not None:
                self.start_multi_turn(5)
        else:
            pass

    def tl_function(self):
        if self.in_game and not self.in_progress:
            self.game.play_turn(6)
            self.update_hex_map()
            if self.ai and not self.game.finished:
                self.start_ai_turn()
            elif self.multi is not None:
                self.start_multi_turn(6)
        else:
            pass

    def save_game_function(self):
        if self.multi.mode == 'Client':
            print("You can't save game in Client Mode!")
            pass
        elif self.in_game and not self.in_progress:
            data = et.tostring(self.game.game_history)
            file = open("game_history.xml", "wb")
            file.write(data)
            print("Game Saved Successfully")
        else:
            pass

    def menu_function(self):
        if not self.in_progress:
            if self.multi is not None:
                self.multi.send_exit()
            self.in_game = False
            self.game = None
            self.close()
            self.parent.show()

    def create_worker(self, thread_function, signal_function):
        worker = thread.thread(thread_function)
        worker.signals.game.connect(signal_function)
        self.threadpool.start(worker)

    def start_ai_turn(self):
        self.in_progress = True
        self.create_worker(self.game.play_turn_ai, self.update_map_thread_finished)

    def start_multi_turn(self, move):
        self.in_progress = True
        self.multi.send_move_and_agent(move, self.game.agents[len(self.game.agents) - 1])
        self.create_worker(self.multi.get_move_and_agent, self.update_map_thread_finished)

    def update_map_thread_finished(self):
        self.update_hex_map()
        self.in_progress = False

    def replay(self, game_callback):
        tree = et.parse('game_history.xml')
        root = tree.getroot()
        self.player = root.attrib['Nickname']
        if root.attrib['AI'] == '1':
            self.ai = True
            self.player_2 = 'AI'
        else:
            self.ai = False
            self.player_2 = 'Player 2'
        self.game = game(root.attrib['AI'], self.multi, self.player)
        self.in_game = True
        self.in_progress = True
        for elem in root:
            self.game.agents.clear()
            self.game.turn = int(elem.attrib['Number'])
            for subelem in elem:
                new_agent = agent()
                new_agent.pos_x = int(subelem.attrib['X'])
                new_agent.pos_y = int(subelem.attrib['Y'])
                new_agent.player = int(subelem.attrib['Player'])
                new_agent.value = int(subelem.text)
                self.game.agents.append(new_agent)
            self.game.update_turn()
            game_callback.emit(self.game)
            time.sleep(1)
        self.in_progress = False
        game_callback.emit(self.game)

    def check_finished(self):
        if self.game.finished:
            if self.game.curr_turn == 1:
                print(self.player, " Won the game!")
            else:
                print(self.player_2, " Won the game!")
            time.sleep(2)
            self.close()
            self.parent.show()

    def create_polygons(self, side_len, height):
        polygons = []
        for j in range(5):
            polygons_line = []
            for i in range(5+j):
                polygon = QPolygonF()
                polygon.append(QPointF(2*i*height - j*height, -1*side_len/2 + 3*side_len/2*j))
                polygon.append(QPointF(height + 2*i*height - j*height, -1*side_len + 3*side_len/2*j))
                polygon.append(QPointF(2*height + 2*i*height - j*height, -1*side_len/2 + 3*side_len/2*j))
                polygon.append(QPointF(2*height + 2*i*height - j*height, side_len/2 + 3*side_len/2*j))
                polygon.append(QPointF(height + 2*i*height - j*height, side_len + 3*side_len/2*j))
                polygon.append(QPointF(2*i*height - j*height, side_len/2 + 3*side_len/2*j))
                polygons_line.append(self.scene.addPolygon(polygon, self.pen))
            polygons.append(polygons_line)
        for j in range(4):
            polygons_line = []
            for i in range(8-j):
                polygon = QPolygonF()
                polygon.append(QPointF(-3*height + 2*i*height + j*height, 14*side_len/2 + 3*side_len/2*j))
                polygon.append(QPointF(-2*height + 2*i*height + j*height, 13*side_len/2 + 3*side_len/2*j))
                polygon.append(QPointF(-1*height + 2*i*height + j*height, 14*side_len/2 + 3*side_len/2*j))
                polygon.append(QPointF(-1*height + 2*i*height + j*height, 16*side_len/2 + 3*side_len/2*j))
                polygon.append(QPointF(-2*height + 2*i*height + j*height, 17*side_len/2 + 3*side_len/2*j))
                polygon.append(QPointF(-3*height + 2*i*height + j*height, 16*side_len/2 + 3*side_len/2*j))
                polygons_line.append(self.scene.addPolygon(polygon, self.pen))
            polygons.append(polygons_line)
        return polygons

    def create_text_edits(self, side_len, height):
        text_edits = []
        font = QFont("Arial", 12)
        font.setBold(True)
        for j in range(5):
            hextext_line = []
            for i in range(5 + j):
                text = self.scene.addSimpleText("", font)
                text.setPos(-5 + height/2 + 2*height*i - height*j, -10 + 3*side_len/2*j)
                text.setScale(1.1)
                hextext_line.append(text)
            text_edits.append(hextext_line)
        for j in range(4):
            hextext_line = []
            for i in range(8 - j):
                text = self.scene.addSimpleText("", font)
                text.setPos(-5 + -5*height/2 + 2*height*i + height*j, 230 + 3*side_len/2*j)
                text.setScale(1.1)
                hextext_line.append(text)
            text_edits.append(hextext_line)
        return text_edits

    def create_hex_map(self):
        side_len = 32
        height = side_len * np.sqrt(3)/2
        self.hexpolygons = self.create_polygons(side_len, height)
        self.hextexts = self.create_text_edits(side_len, height)

    def update_hex_map(self):
        if self.game.curr_turn % 2 == 0:
            self.label_player.setText(self.player)
            self.label_color.setText('Red')
        else:
            self.label_player.setText(self.player_2)
            self.label_color.setText('Blue')
        for lines in self.hexpolygons:
            for element in lines:
                element.setBrush(self.white_brush)
        for lines in self.hextexts:
            for element in lines:
                element.setText("")
        for elem in self.game.agents:
            str_val = str(elem.value)
            if len(str_val) == 1:
                str_val = "   " + str_val
            elif len(str_val) == 2:
                str_val = "  " + str_val
            elif len(str_val) == 3:
                str_val = " " + str_val
            self.hextexts[elem.pos_y][elem.pos_x].setText(str_val)
            if elem.player == 0:
                self.hexpolygons[elem.pos_y][elem.pos_x].setBrush(self.red_brush)
            else:
                self.hexpolygons[elem.pos_y][elem.pos_x].setBrush(self.blue_brush)
        self.check_finished()


class scoresWindow(QMainWindow, Ui_ScoresWindow, QWidget):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.setWindowTitle("2048 - HexEdition - Multiplayer")
        self.show()
        if os.path.exists('scoreboards.xml'):
            scoreboards_tree = et.parse('scoreboards.xml')
            root = scoreboards_tree.getroot()
            nicknames_text = ''
            scores_text = ''
            for elem in root:
                nicknames_text += elem.attrib['Nickname'] + '\n'
                scores_text += elem.attrib['Score'] + '\n'
            self.nick_text_edit.setPlainText(nicknames_text)
            self.score_text_edit.setPlainText(scores_text)
        else:
            self.nick_text_edit.setPlainText('Your Scoreboard')
            self.score_text_edit.setPlainText('does not exist!')


class startWindow(QMainWindow, Ui_StartWindow, QWidget):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.setWindowTitle("2048 - HexEdition - Menu")
        self.show()

        self.new_button.clicked.connect(self.new_game)
        self.ai_button.clicked.connect(self.play_ai)
        self.multi_button.clicked.connect(self.multi)
        self.load_button.clicked.connect(self.load)
        self.scores_button.clicked.connect(self.scores)
        self.quit_button.clicked.connect(app.quit)

    def new_game(self):
        main_window = mainWindow('New', self.get_nickname(), None,  self)
        main_window.show()
        self.hide()

    def play_ai(self):
        main_window = mainWindow('Ai', self.get_nickname(), None, self)
        main_window.show()
        self.hide()

    def multi(self):
        multi_window = multiWindow(self.get_nickname(), self)
        multi_window.show()
        self.hide()

    def load(self):
        main_window = mainWindow('Load', '', None, self)
        main_window.show()
        self.hide()

    def scores(self):
        scores_window = scoresWindow(self)
        scores_window.show()

    def get_nickname(self):
        if str(self.nick_edit.toPlainText()) != '':
            return str(self.nick_edit.toPlainText())
        else:
            return 'User'


class multiWindow(QMainWindow, Ui_MultiWindow, QWidget):
    def __init__(self, nickname, parent=None):
        self.parent = parent
        self.nickname = nickname
        self.buffer = 100
        self.port = 0
        self.address = ''
        self.conn = None
        self.socket = None

        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.setWindowTitle("2048 - HexEdition - Multiplayer")
        self.show()
        self.load_data()

        self.connect_button.clicked.connect(self.client)
        self.server_button.clicked.connect(self.server)
        self.menu_button.clicked.connect(self.menu)

    def client(self):
        if self.save_data():
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.address, int(self.port)))
            data = self.socket.recv(self.buffer)
            data = data.decode()
            print(data)
            main_window = mainWindow('Client', self.nickname, self.socket, self)
            main_window.show()
            self.hide()

    def server(self):
        if self.save_data():
            print('Server started. Waiting for clients...')
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    s.bind((self.address, int(self.port)))
                except socket.error:
                    return
                s.listen(2)
                self.conn, addr1 = s.accept()
                print('Connected by', addr1)
                self.conn.sendall("Connected".encode())
                main_window = mainWindow('Server', self.nickname, self.conn, self)
                main_window.show()
                self.hide()

    def menu(self):
        self.close()
        self.parent.show()

    def save_data(self):
        self.port = self.port_edit.toPlainText()
        self.address = self.address_edit.toPlainText()
        if re.search('[a-zA-Z]', self.address) is None and re.search('[a-zA-Z]', self.port) is None \
                and self.address != '' and self.port != '':
            data = {'config': []}
            data['config'].append({'Address': self.address, 'Port': int(self.port)})
            with open('config.json', 'w') as outfile:
                json.dump(data, outfile)
            return True
        else:
            print('Wrong Address or Port')
            return False

    def load_data(self):
        if os.path.exists('config.json'):
            with open('config.json') as json_file:
                data = json.load(json_file)
                for p in data['config']:
                    self.port = int(p['Port'])
                    self.address = p['Address']
                    self.port_edit.setText(str(p['Port']))
                    self.address_edit.setText(str(p['Address']))


if __name__ == '__main__':
    app = QApplication()
    start_window = startWindow()
    start_window.show()
    sys.exit(app.exec_())
