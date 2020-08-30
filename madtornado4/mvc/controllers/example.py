from tornado.web import removeslash

from core.register import uri, ArgType
from core.form import verify
from mvc.controllers import ApiController
from mvc.models import example

import json


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
        uri("/example/{}", ArgType.Letter),
        "/example", "/index"
    ]

    async def get(self, *args):
        # service = await self.spit_out("MysqlService")(self.spit_out("MysqlPoolService"))
        # self.write(await service.queryone("select * from goods"))

        self.write({})

    @removeslash
    async def async_post(self, *args):
        """

        示例数据::

            {
                "name": "qlys",
                "age": 3500,
                "props": [
                    {
                        "name": "f22222222232d",
                        "power": 100
                    },
                    {
                        "name": "2323",
                        "power": 100
                    },
                    {
                        "name": "fd",
                        "power": 100
                    }
                ],
                "halo": {
                    "light": 1,
                    "p": {
                        "name": "fd",
                        "power": 100
                    }
                }
            }

        :param args:
        :return:

        """
        # 让mad帮你验证实体模型并返回它
        elves_obj = verify(example.Elves, json.loads(self.request.body.decode("utf-8")).get)

        # 将验证通过的实体模型返回到前台页面当中
        self.write(elves_obj.__dict__)
