class Stack:
    def __init__(self):
        self.stack = ['empty']

    def push(self, value):
        self.stack.append(value)
        
    def pop(self):
        try:
            return self.stack.pop()
        except IndexError:
            raise

    def getLength(self):
        return len(self.stack)
