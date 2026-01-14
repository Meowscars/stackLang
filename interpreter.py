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
        self.programStack = Stack()
        self.ifIsTrue = True

        for token in content:        
            if self.ifIsTrue:
                if "identifier" in token:
                    self.keywordDefinition(token)
                else:
                    self.nonKeywordDefinitions(token)
            else:
                if "closecurly" in token:
                    self.ifIsTrue = True

    def nonKeywordDefinitions(self, token):
            if "int" in token:
                num = int(token["int"]) # current assumption to be a int only. no other types implemented
                self.programStack.push(num)
                
            elif "str" in token:
                value = token["str"]
                self.programStack.push(value)
    
    def keywordDefinition(self, token):
        match token["identifier"]:
            case "sum":
                a = self.programStack.pop()
                b = self.programStack.pop()
                self.programStack.push(a+b)
                    
            case "mul":
                a = self.programStack.pop()
                b = self.programStack.pop()
                self.programStack.push(a*b)
                    
            case "sub":
                a = self.programStack.pop()
                b = self.programStack.pop()
                self.programStack.push(b-a)
                    
            case "div":
                a = self.programStack.pop()
                b = self.programStack.pop()
                self.programStack.push(b/a)
                    
            case "display":
                a = self.programStack.peek()
                print(a)
                    
            case "greater":
                a = self.programStack.pop()
                b = self.programStack.pop()
                if b > a:
                    self.programStack.push(1)
                else: 
                    self.programStack.push(0)

            case "lesser":
                a = self.programStack.pop()
                b = self.programStack.pop()
                if b < a:
                    self.programStack.push(1)
                else: 
                     self.programStack.push(0)
            
            case "equal":
                a = self.programStack.pop()
                b = self.programStack.pop()
                if a == b:
                    self.programStack.push(1)
                else:
                    self.programStack.push(0)
                    
            case "if":
                if self.programStack.pop() == 1:
                    self.ifIsTrue = True
                else:
                    self.ifIsTrue = False
            
            case "throw":
                self.programStack.pop()