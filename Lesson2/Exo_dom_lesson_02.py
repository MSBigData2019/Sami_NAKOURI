import requests
from bs4 import BeautifulSoup


def build_soup(corpo):

    website_prefix = "https://www.reuters.com"
    url = website_prefix + "/finance/stocks/financial-highlights/" + corpo
    request_result = requests.get(url)
    if request_result.status_code == 200:
        html_doc = request_result.text
        soup = BeautifulSoup(html_doc, "html.parser")
    return soup


def find_data(soup, data_dic):

    specific_text = "Quarter Ending Dec-18"
    data_dic[specific_text] = soup.find_all("tr", attrs={'class': 'stripe'})[0].contents[5].text

    specific_text = "Share Price"
    data_dic[specific_text] = soup.find_all('span', attrs={'style': 'font-size: 23px;'})[0].string.strip()

    specific_text = "valueContentPercent"
    data_dic[specific_text] = soup.find_all("span", attrs={'class': specific_text})[0].text.strip()[1:-1]


    specific_text = "% Shares Owned:"
    data_dic[specific_text] = soup.find("td", text=specific_text).findNext("td").text

    specific_text = "Dividend Yield"

    data_dic[specific_text + " company"] = soup.find("td", text=specific_text).findNext("td").text
    data_dic[specific_text + " industry"] = soup.find("td", text=specific_text).findNext("td").findNext("td").text
    data_dic[specific_text + " sector"] = soup.find("td", text=specific_text).findNext("td").findNext("td").findNext("td").text

    return data_dic



corpo_list = ['LVMH.PA', 'AIR.PA', 'DANO.PA']
result_dic = {}

for corpo in corpo_list:
    data_dic = {}
    soup = build_soup(corpo)
    find_data(soup, data_dic)
    result_dic[corpo[:-3]] = data_dic

print(result_dic)

