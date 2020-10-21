#部署
1. excute command "scrapyd-deploy" (依據scrapy.cfg中的設定的scrapyd server url，將專案部署到指定的scrapyd server)
2. curl http://localhost:6800/schedule.json -d project=article_scrapy -d spider=articleSpider (要求scrapd server執行article_scrapy專案的articleSpider爬蟲)
3. curl http://localhost:6800/cancel.json -d project=article_scrapy -d job=6487ec79947edab326d6db28a2d86511e8247444 (停止執行article_scrapy專案job_id=6487ec79947edab326d6db28a2d86511e8247444的任務)


#scrapyd api 參考

#列出所有工程
scrapyd-client -t http://10.11.2.102:6800 projects
或
curl http://10.11.2.102:6800/listprojects.json
{"status": "ok", "projects": ["default", "douban"], "node_name": "yanggd-QiTianM4650-D089"}
#查看爬蟲
curl http://10.11.2.102:6800/listspiders.json?project=douban
{"status": "ok", "spiders": ["douban_login", "fanghua", "langyabang", "movieTop250", "movieTop250_crawlspider", "movieTop250_login_crawlspider", "tongcheng_pipeline"], "node_name": "yanggd-QiTianM4650-D089"}
#列出版本
curl http://10.11.2.102:6800/listversions.json?project=douban
{"status": "ok", "versions": ["1516115564", "1516199516", "1516265513", "v1"], "node_name": "yanggd-QiTianM4650-D089"}
#刪除版本
curl http://10.11.2.102:6800/delversion.json -d "project=douban&version=1516115564"
{"status": "ok", "node_name": "yanggd-QiTianM4650-D089"}
#調度執行爬蟲
curl http://10.11.2.102:6800/schedule.json -d "project=douban&spider=tongcheng_pipeline&jobid=tongcheng_pipeline"
{"status": "ok", "jobid": "tongcheng_pipeline", "node_name": "yanggd-QiTianM4650-D089"}
#查看爬蟲的執行狀態
curl http://10.11.2.102:6800/listjobs.json?project=douban|| python -m json.tool
{"status": "ok", "running": [{"start_time": "2018-01-22 19:45:14.376731", "pid": 28067, "id": "tongcheng_pipeline", "spider": "tongcheng_pipeline"}], "finished": [], "pending": [], "node_name": "yanggd-QiTianM4650-D089"}
#停止爬蟲
curl http://10.11.2.102:6800/cancel.json -d "project=douban&job=tongcheng_pipeline"
{"status": "ok", "prevstate": null, "node_name": "yanggd-QiTianM4650-D089"}


#環境安裝與導出

pip3 instal pipreqs

生成requirements.txt文件
pipreqs ./

安裝、requirements.txt依賴
pip install -r requirements.txt


#利用scrapydweb做管理
pip3 instal scrapydweb


# redis login

* rdcli -h 127.0.0.1 -p 6379 -a 'mypassword'

# hash
```
del keys 刪除keys
Hgetall keys 取得hash格式中的 keys 所有資料
```