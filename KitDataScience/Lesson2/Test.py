
words = ["xerd", "erdst", "godje"]
list_x = []
list_others = []
for s in words:
    if s[0] == "x":
        list_x.append(s)
    else:
        list_others.append(s)

s1 = sorted(list_x.sort)
s2 = sorted(list_others)

# result = s1 + s2
print(s1, s2)
