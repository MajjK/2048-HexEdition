import xml.etree.ElementTree as ET
from Hex2048 import Ui_MainWindow
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from copy import deepcopy
import numpy as np
import traceback
import os.path
import random
import time
import sys
# pyside2-uic Hex2048.ui > Hex2048.py
AI_DEPTH_SEARCH = 3
# Zwycięzca gry - przerwanie
# Poczatek gry - okno
# Przerwa pomiedzy ruchem a wygenerowaniem nowego agenta
# Zmiana Nazw
# Zmiana Grafiki
# Rozbić na pliki klas
# Dodać Multi
# Dodać Animacje Ruchu


class ThreadSignals(QObject):
    finished = Signal()
    error = Signal(tuple)
    result = Signal(object)
    game = Signal(object)


class Thread(QRunnable):
    # Class needed to implement multi-threading
    def __init__(self, fn, *args, **kwargs):
        super(Thread, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = ThreadSignals()
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


class Map:
    def __init__(self):
        self.map = []
        for i in range(9):
            line = []
            if i < 5:
                for j in range(5 + i):
                    line.append(field())
            else:
                for j in range(5 + 8 - i):
                    line.append(field())
            self.map.append(line)

    def update_map(self, agents):
        # Main function to clear and re-update agents positions and values on the map
        # It also checks if any agent has 2048 value, if so, game is finished
        max = 0
        finished = False

        for lines in self.map:
            for element in lines:
                element.color = ""
                element.value = ""
        for agent in agents:
            self.map[agent.pos_y][agent.pos_x].update_field(agent)
            if agent.value > max:
                max = agent.value
        if max >= 32:
            finished = True
        return finished


class Game:
    # Main Class connected with current game instance
    def __init__(self, Connection, AI):
        self.agents = []
        self.map = Map()
        self.finished = False
        self.turn = 0
        self.GameHistory = ET.Element('Game')
        self.GameHistory.set('AI', str(AI))

        new_agent1 = agent()
        new_agent1.create_agent(0, self.map.map)
        self.agents.append(new_agent1)
        self.finished = self.map.update_map(self.agents)

        new_agent2 = agent()
        new_agent2.create_agent(1, self.map.map)
        self.agents.append(new_agent2)

        self.update_turn()

    def update_history(self):
        turn = ET.SubElement(self.GameHistory, 'Turn')
        turn.set('number', str(self.turn))
        for agent in self.agents:
            NewAgent = ET.SubElement(turn, 'Agent')
            NewAgent.set('player', str(agent.player))
            NewAgent.set('X', str(agent.pos_x))
            NewAgent.set('Y', str(agent.pos_y))
            NewAgent.text = str(agent.value)

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

    def play_turn(self, move, createAgent=True):
        self.sort_agents(move)
        for current_agent in self.agents:
            if current_agent.player == self.curr_turn:
                current_agent.move_agent(self.map.map, move, self.agents)
        for current_agent in self.agents:
            if current_agent.player == self.curr_turn:
                current_agent.move_agent(self.map.map, move, self.agents)

        self.finished = self.map.update_map(self.agents)
        self.turn += 1
        if createAgent:
            new_agent = agent()
            new_agent.create_agent(self.turn % 2, self.map.map)
            self.agents.append(new_agent)
        self.update_turn()

    def update_turn(self):
        self.finished = self.map.update_map(self.agents)
        self.curr_turn = self.turn % 2
        self.update_history()


class field:
    def __init__(self):
        self.color = ""
        self.value = ""

    def return_value(self):
        str_val = str(self.value)
        for i in range(4 - len(str_val)):
            if i < 2:
                str_val = " " + str_val
            else:
                str_val = str_val + " "

        if self.color == '0':
            str_val = '\x1b[0;30;41m' + str_val + '\x1b[0m'
        elif self.color == '1':
            str_val = '\x1b[0;30;44m' + str_val + '\x1b[0m'
        return str_val

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
        for agent in agents:
            if agent.pos_y == pos_y and agent.pos_x == pos_x:
                if agent.player == self.player and agent.value == self.value:
                    agent.value += self.value
                    agents.pop(agents.index(self))
                return True
        return False


class GameNode:
    # Class connected with AI game mode
    def __init__(self, game, level):
        self.game = game
        self.level = level
        self.children = []

    def generateNextLevel(self):
        # Main function to generate game node for AI action evaluation
        if len(self.children) == 0:
            if self.level == 0 or self.level == 2:
                self.generateNextLevelForPlayerMove()
            else:
                self.generateNextLevelForAgents()
        else:
            for child in self.children:
                child.generateNextLevel()

    def generateNextLevelForPlayerMove(self):
        # It generates node if its a player turn, 6 possible moves
        for move in range(1, 7):
            newGame = deepcopy(self.game)
            newGame.play_turn(move, False)
            gameNode = GameNode(newGame, (self.level + 1) % 4)
            self.children.append(gameNode)

    def generateNextLevelForAgents(self):
        # It generates node if its AI turn, its more complicated because this function
        # try to guess next new agent position
        for y in range(0, len(self.game.map.map)):
            for x in range(0, len(self.game.map.map[y])):
                if self.game.map.map[y][x].value == '':
                    newGame = deepcopy(self.game)
                    newAgent = agent()
                    newAgent.player = newGame.curr_turn
                    newAgent.pos_x = x
                    newAgent.pos_y = y
                    newGame.agents.append(newAgent)
                    newGame.finished = newGame.map.update_map(newGame.agents)
                    gameNode = GameNode(newGame, (self.level + 1) % 4)
                    self.children.append(gameNode)

    def evaluate(self):
        # The most important function in AI mode, it evaluates profitability of specific move and its consequences
        if len(self.children) == 0:
            result = 0
            if self.game.finished:
                return 1000

            for agent in self.game.agents:
                if agent.player == 1:
                    result = result - 1
                else:
                    result = result + 1
            return result
        elif self.level == 0:
            max = -1000000
            for child in self.children:
                childEveluation = child.evaluate()
                if childEveluation > max:
                    max = childEveluation
            return max
        elif self.level == 1 or self.level == 3:
            sum = 0
            for child in self.children:
                childEveluation = child.evaluate()
                sum = sum + childEveluation
            return sum / len(self.children)
        else:
            min = 1000000
            for child in self.children:
                childEveluation = child.evaluate()
                if childEveluation < min:
                    min = childEveluation
            return min


class MainWindow(QMainWindow, Ui_MainWindow, QWidget):
    # Class connected with main QT window, it contains button functions and calls all program actions
    def __init__(self):
        QMainWindow.__init__(self)
        self.game = None
        self.in_game = False
        self.ai = False
        self.in_progress = False
        self.Connection = False
        self.current_player = 0
        self.hexpolygons = []
        self.hextexts = []

        self.setupUi(self)
        self.setWindowTitle("2048 - HexEdition")
        self.createGraphicScene()
        self.show()
        self.threadpool = QThreadPool()

        self.NewButton.clicked.connect(self.NewGame)
        self.QuitButton.clicked.connect(self.Quit)
        self.TRButton.clicked.connect(self.TRFunction)
        self.RButton.clicked.connect(self.RBFunction)
        self.BRButton.clicked.connect(self.BRFunction)
        self.BLButton.clicked.connect(self.BLFunction)
        self.LButton.clicked.connect(self.LBFunction)
        self.TLButton.clicked.connect(self.TLFunction)
        self.SaveGameButton.clicked.connect(self.SaveGameFunction)
        self.LoadButton.clicked.connect(self.LoadFunction)
        self.AIButton.clicked.connect(self.PlayAI)

    def createGraphicScene(self):
        self.scene = QGraphicsScene()
        self.WhiteBrush = QBrush(Qt.white)
        self.RedBrush = QBrush(Qt.red)
        self.BlueBrush = QBrush(Qt.blue)
        self.pen = QPen(Qt.black)
        self.pen.setWidth(2)
        self.graphicsView.setScene(self.scene)
        self.CreateHexMap()

    def CreateHexMap(self):
        a = 32
        h = a * np.sqrt(3)/2
        for j in range(5):
            polygons_line = []
            for i in range(5+j):
                polygon = QPolygonF()
                polygon.append(QPointF(0 + 2*i*h - j*h, -1*a/2 + 3*a/2*j))
                polygon.append(QPointF(h + 2*i*h - j*h, -1*a + 3*a/2*j))
                polygon.append(QPointF(2*h + 2*i*h - j*h, -1*a/2 + 3*a/2*j))
                polygon.append(QPointF(2*h + 2*i*h - j*h, a/2 + 3*a/2*j))
                polygon.append(QPointF(h + 2*i*h - j*h, a + 3*a/2*j))
                polygon.append(QPointF(0 + 2*i*h - j*h, a/2 + 3*a/2*j))
                polygons_line.append(self.scene.addPolygon(polygon, self.pen))
            self.hexpolygons.append(polygons_line)

        for j in range(4):
            polygons_line = []
            for i in range(8-j):
                polygon = QPolygonF()
                polygon.append(QPointF(-3*h + 2*i*h + j*h, 14*a/2 + 3*a/2*j))
                polygon.append(QPointF(-2*h + 2*i*h + j*h, 13*a/2 + 3*a/2*j))
                polygon.append(QPointF(-1*h + 2*i*h + j*h, 14*a/2 + 3*a/2*j))
                polygon.append(QPointF(-1*h + 2*i*h + j*h, 16*a/2 + 3*a/2*j))
                polygon.append(QPointF(-2*h + 2*i*h + j*h, 17*a/2 + 3*a/2*j))
                polygon.append(QPointF(-3*h + 2*i*h + j*h, 16*a/2 + 3*a/2*j))
                polygons_line.append(self.scene.addPolygon(polygon, self.pen))
            self.hexpolygons.append(polygons_line)

        for j in range(5):
            hextext_line = []
            for i in range(5 + j):
                text = self.scene.addSimpleText("")
                text.setPos(h/2 + 2*h*i - h*j, -10 + 3*a/2*j)
                text.setScale(1.1)
                hextext_line.append(text)
            self.hextexts.append(hextext_line)

        for j in range(4):
            hextext_line = []
            for i in range(8 - j):
                text = self.scene.addSimpleText("")
                text.setPos(-5*h/2 + 2*h*i + h*j, 231 + 3*a/2*j)
                text.setScale(1.1)
                hextext_line.append(text)
            self.hextexts.append(hextext_line)

    def UpdateHexMap(self, agents, curr_turn, finished):
        if curr_turn % 2 == 0:
            self.Label_player.setText('RED')
        else:
            self.Label_player.setText('BLUE')
        for lines in self.hexpolygons:
            for element in lines:
                element.setBrush(self.WhiteBrush)
        for lines in self.hextexts:
            for element in lines:
                element.setText("")

        for agent in agents:
            str_val = str(agent.value)
            if len(str_val) == 1:
                str_val = "   " + str_val
            elif len(str_val) == 2:
                str_val = "  " + str_val
            elif len(str_val) == 3:
                str_val = " " + str_val
            if agent.player == 0:
                self.hexpolygons[agent.pos_y][agent.pos_x].setBrush(self.RedBrush)
            else:
                self.hexpolygons[agent.pos_y][agent.pos_x].setBrush(self.BlueBrush)
            self.hextexts[agent.pos_y][agent.pos_x].setText(str_val)

        if finished:
            print("Player: ", curr_turn, " Won the game!")

    def NewGame(self):
        if not self.in_progress:
            self.game = Game(self.Connection, 0)
            self.in_game = True
            self.ai = False
            self.UpdateHexMap(self.game.agents, self.game.curr_turn, self.game.finished)

    def Quit(self):
        app.quit()

    def TRFunction(self):
        if self.in_game and not self.in_progress:
            self.game.play_turn(1)
            self.UpdateHexMap(self.game.agents, self.game.curr_turn, self.game.finished)
            if self.ai:
                worker = Thread(self.PlayTurnAI)
                worker.signals.game.connect(self.UpdateMapThread)
                self.threadpool.start(worker)
        else:
            pass

    def RBFunction(self):
        if self.in_game and not self.in_progress:
            self.game.play_turn(2)
            self.UpdateHexMap(self.game.agents, self.game.curr_turn, self.game.finished)
            if self.ai:
                worker = Thread(self.PlayTurnAI)
                worker.signals.game.connect(self.UpdateMapThread)
                self.threadpool.start(worker)
        else:
            pass

    def BRFunction(self):
        if self.in_game and not self.in_progress:
            self.game.play_turn(3)
            self.UpdateHexMap(self.game.agents, self.game.curr_turn, self.game.finished)
            if self.ai:
                worker = Thread(self.PlayTurnAI)
                worker.signals.game.connect(self.UpdateMapThread)
                self.threadpool.start(worker)
        else:
            pass

    def BLFunction(self):
        if self.in_game and not self.in_progress:
            self.game.play_turn(4)
            self.UpdateHexMap(self.game.agents, self.game.curr_turn, self.game.finished)
            if self.ai:
                worker = Thread(self.PlayTurnAI)
                worker.signals.game.connect(self.UpdateMapThread)
                self.threadpool.start(worker)
        else:
            pass

    def LBFunction(self):
        if self.in_game and not self.in_progress:
            self.game.play_turn(5)
            self.UpdateHexMap(self.game.agents, self.game.curr_turn, self.game.finished)
            if self.ai:
                worker = Thread(self.PlayTurnAI)
                worker.signals.game.connect(self.UpdateMapThread)
                self.threadpool.start(worker)
        else:
            pass

    def TLFunction(self):
        if self.in_game and not self.in_progress:
            self.game.play_turn(6)
            self.UpdateHexMap(self.game.agents, self.game.curr_turn, self.game.finished)
            if self.ai:
                worker = Thread(self.PlayTurnAI)
                worker.signals.game.connect(self.UpdateMapThread)
                self.threadpool.start(worker)
        else:
            pass

    def SaveGameFunction(self):
        if self.in_game and not self.in_progress:
            data = ET.tostring(self.game.GameHistory)
            file = open("game_history.xml", "wb")
            file.write(data)
            print("Game Saved Successfully")
        else:
            pass

    def PlayAI(self):
        if self.Connection:
            pass
        if not self.in_progress:
            self.ai = True
            self.game = Game(self.Connection, 1)
            self.in_game = True
            self.UpdateHexMap(self.game.agents, self.game.curr_turn, self.game.finished)

    def PlayTurnAI(self, game_callback):
        if self.in_game and self.ai:
            self.in_progress = True
            game_callback.emit(self.game)
            time.sleep(1)
            gameNode = GameNode(self.game, 0)
            for i in range(0, AI_DEPTH_SEARCH):
                gameNode.generateNextLevel()

            max = -100000
            moveEvaluations = []
            bestEvaluations = []
            for i in range(0, 6):
                if self.game.curr_turn == 0:
                    moveEvaluations.append(-1 * gameNode.children[i].evaluate())
                else:
                    moveEvaluations.append(gameNode.children[i].evaluate())
                # print(i+1, ': ', moveEvaluations[i])
                if moveEvaluations[i] > max:
                    max = moveEvaluations[i]

            for i in range(0, 6):
                if moveEvaluations[i] == max:
                    bestEvaluations.append(i+1)
            bestMove = random.choice(bestEvaluations)

            print('best move: ', bestMove, ' (', max, ')')
            self.game.play_turn(bestMove)
            self.in_progress = False
            game_callback.emit(self.game)
        else:
            pass

    def UpdateMapThread(self, game):
        LoadedGame = game
        self.UpdateHexMap(LoadedGame.agents, LoadedGame.curr_turn, LoadedGame.finished)

    def LoadFunction(self):
        if self.Connection:
            pass
        elif os.path.exists('game_history.xml'):
            worker = Thread(self.Replay)
            worker.signals.game.connect(self.UpdateMapThread)
            self.threadpool.start(worker)
            print("Game Loaded Successfully")
        else:
            print("Cant find game_history.xml")
            print("Create your game history!")

    def Replay(self, game_callback):
        tree = ET.parse('game_history.xml')
        root = tree.getroot()
        self.game = Game(self.Connection, root.attrib['AI'])
        self.in_game = True
        self.in_progress = True

        for elem in root:
            self.game.agents.clear()
            self.game.turn = int(elem.attrib['number'])
            for subelem in elem:
                NewAgent = agent()
                NewAgent.pos_x = int(subelem.attrib['X'])
                NewAgent.pos_y = int(subelem.attrib['Y'])
                NewAgent.player = int(subelem.attrib['player'])
                NewAgent.value = int(subelem.text)
                self.game.agents.append(NewAgent)
            self.game.update_turn()
            game_callback.emit(self.game)
            time.sleep(1)
        self.in_progress = False
        if root.attrib['AI'] == '1':
            self.ai = True
        else:
            self.ai = False
        game_callback.emit(self.game)

    def TurnFunction(self):
        if self.current_player == 1 and self.Connection:
            self.current_player = 0
            self.game.wait_rival()
            self.UpdateHexMap(self.game.agents, self.game.curr_turn, self.game.finished)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
