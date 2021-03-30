from agent import agent


class multiMode:
    def __init__(self, mode, parent):
        self.BUFFER = 100
        self.mode = mode
        self.parent = parent
        self.socket = self.parent.socket

    def send_exit(self):
        message = str(7)
        self.socket.sendall(message.encode())

    def send_move_and_agent(self, move, agent):
        message = str(move) + " " + str(agent.player) + " " + str(agent.pos_x) + " " + \
                  str(agent.pos_y) + " " + str(agent.value)
        self.socket.sendall(message.encode())

    def get_move_and_agent(self, update_callback, finish_callback):
        data = self.socket.recv(self.BUFFER)
        data = data.decode()
        message = data.split()
        move = int(message[0])
        if move == 7:
            print('Your opponent closed connection !')
            self.parent.close()
            self.parent.parent.show()
        else:
            self.parent.game.play_turn(move, update_callback, create_agent=False)
            self.parent.game.agents.append(self.get_agent_from_message(message[1:]))
        finish_callback.emit(self.parent.game)

    def send_agent(self, agent):
        message_agent = str(agent.player) + " " + str(agent.pos_x) + " " + str(agent.pos_y) + " " + str(agent.value)
        self.socket.sendall(message_agent.encode())

    def get_agent(self):
        data = self.socket.recv(self.BUFFER)
        data = data.decode()
        message = data.split()
        return self.get_agent_from_message(message)

    def get_agent_from_message(self, message):
        new_agent = agent()
        new_agent.player = int(message[0])
        new_agent.pos_x = int(message[1])
        new_agent.pos_y = int(message[2])
        new_agent.value = int(message[3])
        return new_agent

    def send_nickname(self, nickname):
        message_nickname = str(nickname)
        self.socket.sendall(message_nickname.encode())

    def get_nickname(self):
        data = self.socket.recv(self.BUFFER)
        data = data.decode()
        nickname = data
        if nickname == 'User':
            nickname = 'Opponent'
        return nickname

    def nickname_transmission(self, nickname):
        if self.mode == 'Server':
            self.send_nickname(nickname)
            player_2 = self.get_nickname()
            return player_2
        elif self.mode == 'Client':
            player = self.get_nickname()
            self.send_nickname(nickname)
            return player
