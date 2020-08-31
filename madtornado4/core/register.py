from collections import defaultdict


def param(method):
    """

    param装饰器允许你自由定义http方法接收的参数，

    示例内容::

        @param
        async def get(self, name):
            # name参数可自由定义是否接收
            self.write({})

        @param
        async def get(self):
            # 两种方式都不会产生异常，使用更灵活
            self.write({})

    :param method: 异步http方法函数
    :return: 装饰包裹后的函数

    """

    async def wrap(self, *args):
        size = len(args)
        new_args = []
        for i in range(method.__code__.co_argcount - 1):
            if i > size:
                new_args.append(None)
            else:
                new_args.append(args[i])
        await method(self, *new_args)

    return wrap


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
