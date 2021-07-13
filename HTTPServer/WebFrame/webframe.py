from socket import *
import json
from setting import *
from select import select


# 应用类，处理某一方面的请求
class Application:
    def __init__(self):
        self._rlist = []
        self._wlist = []
        self._xlist = []
        self._sockfd = socket()
        self._sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, DEBUG)
        self._sockfd.bind((HOST, PORT))

    def start(self):
        self._sockfd.listen(5)
        print("Start app listen %d " % PORT)
        self._rlist.append(self._sockfd)
        while True:
            rs, ws, xs = select(self._rlist, self._wlist, self._xlist)
            for r in rs:
                if r is self._sockfd:
                    connfd, addr = self._sockfd.accept()
                    self._rlist.append(connfd)
                else:
                    self._handel(r)
                    self._rlist.remove(r)

    def _handel(self, connfd):
        request = connfd.recv(1024).decode()
        request = json.loads(request)
        response = {"status": "200", "data": "页面找不到了"}
        if request["method"] == "GET":
            if request["info"] == "/" or \
                    request["info"][-5] == ".html":
                response = self._get_html(request["info"])
            else:
                pass#urls--views
        elif request["method"] == "HOST":
            pass
        response = json.dumps(response)
        connfd.send(response.encode())
        connfd.close()

    def _get_html(self, info):
        if info == "/":
            filename = STATIC_DIR + "/meinv.html"
        try:
            file = open(filename)
        except Exception as e:
            filename = STATIC_DIR + "/xinlang.html"
            file = open(filename)
            return {"status": "404", "data": file.read()}
        return {"status": "200", "data": file.read()}


app = Application()
app.start()
