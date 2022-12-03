from bs4 import BeautifulSoup
import requests
import re

URL = "https://finance.yahoo.com/quote/"
HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})


def getStockSoup(stock):
    print("Sending request...")
    request = requests.get(URL + stock, headers = HEADERS)
    print("Sent!")
    content = request.content
    stockSoup = BeautifulSoup(content, "html.parser")
    return stockSoup


def getStockTitle(title):
    title = title.text
    stockTitle = re.search(r"^(.+)\.(.+)$", title)
    name, symbol = stockTitle.groups()
    symbol = re.sub("[()]", "", symbol)
    return name, symbol.strip()


def getStockGeneralInfo(tableRows):
    infoKeys = []
    infoValues = []

    for row in tableRows:
        infoKeys.append(row.find("td", class_ = "C($primaryColor) W(51%)").text)
        infoValues.append(row.find("td", class_ = "Ta(end) Fw(600) Lh(14px)").text)
    return infoKeys, infoValues


def getStockInfo(soup):
    stockInfo = {}

    title = soup.find("h1", class_ = "D(ib) Fz(18px)")
    price = soup.find("fin-streamer", class_ = "Fw(b) Fz(36px) Mb(-4px) D(ib)")
    tableRows = soup.find_all("tr", class_ = "Bxz(bb) Bdbw(1px) Bdbs(s) Bdc($seperatorColor) H(36px)")
    
    if title and price and tableRows:
        name, symbol = getStockTitle(title)
        stockInfo["stockName"] = name
        stockInfo["stockSymbol"] = symbol
        stockInfo["stockPrice"] = price.text

        infoKeys, infoValues = getStockGeneralInfo(tableRows)

        for key, value in zip(infoKeys, infoValues):
            stockInfo[key] = value
        return stockInfo
    return {}


def main():
    soup = getStockSoup(input("Stock: "))
    getStockInfo(soup)


if __name__ == "__main__":
    main()
