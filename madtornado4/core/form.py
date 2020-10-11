from tornado.web import HTTPError

from typing import TypeVar, Type, Callable, Any, Dict, List

Model = TypeVar("Model", Any, Any)
F = TypeVar("F")


def weak_verify(pool: List[str], catch_method: Callable[[str], Any]) -> Dict:
    """

    对类型验证更随意，主要用来收集数据，无须建立model实例对象

    :return: 数据对象Dict

    """
    obj = {}
    for i in pool:
        obj[i] = catch_method(i)

    return obj


def verify(model_type: Type[Model], catch_method: Callable[[str], Any]) -> Model:
    """

    验证参数是否符合模型需求

    :param model_type: 继承IModal的模型对象
    :param catch_method: 捕获参数的方法，例如self.get_argument，dict().get等等，你甚至可以自定义，始终会传递一个value参数
    :return: 验证后的模型实例对象

    """
    obj = model_type()
    for key in obj.__dict__:
        setattr(obj, key, catch_method(key))
    return obj


class Rule:
    """

    定义规则限制，用于验证属性，注意装饰器必须加在property.setter下面

    """

    @staticmethod
    def length(min_len: int, max_len: int) -> Callable:
        """

        字段长度限制规则

        :param min_len: 字符串最小长度
        :param max_len: 字符串最大长度
        :return: Callable

        """

        def box(func: F) -> F:
            def wrap(self: Any, value: Any) -> Any:
                if min_len < len(value) < max_len:
                    return func(self, value)
                raise HTTPError(400, log_message="参数长度{}不在{}-{}之间".format(func.__code__.co_name, min_len, max_len))

            return wrap

        return box

    @staticmethod
    def scope(min_size: int, max_size: int, number=int) -> Callable:
        """

        参数最小到最大的范围

        :param min_size: 字符串最小长度
        :param max_size: 字符串最大长度
        :param number: 数字类型，整型或者浮点类型
        :return: Callable

        """

        def box(func: F) -> F:
            def wrap(self: Any, value: Any) -> Any:
                try:
                    v = number(value)
                except ValueError:
                    raise HTTPError(400, log_message="参数{}值不正确".format(func.__code__.co_name))
                if min_size < v < max_size:
                    return func(self, v)
                raise HTTPError(400, log_message="参数{}不在{}-{}之间".format(func.__code__.co_name, min_size, max_size))

            return wrap

        return box


class PropertyType:
    """

    定义模型属性类型，用于验证映射，注意装饰器必须加在property.setter下面

    """

    @staticmethod
    def array(modal_type: Type[Model]) -> Callable:
        """

        数组类实例模型

        :return: Callable

        """

        def box(func: F) -> F:
            def wrap(self: Any, value: list) -> Model:
                if not isinstance(value, list):
                    raise HTTPError(400, log_message="缺少{}实例数组".format(func.__code__.co_name))
                return func(self, list(map(lambda v: verify(modal_type, v.get), value)))

            return wrap

        return box

    @staticmethod
    def model(modal_type: Type[Model]) -> Callable:
        """

        嵌套子模型类型

        :return: Callable

        """

        def box(func: F) -> F:
            def wrap(self: Any, value: dict) -> Model:
                if not isinstance(value, dict):
                    raise HTTPError(400, log_message="缺少{}实例对象".format(func.__code__.co_name))
                return func(self, verify(modal_type, value.get))

            return wrap

        return box
