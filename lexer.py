class Lexer:
    def __init__(self):
        self.splitChars = ["{","}"]
    
    def lex(self, content: str):
        commentState = False

        tokenList = []
        currentToken = ""
        for char in content:
            if commentState and char == "\n":
                commentState = False
            
            elif commentState:
                continue

            elif (char == " " or char == "\n") and currentToken:
                tokenList.append(currentToken)
                currentToken = ""
            
            elif char == "?":
                commentState = True
                if currentToken:
                    tokenList.append(currentToken)

            elif char in self.splitChars:
                if currentToken:
                    tokenList.append(currentToken)
                    currentToken = ""
                
                tokenList.append(char)
            
            else:
                currentToken += char
        
        if currentToken:
            tokenList.append(currentToken)
        
        return tokenList