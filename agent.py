import random


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

    def move_agent(self, game, direction):
        if direction == 1:
            self.move_tr(game.map.map_area, game.agents)
        elif direction == 2:
            self.move_r(game.map.map_area, game.agents)
        elif direction == 3:
            self.move_br(game.map.map_area, game.agents)
        elif direction == 4:
            self.move_bl(game.map.map_area, game.agents)
        elif direction == 5:
            self.move_l(game.map.map_area, game.agents)
        elif direction == 6:
            self.move_tl(game.map.map_area, game.agents)

    def move_tr(self, map_area, agents):
        while True:
            if 0 < self.pos_y < 5:
                if self.pos_x < len(map_area[self.pos_y]) - 1:
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

    def move_r(self, map_area, agents):
        while True:
            if self.pos_x < len(map_area[self.pos_y]) - 1:
                if not self.look_for_collision(self.pos_y, self.pos_x + 1, agents):
                    self.pos_x += 1
                else:
                    break
            else:
                break

    def move_br(self, map_area, agents):
        while True:
            if self.pos_y < 4:
                if not self.look_for_collision(self.pos_y + 1, self.pos_x + 1, agents):
                    self.pos_y += 1
                    self.pos_x += 1
                else:
                    break
            elif self.pos_y < 8:
                if self.pos_x < len(map_area[self.pos_y]) - 1:
                    if not self.look_for_collision(self.pos_y + 1, self.pos_x, agents):
                        self.pos_y += 1
                    else:
                        break
                else:
                    break
            else:
                break

    def move_bl(self, map_area, agents):
        while True:
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

    def move_l(self, map_area, agents):
        while True:
            if self.pos_x > 0:
                if not self.look_for_collision(self.pos_y, self.pos_x - 1, agents):
                    self.pos_x -= 1
                else:
                    break
            else:
                break

    def move_tl(self, map_area, agents):
        while True:
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
