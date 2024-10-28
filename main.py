import heapq

def create_state(height, width, vehicles, parent=None, cost=0):
    vehicles = tuple(vehicles)
    is_goal = check_goal_state(vehicles, width)
    return {
        'height': height,
        'width': width,
        'vehicles': vehicles,
        'parent': parent,
        'cost': cost,
        'is_goal': is_goal
    }

def check_goal_state(vehicles, width):
    return vehicles[0][1] + vehicles[0][3] - 1 == width

def is_vehicle_blocked(vehicles, vehicle, direction, height, width):
    row, col, orientation, length = vehicle
    if orientation == 'h':
        if direction == 'left':
            if col <= 1:
                return True
            return any(
                other_vehicle != vehicle and (
                    (other_vehicle[2] == 'h' and other_vehicle[0] == row and other_vehicle[1] + other_vehicle[3] == col) or
                    (other_vehicle[2] == 'v' and other_vehicle[0] <= row < other_vehicle[0] + other_vehicle[3] and other_vehicle[1] == col - 1)
                ) for other_vehicle in vehicles
            )
        elif direction == 'right':
            if col + length > width:
                return True
            return any(
                other_vehicle != vehicle and (
                    (other_vehicle[2] == 'h' and other_vehicle[0] == row and col + length == other_vehicle[1]) or
                    (other_vehicle[2] == 'v' and other_vehicle[0] <= row < other_vehicle[0] + other_vehicle[3] and other_vehicle[1] == col + length)
                ) for other_vehicle in vehicles
            )
    elif orientation == 'v':
        if direction == 'up':
            if row <= 1:
                return True
            return any(
                other_vehicle != vehicle and (
                    (other_vehicle[2] == 'v' and other_vehicle[1] == col and other_vehicle[0] + other_vehicle[3] == row) or
                    (other_vehicle[2] == 'h' and other_vehicle[1] <= col < other_vehicle[1] + other_vehicle[3] and other_vehicle[0] == row - 1)
                ) for other_vehicle in vehicles
            )
        elif direction == 'down':
            if row + length > height:
                return True
            return any(
                other_vehicle != vehicle and (
                    (other_vehicle[2] == 'v' and other_vehicle[1] == col and row + length == other_vehicle[0]) or
                    (other_vehicle[2] == 'h' and other_vehicle[1] <= col < other_vehicle[1] + other_vehicle[3] and other_vehicle[0] == row + length)
                ) for other_vehicle in vehicles
            )
    return False

def get_next_states(current_state):
    possible_states = []
    parent = current_state
    height = current_state['height']
    width = current_state['width']
    cost = current_state['cost']
    vehicles_list = list(current_state['vehicles'])

    for index, vehicle in enumerate(current_state['vehicles']):
        row, col, orientation, length = vehicle

        if orientation == 'h':
            if not is_vehicle_blocked(current_state['vehicles'], vehicle, 'left', height, width):
                vehicles_list[index] = (row, col - 1, orientation, length)
                new_state_instance = create_state(height, width, tuple(vehicles_list), parent=parent, cost=cost + 1)
                possible_states.append(new_state_instance)
                vehicles_list[index] = vehicle

            if not is_vehicle_blocked(current_state['vehicles'], vehicle, 'right', height, width):
                vehicles_list[index] = (row, col + 1, orientation, length)
                new_state_instance = create_state(height, width, tuple(vehicles_list), parent=parent, cost=cost + 1)
                possible_states.append(new_state_instance)
                vehicles_list[index] = vehicle

        elif orientation == 'v':
            if not is_vehicle_blocked(current_state['vehicles'], vehicle, 'up', height, width):
                vehicles_list[index] = (row - 1, col, orientation, length)
                new_state_instance = create_state(height, width, tuple(vehicles_list), parent=parent, cost=cost + 1)
                possible_states.append(new_state_instance)
                vehicles_list[index] = vehicle

            if not is_vehicle_blocked(current_state['vehicles'], vehicle, 'down', height, width):
                vehicles_list[index] = (row + 1, col, orientation, length)
                new_state_instance = create_state(height, width, tuple(vehicles_list), parent=parent, cost=cost + 1)
                possible_states.append(new_state_instance)
                vehicles_list[index] = vehicle

    return possible_states

def heuristic(vehicles, height, width):
    red_car = vehicles[0]
    red_car_row, red_car_col, red_car_orientation, red_car_length = red_car
    return width - (red_car_col + red_car_length) + 1


def fn(state):
    return state['cost'] + heuristic(state['vehicles'], state['height'], state['width'])

def state_hash(state):
    return hash(state['vehicles'])

def a_star_algorithm(initial_vehicles, height, width):
    initial_state = create_state(height, width, initial_vehicles)
    priority_queue = []
    heapq.heapify(priority_queue)
    state_map = {state_hash(initial_state): initial_state}
    heapq.heappush(priority_queue, (fn(initial_state), state_hash(initial_state)))

    visited = set()
    while priority_queue:
        _, current_state_hash = heapq.heappop(priority_queue)
        current_state = state_map[current_state_hash]

        if current_state['is_goal']:
            return current_state

        visited.add(current_state['vehicles'])

        next_states = get_next_states(current_state)
        for state in next_states:
            state_hash_val = state_hash(state)
            if state['vehicles'] not in visited and state_hash_val not in state_map:
                state_map[state_hash_val] = state
                heapq.heappush(priority_queue, (fn(state), state_hash_val))


test_count = int(input())  # Fixed prompt message
for test in range(test_count):
    line = input()  
    inputs = [int(i) for i in line.split()] 
    height, width, cars_count = inputs

    initial_state = []
    for car in range(cars_count):
        line = input()  
        parts = line.split()
        initial_state.append((int(parts[0]), int(parts[1]), parts[2], int(parts[3])))


    goal_state = a_star_algorithm(initial_state, height, width)
    print(goal_state["cost"])


