import json
from typing import List, Dict, Union, Optional, Callable, TypeVar, Iterable, Tuple


def find_key(obj: Union[Dict, List], key: str):
    """

    根据字符串查找对象值，字符串形式如a.b.0，
    查找对象，如::

        {"a":{"b":["val"]}}

    val值将被查出

    :param obj: 查找key值的对象
    :param key: 查找key
    :return: 查找到的值

    """
    key_list = key.split(".")
    for k in key_list:
        if isinstance(obj, list):
            val = obj[int(k)]
        else:
            val = obj.get(k)
        if val is None:
            return None
        else:
            obj = val
    return obj


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


class UpdateList(list):
    """

    主要方法update()，该方法是对list类型拓展，
    当update的数据对象存在时对其更新，注意请保证UpdateList
    的子项是dict类型而不要使用值类型，值类型对于UpdateList毫无意义

    on_update hook函数，接收old_val(旧数据), p_object(新数据)，需要返回更新数据
    on_append hook函数，接收p_object(添加数据)，需要返回添加数据
    on_fetch_key hook函数，当key属性定义为函数时需要同时定义如何捕获key值

    key 支持字符串，字符串指定子元素中的更新参考值
        支持函数，接收val(当前数据)，key(参考key值)该key值由on_fetch_key返回，函数返回bool值True为更新，False为添加

    on_fetch_key作用::

        复杂场景下我们可能需要up[("home2", True)]这样来找到响应的item，这样显示传递key值没有什么问题，key函数可以获取到
        相应的key数据以供我们处理，但是当我们调用update时，update需要判断该内容是更新还是添加，这时我们传入的内容是数据，显然
        update无法知晓如何获取我们想要的类型key值，如("home2", True)，所以我们要定义on_fetch_key来告知update如何捕获我们
        想要的类型的key值，on_fetch_key只有当key属性定义为函数时才有意义。

    """

    def __init__(self, *args, **kwargs):
        super(UpdateList, self).__init__(*args, **kwargs)

        # 对象key值，可以是函数，函数接收val, key返回布尔值代表满足条件
        self.key = None
        # 当key设置为函数时必须定义的回调，传入item对象返回该对象key值内容
        self.on_fetch_key = None
        # 当元素是更新时调用的更新方法，如果元素是插入时不调用，如果不定义该回调默认直接替换
        self.on_update = None
        # 当元素update方法触发的是添加时调用的回调函数，可以自定义append类型
        self.on_append = None

    def __getitem__(self, key):
        if isinstance(self.key, str):
            return self.find(lambda val: val[self.key] == key)
        elif hasattr(self.key, "__call__"):
            return self.find(lambda val: self.key(val, key))
        else:
            return super(UpdateList, self).__getitem__(key)

    def __setitem__(self, key, value):
        if isinstance(self.key, str):
            key = self.find(lambda val: val[self.key] == key)[0]
        elif hasattr(self.key, "__call__"):
            key = self.find(lambda val: self.key(val, key))[0]
        super(UpdateList, self).__setitem__(key, value)

    def update(self, p_object):
        """

        类似于append方法，不同的是当内容存在时会对内容进行更新，更新逻辑遵从update_callback
        而当内容不存在时与append方法一致进行末尾加入内容

        :param p_object: 内容对象
        :return: None

        """
        if not self.on_update:
            self.on_update = lambda o, p: p

        old_val = None
        if isinstance(self.key, str):
            key = p_object.get(self.key) or -1
            if key != -1:
                key, old_val = self.find(lambda val: val[self.key] == key)
        elif hasattr(self.key, "__call__"):
            try:
                key, old_val = self.find(lambda val: self.key(val, self.on_fetch_key(p_object)))
            except TypeError:
                raise TypeError("Function `on_fetch_key` is not defined")
        else:
            raise TypeError("`key` is TypeError")

        if key == -1:
            if self.on_append:
                self.append(self.on_append(p_object))
            else:
                self.append(p_object)
        else:
            super(UpdateList, self).__setitem__(key, self.on_update(old_val, p_object))

    def find(self, callback):
        """

        返回满足回调函数的内容

        :param callback: 回调函数，返回布尔类型用于判断是否满足要求
        :return: (索引，值)

        """
        for index, item in enumerate(self):
            if callback(item):
                return index, item
