def remove_triple_backticks(s: str) -> str:
    lines = s.splitlines()
    if lines:
        if lines[0].strip() == "```json":
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
    return "\n".join(lines)


f = open("./meals.json", 'r')
str = f.read()
f.close()

str = remove_triple_backticks(str) 

with open("./meals.json", 'w') as f:
    f.write(str)





