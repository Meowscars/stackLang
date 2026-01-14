class Stack:
    def __init__(self):
        self._stack = []
    
    def push(self, element):
        self._stack.append(element)
    
    def pop(self):
        if self._stack:
            return self._stack.pop()

    def peek(self):
        if self._stack:
            return self._stack[-1]


class Interpreter:
    def __init__(self):
        self.keywords = ["sum", "sub", "div", "mul"]
    
    def interpret(self, content: list):
        programStack = Stack()

        for token in content:
            if "identifier" in token:
                match token["identifier"]:
                    case "sum":
                        a = programStack.pop()
                        b = programStack.pop()
                        programStack.push(a+b)
                    
                    case "mul":
                        a = programStack.pop()
                        b = programStack.pop()
                        programStack.push(a*b)
                    
                    case "sub":
                        a = programStack.pop()
                        b = programStack.pop()
                        programStack.push(b-a)
                    
                    case "div":
                        a = programStack.pop()
                        b = programStack.pop()
                        programStack.push(b/a)
                    
                    case "display":
                        a = programStack.peek()
                        print(a)
            
            if "int" in token:
                num = int(token["int"]) # current assumption to be a int only. no other types implemented
                programStack.push(num)
            
            elif "str" in token:
                value = token["str"]
                programStack.push(value)