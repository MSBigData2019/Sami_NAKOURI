
import re

s ="11650€"


reg = r"\d+"
reg2 = r"^(\s+)"

b = re.sub("€", "", s)
#a = re.sub(reg2, s)
print(b)
