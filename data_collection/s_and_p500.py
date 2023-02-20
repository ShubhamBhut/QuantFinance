import bs4 as bs
import requests

html = requests.get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")

soup = bs.BeautifulSoup(html.text)

table = soup.find("table", {"class": "wikitable sortable"})

tickers = []
rows = table.findAll("tr")[1:]

for row in rows:
    ticker = row.findAll("td")[0].text
    tickers.append(ticker[:-1])

print(tickers)
print(len(tickers))

# With tickers we can query in yfinance and get desired data
# However we also can webscrap barchart.com to get values as well as ticker, since it's not urgent, it's future plan
