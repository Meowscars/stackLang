import lexer

with open("script.sl") as f:
    content = f.read()

le = lexer.Lexer()
split = le.split(content)
print(split)

codeblocks = []
tokenList = []
for token in split:
    if token == "{":
        codeblocks.append([])
    
    elif token == "}":
        if len(codeblocks) != 1:
            block = {"codeblock": codeblocks.pop()}
            codeblocks[-1].append(block)
        else:
            tokenList.append({"codeblock": codeblocks[0]})
            codeblocks = []
    
    else:
        if codeblocks:
            codeblocks[-1].append({"statement": token})
        
        else:
            tokenList.append({"statement": token})

print(tokenList)