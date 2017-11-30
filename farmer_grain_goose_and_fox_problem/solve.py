import copy


class RiverBank:
    def __init__(self, entities):
        self.farmer = entities[0]
        self.grain = entities[1]
        self.goose = entities[2]
        self.fox = entities[3]

        self.o_farmer = not entities[0]
        self.o_grain = not entities[1]
        self.o_goose = not entities[2]
        self.o_fox = not entities[3]

    def is_safe(self):
        if self.grain and self.goose and self.o_farmer:
            return False
        if self.goose and self.fox and self.o_farmer:
            return False

        if self.o_grain and self.o_goose and self.farmer:
            return False
        if self.o_goose and self.o_fox and self.farmer:
            return False

        return True

    def entities(self):
        return [self.farmer, self.grain, self.goose, self.fox]


class State:
    def __init__(self, state_id, river_bank_one):
        self.state_id = state_id
        self.river_bank = river_bank_one
        self.linked_states = []

    def add_link(self, linked_id):
        self.linked_states.append(linked_id)


def is_transition_possible(state_1, state_2):
    state_1_entities = state_1.river_bank.entities()
    state_2_entities = state_2.river_bank.entities()

    transported_entity_count = 0
    for entity_1, entity_2 in zip(state_1_entities, state_2_entities):

        if entity_1 != entity_2:
            transported_entity_count += 1
        if transported_entity_count > 2:
            return False

    farmer_traveled = True if state_1_entities[0] != state_2_entities[0] else False

    if farmer_traveled:
        farmer_was_in = 1 if state_1_entities[0] else 2
        if farmer_was_in == 1:
            elements_in_state1 = state_1_entities.count(True)
            elements_in_state2 = state_2_entities.count(True)
            if elements_in_state1 >= elements_in_state2:
                return False
        return True
    else:
        return False


state_possibilities = [[[farmer, grain, goose, fox], [not farmer, not grain, not goose, not fox]]
                       for farmer in [False, True]
                       for grain in [False, True]
                       for goose in [False, True]
                       for fox in [False, True]]

valid_states = []
state_count = 0
for state in state_possibilities:
    current_state_river_bank = RiverBank(state[0])
    if not current_state_river_bank.is_safe():
        continue
    valid_states.append(State(state_count, current_state_river_bank))
    state_count += 1

final_states = copy.deepcopy(valid_states)

for p in range(len(valid_states)):
    for q in range(p + 1, len(valid_states)):
        state_one = valid_states[p]
        state_two = valid_states[q]
        is_possible = is_transition_possible(state_one, state_two)
        if is_possible:
            final_states[p].add_link(state_two.state_id)
            final_states[q].add_link(state_one.state_id)

ids = [s.state_id for s in final_states]

start_state_id = [s.state_id for s in final_states if s.river_bank.entities() == [True, True, True, True]][0]
end_state_id = [s.state_id for s in final_states if s.river_bank.entities() == [False, False, False, False]][0]

nodes = {}
added = []
current_branch = [start_state_id]

while len(current_branch) > 0:
    current_node_id = current_branch.pop(0)
    current_node = [node for node in final_states if node.state_id == current_node_id][0]
    added.append(current_node_id)
    nodes_to_be_added = [n for n in current_node.linked_states if n not in added]
    current_branch += nodes_to_be_added
    nodes[current_node_id] = nodes_to_be_added

links = {}
for key, value in nodes.items():
    links[str(key)] = set([str(v) for v in value])


def depth_first_search_paths(graph, start, goal):
    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()
        for next_item in graph[vertex] - set(path):
            if next_item == goal:
                yield path + [next_item]
            else:
                stack.append((next_item, path + [next_item]))


paths = list(depth_first_search_paths(links, '9', '0'))


def print_current_node(node):
    positions = [' Farmer', ' Grain ', ' Goose ', ' Fox ']
    river_bank = node.river_bank.entities()
    other_river_bank = [not e for e in river_bank]

    drawing = ['']
    for place in range(len(river_bank)):
        if river_bank[place]:
            drawing.append(positions[place])
        else:
            drawing.append('       ')
        drawing.append('\t|~~~~~~~|\t')
        if other_river_bank[place]:
            drawing.append(positions[place])
        else:
            drawing.append('       ')
        drawing.append('\n')
    print('\n')
    print(''.join(drawing))


c = 1
for current_path in paths:
    print('\nSolution ' + str(c) + ' ===================================================')
    for n in current_path:
        n1 = [node for node in final_states if node.state_id == int(n)][0]
        print_current_node(n1)
    c += 1
