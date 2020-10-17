from tornado.web import HTTPError

from core.register import api_method
from core.fs import require
from mvc.controllers import ApiGhost

import os


class Mock(ApiGhost):
    __urls = [
        "/mock/(.+)$"
    ]

    def mock(self, path):
        try:
            return require(os.path.join(self.galaxy("mock_path"), path) + ".json")
        except FileNotFoundError:
            raise HTTPError(404, log_message="not found")

    @api_method
    async def get(self, path):
        return self.mock(path)

    @api_method
    async def post(self, path):
        return self.mock(path)

    @api_method
    async def put(self, path):
        return self.mock(path)

    @api_method
    async def delete(self, path):
        return self.mock(path)
