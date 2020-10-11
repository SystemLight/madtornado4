from core.register import api_method, create_router
from mvc.controllers import ApiGhost
from mvc.models import example

api_router = create_router("/api", use_uri=True)


class Example(ApiGhost):
    """

    示例控制器，注意tornado路由是严格区分大小写的，
    如果不指定__urls = []，默认注册为/example

    """

    __urls = api_router(["/example/{Word}"])

    @api_method
    async def get(self, word):
        if word == "model":
            return example.Elves()
        else:
            return {"hello": "get"}

    async def post(self):
        self.write({"msg": "Example"})
