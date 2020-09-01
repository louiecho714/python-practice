import requests
from bs4 import BeautifulSoup
import bs4



def getHTMLText(url):
    try:
        kv={'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'}
        r = requests.get(url,params=kv,timeout=30)
        r.raise_for_status()
        r.encoding=r.apparent_encoding
        
        return r.text
    except:
        return ""

def fillUnivList(ulist,html):
    soup=BeautifulSoup(html,"html.parser")
    
    for tr in soup.find("tbody").children:
        if isinstance(tr,bs4.element.Tag):
            tds=tr('td')
            data={
                "ip":tds[0].string,
                "port":tds[1].string,
                "code":tds[2].string,
                "country":tds[3].string,
                "anonymity":tds[4].string,
                "google":tds[5].string,
                "https":tds[6].string,
                "lastChecked":tds[7].string,
            }

            freeProxyConfig=FreeProxyConfig(data)  
            ulist.append(freeProxyConfig)
            

class FreeProxyConfig:
    def __init__(self,config):
        self.ip=config["ip"]   
        self.port=config["port"]
        self.code=config["code"]
        self.country=config["country"]
        self.anonymity=config["anonymity"]
        self.google=config["google"]
        self.https=config["https"]
        self.lastChecked=config["lastChecked"]

    def __repr__(self):
        return str(self.__dict__)



sqlConnection="postgresql://username:password@ip:port/dbname"


free_proxy_url='https://www.us-proxy.org/'

text=getHTMLText(free_proxy_url)
list=[]
fillUnivList(list,text)
print("size :"+str(len(list)))
for data in list:
    print(data.__repr__())
