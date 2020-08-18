import MySQLdb
from AmazonCrapy import settings
from MySQLdb import escape_string
class mysqlcenter():
    def __init__(self):
        self.db = MySQLdb.connect(settings.MYSQL_HOST, settings.MYSQL_USER, settings.MYSQL_PASSWORD, settings.MYSQL_DB, charset='utf8', port=settings.MYSQL_PORT)
        # self.db = MySQLdb.connect("rm-uf6mtq60fvi08f1416o.mysql.rds.aliyuncs.com", "toubang", "!@Toubang123Product", "tb", charset='utf8', port=3306)
        # self.db = MySQLdb.connect("rm-uf6mtq60fvi08f141.mysql.rds.aliyuncs.com", "toubang", "!@Toubang123Product", "tb",charset='utf8', port=5101)
        self.cursor=self.db.cursor()
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
    def execute(self,cmd):
        bb=True
        # print(cmd)
        try:
            # 执行sql语句
            bc= self.cursor.execute(cmd)
            # 提交到数据库执行
            self.db.commit()
            # print("执行成功")
        except Exception as e:
            print(e)
            # Rollback in case there is any error
            bb=False
            self.db.rollback()
        return bb
    def AddData(self,TableName,nature,value):
        cmd="INSERT INTO "+TableName+nature+"\n"+"VALUES "+value
        bb=self.execute(cmd)
        if bb:
            print("添加成功")
        else:
            print("添加失败")
        return bb
    def AddDataPro(self,TableName,nvDict):
        nature = "("
        value = "("
        for key in nvDict:
            nature = nature + key + ", "
            if type(nvDict[key])==str:
                value = value + "'" + self.transferContent(nvDict[key]) + "', "
            else:
                value = value  + str(nvDict[key]) + ", "
        nature = nature[:-2]
        value = value[:-2]
        nature = nature + ")"
        value = value + ")"
        print(nature)
        print(value)
        cmd="INSERT INTO "+TableName+nature+"\n"+"VALUES "+value
        bb=self.execute(cmd)
        if bb:
            print("添加成功")
        else:
            print("添加失败")
        return bb
    def DeleteData(self,TableName,condition):
        cmd ='delete from '+TableName+' where '+condition
        bb=self.execute(cmd)
        if bb:
            print("删除成功")
        else:
            print("删除失败")
        return bb
    def IsInside(self,TableName,condition):
        cmd = 'SELECT * FROM ' + TableName + ' where ' + condition
        bb = self.execute(cmd)

        if bb:
            # print("查询成功")
            results = self.cursor.fetchall()
            # print(results)
            if results==():
                print("数据不存在")
                bb=False
        else:
            print("查询失败")
        return bb
    def getData(self,TableName,condition):
        cmd = 'SELECT * FROM ' + TableName + ' where ' + condition
        bb = self.execute(cmd)
        results=None
        if bb:
            print("查询成功")
            results = self.cursor.fetchall()
            print(results)
            if results == () or results==[]:
                results=None
                print("数据不存在")
                bb = False
        else:
            print("查询失败")
        return results
    def Modify(self,TableName,SetValue,condition):
        cmd = 'UPDATE '+TableName+' SET '+SetValue+' where '+condition
        # print(cmd)
        bb = self.execute(cmd)
        if bb:
            print("修改成功")
        else:
            print("修改失败")
        return bb

    def Close(self):
        self.db.close()


# ms1=mysqlcenter()
# ms1.AddData("t_article","(articleTitle, articleAuthor, typeId, articleContent, scaleImageUrl, articleAbstract, createTime, ext)","('testTitle', HY按理说事, 541524, 'TestContent', 'testImage', 'testAbstract', 1585281152, 'testExt')")
# ms1.DeleteData("t_article","id>1470")
# ms1.Modify("t_article","ext='11111111'","id=1080")
# ms1.IsInside("t_test","id=3")
# ms1.Close()
