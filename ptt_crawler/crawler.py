import urllib.request as req
import bs4

host="https://www.ptt.cc"
urlPage="https://www.ptt.cc/bbs/Gossiping/index.html"

def getData(url):
    request = req.Request(url,headers={
        "cookie":"over18=1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"
    }) 
    with req.urlopen(request) as response:
        data=response.read().decode("utf-8")

    root=bs4.BeautifulSoup(data,"html.parser")

    titles=root.find_all("div",class_="title")

    for title in titles :
        if title.a !=None:
            print(title.a.string)

    nextLink=root.find("a",string="‹ 上頁")
    return nextLink["href"]

 
for i in range(10):
    if i==0:
        urlPage=host+ "/bbs/Gossiping/index.html"   
    
    url=getData(urlPage)
    urlPage=host+url


 
