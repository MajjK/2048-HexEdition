from modules.agent import agent
from modules.gameMap import map


def test_create_agent():
    new_map = map()
    new_agent = agent()

    new_agent.create_agent(1, new_map.map_area)

    assert new_agent.player == 1
    assert new_agent.pos_x != -1
    assert new_agent.pos_y != -1
    assert new_agent.value == 2


def test_look_for_collision():
    agents = []
    new_map = map()
    for i in range(2):
        new_agent = agent()
        new_agent.create_agent(1, new_map.map_area)
        agents.append(new_agent)
        new_map.update_map(agents)

    agents[0].look_for_collision(agents[1].pos_y, agents[1].pos_x, agents)

    assert len(agents) == 1
    assert agents[0].value == 4


def test_move():
    agents = []
    new_map = map()
    moved_agent = agent()
    moved_agent.create_agent(1, new_map.map_area)
    moved_agent.pos_x = 0
    agents.append(moved_agent)
    new_map.update_map(agents)

    second_agent = agent()
    second_agent.create_agent(2, new_map.map_area)
    second_agent.pos_x = 1
    second_agent.pos_y = moved_agent.pos_y
    agents.append(second_agent)
    new_map.update_map(agents)

    moved_agent.move_l(new_map.map_area, agents)
    moved_agent.move_r(new_map.map_area, agents)

    assert moved_agent.pos_x == 0
    assert len(agents) == 2









