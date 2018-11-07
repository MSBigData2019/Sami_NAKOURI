import re

text = " ashjdjzbdzj Popularity in 1990"
year_match = re.search(r'Popularity\sin\s(\d\d\d\d)', text)

print(year_match)
