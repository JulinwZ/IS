class ElevatorHandler():

    def __init__(self, elevator_state, elevator_controller):
        self.state_name = 'SE'
        self.elevator_controller = elevator_controller
        self.elevator_state = elevator_state
        self.logs = []

    def process_next_step(self):
        self.elevator_state, self.state_name = self.elevator_controller.get_next_state(self.elevator_state, self.state_name)
        self.perform_action(self.elevator_controller.get_action(self.state_name))
        self.perform_action(self.elevator_controller.get_end_action(self.state_name))

    def perform_action(self, action):
        actions = {
            'UP': self.move_up,
            'DOWN': self.move_down,
            'OPEN': self.open_doors,
            'CLOSE': self.close_doors,
        }
        actions.get(action, self.no_action)()

    def move_up(self):
        self.elevator_state[0] += 1
        self.logs.append(f'Лифт поднялся на {self.elevator_state[0]} этаж')

    def move_down(self):
        self.elevator_state[0] -= 1
        self.logs.append(f'Лифт опустился на {self.elevator_state[0]} этаж')

    def open_doors(self):
        self.elevator_state[2] = True
        self.logs.append('Лифт открыл двери')

    def close_doors(self):
        self.elevator_state[2] = False
        self.logs.append('Лифт закрыл двери')

    def no_action(self):
        pass
    