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
