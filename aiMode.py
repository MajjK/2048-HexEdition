from copy import deepcopy
from agent import agent


class aiMode:
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
            node = aiMode(newGame, (self.level + 1) % 4)
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
                    node = aiMode(new_game, (self.level + 1) % 4)
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
