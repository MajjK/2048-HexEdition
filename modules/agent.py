import random


class agent:
    def __init__(self):
        self.player = -1
        self.value = 0
        self.pos_x = -1
        self.pos_y = -1

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def create_agent(self, player, map_field):
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
            if map_field[y][x].value == "":
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
        if 0 < self.pos_y < 5 and self.pos_x < len(map_area[self.pos_y]) - 1 \
                and not self.look_for_collision(self.pos_y - 1, self.pos_x, agents):
            self.pos_y -= 1
        elif 4 < self.pos_y < 9 and not self.look_for_collision(self.pos_y - 1, self.pos_x + 1, agents):
            self.pos_y -= 1
            self.pos_x += 1

    def move_r(self, map_area, agents):
        if self.pos_x < len(map_area[self.pos_y]) - 1 \
                and not self.look_for_collision(self.pos_y, self.pos_x + 1, agents):
            self.pos_x += 1

    def move_br(self, map_area, agents):
        if self.pos_y < 4 and not self.look_for_collision(self.pos_y + 1, self.pos_x + 1, agents):
            self.pos_y += 1
            self.pos_x += 1
        elif self.pos_y < 8 and self.pos_x < len(map_area[self.pos_y]) - 1 \
                and not self.look_for_collision(self.pos_y + 1, self.pos_x, agents):
            self.pos_y += 1

    def move_bl(self, map_area, agents):
        if self.pos_y < 4 and not self.look_for_collision(self.pos_y + 1, self.pos_x, agents):
            self.pos_y += 1
        elif self.pos_y < 8 and self.pos_x > 0 and not self.look_for_collision(self.pos_y + 1, self.pos_x - 1, agents):
            self.pos_y += 1
            self.pos_x -= 1

    def move_l(self, map_area, agents):
        if self.pos_x > 0 and not self.look_for_collision(self.pos_y, self.pos_x - 1, agents):
            self.pos_x -= 1

    def move_tl(self, map_area, agents):
        if 0 < self.pos_y < 5 and self.pos_x > 0 \
                and not self.look_for_collision(self.pos_y - 1, self.pos_x - 1, agents):
            self.pos_y -= 1
            self.pos_x -= 1
        elif 4 < self.pos_y < 9 and not self.look_for_collision(self.pos_y - 1, self.pos_x, agents):
            self.pos_y -= 1

    def look_for_collision(self, pos_y, pos_x, agents):
        for elem in agents:
            if elem.pos_y == pos_y and elem.pos_x == pos_x:
                if elem.player == self.player and elem.value == self.value:
                    elem.value += self.value
                    if self in agents:
                        agents.pop(agents.index(self))
                return True
        return False
