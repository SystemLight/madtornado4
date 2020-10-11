from tornado.httpclient import AsyncHTTPClient, HTTPClientError
from tornado.web import HTTPError

from core.register import cross_domain
from mvc.controllers import ApiGhost

"""

该模块用做HTTP代理转发通过改写host参数改变代理主机，
访问规则为/proxy/目标主机URI

"""


class Proxy(ApiGhost):
    __urls = [
        "/proxy/(.*)$"
    ]

    def __init__(self, application, request, **kwargs):
        super(Proxy, self).__init__(application, request, **kwargs)

        self.is_status = True
        self.proxy_code = 200

    @cross_domain()
    async def prepare(self):
        """

        预处理回调，在请求开始之前执行的内容，设置允许跨域

        :return: None

        """
        pass

    @cross_domain()
    async def options(self, *args, **kwargs):
        """

        符合下列条件，会跨域预检::

            1. 请求方法不是HEAD/GET/POST
            2. POST请求的Content-Type并非application/x-www-form-urlencoded, multipart/form-data, 或text/plain
            3. 请求设置了自定义的header字段

        :return: None

        """
        pass

    async def get(self, proxy_uri):
        """

        GET方法请求代理

        :return: None

        """
        await self.proxy(proxy_uri)

    async def post(self, proxy_uri):
        """

        POST方法请求代理

        :return:  None

        """
        await self.proxy(proxy_uri)

    async def put(self, proxy_uri):
        """

        PUT方法请求代理

        :return: None

        """
        await self.proxy(proxy_uri)

    async def delete(self, proxy_uri):
        """

        DELETE方法请求代理

        :return:  None

        """
        await self.proxy(proxy_uri)

    def proxy_received_header(self, chunk):
        """

        处理收到的头部信息

        :param chunk: 收到的一行头部信息
        :return: None

        """
        if self.is_status:
            self.is_status = False
            self.proxy_code = int(chunk.split(" ")[1])
        elif chunk == "\r\n":
            self.set_status(self.proxy_code)
            self.set_header("Proxy", "madtornado")
        else:
            if not next((code for code in [
                "Transfer-Encoding",
                "Content-Length",
                "Server",
            ] if code in chunk), None):
                if "Content-Type" in chunk:
                    self.set_header("Content-Type", chunk.split(":")[1].strip(" \r\n"))
                else:
                    self._headers.parse_line(chunk)

    def proxy_received_body(self, chunk):
        """

        处理收到的body信息

        :param chunk: 收到的body块
        :return: None

        """
        self.write(chunk)
        self.flush()

    async def proxy(self, proxy_uri: str):
        """

        访问代理::

            http://域名/proxy/代理的内容路径

        :return:  None

        """
        host = "www.baidu.com"

        req_uri = "http://{host}/{proxy_uri}".format(host=host, proxy_uri=proxy_uri)
        body = self.request.body if self.request.body else None
        method = self.request.method
        headers = self.request.headers
        headers["Host"] = host

        try:
            await AsyncHTTPClient().fetch(req_uri, method=method, body=body, headers=headers,
                                          validate_cert=False, request_timeout=10,
                                          header_callback=self.proxy_received_header,
                                          streaming_callback=self.proxy_received_body)
        except HTTPClientError as e:
            if e.code > 555:
                raise HTTPError(e.code)
