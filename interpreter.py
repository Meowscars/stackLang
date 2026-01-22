import errors


class Stack:
    def __init__(self):
        self._stack = []
        self.error = errors.Error()
    
    def push(self, element):
        self._stack.append(element)
    
    def pop(self):
        if self._stack:
            return self._stack.pop()
        else:
            self.error.emptyStack()

    def peek(self):
        if self._stack:
            return self._stack[-1]


class Interpreter:
    def __init__(self):
        self.error = errors.Error()
    
    def interpret(self, content: list):
        self.programStack = Stack()
        self.skipCodeblock = False
        self.variables = {}
        self.variableInitialization = False
        self.loopState = False
        self.functions = {}
        self.funcName = ""
        self.functionInitialization = False

        for token in content:
            if self.loopState:
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
        if not self.skipCodeblock:
            if self.functionInitialization:
                self.functions[self.funcName] = codeblock
                self.funcName = ""
                self.functionInitialization = False

            else:
                for token in codeblock["codeblock"]:
                    if "codeblock" in token:
                        self.codeblockExecuter(token)
                
                    elif "identifier" in token:
                        self.keywordDefinition(token)
                
                    else:
                        self.nonKeywordDefinitions(token)
                    #print(token, self.programStack._stack, sep="\n")

        else:
            self.skipCodeblock = False

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
                if type(a) == type(int()):
                    if type(b) == type(int()):
                        self.programStack.push(a+b)
                    
                    else:
                        self.error.typeMismatch("sum", str(type(b)), ("int", "int"))
                
                else:
                    self.error.typeMismatch("sum", str(type(a)), ("int", "int"))


            case "mul":
                a = self.programStack.pop()
                b = self.programStack.pop()
                if type(a) == type(int()):
                    if type(b) == type(int()):
                        self.programStack.push(a*b)
                    
                    else:
                        self.error.typeMismatch("mul", str(type(b)), ("int", "int"))
                
                else:
                    self.error.typeMismatch("mul", str(type(a)), ("int", "int"))


            case "sub":
                a = self.programStack.pop()
                b = self.programStack.pop()
                if type(a) == type(int()):
                    if type(b) == type(int()):
                        self.programStack.push(b-1)
                    
                    else:
                        self.error.typeMismatch("sub", str(type(b)), ("int", "int"))
                
                else:
                    self.error.typeMismatch("sub", str(type(a)), ("int", "int"))


            case "div":
                a = self.programStack.pop()
                b = self.programStack.pop()
                if type(a) == type(int()):
                    if type(b) == type(int()):
                        self.programStack.push(b/a)
                    
                    else:
                        self.error.typeMismatch("div", str(type(b)), ("int", "int"))
                
                else:
                    self.error.typeMismatch("div", str(type(a)), ("int", "int"))


            case "display":
                a = self.programStack.peek()
                print(a)

            case "greater":
                a = self.programStack.pop()
                b = self.programStack.pop()
                if type(a) == type(int()):
                    if type(b) == type(int()):
                        if b > a:
                            self.programStack.push(1)
                        else: 
                            self.programStack.push(0)
                    
                    else:
                        self.error.typeMismatch("greater", str(type(b)), ("int", "int"))
                
                else:
                    self.error.typeMismatch("greater", str(type(a)), ("int", "int"))


            case "lesser":
                a = self.programStack.pop()
                b = self.programStack.pop()
                if type(a) == type(int()):
                    if type(b) == type(int()):
                        if b < a:
                            self.programStack.push(1)
                        else: 
                            self.programStack.push(0)
                    
                    else:
                        self.error.typeMismatch("greater", str(type(b)), ("int", "int"))
                
                else:
                    self.error.typeMismatch("greater", str(type(a)), ("int", "int"))


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
                else:
                    self.error.typeMismatch("if", str(type(self.programStack.peek())), ("soft bool \"1 or 0\""))


            case "throw":
                if self.programStack._stack.__len__ == 0:
                    self.error.notEnoughArgumentsInStack("throw", 1)
                else:
                    self.programStack.pop()


            case "not":
                a = self.programStack.pop()
                if a == 1:
                    self.programStack.push(0)
                elif a == 0:
                    self.programStack.push(1)
                else:
                    self.error.typeMismatch("not", str(type(self.programStack.peek())), ("soft bool \"1 or 0\""))


            case "and":
                a = self.programStack.pop()
                b = self.programStack.pop()
                if a == 1 or a == 0:
                    if b == 1 or b == 0:
                        result = a and b
                        self.programStack.push(result)
                    else:
                        self.error.typeMismatch("and", type(b), ("soft bool \"1 or 0\""))
                else:
                    self.error.typeMismatch("and", type(a), ("soft bool \"1 or 0\""))


            case "or":
                a = self.programStack.pop()
                b = self.programStack.pop()
                if a == 1 or a == 0:
                    if b == 1 or b == 0:
                        result = a or b
                        self.programStack.push(result)
                    else:
                        self.error.typeMismatch("or", type(b), ("soft bool \"1 or 0\""))
                else:
                    self.error.typeMismatch("or", type(a), ("soft bool \"1 or 0\""))


            case "var":
                self.variableInitialization = True


            case "loop":
                self.loopState = True


            case "quit":
                self.loopState = False


            case "func":
                self.functionInitialization = True


            case _:
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
                    
                else:
                    self.error.unexpectedIdentifier(token["identifier"])
