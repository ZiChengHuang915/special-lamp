from urllib import request
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

page_url = "https://whattomine.com/gpus"
req = Request(page_url, headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req)
page_soup = BeautifulSoup(webpage.read(), "html.parser")
webpage.close()

entries = page_soup.findAll("tr")

headers = "Name,Revenue 24H\n"
f = open("test.csv", "w")
f.write(headers)


for index in range(1, len(entries)):
    name_container = entries[index].find("a")
    name = name_container.text.strip().splitlines()[2].strip()
    print(name)

    revenue_24h = entries[index].find("td", {"class":"text-right table-"}).text.strip()
    print(revenue_24h)

    f.write(name + ", " + revenue_24h + "\n")

f.close()

