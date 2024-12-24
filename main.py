from lexer import Lexer
from stack import Stack
from states import StateN, StateNE, StateER, StateNSE, StateNAE, StateAER
import pickle

stack = Stack()
lexer = Lexer()

stateN = StateN(lexer)
stateNE = StateNE(lexer)
stateER = StateER(lexer)
stateNSE = StateNSE(lexer, stack)
stateNAE = StateNAE(lexer)
stateAER = StateAER(lexer)

object_dict = {
            (False, False, False, False) : stateN,
            (False, False, True, False) : stateNE,
            (False, False, True, True) : stateER,
            (False, True, True, False) : stateNSE,
            (True, False, True, False) : stateNAE,
            (True, False, True, True) : stateAER,
}

with open("table.pkl", 'rb') as file:
    transitions = pickle.load(file)
    
inputs = [
    ['int', 'id', '(', 'int', 'id', ',', 'int', 'id', ')', '{', 'return', 'id', '+', 'id', '}', 'empty'],
    ['int', 'id', '=', 'NUM', '*', 'empty']
]

lexer.initInput(inputs[0])
lexer.initStack(stack)
lexer.initDKA(transitions, object_dict)

lexer.run()
