from core.register import uri, cross_domain, api_method
from mvc.controllers import ApiController


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

    @cross_domain()
    @api_method
    async def get(self):
        pass

    async def post(self):
        await self.get()
