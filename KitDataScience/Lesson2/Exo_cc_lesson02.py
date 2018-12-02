import requests
from bs4 import BeautifulSoup


def single_promo(url):
    promos = []
    request_result = requests.get(url)
    soup = BeautifulSoup(request_result.text,'html.parser')
    req = soup.find_all('p', class_='darty_prix_barre_remise darty_small separator_top')
    promos += [float(request.text[2:-1]) for request in req]
    return sum(promos)/len(promos)

def all_promos(marques):
    page = ""
    for m in marques :
            marque = m
            url = f'https://www.darty.com/nav/achat/informatique/ordinateur_portable/portable/marque_{page}_{marque}__{marque.upper()}.html'
            print('Moyenne des soldes de ' + marque + ' : ' + str(single_promo(url)))

pc = ['hp', 'dell']
all_promos(pc)

