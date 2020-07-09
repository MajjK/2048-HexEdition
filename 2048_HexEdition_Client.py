from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from Hex2048 import Ui_MainWindow
import random
import re
import json
import os.path
import numpy as np
import socket
import sys

#Variables related with multiplayer connection
HOST = ''
PORT = 0
BUFFER = 100
Start = "Start"
End = "End"
TopLeft = "TopLeft"
TopRight = "TopRight"
Left = "Left"
Right = "Right"
BottomLeft = "BottomLeft"
BottomRight = "BottomRight"


def translate_move(data):
    if data == TopLeft:
        return 6
    if data == TopRight:
        return 1
    if data == BottomLeft:
        return 4
    if data == BottomRight:
        return 3
    if data == Left:
        return 5
    if data == Right:
        return 2


def translate_move_to_message(move):
    if move == 6:
        return TopLeft
    if move == 1:
        return TopRight
    if move == 4:
        return BottomLeft
    if move == 3:
        return BottomRight
    if move == 5:
        return Left
    if move == 2:
        return Right


def update_map(map, agents):
    #Main function to clear and re-update agents positions and values on the map
    #It also checks if any agent has 2048 value, if so, game is finished
    for lines in map:
        for element in lines:
            element.color = ""
            element.value = ""

    max = 0
    for agent in agents:
        map[agent.pos_y][agent.pos_x].update_field(agent)
        if agent.value > max:
            max = agent.value

    finished = False
    if max >= 2048:
        finished = True
    return map, finished


def create_map():
    hex_map = []
    for i in range(9):
        line = []
        if i < 5:
            for j in range(5 + i):
                line.append(field())
        else:
            for j in range(5 + 8 - i):
                line.append(field())

        hex_map.append(line)
    return hex_map


def look_for_collision(pos_y, pos_x, agents, curr_agent):
    for agent in agents:
        if agent.pos_y == pos_y and agent.pos_x == pos_x:
            if agent.player == curr_agent.player and agent.value == curr_agent.value:
                agent.value += curr_agent.value
                agents.pop(agents.index(curr_agent))
            return True
    return False


