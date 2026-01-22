import re
print

class Lexer:
    def __init__(self):
        self.splitChars = ["{","}", "\""]

    def split(self, content: str):
        commentState = False
        stringState = False

        tokenList = []
        currentToken = ""
        for char in content:
            if commentState and char == "\n": #escape comment
                commentState = False

            elif commentState: # skip comments
                continue
            
            elif stringState and char != "\"": 
                currentToken += char

            elif (char == " " or char == "\n" or char == "\t"): #split on empty space or newline. also append the last token formed
                if currentToken:
                    tokenList.append(currentToken)
                    currentToken = ""

            elif char == "?": #start comments
                commentState = True
                if currentToken:
                    tokenList.append(currentToken)

            elif char == "\"":
                stringState = not stringState
                if not stringState:
                    tokenList.append("\""+currentToken+"\"")
                    currentToken = ""
            
            elif char == "{" or char == "}":
                if currentToken:
                    tokenList.append(currentToken)
                    currentToken = ""
                
                tokenList.append(char)

            else:
                currentToken += char

        if currentToken:
            tokenList.append(currentToken)

        return tokenList
    

    def postprocessing(self, splitContent: list):
        refinedList = []
        codeblocks = []

        currentToken = {}
        self.codeBlock = []
        for token in splitContent:
            if token.isdigit():
                currentToken = {"int": token}
                
            elif re.match(r"\".*\"", token):
                currentToken = {"str": token}
                
            elif token.isalpha():
                currentToken = {"identifier": token}
                
            elif token in ["{", "}"]:
                if token == "{":
                    codeblocks.append([])
                else:
                    if len(codeblocks) != 1:
                        block = {"codeblock": codeblocks.pop()}
                        codeblocks[-1].append(block)
                    else:
                        block = {"codeblock": codeblocks.pop()}
                        refinedList.append(block)
                
            else:
                print("illegal value encountered!")
                currentToken = {"illegal value": "null"}


            if currentToken:
                if codeblocks:
                    codeblocks[-1].append(currentToken)
                    currentToken = {}
                else:
                    refinedList.append(currentToken)
                    currentToken = {}
        
        return refinedList

    def lex(self, content: str):
        splitContent = self.split(content)
        pp = self.postprocessing(splitContent)
        return pp
