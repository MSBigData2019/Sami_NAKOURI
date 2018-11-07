
filename = "/Users/Nakouri/Desktop/test.txt"
#lines = [line.rstrip('\n') for line in open(filename)]



dict_word = {}
with open(filename, 'r') as text:
    for line in text:
        for word in line.lower().split():
            if word not in dict_word.keys():
                dict_word[word] = 1
            else:
                dict_word[word] += 1

    for key in sorted(dict_word):
        print("%s: %s" % (key, dict_word[key]))
    #print(dict_word)

"""
lines = [line.strip() for line in open(filename)]
print(lines.split())
dict_word = {}



for word in lines:
        dict_word[word] += 1
        print(word)



print(lines)
"""