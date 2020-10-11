from tornado.gen import sleep
from tornado.web import HTTPError

from core.register import api_method
from core.fs import check_join, read_bytes
from core.form import weak_verify
from mvc.controllers import ApiGhost

import os
import shutil

"""

该模块提供了后端文件分块上传API

"""
MD5_CHUNK_ROOT_PATH = "wwwroot/chunks"


class Init(ApiGhost):
    """

    接口: /upload/init

    参数::

        fileMd5: 文件MD5值

        ext: 文件拓展名称

    返回内容::

        {"isExistFile": False, "existChunk": []}

    """

    __urls = ["/upload/init"]

    @api_method
    async def get(self):
        params = weak_verify(["fileMd5", "ext"], self.get_query_argument)

        md5_chunk_path = check_join(MD5_CHUNK_ROOT_PATH, params["fileMd5"])
        md5_file_root_path = self.galaxy("resource.root_path")
        md5_file_path = check_join(md5_file_root_path, params["fileMd5"] + "." + params["ext"])

        exist_chunk = []
        is_exist_file = False

        if os.path.exists(md5_chunk_path):
            exist_chunk = True
        else:
            os.mkdir(md5_chunk_path)

        if os.path.exists(md5_file_path):
            is_exist_file = True

        return {"isExistFile": is_exist_file, "existChunk": exist_chunk}


class Chunk(ApiGhost):
    """

    接口: /upload/chunk

    参数::

        fileMd5: 文件MD5值

        chunk: 当前分块标识符

        file: 当前块的二进制数据

    返回内容::

        {"exist": True}

    """

    __urls = ["/upload/chunk"]

    @api_method
    async def post(self):
        params = weak_verify(["fileMd5", "chunk"], self.get_body_argument)

        md5_file_path = check_join(MD5_CHUNK_ROOT_PATH, params["fileMd5"])

        if not os.path.exists(md5_file_path):
            raise HTTPError(406, "No initialization request, you should first request `/upload/init`")

        md5_chunk_path = check_join(md5_file_path, params["chunk"])

        if os.path.exists(md5_chunk_path):
            return {"exist": True}
        else:
            data = self.request.files["file"][0]
            with open(md5_chunk_path, "wb") as fp:
                fp.write(data.body)
        return {"exist": False}


class Merge(ApiGhost):
    """

    接口: /upload/merge

    参数::

        fileMd5: 文件MD5值

        name: 文件原始名称

        ext: 文件MIME类型

        chunks: 分块总数

    返回内容::

        {"url": ""}

    """

    __urls = ["/upload/merge"]

    @api_method
    async def post(self):
        params = weak_verify(["fileMd5", "name", "ext", "chunks"], self.get_body_argument)

        source_name = params["name"] + "." + params["ext"]
        md5_chunk_path = check_join(MD5_CHUNK_ROOT_PATH, params["fileMd5"])
        md5_file_merge_path = os.path.join(md5_chunk_path, source_name)

        try:
            with open(md5_file_merge_path, "wb") as fp:
                for i in range(int(params["chunks"])):
                    item_path = os.path.join(md5_chunk_path, str(i))
                    fp.write(read_bytes(item_path))
                    await sleep(0)
        except Exception as e:
            shutil.rmtree(md5_file_merge_path, True)
            raise HTTPError(406, "Merge failed")

        md5_file_root_path = self.galaxy("resource.root_path")
        md5_target_file_path = os.path.join(md5_file_root_path, source_name)
        shutil.copy(md5_file_merge_path, md5_target_file_path)
        shutil.rmtree(md5_file_merge_path)

        return {"url": "/storage/" + source_name}
