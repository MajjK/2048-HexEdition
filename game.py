import xml.etree.ElementTree as et
from aiMode import aiMode
from agent import agent
import os.path
import random
import time
import map


class game:
    def __init__(self, ai, multi, player):
        self.agents = []
        self.map = map.map()
        self.finished = False
        self.turn = 0
        self.curr_turn = 0
        self.ai_depth_search = 3
        self.player = str(player)
        self.multi = multi
        self.record = 2
        self.root = None
        if self.multi != 'Client':
            self.init_scoreboards()
            self.game_history = et.Element('Game')
            self.game_history.set('AI', str(ai))
            self.game_history.set('Nickname', self.player)
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

    def update_scoreboards(self, player_color):
        for elem_agents in self.agents:
            if elem_agents.value > self.record and elem_agents.player == player_color:
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
        if create_agent and len(self.agents) < 61:
            new_agent = agent()
            new_agent.create_agent(self.turn % 2, self.map.map_area)
            self.agents.append(new_agent)
        self.update_turn()

    def play_turn_ai(self, game_callback):
        max_val = -100000
        move_evaluations = []
        best_evaluations = []
        time.sleep(1)
        game_node = aiMode(self, 0)
        for i in range(0, self.ai_depth_search):
            game_node.generate_next_level()
        for i in range(0, 6):
            if self.curr_turn == 0:
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
        self.play_turn(bestMove)
        game_callback.emit(self)

    def update_turn(self):
        self.finished = self.map.update_map(self.agents)
        self.curr_turn = self.turn % 2
        if self.multi != 'Client':
            self.update_scoreboards(0)
            self.update_history()