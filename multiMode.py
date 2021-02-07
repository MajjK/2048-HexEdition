from agent import agent
import socket


class multiMode:
    def __init__(self, multi, socket):
        self.BUFFER = 100
        self.mode = multi
        self.socket = socket

    def send_exit(self):
        message = str(7)
        self.socket.sendall(message.encode())

    def send_move_and_agent(self, move, agent):
        message = str(move) + " " + str(agent.player) + " " + str(agent.pos_x) + " " + \
                  str(agent.pos_y) + " " + str(agent.value)
        self.socket.sendall(message.encode())

    def get_move_and_agent(self, game, window, parent_window):
        data = self.socket.recv(self.BUFFER)
        data = data.decode()
        message = data.split()
        move = int(message[0])
        if move == 7:
            print('Your opponent closed connection !')
            window.close()
            parent_window.show()
            return None
        else:
            game.play_turn(int(message[0]), create_agent=False)
            new_agent = agent()
            new_agent.player = int(message[1])
            new_agent.pos_x = int(message[2])
            new_agent.pos_y = int(message[3])
            new_agent.value = int(message[4])
            game.agents.append(new_agent)
            return game

    def send_agent(self, agent):
        message_agent = str(agent.player) + " " + str(agent.pos_x) + " " + str(agent.pos_y) + " " + str(agent.value)
        self.socket.sendall(message_agent.encode())

    def get_agent(self):
        data = self.socket.recv(self.BUFFER)
        data = data.decode()
        message = data.split()
        new_agent = agent()
        new_agent.player = int(message[0])
        new_agent.pos_x = int(message[1])
        new_agent.pos_y = int(message[2])
        new_agent.value = int(message[3])
        return new_agent

    def nickname_transmission(self, nickname):
        if self.mode == 'Server':
            message_nickname = str(nickname)
            self.socket.sendall(message_nickname.encode())
            data = self.socket.recv(self.BUFFER)
            data = data.decode()
            player_2 = data
            if player_2 == 'User':
                player_2 = 'Opponent'
            return player_2
        elif self.mode == 'Client':
            data = self.socket.recv(self.BUFFER)
            data = data.decode()
            player = data
            if player == 'User':
                player = 'Opponent'
            message_nickname = str(nickname)
            self.socket.sendall(message_nickname.encode())
            return player
