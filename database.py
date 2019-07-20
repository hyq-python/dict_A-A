import pymysql


class databases:
    def __init__(self, host='localhost',
                 port=3306,
                 user='root',
                 password='123456',
                 database=None,
                 charset='utf8'):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.charset = charset
        self.connection()  # 将数据库链接作为实例属性，使得创建对象时就已经生成链接
        self.cur = self.db.cursor()
    def connection(self):
        self.db = pymysql.connect(host=self.host,
                                  port=self.port,
                                  user=self.user,
                                  passwd=self.password,
                                  database=self.database,
                                  charset=self.charset)
    def do_login(self, key_1, key_2):
        # self.curs()
        sql = "select * from user where name = '%s' and \
              password = '%s'" % (key_1, key_2)
        self.cur.execute(sql)
        data = self.cur.fetchone()
        if data:
            return True
        else:
            return False


    def do_register(self,key_1,key_2):
        sql = "select * from user where name = '%s' "% (key_1)
        self.cur.execute(sql)
        data = self.cur.fetchone()
        if data:
            return False
        else:
            sql = "insert into user(name,password) values(%s,%s)"
            try:
                self.cur.execute(sql,[key_1,key_2])
                self.db.commit()
            except Exception as e:
                print(e)
                self.db.rollback()
                return False
            else:
                return True

    def do_query(self,name,words):
        sql = "select meaning from words where word= '%s' " % (words)
        self.cur.execute(sql)
        data = self.cur.fetchone()
        if data:
            sql2 = "insert into records(name,word) values(%s,%s)"
            try:
                self.cur.execute(sql2,[name,words])
                self.db.commit()
            except Exception as e:
                print(e)
                self.db.rollback()
            return data[0]
        else:
            return False
    def history(self,name):
        sql = "select word from records where name = '%s'" %(name)
        self.cur.execute(sql)
        data = self.cur.fetchall()
        if  data:
            try:
                data[-10:]
            except Exception as e:
                print(e)
                return data
            else:
                return data[-10:]
        else:
            return







if __name__ == '__main__':
    databases(database='dict')
