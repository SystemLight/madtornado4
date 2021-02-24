from tornado.ioloop import IOLoop
from tornado.concurrent import run_on_executor

from core.register import api_method, create_router
from mvc.controllers import ApiGhost
from mvc.models import example

import time
from concurrent.futures import ThreadPoolExecutor

api_router = create_router("/api", use_uri=True)

"""

IO阻塞请使用await弹出，
CPU阻塞参考下面两个案例

"""


class Example(ApiGhost):
    """

    示例控制器，注意tornado路由是严格区分大小写的，
    如果不指定__urls = []，默认注册为/example

    """

    __urls = api_router(["/example/{Word}"])

    @api_method
    async def get(self, word):
        """

        访问地址：/api/example/model

        """

        # 解决CPU阻塞方法一
        await IOLoop.current().run_in_executor(None, self.cpu_sleep, 5)

        if word == "model":
            return example.Elves()
        else:
            return {"hello": "get"}

    async def post(self):
        self.write({"msg": "Example"})

    @staticmethod
    def cpu_sleep(delay=3):
        time.sleep(delay)


class Example2(ApiGhost):
    __urls = api_router(["/example2/{Word}"])
    executor = ThreadPoolExecutor(20)

    @api_method
    async def get(self, word):
        """

        访问地址：/api/example2/model

        """

        # 解决CPU阻塞方法二
        await self.cpu_sleep(5)

        return "hello " + word

    @run_on_executor
    def cpu_sleep(self, delay=3):
        time.sleep(delay)
