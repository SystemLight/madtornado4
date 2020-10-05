from tornado.web import Application
from tornado.httpserver import HTTPServer
from tornado.tcpserver import socket
from tornado.gen import isawaitable, convert_yielded
from tornado.ioloop import IOLoop
from tornado.routing import HostMatches
from tornado.log import app_log, gen_log
from tornado.options import options, define, parse_command_line

from core.fs import require
from core.register import RegisterMeta
from core.ui import method, module
from core.interface import IStartup, IDispose
from mvc.controllers import StaticController

import os
from typing import List, Dict, Tuple, Type, Awaitable, Union, Any

"""

    madtornado启动器，一般来说你不应该修改这里的内容，
    由主程序调用并使用

"""

# 尝试加载launch配置参数
try:
    launch = require("launch.json")
except FileNotFoundError:
    launch = require(os.path.join(os.path.dirname(__file__), "launch.json"))
conf = launch[launch["env"]]

# 定义options可用变量
define("port", conf["port"], int, "定义服务监听端口", group="HTTPServer")
define("address", conf["address"], str, "定义接收请求匹配地址", group="HTTPServer")


class MVCApplication(Application):

    def __init__(self, handlers=None, default_host=None, transforms=None, **settings: Any):
        super().__init__(handlers, default_host, transforms, **settings)
        self.singleton = {}
        self.scoped = {}

    async def destroy(self):
        """

        销毁注册的单例服务

        :return:

        """
        for key in self.singleton:
            d = self.singleton[key].destroy()
            if isawaitable(d):
                await d


class Startup(IStartup):

    def __init__(self):
        self.route = []

        self.launch = launch
        self.env = self.launch["env"]

        self.debug_setting = {}
        self.static_file_setting = []

        self.singleton_services = {}
        self.scoped_services = {}

    @staticmethod
    def generate_static_route(setting: List[Dict]) -> List[Tuple]:
        """

        根据静态文件配置项生成路由表

        :param setting: static_file_setting 字典
        :return: 路由数组

        """
        routes = []
        for s in setting:
            static_url_prefix = s["url_prefix"].rstrip("/")
            routes.append((
                r"{}/(.*)$".format(static_url_prefix), StaticController,
                {
                    "path": s["map_path"], "default_filename": s["default_filename"],
                    "use_spa": s["use_spa"]
                }
            ))
        return routes

    def config_static_file(self) -> IStartup:
        self.static_file_setting = launch["static_file"]
        return self

    def config_debug(self) -> IStartup:
        if self.env == "production":
            self.debug_setting = {
                "autoreload": False,
                "serve_traceback": True,
                "compiled_template_cache": False,
                "static_hash_cache": False
            }
        else:
            self.debug_setting = {
                "autoreload": False,
                "serve_traceback": False,
                "compiled_template_cache": True,
                "static_hash_cache": True
            }
        return self

    def config_route(self) -> IStartup:
        for v_host in launch["virtual_host"]:
            self.route.append((HostMatches(v_host), [
                *RegisterMeta.route_pool[v_host],
                *self.generate_static_route(self.static_file_setting[v_host])
            ]))
        return self

    def add_singleton(self, service: Union[Type[IDispose], Type[Awaitable]]) -> IStartup:
        key = service.__name__
        service_instance = service(self.launch)
        if isawaitable(service_instance):
            IOLoop.instance().add_future(
                convert_yielded(service_instance),
                lambda v: gen_log.info("%s asynchronous registration singleton completed", key)
            )
        self.singleton_services[key] = service_instance
        return self

    def add_scoped(self, service: Type[IDispose]) -> IStartup:
        key = service.__name__
        self.scoped_services[key] = service
        return self

    def build(self) -> Application:
        settings = {
            "template_path": "mvc/views",

            "ui_methods": method,
            "ui_modules": module.export,

            "launch": launch,

            **self.debug_setting
        }
        app = MVCApplication(handlers=self.route, **settings)
        app.singleton = self.singleton_services
        app.scoped = self.scoped_services
        return app


def build_host(stp: IStartup) -> HTTPServer:
    """

    构建主机服务对象

    :param stp: startup.Startup 启动配置对象，用于启动之前对应用进行构建生成
    :return: HTTPServer

    """
    # 解析加载options参数
    if launch["env"] == "production":
        options.log_file_prefix = os.path.join(conf["log_dir"], "madtornado.log")
    parse_command_line()

    # 构建HTTPServer对象，打印log信息
    server = HTTPServer(
        stp.config_debug().config_static_file().config_route().build()
    )
    host_tuple = socket.gethostbyname_ex(socket.gethostname())[2]

    for host in host_tuple:
        app_log.info("Remote access address: http://%s:%d", host, options.port)
    app_log.info("Allow access address: http://%s:%d", options.address, options.port)
    server.bind(options.port, options.address)

    return server
