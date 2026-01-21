from sys import exit

class Error:
    def __init__(self, ):
        ...
    
    def unexpectedIdentifier(self, Identifier):
        exit(f"ERROR## Unexpected identifier encountered: \"{Identifier}\" not defined")
    
    def notEnoughArgumentsInStack(self, Identifier, requiredArguments):
        exit(f"ERROR## The stack doesn't contain enough elements: function {Identifier} reuires {requiredArguments} in the stack")
    
    def typeMismatch(self, Identifier, typeIncountered, typesrequired):
        exit(f"ERROR## Type mismatch: function {Identifier} requires argument type {typesrequired} but encountered {typeIncountered}")
    
    def emptyStack(self):
        exit("ERROR## popping from an empty stack")