from scrapy.cmdline import execute
from  AmazonCrapy import xici
from AmazonCrapy import MySQLCenter
from MySQLdb import escape_string


# def transferContent(content):
#     if content is None:
#         return None
#     else:
#         string = ""

#         for c in content:
#             if c == '"':
#                 string += '\\\"'
#             elif c == "'":
#                 string += "\\\'"
#             elif c == "\\":
#                 string += "\\\\"
#             else:
#                 string += c
#         return string

#Just run once
xc1=xici.xiciip()
xc1.FlushStart()
while True:
    execute("scrapy crawl listspider".split())
# execute("scrapy crawl asin".split())
# Mysql=MySQLCenter.mysqlcenter()
# tablename="a_tpye"
# data="Hello'World\"!"
# print(data)
# data=transferContent(data)
# datadict={
#                     "name":data,
#                     "parentId":0,
#                     "allType":"test",
#                     "creatTime":0
#                 }
# Mysql.AddDataPro(tablename,datadict)

