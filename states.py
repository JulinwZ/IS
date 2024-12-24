from abc import ABC, abstractmethod

class State(ABC):
    @abstractmethod
    def next(self):
        pass

class StateN(State):
    def __init__(self, lexer):
        self.lexer = lexer

    def next(self):
        try:
            self.lexer.must_error()
        except ValueError:
            self.lexer.incrementState()
            return

        self.lexer.nextState()

class StateNE(State):
    def __init__(self, lexer):
        self.lexer = lexer

    def next(self):
        try:
            self.lexer.must_error()
        except ValueError:
            self.lexer.error = True
            return

        self.lexer.nextState()

class StateER(State):
    def __init__(self, lexer):
        self.lexer = lexer

    def next(self):
        try:
            self.lexer.must_error()
        except ValueError:
            self.lexer.error = True
            return

        self.lexer.return_()

class StateAER(State):
    def __init__(self, lexer):
        self.lexer = lexer

    def next(self):
        try:
            self.lexer.must_error()
        except ValueError:
            self.lexer.error = True
            return

        self.lexer.accept()
        self.lexer.return_()

class StateNSE(State):
    def __init__(self, lexer, stack):
        self.lexer = lexer
        self.stack = stack

    def next(self):
        try:
            self.lexer.must_error()
        except ValueError:
            self.lexer.error = True
            return

        self.stack.push(self.lexer.state + 1)
        self.lexer.nextState()

class StateNAE(State):
    def __init__(self, lexer):
        self.lexer = lexer

    def next(self):
        try:
            self.lexer.must_error()
        except ValueError:
            self.lexer.error = True
            return

        self.lexer.accept()
        self.lexer.nextState()
