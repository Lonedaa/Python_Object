from socket import *
from multiprocessing import Process
import signal
from dictServer.databaseControl import DatabaseController
import os
from time import sleep


class TCPServer:
    def __init__(self, HOST, PORT):
        """
            初始化服务端套接字
        :param HOST: 服务端IP地址
        :param PORT: 服务端端口号
        """
        self._HOST = HOST
        self._PORT = PORT
        self._ADDR = (HOST, PORT)
        self._init()
        super().__init__()

    def _init(self):
        """
            配置套接字
        :return:
        """
        signal.signal(signal.SIGCHLD, signal.SIG_IGN)  # 处理僵尸
        self._s = socket(AF_INET, SOCK_STREAM)
        self._s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self._s.bind(self._ADDR)
        self._s.listen(5)

    def _login(self, c, dbc, account, password):
        result = dbc.userinfo_compare(account, password)
        mes = result.encode()
        c.send(mes)

    def _logon(self, c, dbc, account, password, username):
        result = dbc.userinfo_compare(account, password)
        if result == "该账号未注册":
            logon_result = dbc.save_userinfo(account, password, username)
            mes = logon_result.encode()
            c.send(mes)
        else:
            c.send("该账号已注册".encode())

    def _search(self, c, dbc, word):
        result = dbc.search_word(word, 1)
        mes = result.encode()
        c.send(mes)

    def _history(self, c, dbc, num):
        result = dbc.show_history(num)
        for h in result:
            meg = "%s %s %s" % (h[1], dbc.search_word(h[1], 0), h[2])
            meg = "STEP " + meg
            c.send(meg.encode())
        sleep(0.1)
        c.send(b"^^END**")

    def _handel(self, c):
        dbc = DatabaseController({"host": "localhost",
                                  "port": 3306,
                                  "user": "root",
                                  "password": "123456",
                                  "database": "dict",
                                  "charset": "utf8"})
        while True:
            data = c.recv(1024).decode()
            mes = data.split(" ")
            if not data or mes[0] == "EXIT":
                c.close()  # 关闭客户端
                os._exit(0)
                break
            elif mes[0] == "LOGIN":
                self._login(c, dbc, mes[1], mes[2])
            elif mes[0] == "LOGON":
                self._logon(c, dbc, mes[1], mes[2], mes[3])
            elif mes[0] == "SEARCH":
                self._search(c, dbc, mes[1])
            elif mes[0] == "HISTORY":
                self._history(c, dbc, mes[1])

    def main(self):
        while True:
            c, addr = self._s.accept()
            print("收到连接来自：", addr)
            p = Process(target=self._handel, args=(c,))
            p.start()


if __name__ == "__main__":
    ts = TCPServer("127.0.0.1", 41500)
    ts.main()
