from typing import Optional, List


def static_url(self, path: str, name: Optional[str] = None, **kwargs) -> str:
    """

    生成静态目录路径

    :param self: ApiController
    :param path: 传进来的文件位置参数
    :param name: 静态文件寻址注册名称
    :return: 合成的文件路径

    """
    static_file = self.settings.get("launch").get("static_file")  # type: List
    for f in static_file:
        if f["name"] == name:
            prefix = f["static_url_prefix"].rstrip("/")
            return "{}/{}".format(prefix, path).lstrip("/")
    return ""
