from time import sleep
import re
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
MAX_COLUMNS = 80 #kijiji has max 40 listings in one page

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

whattomine_url = "https://whattomine.com/gpus"
req = Request(whattomine_url, headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req)
page_soup = BeautifulSoup(webpage.read(), "html.parser")
webpage.close()

whattomine_entries = page_soup.findAll("tr")

headers = "Name,Revenue 24H"
for index in range(0, MAX_COLUMNS):
    headers = headers + "," + " "
headers = headers + "\n"
f = open("test.csv", "w")
f.write(headers)

print(len(whattomine_entries))
for index in range(1, len(whattomine_entries)):
    kijiji_entries = []
    
    name_container = whattomine_entries[index].find("a")
    gpu_name = name_container.text.strip().splitlines()[2].strip()
    #gpu_name = "geforce rtx 3070"
    #print(name)
    revenue_24h = whattomine_entries[index].find("td", {"class":"text-right table-"}).text.strip()
    #print(revenue_24h)

    temp_name = gpu_name.replace(" ", "-")
    link = "https://www.kijiji.ca/b-gta-greater-toronto-area/" + temp_name + "/k0l1700272?rb=true&dc=true"
    GPUS.append(GPU(gpu_name, revenue_24h, link));
    
    kijiji_url = GPUS[len(GPUS) - 1].link
    #kijiji_url = "https://www.kijiji.ca/b-gta-greater-toronto-area/geforce-rtx-3070/k0l1700272?rb=true&dc=true"
    print(kijiji_url)
    req = Request(kijiji_url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req)
    kijiji_page_soup = BeautifulSoup(webpage.read(), "html.parser")
    webpage.close()
    
    names = kijiji_page_soup.findAll("a", {"class":"title"})
    prices = kijiji_page_soup.findAll("div", {"class":"price"})
    print("has " + str(len(names)))
    for index in range(0, len(names)):
        if ("Please Contact" not in prices[index].text.strip() and 
            "Free" not in prices[index].text.strip() and
            "Swap / Trade" not in prices[index].text.strip()):
            if len(re.findall('\d+', gpu_name)) > 0:
                if re.findall('\d+', gpu_name)[0] in names[index].text.strip() or (len(re.findall('\d+', gpu_name)) > 1 and re.findall('\d+', gpu_name)[1] in names[index].text.strip()):
                    kijiji_entries.append(kijiji_entry(names[index].text.strip().replace("\n", "").replace(",", "").replace("\"", ""), prices[index].text.strip().replace("\n", "").replace(",", "").replace("$", "").replace(".00", "")))
                    #print(names[index].text.strip() + "\n" + prices[index].text.strip())
            else:
                kijiji_entries.append(kijiji_entry(names[index].text.strip().replace("\n", "").replace(",", "").replace("\"", ""), prices[index].text.strip().replace("\n", "").replace(",", "")))
                #print(names[index].text.strip() + "\n" + prices[index].text.strip())
                
    GPUS[len(GPUS) - 1].kijiji_entries = kijiji_entries
    print(len(kijiji_entries))
    write_string = gpu_name + ", " + revenue_24h
    for index in GPUS[len(GPUS) - 1].kijiji_entries:
        write_string = write_string + ", " + str(index.name).replace('\uff08', "").replace('\uff09', "") + ", " + str(index.price) # replace is for bad unicode
    for index in range(0, MAX_COLUMNS - len(GPUS[len(GPUS) - 1].kijiji_entries) * 2):
        write_string = write_string + ", " + " "
    write_string = write_string + "\n"
    print(write_string)
    f.write(write_string)
    sleep(5)

f.close()


        
    
    
    