class Game:
    #Main Class connected with current game instance
    def __init__(self):
        self.agents = []
        self.map = create_map()
        self.finished = False
        self.turn = 0

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((HOST, PORT))

        data = self.socket.recv(BUFFER)
        data = data.decode()
        print(data)

        self.get_agent(self.socket)
        self.get_agent(self.socket)
        self.update_turn()
        print("Rival turn")

    def wait_rival(self):
        data = self.socket.recv(BUFFER)
        data = data.decode()
        move = translate_move(data)
        self.play_rival_turn(move)

    def send_agent(self, agent, conn):
        x = agent.pos_x
        y = agent.pos_y
        player = agent.player
        Message = str(player) + " " + str(x) + " " + str(y)
        conn.sendall(Message.encode())

    def get_agent(self, conn):
        data = conn.recv(BUFFER)
        data = data.decode()
        message = data.split()

        new_agent = agent()
        new_agent.player = int(message[0])
        new_agent.pos_x = int(message[1])
        new_agent.pos_y = int(message[2])
        new_agent.value = 2
        self.agents.append(new_agent)

    def sort_agents(self, move):
        if move == 1:
            self.agents.sort(key = lambda x: x.pos_y)
        elif move == 2:
            self.agents.sort(key = lambda x: x.pos_x, reverse = True)
        elif move == 3:
            self.agents.sort(key = lambda x: x.pos_y, reverse = True)
        elif move == 4:
            self.agents.sort(key = lambda x: x.pos_y, reverse = True)
        elif move == 5:
            self.agents.sort(key = lambda x: x.pos_x)
        elif move == 6:
            self.agents.sort(key = lambda x: x.pos_y)

    def play_turn(self, move):
        self.sort_agents(move)
        for current_agent in self.agents:
            if current_agent.player == 1:
                current_agent.move_agent(self.map, move, self.agents)

        for current_agent in self.agents:
            if current_agent.player == 1:
                current_agent.move_agent(self.map, move, self.agents)

        self.map, self.finished = update_map(self.map, self.agents)
        self.turn += 1

        data = translate_move_to_message(move)
        self.socket.sendall(data.encode())

        new_agent = agent()
        new_agent.create_agent(self.turn % 2, self.map)
        self.agents.append(new_agent)

        self.send_agent(new_agent, self.socket)
        self.update_turn()
        print("Rival Turn")

    def play_rival_turn(self, move):
        self.sort_agents(move)
        for current_agent in self.agents:
            if current_agent.player == 0:
                current_agent.move_agent(self.map, move, self.agents)

        for current_agent in self.agents:
            if current_agent.player == 0:
                current_agent.move_agent(self.map, move, self.agents)

        self.map, self.finished = update_map(self.map, self.agents)
        self.turn += 1
        self.get_agent(self.socket)
        self.update_turn()
        print("Your turn")

    def update_turn(self):
        self.map, self.finished = update_map(self.map, self.agents)
        self.curr_turn = self.turn % 2


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
                        if not look_for_collision(self.pos_y - 1, self.pos_x, agents, self):
                            self.pos_y -= 1
                        else:
                            break
                    else:
                        break

                elif 4 < self.pos_y < 9:
                    if not look_for_collision(self.pos_y - 1, self.pos_x + 1, agents, self):
                        self.pos_y -= 1
                        self.pos_x += 1
                    else:
                        break
                else:
                    break

            elif direction == 2:
                if self.pos_x < len(map[self.pos_y]) - 1:
                    if not look_for_collision(self.pos_y, self.pos_x + 1, agents, self):
                        self.pos_x += 1
                    else:
                        break
                else:
                    break

            elif direction == 3:
                if self.pos_y < 4:
                    if not look_for_collision(self.pos_y + 1, self.pos_x + 1, agents, self):
                        self.pos_y += 1
                        self.pos_x += 1
                    else:
                        break
                elif self.pos_y < 8:
                    if self.pos_x < len(map[self.pos_y]) - 1:
                        if not look_for_collision(self.pos_y + 1, self.pos_x, agents, self):
                            self.pos_y += 1
                        else:
                            break
                    else:
                        break
                else:
                    break

            elif direction == 4:
                if self.pos_y < 4:
                    if not look_for_collision(self.pos_y + 1, self.pos_x, agents, self):
                        self.pos_y += 1
                    else:
                        break
                elif self.pos_y < 8:
                    if self.pos_x > 0:
                        if not look_for_collision(self.pos_y + 1, self.pos_x - 1, agents, self):
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
                    if not look_for_collision(self.pos_y, self.pos_x - 1, agents, self):
                        self.pos_x -= 1
                    else:
                        break
                else:
                    break

            elif direction == 6:
                if 0 < self.pos_y < 5:
                    if self.pos_x > 0:
                        if not look_for_collision(self.pos_y - 1, self.pos_x-1, agents, self):
                            self.pos_y -= 1
                            self.pos_x -= 1
                        else:
                            break
                    else:
                        break

                elif 4 < self.pos_y < 9:
                    if not look_for_collision(self.pos_y - 1, self.pos_x, agents, self):
                        self.pos_y -= 1
                    else:
                        break
                else:
                    break


