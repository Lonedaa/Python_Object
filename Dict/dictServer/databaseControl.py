import pymysql
import datetime
from dictServer.mydefine import *
import hashlib
# 宏定义
log = Log()
hist = History()
dicter = Dicter()


class DatabaseController:
    def __init__(self, kwargs={}):
        """
            初始化
        :param kwargs: host port user password database charset
        """
        self._db = pymysql.connect(**kwargs)
        self._cur = self._db.cursor()
        self._now_user = ("lang", "123","loneda")  # 赋值测试

    def userinfo_compare(self, account, password):
        """
            功能：与校对用户数据
        :param account: 用户账号
        :param password: 用户密码
        :return: 校对提示--“密码正确” “密码错误” “该账号未注册”
        """
        # 获取数据库数据
        sql = "select * from userinfo where account='%s'" % account
        # 执行语句
        self._cur.execute(sql)
        result = self._cur.fetchone()
        if result:
            hash = hashlib.md5("意外不，我也是盐".encode())  # 生成对象
            hash.update(password.encode('utf8'))
            password = hash.hexdigest()
            if result[log.PASSWORD] == password:
                self._now_user = (account, password, result[log.USERNAME])
                return "密码正确"
            return "密码错误"
        else:
            return "该账号未注册"

    def save_userinfo(self, account, password, username):
        """
            功能： 保存用户信息
        :param account:用户账号
        :param password:用户密码
        :param username:用户昵称
        :return:保存提示--“success” e
        """
        try:
            hash = hashlib.md5("意外不，我也是盐".encode())  # 生成对象
            hash.update(password.encode('utf8'))
            password = hash.hexdigest()
            sql = "insert into userinfo(account,password,username)values(%s,%s,%s)"
            self._cur.execute(sql, (account, password, username))
            self._db.commit()
            self._now_user = (account, password, username)
            return "success"
        except:
            self._db.rollback()
            return "Error"

    def search_word(self, word,record_flag=1):
        """
            功能： 查询单词
        :param word: 要查询的单词
        :return: 查询结果
        """
        sql = "select * from words where word='%s'" % word
        self._cur.execute(sql)
        result = self._cur.fetchone()
        if result:
            if record_flag==1:
                self._history(word)
            return result[dicter.EXPLANATION]
        else:
            return "没有找到该单词～～"

    def _history(self, word):
        """
            功能： 记录当前用户查询历史
        :param word: 需记录的单词
        :return: 记录提示
        """
        try:
            sql = "insert into history values(%s,%s,%s)"
            self._cur.execute(sql, (self._now_user[0], word, datetime.datetime.now()))
            self._db.commit()
        except:
            self._db.rollback()
            return "Error"

    def show_history(self, n):
        """
            功能：查询搜索历史
        :param n: 查询数量f
        :return: 查结果
        """
        if int(n) > 0:
            sql = "select * from history where account=%s order by time DESC limit %s"
            self._cur.execute(sql, (self._now_user[0], int(n)))
            return self._cur.fetchall()
        else:
            return "Error"

    def close(self):
        self._db.close()

# --------------------------------test--------------------------------------------
# dbc = DatabaseController({"host": "localhost",
#                           "port": 3306,
#                           "user": "root",
#                           "password": "123456",
#                           "database": "dict",
#                           "charset": "utf8"})
#
#
# def logon():
#     account = input("请输入账号:>")
#     password = input("请输入密码:>")
#     username = input("请输入用户名:>")
#     account.strip()  # 去除两端空格
#     password.strip()
#     username.strip()
#     result = dbc.compare(account, password)  # 与数据库校对账户
#     if result == "该账号未注册":
#         dbc.save_data(account, password, username)
#     else:
#         print("该账号已注册")
#
#
# def login():
#     account = input("请输入账号:>")
#     password = input("请输入密码:>")
#     account.strip()  # 去除两端空格
#     password.strip()
#     result = dbc.compare(account, password)  # 与数据库校对账户
#     if result == "密码正确":
#         print("登录成功")
#     else:
#         print(result)
#
#
# def find():
#     word = input("请输入单词:>")
#     result = dbc.search_word(word)
#     print(result)
#
#
# def get_history():
#     num = int(input("回顾数量:>"))
#     print(dbc.show_history(num))
#
#
# if __name__ == "__main__":
#     while True:
#         # choice = input("登录/注册:>")
#         # if not choice:
#         #     break
#         # elif choice == "登录":
#         #     login()
#         # elif choice == "注册":
#         #     logon()
#         # else:
#         #     print("臣妾错不到呀～～")
#         choice = int(input("选择"))
#         if choice == 1:
#             find()
#         elif choice == 2:
#             get_history()
#         else:
#             break
