import scrapy
import time
import json

class BingwallpaperSpider(scrapy.Spider):
    name = 'BingWallpaper'
    allowed_domains = ['cn.bing.com']
    start_urls = ['https://www.bing.com/HPImageArchive.aspx?format=js&idx=1&n=71&nc={ts}&pid=hp'.format(ts=int(time.time()))]

    def parse(self, response):
        #self.logger.debug(response.body.decode('utf-8'))
        json_result=json.loads(response.body.decode('utf8'))
        images=json_result['images']
        if images is not None :
            for image in images :
                self.logger.debug(image['url'])