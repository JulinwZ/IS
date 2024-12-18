import numpy as np

class ElevatorController():
    def __init__(self, env_state):
        self.env_state = env_state

    def get_next_state(self, elevator_state, state_name):
        end_dict = {
            (0, 0): self.__generate_end_state,
        }
        return end_dict.get((len(elevator_state[1]), len(self.env_state)), self.__generate_state)(elevator_state, state_name)

    @staticmethod
    def get_action(state_name):
        dir_action = {
            'O': 'OPEN',
            'U': 'UP',
            'D': 'DOWN',
        }
        return dir_action.get(state_name[0], 'NONE')

    @staticmethod
    def get_end_action(state_name):
        dir_action = {
            'O': 'CLOSE',
        }
        return dir_action.get(state_name[0], 'NONE')

    def __generate_end_state(self, elevator_state, state_name):
        return elevator_state, 'END'

    def __generate_state(self, elevator_state, state_name):
        check_dict = {
            0: self.__generate_state_no_env,
        }
        return check_dict.get(len(self.env_state), self.__generate_state_env)(elevator_state, state_name)

    def __generate_state_env(self, elevator_state, state_name):
        state_dict = {
            'O': self.__check_go,
        }
        elevator_state, state = state_dict.get(state_name[0], self.__check_doors)(elevator_state, state_name)
        return elevator_state, state

    def __generate_state_no_env(self, elevator_state, state_name):
        check_dict = {
            True: self.__open_doors_no_env,
        }
        pas_inside_cond = min(elevator_state[1], key=lambda x: abs(x - elevator_state[0])) == elevator_state[0]
        elevator_state, state = check_dict.get(pas_inside_cond, self.__check_go)(elevator_state, state_name)
        return elevator_state, state

    def __open_doors_no_env(self, elevator_state, state_name):
        check_dict = {
            0: 'E',
        }
        elevator_state[1] = list(filter(lambda pas: pas != elevator_state[0], elevator_state[1]))
        empty_char = check_dict.get(len(elevator_state[1]), 'F')
        return elevator_state, 'O' + empty_char

    def __check_doors(self, elevator_state, state_name):
        doors_dict = {
            True: self.__open_doors,
            False: self.__check_go,
        }
        doors_condition = self.__check_door_condition(elevator_state, state_name)
        elevator_state, state = doors_dict[doors_condition](elevator_state, state_name)
        return elevator_state, state

    def __open_doors(self, elevator_state, state_name):
        check_dict = {
            0: self.__open_doors_empty,
        }
        elevator_state[1] = list(filter(lambda pas: pas != elevator_state[0], elevator_state[1]))
        elevator_state, state = check_dict.get(len(elevator_state[1]), self.__open_doors_full)(elevator_state, state_name)
        return elevator_state, state

    def __open_doors_empty(self, elevator_state, state_name):
        passengers_on_floor = list(filter(lambda pas: pas[0] == elevator_state[0], self.env_state))
        for pas in passengers_on_floor:
            elevator_state[1].append(pas[1])
        self.env_state = list(filter(lambda pas: pas[0] != elevator_state[0], self.env_state))
        check_dict = {
            0: 'E',
        }
        empty_char = check_dict.get(len(elevator_state[1]), 'F')
        return elevator_state, 'O' + empty_char

    def __open_doors_full(self, elevator_state, state_name):
        dir_dict = {
            'U': 1,
            'D': -1,
        }
        direction = dir_dict[state_name[0]]
        passengers_on_floor = list(filter(lambda pas: pas[0] == elevator_state[0] and ((pas[1] - pas[0] > 0) == direction), self.env_state))
        for pas in passengers_on_floor:
            elevator_state[1].append(pas[1])
        self.env_state = list(filter(lambda pas: not(pas[0] == elevator_state[0] and ((pas[1] - pas[0] > 0) == direction)), self.env_state))
        return elevator_state, 'OF'

    def __check_go(self, elevator_state, state_name):
        elevator_dict = {
                'E': self.__find_nearest_out,
                'F': self.__find_nearest_in,
        }
        nearest = elevator_dict[state_name[1]](elevator_state)
        elevator_state, state = self.__elevator_go(elevator_state, state_name, nearest)
        return elevator_state, state

    def __find_nearest_out(self, elevator_state):
        return min(self.env_state, key=lambda x: abs(x[0] - elevator_state[0]))[0]

    def __find_nearest_in(self, elevator_state):
        return min(elevator_state[1], key=lambda x: abs(x - elevator_state[0]))

    def __elevator_go(self, elevator_state, state_name, nearest):
        dir_dict = {
            False: 'U',
            True: 'D',
        }
        direction_condition = (elevator_state[0] - nearest) > 0
        dir_char = dir_dict[direction_condition]
        return elevator_state, dir_char + state_name[1]

    def __check_door_condition(self, elevator_state, state_name):
        empty_dict = {
            'E': self.__check_empty_door_condition,
            'F': self.__check_full_door_condition,
        }
        return empty_dict[state_name[1]](elevator_state, state_name)

    def __check_empty_door_condition(self, elevator_state, state_name):
        pas_outside_cond = any(np.where(np.array(self.env_state)[:, 0] == elevator_state[0], 1, 0) == 1)
        return pas_outside_cond

    def __check_full_door_condition(self, elevator_state, state_name):
        dir_dict = {
            'U': 1,
            'D': -1,
        }
        direction = dir_dict[state_name[0]]
        pas_inside_cond = min(elevator_state[1], key=lambda x: abs(x - elevator_state[0])) == elevator_state[0]
        pas_outside = np.where(np.array(self.env_state)[:, 0] == elevator_state[0])
        pas_outside_cond = any(np.where(np.array(self.env_state)[pas_outside][:, 1] - elevator_state[0] > 0, 1, -1) == direction)
        return pas_outside_cond or pas_inside_cond
