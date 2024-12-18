from ElevatorController import ElevatorController
from ElevatorHandler import ElevatorHandler

def read_input(filename='input.txt'):
    env_state = []
    with open(filename, 'r') as file:
        n_floors = int(file.readline())
        start_floor_1, start_floor_2 = map(int, file.readline().split(' '))
        env_states = file.readline().split(' ')
        for pas_state in env_states:
            pas_state_1, pas_state_2 = map(int, pas_state.split(','))
            env_state.append((pas_state_1, pas_state_2))
    return env_state, start_floor_1, start_floor_2

def write_logs(elevator1, elevator2, filename='output.txt'):
    with open(filename, 'w') as file:
        file.write('Лифт 1 выполнил: \n')
        file.writelines([log + '\n' for log in elevator1.logs])
        file.write('-------------------------\n')
        file.write('Лифт 2 выполнил: \n')
        file.writelines([log + '\n' for log in elevator2.logs])

def initialize_elevators(env_state, start_floor_1, start_floor_2):
    elevator_controller = ElevatorController(env_state)
    elevator1 = ElevatorHandler([start_floor_1, [], False], elevator_controller)
    elevator2 = ElevatorHandler([start_floor_2, [], False], elevator_controller)
    return elevator1, elevator2

def run_elevators(elevator1, elevator2):
    while not(elevator1.state_name == 'END' and elevator2.state_name == 'END'):
        elevator1.process_next_step()
        elevator2.process_next_step()

if __name__ == "__main__":
    env_state, start_floor_1, start_floor_2 = read_input()
    elevator1, elevator2 = initialize_elevators(env_state, start_floor_1, start_floor_2)
    run_elevators(elevator1, elevator2)
    write_logs(elevator1, elevator2)
