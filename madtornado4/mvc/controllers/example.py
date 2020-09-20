from core.register import api_method, create_router
from mvc.controllers import ApiController

api_router = create_router("/api")


class Example(ApiController):
    """

    示例控制器，注意tornado路由是严格区分大小写的，
    如果不指定__urls = []，默认注册为/example

    """

    __urls = api_router(["/example"])

    @api_method
    async def get(self):
        return {"hello": "example"}

    @api_method
    async def post(self):
        pass
