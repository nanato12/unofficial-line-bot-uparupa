from parsers import FlexParser

parser = FlexParser()

data = parser.target_str.split("/")

result = []
for d in data:
    if not d:
        continue
    elif d.isdecimal():
        result.append(f"[{d}]")
    else:
        result.append(f"['{d}']")

print("content" + "".join(result))
