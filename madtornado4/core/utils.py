import json

from typing import List, Optional, Callable, TypeVar, Iterable, Tuple


def inin(content: str, pool: List[str]) -> Optional[str]:
    """

    查找指定内容是否存在于列表的字符串中，这种情况content一定要比列表中字符串短

    举例::

        inin("a",["asdf","fsfsdf"]) 将返回 "asdf"

    :param content: 内容
    :param pool: 列表
    :return: 匹配内容

    """
    for p in pool:
        if content in p:
            return p
    return None


def rinin(content: str, pool: List[str]) -> Optional[str]:
    """

    查找指定内容是否存在于列表的字符串中，这种情况content一定要比列表中字符串长

    举例::

        inin("asdf",["a","fsfsdf"]) 将返回 "a"

    :param content: 内容
    :param pool: 列表
    :return: 匹配内容

    """
    for p in pool:
        if p in content:
            return p
    return None


IT = TypeVar("IT")


def find(iterable: Iterable[IT], func: Callable[[IT], bool]) -> Tuple[int, Optional[IT]]:
    """

    查找可迭代对象的指定项，匹配第一个子项并返回，无匹配项时返回(-1,None)

    :param func: 匹配函数
    :param iterable: 可迭代对象
    :return: 索引，子对象

    """
    for i, v in enumerate(iterable):
        if func(v):
            return i, v
    return -1, None


def retry(freq: int = 3, retry_hook: Optional[Callable[[int], None]] = None) -> Callable:
    """

    装饰器，为函数添加此装饰器当函数抛出异常时会对函数重新调用，重新调用次数取决于freq指定的参数

    :param freq: 重试次数
    :param retry_hook: 钩子函数，当函数重调用时回调的函数
    :return: 原函数返回值

    """

    def decorator(func):
        def wrap(*args, **kwargs):
            now_freq = 1
            while True:
                try:
                    result = func(*args, **kwargs)
                    break
                except Exception as e:
                    if now_freq > freq:
                        raise e
                    now_freq += 1
                    if hasattr(retry_hook, "__call__"):
                        retry_hook(now_freq)

            return result

        return wrap

    return decorator


class AdvancedJSONEncoder(json.JSONEncoder):
    """

    定义ApiController JSON解析器

    """
    find_dict = {
        "date": lambda v: v.strftime("%Y-%m-%d"),
        "datetime": lambda v: v.strftime("%Y-%m-%d %H:%M"),
        "Decimal": lambda v: v.to_eng_string()
    }

    def default(self, obj):
        deal_with = self.find_dict.get(type(obj).__name__, None)
        if deal_with:
            return deal_with(obj)
        else:
            return super(AdvancedJSONEncoder, self).default(obj)
