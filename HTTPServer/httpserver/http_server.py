"""
HTTPServer部分主程序：
    httpserver部分
    获取http请求
    解析http请求
    将请求发送给WebFrame
    从WebFrame接收反馈数据
    将数据组织为Response格式发送给客户端
"""

from socket import *
import sys
from threading import Thread
from config import *
import re, json

# 服务器地址
ADDR = (HOST, PORT)


# 将httpserver基本功能封装为类

class HTTPServer:
    def __init__(self):
        self._host = HOST
        self._port = PORT
        self._create_socket()  # 和浏览器交互
        self._bind()

    def _connect_socket(self, env):
        connect_sockfd = socket()
        frame_addr = ((frame_ip, frame_port))
        try:
            connect_sockfd.connect(frame_addr)
        except Exception as e:
            print(e)
            sys.exit()
        else:
            data = json.dumps(env)
            connect_sockfd.send(data.encode())
            data = connect_sockfd.recv(1024*1024*1024).decode()
            return data

    # 创建套接字
    def _create_socket(self):
        self._sockfd = socket()
        self._sockfd.setsockopt(SOL_SOCKET,
                                SO_REUSEADDR,
                                DEBUG)

    # 绑定地址
    def _bind(self):
        self._address = (self._host, self._port)
        self._sockfd.bind(self._address)

    # 启动服务
    def server_forever(self):
        self._sockfd.listen(5)
        print("Listen the port %d" % self._port)
        while True:
            connfd, addr = self._sockfd.accept()
            print("Connet from ", addr)
            client = Thread(target=self._handel, args=(connfd,))
            client.setDaemon(True)
            client.start()

    # 具体处理客户端请求
    def _handel(self, connfd):
        request = connfd.recv(4096).decode()
        pattern = r"(?P<method>[A-Z]+)\s+(?P<info>/\S*)"
        try:
            env = re.match(pattern, request).groupdict()
        except:
            connfd.close()
            return
        else:
            data = self._connect_socket(env)  # 连接WebFrame
            self._response(connfd, json.loads(data))


    def _response(self, connfd, data):
        # data => {"status": "200", "data": "xxx"}
        print(data)
        if data["status"] == "200":
            response = "HTTP/1.1 200 OK\r\n"
            response += "Connect-Type:text/html\r\n"
            response += "\r\n"
            response += data["data"]
        elif data["status"] == "404":
            response = "HTTP/1.1 404 OK\r\n"
            response += "Connect-Type:text/html\r\n"
            response += "\r\n"
            response += data["data"]
        connfd.send(response.encode())


if __name__ == "__main__":
    https = HTTPServer()
    https.server_forever()
