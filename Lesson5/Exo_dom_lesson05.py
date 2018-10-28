import requests
from bs4 import BeautifulSoup
from math import ceil
import pandas as pd
from selenium import webdriver
import re


def build_soup(url):
    request_result = requests.get(url)
    if request_result.status_code == 200:
        text = request_result.text
        #text = request_result.text.encode('ascii').encode('utf-8', 'ignore')
        html_doc = text
        soup = BeautifulSoup(html_doc, "html.parser")
    else:
        print("request code error")
    return soup


def find_number_pages(soup):
    number_add = soup.find("span", attrs={'class': "numAnn"}).text.strip()
    number_pages = ceil(int(number_add) / 16)
    return number_pages


def url_list_for_all_cars(soup):
    all_urls1 = list(map(lambda x: "https://www.lacentrale.fr" + x.attrs['href'], soup.find_all("a", class_="linkAd ann")))
    all_urls2 = list(map(lambda x: "https://www.lacentrale.fr" + x.attrs['href'], soup.find_all("a", class_="linkAd annJB")))
    all_urls = all_urls1 + all_urls2
    return all_urls


def all_data_car(url_list):
    data_cars = {}
    for url_car in url_list:
        soup = build_soup(url_car)
        version = soup.find("span", attrs={'class': "noBold"}).text.strip()
        year = soup.find("ul", attrs={'class': "infoGeneraleTxt column2"}).findNext("span").text
        km = soup.find("ul", attrs={'class': "infoGeneraleTxt column2"}).findNext("span").findNext("span").text
        seller = soup.find("div", attrs={'class': "bold italic mB10"}).text.strip().split(" ")[0]
        price = soup.find("strong", attrs={'class': "sizeD lH35 inlineBlock vMiddle "}).text.strip()
        data_cars[url_car] = [version, year, km, seller, price]
    return data_cars



dic_result = {}
url  = "https://www.lacentrale.fr/listing?makesModelsCommercialNames=RENAULT%3AZOE%3A&options=&regions=FR-IDF%2CFR-NAQ%2CFR-PAC"
soup = build_soup(url)
number_pages = find_number_pages(soup)
list_url_cars = url_list_for_all_cars(soup)
dic_result = all_data_car(list_url_cars)
#for page in range(1, number_pages + 1):
page = 1
url_page = f"https://www.lacentrale.fr/listing?makesModelsCommercialNames=RENAULT%3AZOE%3A&options=&page={page}&regions=FR-IDF%2CFR-NAQ%2CFR-PAC"
soup = build_soup(url_page)
list_url_cars = url_list_for_all_cars(soup)
dic_result.update( all_data_car(list_url_cars))

df = pd.DataFrame(dic_result).T
df.columns = ["Version", "Year", "KM", "Seller", "price"]
df.reset_index(drop=True, inplace=True)

#df["version"].str.replace("-", "", inplace=True)
print(df.describe())
print(df)

