from Hex2048_Menu import Ui_StartWindow
from Hex2048_Multi import Ui_MultiWindow
from Hex2048 import Ui_MainWindow
import xml.etree.ElementTree as et
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from copy import deepcopy
import numpy as np
import traceback
import os.path
import random
import json
import time
import sys
import re
# pyside2-uic Hex2048.ui > Hex2048.py
# Koniec Gry w przypadku braku ruchów
# Przerwa pomiedzy ruchem a wygenerowaniem nowego agenta
# Dodać Multi
# Rozbić na pliki klas
# **Dodać Animacje Ruchu


class threadSignals(QObject):
    finished = Signal()
    error = Signal(tuple)
    result = Signal(object)
    game = Signal(object)


class thread(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(thread, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = threadSignals()
        self.kwargs['game_callback'] = self.signals.game

    @Slot()
    def run(self):
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()


class map:
    def __init__(self):
        self.map_area = []
        for i in range(9):
            line = []
            if i < 5:
                for j in range(5 + i):
                    line.append(field())
            else:
                for j in range(5 + 8 - i):
                    line.append(field())
            self.map_area.append(line)

    def update_map(self, agents):
        # Main function to clear and re-update agents positions and values on the map
        # It also checks if any agent has 2048 value, if so, game is finished
        max_value = 0
        finished = False

        for lines in self.map_area:
            for element in lines:
                element.color = ""
                element.value = ""
        for elem in agents:
            self.map_area[elem.pos_y][elem.pos_x].update_field(elem)
            if elem.value > max_value:
                max_value = elem.value
        if max_value >= 2048:
            finished = True
        return finished


class game:
    # Main Class connected with current game instance
    def __init__(self, ai, player):
        self.agents = []
        self.map = map()
        self.finished = False
        self.turn = 0
        self.curr_turn = 0
        self.ai_mode = str(ai)
        self.player = str(player)
        self.record = 2
        self.root = None
        self.game_history = et.Element('Game')
        self.game_history.set('AI', self.ai_mode)
        self.game_history.set('Nickname', self.player)
        self.init_scoreboards()

        new_agent_1 = agent()
        new_agent_1.create_agent(0, self.map.map_area)
        self.agents.append(new_agent_1)
        self.finished = self.map.update_map(self.agents)
        new_agent_2 = agent()
        new_agent_2.create_agent(1, self.map.map_area)
        self.agents.append(new_agent_2)
        self.update_turn()

    def init_scoreboards(self):
        if os.path.exists('scoreboards.xml'):
            scoreboards_tree = et.parse('scoreboards.xml')
            self.root = scoreboards_tree.getroot()
            users = {}
            for elem in self.root:
                users[elem.attrib['Nickname']] = int(elem.attrib['Score'])
            if self.player in users:
                self.record = users[self.player]
            else:
                user = et.SubElement(self.root, "User")
                user.set('Nickname', self.player)
                user.set('Score', str(self.record))
                data = et.tostring(self.root)
                file = open("scoreboards.xml", "wb")
                file.write(data)
        else:
            self.root = et.Element('Scores')
            user = et.SubElement(self.root, 'User')
            user.set('Nickname', self.player)
            user.set('Score', str(self.record))
            data = et.tostring(self.root)
            file = open("scoreboards.xml", "wb")
            file.write(data)

    def update_scoreboards(self):
        for elem_agents in self.agents:
            if elem_agents.value > self.record and elem_agents.player == 0:
                self.record = elem_agents.value
                for elem_root in self.root:
                    if elem_root.attrib['Nickname'] == self.player:
                        elem_root.attrib['Score'] = str(self.record)
                data = et.tostring(self.root)
                file = open("scoreboards.xml", "wb")
                file.write(data)

    def update_history(self):
        turn = et.SubElement(self.game_history, 'Turn')
        turn.set('Number', str(self.turn))
        for elem in self.agents:
            NewAgent = et.SubElement(turn, 'Agent')
            NewAgent.set('Player', str(elem.player))
            NewAgent.set('X', str(elem.pos_x))
            NewAgent.set('Y', str(elem.pos_y))
            NewAgent.text = str(elem.value)

    def sort_agents(self, move):
        if move == 1:
            self.agents.sort(key=lambda x: x.pos_y)
        elif move == 2:
            self.agents.sort(key=lambda x: x.pos_x, reverse=True)
        elif move == 3:
            self.agents.sort(key=lambda x: x.pos_y, reverse=True)
        elif move == 4:
            self.agents.sort(key=lambda x: x.pos_y, reverse=True)
        elif move == 5:
            self.agents.sort(key=lambda x: x.pos_x)
        elif move == 6:
            self.agents.sort(key=lambda x: x.pos_y)

    def play_turn(self, move, create_agent=True):
        self.sort_agents(move)
        for current_agent in self.agents:
            if current_agent.player == self.curr_turn:
                current_agent.move_agent(self.map.map_area, move, self.agents)
        for current_agent in self.agents:
            if current_agent.player == self.curr_turn:
                current_agent.move_agent(self.map.map_area, move, self.agents)

        self.finished = self.map.update_map(self.agents)
        self.turn += 1
        if create_agent:
            new_agent = agent()
            new_agent.create_agent(self.turn % 2, self.map.map_area)
            self.agents.append(new_agent)
        self.update_turn()

    def update_turn(self):
        self.finished = self.map.update_map(self.agents)
        self.curr_turn = self.turn % 2
        self.update_history()
        self.update_scoreboards()


class field:
    def __init__(self):
        self.color = ""
        self.value = ""

    def update_field(self, agent):
        self.color = str(agent.player)
        self.value = agent.value


class agent:
    def __init__(self):
        self.player = -1
        self.value = 0
        self.pos_x = -1
        self.pos_y = -1

    def create_agent(self, player, map):
        self.player = player
        self.value = 2
        clear_field = False
        while not clear_field:
            y = random.randrange(9)
            if y == 0 or y == 8:
                x = random.randrange(5)
            elif y == 1 or y == 7:
                x = random.randrange(6)
            elif y == 2 or y == 6:
                x = random.randrange(7)
            elif y == 3 or y == 5:
                x = random.randrange(8)
            else:
                x = random.randrange(9)
            if map[y][x].value == "":
                clear_field = True
                self.pos_y = y
                self.pos_x = x

    def move_agent(self, map, direction, agents):
        while True:
            if direction == 1:
                if 0 < self.pos_y < 5:
                    if self.pos_x < len(map[self.pos_y]) - 1:
                        if not self.look_for_collision(self.pos_y - 1, self.pos_x, agents):
                            self.pos_y -= 1
                        else:
                            break
                    else:
                        break
                elif 4 < self.pos_y < 9:
                    if not self.look_for_collision(self.pos_y - 1, self.pos_x + 1, agents):
                        self.pos_y -= 1
                        self.pos_x += 1
                    else:
                        break
                else:
                    break

            elif direction == 2:
                if self.pos_x < len(map[self.pos_y]) - 1:
                    if not self.look_for_collision(self.pos_y, self.pos_x + 1, agents):
                        self.pos_x += 1
                    else:
                        break
                else:
                    break

            elif direction == 3:
                if self.pos_y < 4:
                    if not self.look_for_collision(self.pos_y + 1, self.pos_x + 1, agents):
                        self.pos_y += 1
                        self.pos_x += 1
                    else:
                        break
                elif self.pos_y < 8:
                    if self.pos_x < len(map[self.pos_y]) - 1:
                        if not self.look_for_collision(self.pos_y + 1, self.pos_x, agents):
                            self.pos_y += 1
                        else:
                            break
                    else:
                        break
                else:
                    break

            elif direction == 4:
                if self.pos_y < 4:
                    if not self.look_for_collision(self.pos_y + 1, self.pos_x, agents):
                        self.pos_y += 1
                    else:
                        break
                elif self.pos_y < 8:
                    if self.pos_x > 0:
                        if not self.look_for_collision(self.pos_y + 1, self.pos_x - 1, agents):
                            self.pos_y += 1
                            self.pos_x -= 1
                        else:
                            break
                    else:
                        break
                else:
                    break

            elif direction == 5:
                if self.pos_x > 0:
                    if not self.look_for_collision(self.pos_y, self.pos_x - 1, agents):
                        self.pos_x -= 1
                    else:
                        break
                else:
                    break

            elif direction == 6:
                if 0 < self.pos_y < 5:
                    if self.pos_x > 0:
                        if not self.look_for_collision(self.pos_y - 1, self.pos_x - 1, agents):
                            self.pos_y -= 1
                            self.pos_x -= 1
                        else:
                            break
                    else:
                        break
                elif 4 < self.pos_y < 9:
                    if not self.look_for_collision(self.pos_y - 1, self.pos_x, agents):
                        self.pos_y -= 1
                    else:
                        break
                else:
                    break

    def look_for_collision(self, pos_y, pos_x, agents):
        for elem in agents:
            if elem.pos_y == pos_y and elem.pos_x == pos_x:
                if elem.player == self.player and elem.value == self.value:
                    elem.value += self.value
                    agents.pop(agents.index(self))
                return True
        return False


class gameNode:
    # Class connected with AI game mode
    def __init__(self, game, level):
        self.game = game
        self.level = level
        self.children = []

    def generate_next_level(self):
        # Main function to generate game node for AI action evaluation
        if len(self.children) == 0:
            if self.level == 0 or self.level == 2:
                self.generate_next_level_for_player_move()
            else:
                self.generate_next_level_for_agents()
        else:
            for child in self.children:
                child.generate_next_level()

    def generate_next_level_for_player_move(self):
        # It generates node if its a player turn, 6 possible moves
        for move in range(1, 7):
            newGame = deepcopy(self.game)
            newGame.play_turn(move, False)
            node = gameNode(newGame, (self.level + 1) % 4)
            self.children.append(node)

    def generate_next_level_for_agents(self):
        # It generates node if its AI turn, its more complicated because this function
        # try to guess next new agent position
        for y in range(0, len(self.game.map.map_area)):
            for x in range(0, len(self.game.map.map_area[y])):
                if self.game.map.map_area[y][x].value == '':
                    new_game = deepcopy(self.game)
                    new_agent = agent()
                    new_agent.player = new_game.curr_turn
                    new_agent.pos_x = x
                    new_agent.pos_y = y
                    new_game.agents.append(new_agent)
                    new_game.finished = new_game.map.update_map(new_game.agents)
                    node = gameNode(new_game, (self.level + 1) % 4)
                    self.children.append(node)

    def evaluate(self):
        # The most important function in AI mode, it evaluates profitability of specific move and its consequences
        if len(self.children) == 0:
            result = 0
            if self.game.finished:
                return 1000
            for elem in self.game.agents:
                if elem.player == 1:
                    result = result - 1
                else:
                    result = result + 1
            return result

        elif self.level == 0:
            max_val = -1000000
            for child in self.children:
                child_evaluation = child.evaluate()
                if child_evaluation > max_val:
                    max_val = child_evaluation
            return max_val

        elif self.level == 1 or self.level == 3:
            sum_val = 0
            for child in self.children:
                child_evaluation = child.evaluate()
                sum_val = sum_val + child_evaluation
            return sum_val / len(self.children)

        else:
            min_val = 1000000
            for child in self.children:
                child_evaluation = child.evaluate()
                if child_evaluation < min_val:
                    min_val = child_evaluation
            return min_val


class mainWindow(QMainWindow, Ui_MainWindow, QWidget):
    def __init__(self, init, nickname, parent=None):
        self.parent = parent
        self.game = None
        self.in_game = False
        self.ai = False
        self.in_progress = False
        self.ai_depth_search = 3
        self.player = nickname
        self.hexpolygons = []
        self.hextexts = []

        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.setWindowTitle("2048 - HexEdition")
        self.label_player.setText(self.player)
        self.scene = QGraphicsScene()
        self.white_brush = QBrush(Qt.white)
        self.red_brush = QBrush(Qt.red)
        self.blue_brush = QBrush(Qt.blue)
        self.pen = QPen(Qt.black)
        self.pen.setWidth(2)
        self.graphics_view.setScene(self.scene)

        self.create_hex_map()
        self.show()
        self.threadpool = QThreadPool()
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
            self.new_game()
            self.player_2 = 'Player 2'
        elif init == 'Load':
            self.load_function()
        elif init == 'Ai':
            self.play_ai()
            self.player_2 = 'AI'

    def new_game(self):
        if not self.in_progress:
            self.game = game(0, self.player)
            self.in_game = True
            self.ai = False
            self.update_hex_map(self.game.agents, self.game.curr_turn, self.game.finished)

    def load_function(self):
        if os.path.exists('game_history.xml'):
            worker = thread(self.replay)
            worker.signals.game.connect(self.update_map_thread)
            self.threadpool.start(worker)
            print("Game Loaded Successfully")
        else:
            print("Cant find game_history.xml")
            print("Create your game history!")

    def play_ai(self):
        if not self.in_progress:
            self.ai = True
            self.game = game(1, self.player)
            self.in_game = True
            self.update_hex_map(self.game.agents, self.game.curr_turn, self.game.finished)

    def create_hex_map(self):
        side_len = 32
        height = side_len * np.sqrt(3)/2
        for j in range(5):
            polygons_line = []
            for i in range(5+j):
                polygon = QPolygonF()
                polygon.append(QPointF(0 + 2*i*height - j*height, -1*side_len/2 + 3*side_len/2*j))
                polygon.append(QPointF(height + 2*i*height - j*height, -1*side_len + 3*side_len/2*j))
                polygon.append(QPointF(2*height + 2*i*height - j*height, -1*side_len/2 + 3*side_len/2*j))
                polygon.append(QPointF(2*height + 2*i*height - j*height, side_len/2 + 3*side_len/2*j))
                polygon.append(QPointF(height + 2*i*height - j*height, side_len + 3*side_len/2*j))
                polygon.append(QPointF(0 + 2*i*height - j*height, side_len/2 + 3*side_len/2*j))
                polygons_line.append(self.scene.addPolygon(polygon, self.pen))
            self.hexpolygons.append(polygons_line)
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
            self.hexpolygons.append(polygons_line)
        for j in range(5):
            hextext_line = []
            for i in range(5 + j):
                text = self.scene.addSimpleText("")
                text.setPos(height/2 + 2*height*i - height*j, -10 + 3*side_len/2*j)
                text.setScale(1.1)
                hextext_line.append(text)
            self.hextexts.append(hextext_line)
        for j in range(4):
            hextext_line = []
            for i in range(8 - j):
                text = self.scene.addSimpleText("")
                text.setPos(-5*height/2 + 2*height*i + height*j, 231 + 3*side_len/2*j)
                text.setScale(1.1)
                hextext_line.append(text)
            self.hextexts.append(hextext_line)

    def update_hex_map(self, agents, curr_turn, finished):
        if curr_turn % 2 == 0:
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
        for elem in agents:
            str_val = str(elem.value)
            if len(str_val) == 1:
                str_val = "   " + str_val
            elif len(str_val) == 2:
                str_val = "  " + str_val
            elif len(str_val) == 3:
                str_val = " " + str_val
            if elem.player == 0:
                self.hexpolygons[elem.pos_y][elem.pos_x].setBrush(self.red_brush)
            else:
                self.hexpolygons[elem.pos_y][elem.pos_x].setBrush(self.blue_brush)
            self.hextexts[elem.pos_y][elem.pos_x].setText(str_val)
        if finished:
            if curr_turn == 1:
                print(self.player, " Won the game!")
            else:
                print(self.player_2, " Won the game!")
            time.sleep(2)
            self.close()
            self.parent.show()

    def tr_function(self):
        if self.in_game and not self.in_progress:
            self.game.play_turn(1)
            self.update_hex_map(self.game.agents, self.game.curr_turn, self.game.finished)
            if self.ai:
                worker = thread(self.play_turn_ai)
                worker.signals.game.connect(self.update_map_thread)
                self.threadpool.start(worker)
        else:
            pass

    def r_function(self):
        if self.in_game and not self.in_progress:
            self.game.play_turn(2)
            self.update_hex_map(self.game.agents, self.game.curr_turn, self.game.finished)
            if self.ai:
                worker = thread(self.play_turn_ai)
                worker.signals.game.connect(self.update_map_thread)
                self.threadpool.start(worker)
        else:
            pass

    def br_function(self):
        if self.in_game and not self.in_progress:
            self.game.play_turn(3)
            self.update_hex_map(self.game.agents, self.game.curr_turn, self.game.finished)
            if self.ai:
                worker = thread(self.play_turn_ai)
                worker.signals.game.connect(self.update_map_thread)
                self.threadpool.start(worker)
        else:
            pass

    def bl_function(self):
        if self.in_game and not self.in_progress:
            self.game.play_turn(4)
            self.update_hex_map(self.game.agents, self.game.curr_turn, self.game.finished)
            if self.ai:
                worker = thread(self.play_turn_ai)
                worker.signals.game.connect(self.update_map_thread)
                self.threadpool.start(worker)
        else:
            pass

    def l_function(self):
        if self.in_game and not self.in_progress:
            self.game.play_turn(5)
            self.update_hex_map(self.game.agents, self.game.curr_turn, self.game.finished)
            if self.ai:
                worker = thread(self.play_turn_ai)
                worker.signals.game.connect(self.update_map_thread)
                self.threadpool.start(worker)
        else:
            pass

    def tl_function(self):
        if self.in_game and not self.in_progress:
            self.game.play_turn(6)
            self.update_hex_map(self.game.agents, self.game.curr_turn, self.game.finished)
            if self.ai:
                worker = thread(self.play_turn_ai)
                worker.signals.game.connect(self.update_map_thread)
                self.threadpool.start(worker)
        else:
            pass

    def save_game_function(self):
        if self.in_game and not self.in_progress:
            data = et.tostring(self.game.game_history)
            file = open("game_history.xml", "wb")
            file.write(data)
            print("Game Saved Successfully")
        else:
            pass

    def menu_function(self):
        self.close()
        self.parent.show()

    def play_turn_ai(self, game_callback):
        if self.in_game and self.ai and not self.game.finished:
            self.in_progress = True
            max_val = -100000
            move_evaluations = []
            best_evaluations = []

            game_callback.emit(self.game)
            time.sleep(1)
            game_node = gameNode(self.game, 0)
            for i in range(0, self.ai_depth_search):
                game_node.generate_next_level()
            for i in range(0, 6):
                if self.game.curr_turn == 0:
                    move_evaluations.append(-1 * game_node.children[i].evaluate())
                else:
                    move_evaluations.append(game_node.children[i].evaluate())
                if move_evaluations[i] > max_val:
                    max_val = move_evaluations[i]
            for i in range(0, 6):
                if move_evaluations[i] == max_val:
                    best_evaluations.append(i+1)
            bestMove = random.choice(best_evaluations)
            print('best move: ', bestMove, ' (', max_val, ')')
            self.game.play_turn(bestMove)
            self.in_progress = False
            game_callback.emit(self.game)
        else:
            pass

    def update_map_thread(self, game):
        loaded_game = game
        self.update_hex_map(loaded_game.agents, loaded_game.curr_turn, loaded_game.finished)

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
        self.game = game(root.attrib['AI'], self.player)
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
        self.quit_button.clicked.connect(self.quit)

    def new_game(self):
        main_window = mainWindow('New', self.get_nickname(), self)
        main_window.show()
        self.hide()

    def play_ai(self):
        main_window = mainWindow('Ai', self.get_nickname(), self)
        main_window.show()
        self.hide()

    def multi(self):
        multi_window = multiWindow(self.get_nickname(), self)
        multi_window.show()
        self.hide()

    def load(self):
        main_window = mainWindow('Load', '', self)
        main_window.show()
        self.hide()

    def scores(self):
        if os.path.exists('scoreboards.xml'):
            scoreboards_tree = et.parse('scoreboards.xml')
            root = scoreboards_tree.getroot()
            for elem in root:
                print(elem.attrib['Nickname'], " - ", elem.attrib['Score'])
        else:
            print("Your Scoreboard does not exist!")

    def quit(self):
        app.quit()

    def get_nickname(self):
        if str(self.nick_edit.toPlainText()) != '':
            return str(self.nick_edit.toPlainText())
        else:
            return 'User'


class multiWindow(QMainWindow, Ui_MultiWindow, QWidget):
    def __init__(self, nickname, parent=None):
        self.parent = parent
        self.port = ''
        self.address = ''

        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.setWindowTitle("2048 - HexEdition - Multiplayer")
        self.show()

        self.connect_button.clicked.connect(self.connect)
        self.server_button.clicked.connect(self.server)
        self.menu_button.clicked.connect(self.menu)
        self.save_config_button.clicked.connect(self.save_config)
        self.load_config_button.clicked.connect(self.load_config)

    def connect(self):
        main_window = mainWindow('New', self.get_nickname(), self)
        main_window.show()
        self.hide()

    def server(self):
        main_window = mainWindow('Ai', self.get_nickname(), self)
        main_window.show()
        self.hide()

    def menu(self):
        self.close()
        self.parent.show()

    def save_config(self):
        self.port = self.port_edit.toPlainText()
        self.address = self.address_edit.toPlainText()
        if re.search('[a-zA-Z]', self.address) is None and re.search('[a-zA-Z]', self.port) is None:
            data = {'config': []}
            data['config'].append({'Address': self.address, 'Port': int(self.port)})
            with open('config.json', 'w') as outfile:
                json.dump(data, outfile)
        else:
            print('Wrong Address or Port')

    def load_config(self):
        main_window = mainWindow('Ai', self.get_nickname(), self)
        main_window.show()
        self.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    start_window = startWindow()
    start_window.show()
    sys.exit(app.exec_())
