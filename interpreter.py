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
        self.keywords = ["sum", "sub", "div", "mul", "if", "and", "or", "not", "greater", "lesser", "equal", "throw", "display", "var"]
    
    def interpret(self, content: list):
        self.programStack = Stack()
        self.skipCodeblock = False
        self.nestLevel: int = True
        self.nonKeywordIdentifier = False
        self.variables = {}
        self.variableInitialization = False
        self.loopState = False
        self.functions = {}
        self.funcName = ""
        self.functionInitialization = False

        for token in content:

            if self.skipCodeblock:
                if "codeblock" in token:
                    self.skipCodeblock = False
            
            elif self.loopState:
                while True:
                    self.codeblockExecuter(token)
                    
                    if not self.loopState:
                        break
            
            elif "codeblock" in token:
                self.codeblockExecuter(token)
            
            elif "identifier" in token:
                self.keywordDefinition(token)
            
            else:
                self.nonKeywordDefinitions(token)

    def codeblockExecuter(self, codeblock):
        if self.functionInitialization:
            self.functions[self.funcName] = codeblock
            self.functionInitialization = False

        else:
            for token in codeblock["codeblock"]:
                if "codeblock" in token:
                    if self.skipCodeblock:
                        self.skipCodeblock = False
                    else:
                        self.codeblockExecuter(token)
            
                elif "identifier" in token:
                    self.keywordDefinition(token)
            
                else:
                    self.nonKeywordDefinitions(token)
                #print(token, self.programStack._stack, sep="\n")

    def nonKeywordDefinitions(self, token):
            if "int" in token:
                num = int(token["int"])
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
                if self.programStack.peek() == 1:
                    self.skipCodeblock = False
                elif self.programStack.peek() == 0:
                    self.skipCodeblock = True
            
            case "throw":
                self.programStack.pop()
            
            case "not":
                a = self.programStack.pop()
                if a == 1:
                    self.programStack.push(0)
                elif a == 0:
                    self.programStack.push(1)
            
            case "and":
                a = self.programStack.pop()
                b = self.programStack.pop()
                result = a and b
                self.programStack.push(result)
            
            case "or":
                a = self.programStack.pop()
                b = self.programStack.pop()
                result = a or b
                self.programStack.push(result)
            
            case "var":
                self.variableInitialization = True
            
            case "loop":
                self.loopState = True
            
            case "quit":
                self.loopState = False
            
            case "func":
                self.functionInitialization = True

            case _:
                self.nonKeywordIdentifier = True
        
        if self.nonKeywordIdentifier:
            if self.variableInitialization:
                self.variables[token["identifier"]] = self.programStack.pop()
                self.variableInitialization = False

            elif self.functionInitialization:
                self.functions[token["identifier"]] = []
                self.funcName = token["identifier"]

            elif token["identifier"] in self.variables:
                value = self.variables[token["identifier"]]
                self.programStack.push(value)

            elif token["identifier"] in self.functions:
                self.codeblockExecuter(self.functions[token["identifier"]])
            
            self.nonKeywordIdentifier = False
