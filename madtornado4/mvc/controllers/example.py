from core.register import api_method
from mvc.controllers import ApiController


class Example(ApiController):
    """

    示例控制器

    """

    @api_method
    async def get(self):
        pass

    @api_method
    async def post(self):
        pass
