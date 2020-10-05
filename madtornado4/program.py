#!/usr/bin/env python3
#
#   Copyright 2020 SystemLight
#   https://github.com/SystemLight/madtornado4
#
# # # # # # # # # # #
from tornado.ioloop import IOLoop

from startup import build_host, Startup, IStartup

try:
    from galaxy import injection
except ImportError:
    def injection(stp: IStartup) -> IStartup:
        return stp

import asyncio
import sys

if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
    # Fix python3.8: https://github.com/tornadoweb/tornado/issues/2608
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

if __name__ == "__main__":
    """

    基础使用::

        1. 通常情况下没有特殊需求你可以在mvc下新建自己的控制器-视图-模型等
        2. madtornado4将各种服务作为程序依赖注入到控制器当中，并自动管理生命周期-即自动销毁
        3. 注册service需要在galaxy下的__init__.py中调用stp的方法，支持单例和会话两种注册方式
        4. 获取服务通过Controller的self.obtain()方法，无需担心滥用该方法返回的实例会根据注册生命周期来创建
        5. self.obtain()方法获取的实例还会被挂载到self下面，也可以通过 ``self.服务名`` 来获取实例
        6. madtornado为使用者提供galaxy包空间，可以放置自行编写的内容，不建议放置到其它位置

    """
    print("[madtornado]-Web server is running...")
    build_host(injection(Startup())).start()
    IOLoop.instance().start()
