# -*- coding: utf-8 -*-
import scrapy
from urllib import parse
from AmazonCrapy.items import AsinBestItem
from AmazonCrapy.items import TypeItem
import re
from  urllib import parse

class ListspiderSpider(scrapy.Spider):
    name = 'listspider'

    def __init__(self,*args, **kwargs):
        super(ListspiderSpider, self).__init__(*args, **kwargs)
        # self.start_urls = [parse.unquote(url)]

    def start_requests(self):
        types=["digital-tex","digital-music","instant-video","stripbooks-intl-ship","baby-products-intl-ship","arts-crafts-intl-ship","automotive-intl-ship","electronics-intl-ship","beauty-intl-ship","computers-intl-ship","fashion-womens-intl-ship","fashion-mens-intl-ship","fashion-girls-intl-ship","fashion-boys-intl-ship","hpc-intl-ship","pets-intl-ship","kitchen-intl-ship","industrial-intl-ship","tools-intl-ship","movies-tv-intl-ship","toys-and-games-intl-ship","luggage-intl-ship","videogames-intl-ship","software-intl-ship","sporting-intl-ship","deals-intl-ship","music-intl-ship"]
        urls = self.start_urls
        print(urls)
        for type in types:
            tmpurl="https://www.amazon.com/s?i="+type
            yield scrapy.Request(url=tmpurl, callback=self.parse_keyword)

        # turl="https://www.amazon.com/Cases-Storage-Accessories/s?rh=n%3A14218851&page=4"
        # yield scrapy.Request(url=turl, callback=self.parse_page,meta = {'allType' :"fuck"})


    def transferContent(self,content):
        if content is None:
            return None
        else:
            string = ""
            for c in content:
                if c == '"':
                    string += '\\\"'
                elif c == "'":
                    string += "\\\'"
                elif c == "\\":
                    string += "\\\\"
                else:
                    string += c
            return string
    #https://www.amazon.com/s?i=pets-intl-ship
     #关键字类别解析
    def Data_asinDeocede(self,response,allType):
        nowtype = response.css('.a-list-item').css('.a-text-bold::text').extract()[0]
        print(nowtype)
        list = response.css('[data-asin]')
        print(len(list))
        items=[]
        for row in list:
            try:
                asin=row.css('[data-asin]::attr(data-asin)').extract()[0]
                # print(asin)
                tmpstar = row.css('.a-icon-alt::text').extract()
                if len(tmpstar)>0:
                    star=tmpstar[0]
                else:
                    star="Empty"
                # print("star获取完成")
                tmpname = row.css('.a-spacing-top-small').css('.a-link-normal').css('.a-size-base-plus::text').extract()
                if len(tmpname)>0:
                    name=tmpname[0]
                else:
                    # print("找不到name")
                    tmpname2 = row.css('.a-spacing-mini').css('.a-link-normal').css(
                        '.a-size-base::text').extract()
                    # print(tmpname2)
                    if len(tmpname2)>0:
                        name = tmpname2[0]
                    else:
                        tmpname3 = row.css('.a-size-mini').css('.a-link-normal').css(
                            '.a-size-medium::text').extract()
                        if len(tmpname3)>0:
                            name = tmpname3[0]
                        else:
                            print("找不到name")
                            name = tmpname3[0]
                    # print(name)
                # print("name获取完成")

                tmpsellnum = row.css('.a-spacing-top-micro').css('.a-size-small').css('.a-size-base::text').extract()
                if len(tmpsellnum)>0:
                    sellnum=tmpsellnum[0]
                else:
                    # print("找不到sellnum")
                    row2=row.css('.a-row')
                    relrow=None
                    for tmprow in row2:
                        if len(tmprow.css('[name]'))>0:
                            relrow=tmprow
                            break
                    # print(relrow)
                    if relrow!=None:
                        tmpsellnum2 = relrow.css('.a-size-small::text').extract()
                        # print(tmpsellnum2)
                        sellnum=tmpsellnum2[0]
                        # print(sellnum)
                    else:
                        sellnum = "None Review"

                # print("sellnum获取完成")
                price="stockout"

                offscreen = row.css('.a-offscreen::text').extract()
                if len(offscreen)>0:
                    price=offscreen[0]
                # print("price获取完成")
                imgurl = row.css('[alt]::attr(src)').extract()[0]
                # print("imgurl获取完成")
            except Exception as e:
                print(e)
                continue
                pass
            item = AsinBestItem()

            item['asin'] = asin
            item['name'] = name
            item['star'] = star
            item['reviewNum'] = sellnum
            item['price'] = price
            item['imgurl'] = imgurl
            item['allType'] = allType
            print("获取完成:"+name)
            items.append(item)
        return items

    def parse_keyword(self,response):

        # print("获取到的内容为")
        # print(response.body)
        # filename = "test.html"
        # with open(filename, "wb")as f:
        #     f.write(response.body)
        try:
            # print(response.url)
            nowtype=response.css('.a-list-item').css('.a-text-bold::text').extract()[0]
            print(nowtype)
            pagnDisabled=response.css('.pagnDisabled::text').extract()[0]
            print("最大页数"+pagnDisabled)
            listitem = response.css('.a-unordered-list').css('.a-list-item')
            if pagnDisabled=="400":
                for tmp in listitem:
                    tmparr=tmp.css(".s-ref-text-link::attr(href)").extract()
                    tmptype=tmp.css(".s-ref-text-link").css(".a-size-small::text").extract()
                    # print(tmparr)
                    # print(tmptype)
                    if len(tmparr)>0:
                        for i in range(0,len(tmparr)):
                            if "www.amazon.com"in tmparr[i]:
                                tItem=TypeItem()
                                tItem['fatherType']=nowtype
                                tItem['fatherAllType'] = "_"+nowtype
                                tItem['sonType'] = tmptype[i]
                                yield tItem
                                print("开始访问"+tmparr[i])
                                yield scrapy.Request(tmparr[i], callback=self.parse_keyword2, meta = {'fathAllType' : tItem['fatherAllType']+"_"+tItem['sonType']})
                        #         break
                        # break
        except Exception as e:
            # items=self.Data_asinDeocede(response,"null")
            # for item in items:
            #     yield item
            pass



    #筛选二级目录
    def parse_keyword2(self, response):
        # print("获取到的内容为")
        # print(response.body)
        # filename = "test.html"
        # with open(filename, "wb")as f:
        #     f.write(response.body)
        fathAllType=response.meta['fathAllType']
        print("接受到上层传来的数据："+fathAllType)
        bb = True
        pagnDisabled=0
        try:
            nowtype = response.css('.a-list-item').css('.a-text-bold::text').extract()[0]
            print(nowtype)
            pagnDisabled = response.css('.pagnDisabled::text').extract()[0]
            print("最大页数" + pagnDisabled)
            listitem = response.css('.s-ref-indent-two')
            print(len(listitem))
            # if pagnDisabled == "400":

            for tmp in listitem:
                tmparr = tmp.css(".s-ref-text-link::attr(href)").extract()
                tmptype = tmp.css(".s-ref-text-link").css(".a-size-small::text").extract()
                if len(tmparr) > 0:
                    for i in range(0,len(tmparr)):
                            bb=False
                            tItem = TypeItem()
                            tItem['fatherType'] = nowtype
                            tItem['fatherAllType'] =fathAllType
                            tItem['sonType'] = tmptype[i]
                            yield tItem
                            print("开始访问" + tmparr[i])
                            yield scrapy.Request(tmparr[i], callback=self.parse_keyword2,meta = {'fathAllType' : tItem['fatherAllType']+"_"+tItem['sonType']})
                    #         break
                    # break
        except Exception as e:
            # items = self.Data_asinDeocede(response)
            # for item in items:
            #     yield item
            bb=False
        if bb:
            print("解码当前目录")
            urls=response.css('.pagnLink').css('a::attr(href)').extract()[0]
            print(urls)
            pat="&page=2"
            for i in range(1,int(pagnDisabled)+1):
                tmpurl=urls.replace(pat,"&page="+str(i))
                print(tmpurl)
                yield scrapy.Request("https://www.amazon.com"+tmpurl, callback=self.parse_page,meta = {'allType' : fathAllType})

    #目录页信息提取
    # def parse_directory(self, response):
    #     print("获取到的内容为")
    #     print(response.body)
    #     filename = "test.html"
    #     with open(filename,"wb")as f:
    #         f.write(response.body)
    #     fsdDeptBox=response.css('.fsdDeptBox')
    #     i=0
    #     print(len(fsdDeptBox))
    #     for fsdDeptCol in fsdDeptBox:
    #         tmparr=fsdDeptCol.css(".fsdDeptLink::attr(href)").extract()
    #         print("切换下一个类型")
    #         print("------------------------------------------------------------------")
    #         if len(tmparr)>0:
    #             for url in tmparr:
    #                 print("https://www.amazon.com"+url)

    #https://www.amazon.com/Dry-Food/s?rh=n%3A2975360011&page=2
    #最低品类页面解析
    def parse_page(self, response):
        print("获取到的内容为")
        print(response.body)
        filename = "test.html"
        with open(filename, "wb")as f:
            f.write(response.body)
        allType = response.meta['allType']
        items=self.Data_asinDeocede(response,allType)
        print("产品信息长度为:")
        print(len(items))
        for item in items:
            yield item




    def parse(self, response):
        print("获取到的内容为")
        print(response.body)
        NextPage=response.css('.pagnNext::attr(href)').extract()

        if len(NextPage)==0:
            NextPage = response.css('.a-last').css('a::attr(href)').extract()
        # print(NextPage)
        if len(NextPage)>0:
            pat='page=(.*)'
            pagenum=int(re.findall(pat,NextPage[0])[0])
            print(pagenum)
            if pagenum<4:
                nexturl="https://www.amazon.com"+NextPage[0]
                print("开始访问"+nexturl)
                yield scrapy.Request(nexturl,callback=self.parse)

        list = response.css('[data-asin]')
        print(len(list))
        for row in list:
            try:
                # print("Fuck")
                # print(row)
                # star=row.xpath('//*[@class="a-icon-alt"]').extract()
                # print(star)
                star=row.css('.a-icon-alt::text').extract()[0]
                # print(star)
                name=row.css('.a-spacing-top-small').css('.a-link-normal').css('.a-size-base-plus::text').extract()[0]
                # print(name)
                #.css(".a-size-base::text")
                # sellnum = row.css('.a-spacing-top-micro').css('.a-size-small').css('.a-link-normal::text').extract()
                sellnum = row.css('.a-spacing-top-micro').css('.a-size-small').css('.a-size-base::text').extract()
                # print(sellnum)
                #.css('.a-row').css('.a-link-normal')
                # price_dw=row.css('.sx-price-currency::text').extract()[0]
                # price_whole=row.css('.sx-price-whole::text').extract()[0]
                # price_fractional = row.css('.sx-price-fractional::text').extract()[0]
                # price=price_dw+price_whole+"."+price_fractional
                price=row.css('.a-offscreen').extract()[0]
                # print(price)
                imgurl=row.css('[alt]::attr(src)').extract()[0]
                # print(imgurl)
            except Exception as e:
                print(e)
                continue
                pass

            item = AsinBestItem()
            item['name'] = name.replace("\n", "")
            item['star'] = star
            item['sellnum'] = sellnum
            item['price'] = price
            item['imgurl'] = imgurl
            print("获取完成")
            yield item
