class Lexer:
    def __init__(self):
        self.result = {
            'empty': 'Удовлетворяет данной грамматике'
        }
    
    def initStack(self, stack):
        self.stack = stack

    def initDKA(self, transition_table, object_dict):
        self.objects = {}
        self.object_dict = object_dict
        self.transition_table = {}
        for current_state, row in transition_table.items():
            self.transition_table[current_state] = {}
            next_state, accept, stack, error, return_, guid_symbols = list(row.values())
            self.objects[current_state] = self.object_dict[accept, stack, error, return_]
            self.transition_table[current_state]['guid_symbols'] = guid_symbols
            self.transition_table[current_state]['next_state'] = next_state

    def run(self):
        self.state = 1
        self.current_symbol = next(self.input)
        self.error = False

        while self.error == False and not (self.current_symbol == 'empty' and self.stack.getLength() == 0):
            obj = self.objects[self.state]
            obj.next()
            
        print(self.result.get(self.state, 'Не удовлетворяет данной грамматике'))

    def accept(self):
        try:
            self.current_symbol = next(self.input)
            return self.current_symbol
        except StopIteration:
            self.error = True

    def return_(self):
        try:
            self.state = self.stack.pop()
        except IndexError:
            self.error = True

    def initInput(self, input):
        self.input = iter(input)

    def incrementState(self):
        self.state += 1

    def must_error(self):
        try:
            self.transition_table[self.state]['guid_symbols'].index(self.current_symbol)
        except ValueError:
            raise

    def nextState(self):
        self.state = self.transition_table[self.state]['next_state']
