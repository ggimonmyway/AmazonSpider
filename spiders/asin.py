# -*- coding: utf-8 -*-
import scrapy
import pydispatch
from scrapy import signals
from AmazonCrapy.mysqlpipelines.pipelines import Sql
from datetime import datetime
from AmazonCrapy.items import AsinBestItem

class AsinSpider(scrapy.Spider):
    name = 'asin'
    custom_settings = {
        'LOG_LEVEL': 'ERROR',
        'LOG_ENABLED': True,
        'LOG_STDOUT': True
    }
    def __init__(self):
        scrapy.Spider.__init__(self)
        pydispatch.dispatcher.connect(self.handle_spider_closed, signals.spider_closed)
        # all asin scrapied will store in the array
        self.asin_pool = []
    def handle_spider_closed(self, spider):
        Sql.store_best_asin()
        work_time = datetime.now()
        print('total spent:', work_time)
        print('done')
    def start_requests(self):
        cates = Sql.findall_cate_level1()
        for row in cates:
            row['link'] += '?ajax=1'
            print("开始请求url"+row['link']+'&pg=1')
            yield scrapy.Request(url=row['link']+'&pg=1', callback=self.parse, meta={'cid': row['id'], 'page': 1, 'link': row['link']})
            break

    def parse(self, response):
        list = response.css('.zg-item-immersion')
        # scrapy next page  go go go !
        response.meta['page'] = response.meta['page'] + 1
        print("开始解析"+str(response.meta['page']))
        if response.meta['page'] < 100:
            print("开始请求url"+response.meta['link'] + '&pg=' + str(response.meta['page']))
            yield scrapy.Request(url=response.meta['link'] + '&pg=' + str(response.meta['page']), callback=self.parse,
                                 meta=response.meta)
        for row in list:
            try:
                # print("Fuck")
                # print(row)
                # star=row.xpath('//*[@class="a-icon-alt"]').extract()
                # print(star)
                star=row.css('.a-icon-alt::text').extract()[0]
                name=row.css('[aria-hidden]::text').extract()[0]
                sellnum=row.css('.a-size-small::text').extract()[0]
                tmpprice=row.css('.p13n-sc-price::text').extract()
                price=tmpprice[0]+"-"+tmpprice[1]
                imgurl=row.css('[alt]::attr(src)').extract()[0]
                # print(imgurl)
            except Exception as e:
                continue
                pass
            item=AsinBestItem()
            item['name'] = name.replace("\n","")
            item['star']=star
            item['sellnum'] = sellnum
            item['price'] = price
            item['imgurl'] = imgurl
            print("获取完成")
            # print(item)
            yield item


        # filename = "test2.html"
        # with open(filename, "wb")as f:
        #     f.write(response.body)
