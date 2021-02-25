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


class field:
    def __init__(self):
        self.color = ""
        self.value = ""

    def update_field(self, agent):
        self.color = str(agent.player)
        self.value = agent.value
