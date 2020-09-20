from core.register import api_method, cross_domain
from mvc.controllers import ApiController

"""

uploadFile模块提供了后端文件分块上传API

"""


class InitUpload(ApiController):
    """

    接口: /file/initupload

    参数::

        fileMd5: 文件MD5值

        name: 文件原始名称

        type: 文件MIME类型

    返回内容::

        {"err": None, "isExistFile": False, "isExistChunk": False, "url": ""}

    """

    __urls = ["/file/initupload"]

    @cross_domain()
    @api_method
    async def get(self):
        # 1. 校验路径是否为合法路径
        # 2. 文件根目录中，检验文件是否存在，不存在则开辟块上传空间
        # 3. 返回检查结果
        return {"err": None, "isExistFile": False, "isExistChunk": False, "url": ""}


class UploadPart(ApiController):
    """

    接口: /file/uploadpart

    参数::

        fileMd5: 文件MD5值

        name: 文件原始名称

        type: 文件MIME类型

        size: 当前块大小

        chunks: 分块总数

        chunk: 当前分块标识符

    返回内容::

        {"err": None,"exist": True}

    """

    __urls = ["/file/uploadpart"]

    @cross_domain()
    @api_method
    async def options(self):
        return {"err": None}

    @cross_domain()
    @api_method
    async def post(self):
        # 1. 检查块是否存在，存在则直接返回
        # 2. 不存在块存储块内容到文件夹当中
        # 3. 返回结果
        return {"err": None, "exist": True}


class MergeFile(ApiController):
    """

    接口: /file/mergefile

    参数::

        fileMd5: 文件MD5值

        name: 文件原始名称

        type: 文件MIME类型

        chunks: 分块总数

    返回内容::

        {"err": None, "url": ""}

    """

    __urls = ["/file/mergefile"]

    @cross_domain()
    @api_method
    async def post(self):
        # 1. 合并数据到临时文件当中，校验MD5是否一致
        # 2. 校验失败或者合并时缺少文件块返回错误结果，清理块文件夹返回上传失败请求重传
        # 3. 校验成功将文件剪切到主目录下，清理块文件夹
        return {"err": None, "url": ""}
