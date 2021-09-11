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
    def __init__(self, gpu_name, gpu_revenue_24h, name, price, description, link):
        self.gpu_name = gpu_name
        self.gpu_revenue_24h = gpu_revenue_24h
        self.name = name
        self.price = price
        self.description = description
        self.link = link
        self.roi = float(price) / float(gpu_revenue_24h)

def getKijijiEntries(gpu_name_param):        
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
    
    index = -1
    for temp_index in range(1, len(whattomine_entries)):
        name_container = whattomine_entries[temp_index].find("a")
        gpu_name = name_container.text.strip().splitlines()[2].strip()
        if gpu_name == gpu_name_param:
            index = temp_index
            break
    
    print(len(whattomine_entries))

    kijiji_entries = []
    
    name_container = whattomine_entries[index].find("a")
    gpu_name = name_container.text.strip().splitlines()[2].strip()
    revenue_24h = float(whattomine_entries[index].find("td", {"class":"text-right table-"}).text.strip().replace("$", "").replace(".", "")) / 100

    temp_gpu_name = gpu_name.replace(" ", "-")
    link = "https://www.kijiji.ca/b-gta-greater-toronto-area/" + temp_gpu_name + "/k0l1700272?rb=true&dc=true"
    GPUS.append(GPU(gpu_name, revenue_24h, link));
    kijiji_url = GPUS[len(GPUS) - 1].link

    print(kijiji_url)
    req = Request(kijiji_url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req)
    kijiji_page_soup = BeautifulSoup(webpage.read(), "html.parser")
    webpage.close()
    
    names = kijiji_page_soup.findAll("a", {"class":"title"})
    prices = kijiji_page_soup.findAll("div", {"class":"price"})
    descriptions = kijiji_page_soup.findAll("div", {"class":"description"})
    print("has " + str(len(names)))
    for index in range(0, len(names)):
        temp_name = names[index].text.strip().replace("\n", "").replace(",", "").replace("\"", "")
        temp_price = prices[index].text.strip().replace("\n", "").replace(",", "").replace("$", "").replace(".00", "")
        temp_description = descriptions[index].text.strip().replace(",", "")
        temp_link = "https://www.kijiji.ca" + names[index]['href']
        if ("Please Contact" not in temp_price and 
            "Free" not in temp_price and
            "Swap / Trade" not in temp_price):
            if len(re.findall('\d+', gpu_name)) > 0:
                if re.findall('\d+', gpu_name)[0] in temp_name or (len(re.findall('\d+', gpu_name)) > 1 and re.findall('\d+', gpu_name)[1] in temp_name):
                    kijiji_entries.append(kijiji_entry(gpu_name, revenue_24h, temp_name, temp_price, temp_description, temp_link))
            else:
                kijiji_entries.append(kijiji_entry(gpu_name, revenue_24h, temp_name, temp_price, temp_description, temp_link))
                
    GPUS[len(GPUS) - 1].kijiji_entries = kijiji_entries
    print(len(kijiji_entries))
    write_string = gpu_name + ", " + str(revenue_24h)
    for index in GPUS[len(GPUS) - 1].kijiji_entries:
        write_string = write_string + ", " + str(index.name).replace('\uff08', "").replace('\uff09', "") + ", " + str(index.price) # replace is for bad unicode
    for index in range(0, MAX_COLUMNS - len(GPUS[len(GPUS) - 1].kijiji_entries) * 2):
        write_string = write_string + ", " + " "
    write_string = write_string + "\n"
    print(write_string)
    f.write(write_string)
    #sleep(3)
    
    f.write("\n")
    f.write("Link, Revenue 24H, Price, ROI, Title, Description\n")
    all_entries = []
    for gpu in GPUS:
        for entry in gpu.kijiji_entries:
            all_entries.append(entry)
            #write_string = entry.link + "," + str(entry.gpu_revenue_24h) + "," + entry.price + "," + str(entry.roi) + "," + entry.name.replace('\uff08', "").replace('\uff09', "")  + "\n"
            #f.write(write_string)
    
    all_entries.sort(key=lambda x: x.roi)
    temp_names, temp_prices, temp_descriptions = [], [], []
    for entry in all_entries:
        temp_names.append(entry.name)
        temp_prices.append(entry.price)
        temp_descriptions.append(entry.description)
        write_string = entry.link + "," + str(entry.gpu_revenue_24h) + "," + entry.price + "," + str(entry.roi) + "," + entry.name.replace('\uff08', "").replace('\uff09', "") + "," + entry.description.replace('\uff08', "").replace('\uff09', "").replace('\uff0c', ".").replace('\u202f', "") + "\n"
        f.write(write_string)
    
    f.close()
    
    return temp_names, temp_prices, temp_descriptions
 