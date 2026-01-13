import re

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

            elif (char == " " or char == "\n"): #split on empty space or newline. also append the last token formed
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

            else:
                currentToken += char

        if currentToken:
            tokenList.append(currentToken)

        return tokenList
    
    def postprocessing(self, splitContent: list):
        refinedList = []

        for token in splitContent:
            if token.isdigit():
                refinedList.append({"int": token})
            
            elif re.match(r"\".*\"", token):
                refinedList.append({"str": token})
            
            elif token.isalpha:
                refinedList.append({"identifier": token})
            
            else:
                print("illegal value encountered!")
                refinedList.append({"illegal value": "null"})
        return refinedList

    def lex(self, content: str):
        splitContent = self.split(content)
        print(splitContent)
        return self.postprocessing(splitContent)