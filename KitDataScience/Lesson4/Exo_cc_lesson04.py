import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


url = "https://www.open-medicaments.fr/api/v1/medicaments?query=paracetamol"
req = requests.get(url)
df = pd.read_json(req.content)
serie = df["denomination"]
reg = r'([\D]*)(\d+)(.*),(.*)'
ds = serie.str.extract(reg)
ds["mult"] = 1000
ds["mult"] = ds["mult"].where(ds[2].str.strip() == "g", 1)
ds["dosage"] = ds["mult"] * ds[1].fillna(0).astype(int)

list_cp = []
reg3 = r"\d+"

for code in df["codeCIS"]:
    url_i = f"https://www.open-medicaments.fr/api/v1/medicaments/{code}"
    req_i = requests.get(url_i)
    jason = req_i.json()
    cp_number = re.findall(reg3, jason["presentations"][0]["libelle"])[-1]
    list_cp.append(cp_number)

ds["gelule"] = pd.DataFrame(list_cp)
#ds["gelule"].astype(int)
ds["dosage_total"] = ds["dosage"] * ds["gelule"].astype(int)

print(ds.head())








