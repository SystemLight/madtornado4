from collections import defaultdict
from typing import List, Union


def api_method(method):
    """

    api装饰的方法将函数定义为API类型请求方法，可以获取到任意param参数值
    同时方法返回的对象值会自动写入到返回请求当中

    举例说明::

        @cross_domain()
        @api_method
        async def get(self):
            return {}

    :param method: 异步http方法函数
    :return: 装饰包裹后的函数

    """

    async def wrap(self, *args):
        size = len(args) - 1
        new_args = []
        for i in range(method.__code__.co_argcount - 1):
            if i > size:
                new_args.append(None)
            else:
                new_args.append(args[i])
        result = await method(self, *new_args)
        result = {} if result is None else result
        self.write(result)
        return result

    return wrap


def cross_domain(origin: str = "*", headers: str = "*", methods: str = "GET,POST,PUT,DELETE,OPTIONS", max_age=600):
    """

    access为当前请求方法添加跨域属性

    :param origin: 允许的作用域
    :param headers: 允许的请求头
    :param methods: 允许的请求方法
    :param max_age: 最大非重复预请求时间
    :return: 装饰包裹后的函数

    """

    def box(method):
        async def wrap(self, *args):
            self.set_header("Access-Control-Allow-Origin", origin)
            self.set_header("Access-Control-Allow-Headers", headers)
            self.set_header("Access-Control-Allow-Methods", methods)
            self.set_header("Access-Control-Max-Age", max_age)
            return await method(self, *args)

        return wrap

    return box


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


def create_router(prefix: str):
    """

    创键router函数，该函数用于包裹__urls，
    添加公用前缀

    举例::

        router = create_router("/api")

        __urls = router(["/test"])
        或者
        __urls = [router("/test")]

    :param prefix: 公用url前缀
    :return: router函数

    """

    def __router(urls: Union[List[str], str]):
        if isinstance(urls, str):
            return "/" + prefix.strip("/") + "/" + urls.lstrip("/")

        new_urls = []
        for url in urls:
            new_urls.append("/" + prefix.strip("/") + "/" + url.lstrip("/"))
        return new_urls

    return __router


class RegisterMeta(type):
    """

    路由注册器元类

    """

    route_pool = defaultdict(list)

    def __init__(cls, what, bases=None, _dict=None):
        super(RegisterMeta, cls).__init__(what, bases, _dict)

        # 获取handler的注册路径地址
        __urls = _dict.get("_{}__urls".format(what), ["/" + what.lower()])

        # 注册到路由池当中
        __virtual_host = _dict.get("_{}__virtual_host".format(what), ".*")

        for url in __urls:
            RegisterMeta.route_pool[__virtual_host].append((url, cls))

    def __call__(cls, *args, **kwargs):
        return super(RegisterMeta, cls).__call__(*args, **kwargs)
