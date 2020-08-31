from typing import Optional, List


class NotFoundStatic(Exception):
    pass


def static_url(self, path: str, name: Optional[str] = None, **kwargs) -> str:
    """

    生成静态目录路径

    :param self: ApiController
    :param path: 传进来的文件位置参数
    :param name: 静态文件寻址注册名称
    :return: 合成的文件路径

    """
    v_host = self.settings["launch"]["virtual_host"]  # type: List
    static_file = self.settings["launch"]["static_file"]  # type: List
    for v in v_host:
        for f in static_file[v]:
            if f["name"] == name:
                return "{}/{}".format(f["url_prefix"].rstrip("/"), path)
    raise NotFoundStatic("Name is not exists")
