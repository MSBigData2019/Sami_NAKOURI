import re

s = "01- Ain"

reg = r"(/W+)"

reg2 = r"[^a-zA-Z]+"

s2 = re.sub(reg2, "", s)
print(s2)