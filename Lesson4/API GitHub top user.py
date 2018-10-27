import requests
from bs4 import BeautifulSoup
from threading import Thread
import time
import pandas as pd


token = ""
headers = {'Authorization': 'token {}'.format(token)}

t1 = time.time()

def find_top_users():
    url = "https://gist.github.com/paulmillr/2657075"
    request_result = requests.get(url)
    if request_result.status_code == 200:
        html_doc = request_result.text
        soup = BeautifulSoup(html_doc, "html.parser")
        list_users = []
    else:
        print("Status Code Error")
    for i in range(256):
        names = soup.find_all("th", scope="row")[i].findNext("td").text.split()[0]
        list_users.append(names)
    return list_users


def find_repos(url):
    req = requests.get(url, headers=headers)
    list_repo = [(elmt["name"], elmt["stargazers_count"]) for elmt in req.json()]
    return list_repo


def find_all_repos(user):
    list_all_repo = []
    url = f"https://api.github.com/users/{user}/repos?per_page=100&page=1"
    req = requests.get(url, headers=headers)
    i = 1
    while (req.json() != []):
        list_all_repo += find_repos(url)
        i += 1
        url = f"https://api.github.com/users/{user}/repos?per_page=100&page={i}"
        req = requests.get(url, headers=headers)
    return list_all_repo


result = {}

for user in find_top_users():
    df = pd.DataFrame(find_all_repos(user), columns=["Name_repo", "Stars_number"])
    result[user] = round(df["Stars_number"].mean(), 1)

df2 = pd.DataFrame.from_dict(result, orient='index', columns=["Stars_mean"])

df2.sort_values("Stars_mean", inplace=True, ascending=False)

print(df2)
t2 = time.time()
print(t2-t1)
