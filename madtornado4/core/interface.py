from tornado.web import Application
from abc import ABC, abstractmethod

from typing import NoReturn, Type


class IDispose(ABC):
    """

    定义可被销毁对象

    """

    def __init__(self, launch):
        self.launch = launch

    @abstractmethod
    def destroy(self) -> NoReturn:
        """

        定义如何销毁对象

        :return: NoReturn

        """
        raise NotImplementedError()


class IStartup(ABC):
    """

    定义web服务启动器

    """

    @abstractmethod
    def config_static_file(self) -> "IStartup":
        """

        实现静态文件参数配置

        :return: NoReturn

        """
        raise NotImplementedError()

    @abstractmethod
    def config_debug(self) -> "IStartup":
        """

        实现debug参数配置

        :return: NoReturn

        """
        raise NotImplementedError()

    @abstractmethod
    def config_route(self) -> "IStartup":
        """

        实现路由配置

        :return: NoReturn

        """
        raise NotImplementedError()

    @abstractmethod
    def add_singleton(self, service: Type[IDispose]) -> "IStartup":
        """

        添加单例对象，该对象必须继承自IDispose抽象类，注意service要保证类名唯一，
        请不要注册同类名的service

        :param service:
        :return: IStartup

        """
        raise NotImplementedError()

    @abstractmethod
    def add_scoped(self, service: Type[IDispose]) -> "IStartup":
        """

        添加会话对象，该对象必须继承自IDispose抽象类，注意service要保证类名唯一，
        请不要注册同类名的service

        :param service:
        :return: IStartup

        """
        raise NotImplementedError()

    @abstractmethod
    def build(self) -> Application:
        """

        实现应用构建逻辑

        :return: Application

        """
        raise NotImplementedError()
