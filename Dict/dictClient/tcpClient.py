from socket import *
import sys
import getpass  # 隐藏输入
import hashlib  # 转换加密


def menu():
    print("==================================")
    print("    login      logon      exit    ")
    print("==================================")


def search():
    print("====================================")
    print("    word    #n    *exit    *back    ")
    print("====================================")


class TCPClient:
    def __init__(self, HOST, PORT):
        """
            初始化客户端套接字
        :param HOST: 客户端IP地址
        :param PORT: 客户端端口号
        """
        self._HOST = HOST
        self._PORT = PORT
        self._ADDR = (HOST, PORT)
        self._init()

    def _init(self):
        """
            配置套接字
        :return:
        """
        self._s = socket(AF_INET, SOCK_STREAM)
        self._s.connect(self._ADDR)

    @staticmethod
    def _login_input():
        account = input("请输入账号(输入*back返回上一级):>").strip()
        if account == "*back":
            return
        password = getpass.getpass("请输入密码:>").strip()
        hash = hashlib.md5("惊喜不，我是盐".encode())  # 生成对象
        hash.update(password.encode('utf8'))
        password = hash.hexdigest()
        msg = "LOGIN %s %s" % (account, password)
        return msg

    def _login(self):
        while True:
            msg = self._login_input()
            if not msg:
                break
            self._s.send(msg.encode())
            info = self._s.recv(1024).decode()
            if info == "密码正确":
                print("登录成功")
                self._search()
                break
            else:
                print(info)

    @staticmethod
    def _logon_input():
        account = input("请输入账号(输入*back返回上一级):>").strip()
        if account == "*back":
            return
        password = getpass.getpass("请输入密码:>").strip()
        hash = hashlib.md5("惊喜不，我是盐".encode())  # 生成对象
        hash.update(password.encode('utf8'))
        password = hash.hexdigest()
        username = input("请输入用户名：").strip()
        msg = "LOGON %s %s %s" % (account, password, username)
        return msg

    def _logon(self):
        while True:
            msg = self._logon_input()
            if not msg:
                break
            self._s.send(msg.encode())
            info = self._s.recv(1024).decode()
            if info == "success":
                print("注册成功")
                self._search()
                break
            else:
                print(info)

    def _search(self):
        while True:
            search()
            info = input("查询:>")
            if info[0] == "#" and info[1:].isdigit():
                msg = "HISTORY %s" % info[1:]
                self._s.send(msg.encode())
                while True:
                    data = self._s.recv(2048).decode()
                    if data == "^^END**":
                        break
                    for i in data.split("**STEP %%"):
                        print(i)
            elif info == "*back":
                break
            elif info == "*exit":
                self._s.send("EXIT".encode())
                sys.exit("客户端已退出")
            else:
                msg = "SEARCH %s" % info
                self._s.send(msg.encode())
                result = self._s.recv(2048)
                print(result.decode())

    def main(self):
        while True:
            menu()
            choice = input("请选择:>").strip()
            if choice == "login":
                self._login()
            elif choice == "logon":
                self._logon()
            elif choice == "exit":
                print("已退出")
                break
            else:
                print("请输入正确指令")


if __name__ == "__main__":
    ts = TCPClient("127.0.0.1", 41500)
    ts.main()
