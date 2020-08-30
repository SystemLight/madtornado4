from collections import defaultdict


class ArgType:
    """

    包含uri可以用到的类型参数

    """
    Number = r"(\d+)"
    Letter = r"([A-Za-z]+)"
    Word = r"([\w-]+)"
    Param = r"([^\\/]+)"
    Any = r"(.+)"


def uri(path: str, *args) -> str:
    """

    快捷的定义url注册，可以根据类型参数生成对应的正则匹配

    使用方法::

        __urls = [
            uri("/home/{Letter}"),
            "/home", "/index"
        ]

        __urls = [
            uri("/home/{}", ArgType.Letter),
            "/home", "/index"
        ]

    :param path: 模板url路径
    :param args: 替换类型参数，ArgType的静态属性
    :return: 渲染后的URL字符串

    """
    if len(args) > 0:
        return path.format(*args)
    return path.format(**ArgType.__dict__)


class RegisterMeta(type):
    """

    路由注册器元类

    """

    route_pool = defaultdict(list)

    def __init__(cls, what, bases=None, _dict=None):
        super(RegisterMeta, cls).__init__(what, bases, _dict)

        # 获取handler的注册路径地址
        __urls = _dict.get("_{}__urls".format(what), ["/" + what])

        # 注册到路由池当中
        __virtual_host = _dict.get("_{}__virtual_host".format(what), ".*")

        for url in __urls:
            RegisterMeta.route_pool[__virtual_host].append((url, cls))

    def __call__(cls, *args, **kwargs):
        return super(RegisterMeta, cls).__call__(*args, **kwargs)
