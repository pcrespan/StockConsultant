from bs4 import BeautifulSoup
import requests


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


def getStockInfo(soup):
    stockInfo = {}

    allInfo = soup.find_all("td", class_ = "Ta(end) Fw(600) Lh(14px)")

    for info in allInfo: 
        print(info.text)


def main():
    soup = getStockSoup(input("Stock: "))
    print(getStockInfo(soup))


if __name__ == "__main__":
    main()



