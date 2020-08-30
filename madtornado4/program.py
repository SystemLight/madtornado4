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

if __name__ == "__main__":
    print("[madtornado]-Web server is running...")
    build_host(injection(Startup())).start()
    IOLoop.instance().start()
