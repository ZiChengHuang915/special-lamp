from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

class GPU:
    def __init__(self, name, revenue_24h, link):
        self.name = name
        self.revenue_24h = revenue_24h
        self.link = link
        self.kijiji_entries = []
        
class kijiji_entry:
    def __init__(self, name, price):
        self.name = name
        self.price = price
        
GPUS = []
kijiji_entries = []

page_url = "https://whattomine.com/gpus"
req = Request(page_url, headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req)
page_soup = BeautifulSoup(webpage.read(), "html.parser")
webpage.close()

whattomine_entires = page_soup.findAll("tr")

headers = "Name,Revenue 24H\n"
f = open("test.csv", "w")
f.write(headers)


for index in range(1, len(whattomine_entires)):
    name_container = whattomine_entires[index].find("a")
    name = name_container.text.strip().splitlines()[2].strip()
    #print(name)
    

    revenue_24h = whattomine_entires[index].find("td", {"class":"text-right table-"}).text.strip()
    #print(revenue_24h)

    temp_name = name.replace(" ", "-")
    link = "https://www.kijiji.ca/b-gta-greater-toronto-area/" + temp_name + "/k0l1700272?rb=true&dc=true"

    GPUS.append(GPU(name, revenue_24h, link));
    f.write(name + ", " + revenue_24h + "\n")

f.close()

page_url = GPUS[0].link
req = Request(page_url, headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req)
page_soup = BeautifulSoup(webpage.read(), "html.parser")
webpage.close()

names = page_soup.findAll("a", {"class":"title"})
prices = page_soup.findAll("div", {"class":"price"})

for index in range(0, len(names)):
    if ("Please Contact" not in prices[index].text.strip() and 
        "Free" not in prices[index].text.strip() and
        "Swap/Trade" not in prices[index].text.strip()):
        kijiji_entries.append(kijiji_entry(names[index], prices[index]))
        print(names[index].text.strip() + "\n" + prices[index].text.strip())
        
    
    
    