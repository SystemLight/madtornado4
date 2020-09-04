from tornado.web import removeslash, stream_request_body
from tornado.gen import sleep

from core.register import uri, param
from core.form import verify
from mvc.controllers import ApiController
from mvc.models import example

import json


@stream_request_body
class Example(ApiController):
    """

    通过__urls可以间接为当前控制器注册多个访问路径，
    @removeslash装饰器可以将/example/ 重定向到 /example
    这样访问的逻辑更加接近restful风格

    访问方式::

        http://localhost:8095/example/  --> http://localhost:8095/example
        http://localhost:8095/example/lisys

    """

    __urls = [
        uri("/example/{Letter}"),
        "/example", "/index"
    ]

    @param
    async def get(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Access-Control-Allow-Methods', 'PUT,POST,GET,DELETE,OPTIONS')
        self.set_header('Access-Control-Max-Age', 600)
        self.write({})

    async def post(self):
        await self.get()