class MainWindow(QMainWindow, Ui_MainWindow, QWidget):
    #Class connected with main QT window, it contains button functions and calls all program actions
    def __init__(self):
        QMainWindow.__init__(self)
        self.game = None
        self.in_game = False
        self.connected = False
        self.current_player = -1
        self.hexpolygons = []
        self.hextexts = []

        self.setupUi(self)
        self.setWindowTitle("2048 - HexEdition - Client")
        self.createGraphicScene()
        self.show()

        self.QuitButton.setGeometry(55, 695, 93, 28)
        self.NewButton.setVisible(False)
        self.SaveGameButton.setVisible(False)
        self.LoadButton.setVisible(False)
        self.AIButton.setVisible(False)

        if os.path.exists('config.json'):
            self.getData()
            self.AddressText.setText(str(HOST))
            self.PortText.setText(str(PORT))

        self.MultiButton.setText("Connect")
        self.MultiButton.clicked.connect(self.Multi)
        self.QuitButton.clicked.connect(self.Quit)
        self.TRButton.clicked.connect(self.TRFunction)
        self.RButton.clicked.connect(self.RBFunction)
        self.BRButton.clicked.connect(self.BRFunction)
        self.BLButton.clicked.connect(self.BLFunction)
        self.LButton.clicked.connect(self.LBFunction)
        self.TLButton.clicked.connect(self.TLFunction)
        self.TurnButton.clicked.connect(self.TurnFunction)
        self.SaveButton.clicked.connect(self.SaveFunction)

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
        self.Label_player.setText(str(curr_turn + 1))
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
            print("Player: ", curr_turn + 1, " Won the game!")
            self.Label_Text_Player.setText("The winner is: ")

    def TurnFunction(self):
        if self.current_player == 0:
            self.current_player = 1
            self.game.wait_rival()
            self.UpdateHexMap(self.game.agents, self.game.curr_turn, self.game.finished)

    def Multi(self):
        if os.path.exists('config.json'):
            self.getData()
            self.AddressText.setText(str(HOST))
            self.PortText.setText(str(PORT))
            self.game = Game()
            self.in_game = True
            self.Label_Text_Player.setText("Player :")
            self.UpdateHexMap(self.game.agents, self.game.curr_turn, self.game.finished)
            self.current_player = 0
        else:
            print('Cant find config.json')
            print('Add your server configuration')

    def Quit(self):
        app.quit()

    def getData(self):
        global HOST
        global PORT

        with open('config.json') as json_file:
            data = json.load(json_file)
            for p in data['config']:
                HOST = p['Address']
                PORT = int(p['Port'])

    def TRFunction(self):
        if self.in_game and self.current_player == 1:
            self.game.play_turn(1)
            self.current_player = 0
            self.UpdateHexMap(self.game.agents, self.game.curr_turn, self.game.finished)
        else:
            pass

    def RBFunction(self):
        if self.in_game and self.current_player == 1:
            self.game.play_turn(2)
            self.current_player = 0
            self.UpdateHexMap(self.game.agents, self.game.curr_turn, self.game.finished)
        else:
            pass

    def BRFunction(self):
        if self.in_game and self.current_player == 1:
            self.game.play_turn(3)
            self.current_player = 0
            self.UpdateHexMap(self.game.agents, self.game.curr_turn, self.game.finished)
        else:
            pass

    def BLFunction(self):
        if self.in_game and self.current_player == 1:
            self.game.play_turn(4)
            self.current_player = 0
            self.UpdateHexMap(self.game.agents, self.game.curr_turn, self.game.finished)
        else:
            pass

    def LBFunction(self):
        if self.in_game and self.current_player == 1:
            self.game.play_turn(5)
            self.current_player = 0
            self.UpdateHexMap(self.game.agents, self.game.curr_turn, self.game.finished)
        else:
            pass

    def TLFunction(self):
        if self.in_game and self.current_player == 1:
            self.game.play_turn(6)
            self.current_player = 0
            self.UpdateHexMap(self.game.agents, self.game.curr_turn, self.game.finished)
        else:
            pass

    def SaveFunction(self):
        if not self.Connection:
            Address = self.AddressText.toPlainText()
            Port = self.PortText.toPlainText()

            if re.search('[a-zA-Z]', Address) is None and re.search('[a-zA-Z]', Port) is None:
                data = {}
                data['config'] = []
                data['config'].append({
                    'Address': Address,
                    'Port': int(Port)
                })
                with open('config.json', 'w') as outfile:
                    json.dump(data, outfile)
            else:
                print('Wrong Address or Port')
        else:
            print('You are already connected !')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
