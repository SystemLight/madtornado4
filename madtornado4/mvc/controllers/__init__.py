from tornado.gen import isawaitable, convert_yielded
from tornado.log import gen_log
from tornado.web import StaticFileHandler, RequestHandler, HTTPError
from tornado.ioloop import IOLoop

from core.register import RegisterMeta
from core.utils import AdvancedJSONEncoder, json
from core import VERSION

from typing import Optional, Awaitable, Any, NoReturn, Union, Type


class ApiController(RequestHandler, metaclass=RegisterMeta):
    """

    基础API控制器，请求控制器的基类

    """

    __urls = []
    __virtual_host = None

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def set_default_headers(self) -> None:
        self.set_header("Server", "madtornado/{}".format(VERSION))

    def write(self, chunk: Union[str, bytes, dict, list],
              encoder: Optional[Type[json.JSONEncoder]] = AdvancedJSONEncoder) -> None:
        if isinstance(chunk, dict) or isinstance(chunk, list):
            self.set_header("Content-Type", "application/json; charset=UTF-8")
            chunk = json.dumps(chunk, cls=encoder, ensure_ascii=False)
        super(ApiController, self).write(chunk)

    def write_error(self, status_code: int, **kwargs: Any) -> None:
        exc_info = kwargs.get("exc_info", None)
        if exc_info and exc_info[0] == HTTPError:
            self.write({
                "status_code": status_code,
                "message": exc_info[1].log_message
            })
        else:
            super(ApiController, self).write_error(status_code, **kwargs)

    def static_url(self, path: str, name: Optional[str] = None, **kwargs) -> str:
        """

        生成静态目录路径

        :param self: ApiController
        :param path: 传进来的文件位置参数
        :param name: 静态文件寻址注册名称
        :return: 合成的文件路径

        """
        return self.ui.static_url(path, name, **kwargs)

    def on_finish(self) -> None:
        IOLoop.instance().add_future(
            convert_yielded(self.async_on_finish()),
            lambda v: gen_log.info("Scope services are automatically cleaned up")
        )

    async def async_on_finish(self) -> NoReturn:
        """

        自动回收scoped注册服务对象调用destroy()方法，
        可支持异步销毁和同步销毁方式

        :return:

        """
        scoped = self.application.scoped
        for key in scoped:
            s = getattr(self, key, None)
            if s:
                d = s.destroy()
                if isawaitable(d):
                    await d

    def obtain(self, service_name: str) -> Any:
        """

        该方法可以将注入的服务类进行实例化弹出，通过该方法获取的内容将会被
        挂载到实例的属性上供二次调用，如果重复调用该方法scoped也不会重复实例，
        singleton注册的service全局共享一个实例对象

        :param service_name: 服务名称，与注册时类名同名
        :return: service对象实例

        """
        service = getattr(self, service_name, None)
        if service:
            return service

        singleton = self.application.singleton
        service = singleton.get(service_name, None)
        if service:
            setattr(self, service_name, service)
            return service

        scoped = self.application.scoped
        service = scoped.get(service_name, None)
        if service:
            service_instance = service(self.settings["launch"])
            setattr(self, service_name, service_instance)
            return service_instance

        return None

    async def close_web(self) -> NoReturn:
        """

        关闭网站，注意关闭网站服务即意味着程序退出

        :return: NoReturn

        """
        await self.application.destroy()
        IOLoop.instance().stop()


class StaticController(StaticFileHandler):
    """

    静态文件处理控制器

    """

    def initialize(self, use_spa: str, path: str, default_filename: str = None) -> None:
        super(StaticController, self).initialize(path, default_filename)
        self.use_spa = use_spa

    def write_error(self, status_code: int, **kwargs: Any) -> None:
        exc_info = kwargs.get("exc_info", None)
        if exc_info and exc_info[0] == HTTPError:
            self.write({
                "status_code": status_code,
                "message": exc_info[1].log_message
            })
        else:
            super().write_error(status_code, **kwargs)

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        raise NotImplementedError()

    def set_default_headers(self) -> None:
        self.set_header("Server", "madtornado/{}".format(VERSION))

    async def get(self, path: str, include_body: bool = True) -> None:
        if self.use_spa:
            try:
                await super(StaticController, self).get(path, include_body)
            except HTTPError:
                await super(StaticController, self).get(self.default_filename, include_body)
        else:
            await super(StaticController, self).get(path, include_body)
