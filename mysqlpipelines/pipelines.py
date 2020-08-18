from scrapy.exceptions import DropItem

from AmazonCrapy.helper import Helper
from AmazonCrapy.sql import ReviewSql, RankingSql
from .sql import Sql
from AmazonCrapy import MySQLCenter
from AmazonCrapy.items import CateItem, ReviewProfileItem, ReviewDetailItem, SalesRankingItem, KeywordRankingItem
from AmazonCrapy.items import AsinBestItem
from AmazonCrapy.items import DetailItem
from AmazonCrapy.items import TypeItem
import time

class AmazonPipeline(object):
    def __init__(self):
        self.Mysql=MySQLCenter.mysqlcenter()
    def process_item(self,item,spider):
        print("开始解析item")
        if isinstance(item,CateItem):
            # Sql.insert_cate_log(item)

            pass

        if isinstance(item,AsinBestItem):
            tmpitem = {}
            for key in item:
                tmpitem[key]=item[key]
            print("开始上传")
            TableName = "a_product"
            TableName2='a_tpye'
            self.Mysql.DeleteData(TableName,"asin='"+item['asin']+"'")
            typeid=0
            try:
                typeid=self.Mysql.getData(TableName2,"allType='"+item['allType']+"'")[0][0]
            except Exception as e:
                print("未找到:"+item['allType'])
            tmpitem['typeId']=typeid
            tmpitem["creatTime"]= int(time.time())
            self.Mysql.AddDataPro(TableName,tmpitem)
            print('save best seller: ' + item['name'])

            pass
        if isinstance(item, TypeItem):
            tmpitem=item
            TableName = "a_tpye"
            if self.Mysql.IsInside(TableName,"allType='"+item['fatherAllType']+"_"+item['sonType']+"'"):
                return item
            if self.Mysql.IsInside(TableName,"allType='"+item['fatherAllType']+"'")==False:
                datadict={
                    "name":item['fatherType'],
                    "parentId":0,
                    "allType":item['fatherAllType'],
                    "creatTime":int(time.time())
                }
                self.Mysql.AddDataPro(TableName,datadict)
            fatherid=-1
            try:
                fatherid=self.Mysql.getData(TableName,"name='"+item['fatherType']+"'")[0][0]
            except Exception as e:
                print(e)

            if fatherid>-1:
                loc=item['fatherAllType'].rfind("_")
                print(loc)
                sonAllType=item['fatherAllType']+"_"+item['sonType']
                print(sonAllType)
                datadict = {
                    "name": item['sonType'],
                    "parentId": fatherid,
                    "allType":sonAllType,
                    "creatTime": int(time.time())
                }
                self.Mysql.AddDataPro(TableName, datadict)
            return item

        if isinstance(item, ReviewProfileItem):
            ReviewSql.insert_profile_item(item)
            return item

        if isinstance(item, ReviewDetailItem):
            delay_date = Helper.delay_forty_days()  # 40天的截止时间
            item_date = Helper.convert_date_str(item['date'])
            if item_date < delay_date:   # 判断是否过了40天限额，如果超出范围 则抛弃此item
                raise DropItem('the review_id:[%s] has been expired' % item['review_id'])
            else:
                item['review_url'] = 'https://www.amazon.com' + item['review_url']
                item['date'] = item_date.strftime('%Y-%m-%d')
                ReviewSql.insert_detail_item(item)

                return item

        if isinstance(item, SalesRankingItem):
            RankingSql.insert_sales_ranking(item)
            return item

        if isinstance(item, KeywordRankingItem):
            RankingSql.insert_keyword_ranking(item)
            return item

        if isinstance(item, DetailItem):
            return item

        pass





