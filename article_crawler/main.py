import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import pymongo
from datetime import datetime 

# 財訊網站
# https://www.wealth.com.tw/


targetHome="https://www.wealth.com.tw"
initNum=0
sartTime=datetime.now()

def getHomeCategory(targetHome):
    
    try:
        kv={'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'}
        response = requests.get(targetHome,params=kv,timeout=30)
        response.raise_for_status()
        
        soup=BeautifulSoup(response.text,"html.parser")
        links = soup.find_all('a',href=re.compile("^\/home\/articles\?category\_id\="),tabindex="-1")
        hrefs=[]
        
        for link in links:
            hrefs.append(targetHome+link["href"])
            
           
        series_data=pd.Series(hrefs)  
        series_data=series_data.drop_duplicates()  # 刪除重複
        
        return series_data.to_list()

    except Exception as e:       
        print("err: fail to get Home Category url")
        print(e)

#https://www.wealth.com.tw/home/articles?category_id=1
def getArticleLitFromCategoryPage(targetHome,categoryPageUrl):
    
    try:
        kv={'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'}
        response = requests.get(categoryPageUrl,params=kv,timeout=30)
        response.raise_for_status()
        
        soup=BeautifulSoup(response.text,"html.parser")

        links = soup.find_all('article')
        articleLinks=[]
        for link in links:
            articleLinks.append(targetHome+link.a["href"])


        #下一頁
        nextPage=soup.find('a',rel="next")
        nextPageLink=None
        if nextPage!=None:
            nextPageLink=targetHome+nextPage["href"]   
        #上一頁
        prevPage=soup.find('a',rel="prev")    
        prevPageLink=None
        if prevPage!=None:
            prevPageLink=targetHome+prevPage["href"]


        return {
            "articleLinks":articleLinks,
            "nextPageLink":nextPageLink,
            "prevPageLink":prevPageLink,
        }     

    except Exception as e:       
        print("err: fail to get Category Page url")
        print(e)

    
        
def getArticleFromWeb(client,articleUrl): 
    
    try:
        kv={'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'}
        response = requests.get(articleUrl,params=kv,timeout=30)
        response.raise_for_status()
        
        soup=BeautifulSoup(response.text,"html.parser")

        titleDiv = soup.find('div',class_="entry-header")

        content = soup.find("meta", property="og:description")   

        dateAndAuthor = titleDiv.find("p")

        matchDate = re.search(r'([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))',dateAndAuthor.text)

        index = dateAndAuthor.text.find(":")
        author= dateAndAuthor.text[index+1:].strip()

        return {
            "url":articleUrl,
            "title":titleDiv.h1.text,
            "author":author,
            "publishDate":matchDate.group(1),
            "content":content["content"],
        }

    except Exception as e:       
        print("err: fail to get article Page url")
        print(e)
        saveFailLog(client,{"url":articleUrl})


def saveFailLog(client,log): 
    db = client['my_test_data']
    # 连接集合user，集合类似关系数据库的数据表
    # 如果集合不存在，会新建集合user
    fail_logs_collection = db["fail_logs"]

    # 使用insert_one单条添加文档，inserted_id获取写入后id
    # 添加文档时，如果文档尚未包含"_id"键，则会自动添加"_id"。 "_id"的值在集合中必须是唯一。
    # inserted_id是获取添加后的id，若不需要可去掉。
    fail_logs_collection.insert_one(log)
    print ("log is :", log)

def saveArticle(client,article):
    
    try:
        # 连接DB数据库
        db = client['my_test_data']
        # 连接集合user，集合类似关系数据库的数据表
        # 如果集合不存在，会新建集合user
        article_collection = db["articles"]
        article["_id"]=article["url"]

        # 使用insert_one单条添加文档，inserted_id获取写入后id
        # 添加文档时，如果文档尚未包含"_id"键，则会自动添加"_id"。 "_id"的值在集合中必须是唯一。
        # inserted_id是获取添加后的id，若不需要可去掉。
        article_collection.insert_one(article)
        print ("article is ", article)
    except Exception as e:       
        print("err: fail to get article Page url : ")
        print(e)
        

def getMyDbClient():
    # 创建对象
    client = pymongo.MongoClient('mongodb://admin:1qaz@localhost:27017/')
    return client

def getArticleInDb(client,url):

    # 连接DB数据库
    db = client['my_test_data']
    # 连接集合user，集合类似关系数据库的数据表
    # 如果集合不存在，会新建集合user
    article_collection = db["articles"]
    return article_collection.find_one({'_id':url})
   

def handleArticleInCategoryPage(client,targetHome,articleLinks):
    
    for articleLink in articleLinks :
        #檢查db url 是否有資料，沒資料在抓取
        global initNum
        global sartTime
        initNum=initNum+1
        dbData=getArticleInDb(client,articleLink)
        if dbData==None:
            article=getArticleFromWeb(client,articleLink)
            saveArticle(client,article)
            print("("+str(initNum)+")had handled : "+articleLink+" [ "+sartTime.strftime("%H:%M:%S")+" ~ "+datetime.now().strftime("%H:%M:%S")+" ]")
        else:
            print("("+str(initNum)+")not handle : "+articleLink+" [ "+sartTime.strftime("%H:%M:%S")+" ~ "+datetime.now().strftime("%H:%M:%S")+" ]")    

def main():
    categorylinks=getHomeCategory(targetHome)
    client=getMyDbClient()

    for categoryStartPage in categorylinks: #取得所有分類文章入口
        print("Current category page : "+categoryStartPage)
        firstArticelInCategoryPage=getArticleLitFromCategoryPage(targetHome,categoryStartPage)

        hasNextPage=True
        currentPage=categoryStartPage
        articleLinks=firstArticelInCategoryPage["articleLinks"]
        while hasNextPage:
            #處理當前頁面
            handleArticleInCategoryPage(client,targetHome,articleLinks)

            #檢查是否有下一頁的資料
            result=getArticleLitFromCategoryPage(targetHome,currentPage)
            if result["nextPageLink"]==None:
                hasNextPage=False
            else:
                currentPage=result["nextPageLink"]
                articleLinks=result["articleLinks"]




main()