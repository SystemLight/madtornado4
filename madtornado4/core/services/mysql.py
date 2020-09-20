import aiomysql

from core.interface import IDispose

from typing import Optional, NoReturn


class MysqlPoolService(IDispose):
    """

    MysqlPoolService是一个单例服务，虽然也可以作为scoped注册，
    但是性能会大幅缩减，该服务为MysqlService提供数据库连接池

    """

    def __init__(self, launch):
        super().__init__(launch)
        self.conf_key = "db"
        self.pool = None  # type: Optional[aiomysql.pool.Pool]

    def __await__(self):
        if self.pool is None:
            self.pool = yield from aiomysql.create_pool(**self.launch["galaxy"][self.conf_key])
        return self

    async def destroy(self):
        if self.pool:
            self.pool.close()
            await self.pool.wait_closed()
        self.pool = None
        self.launch = None


class MysqlConnService(IDispose):
    """

    MysqlConn不依赖任何其它服务，但是每次创建都会开启一个全新的连接，
    你可以全局保持一个连接也可以每次会话都新创建一个连接，取决于哪种注册方式

    """

    def __init__(self, launch):
        super().__init__(launch)
        self.conf_key = "db"
        self.conn = None  # type: Optional[aiomysql.Connection]
        self.cur = None  # type: Optional[aiomysql.Cursor]
        self.is_rollback = False

    async def __call__(self, *args, **kwargs):
        self.conn = await aiomysql.connect(**self.launch["galaxy"]["db"])  # type: Optional[aiomysql.Connection]
        self.cur = await self.conn.cursor()  # type: Optional[aiomysql.Cursor]
        return self

    async def queryone(self, query: str, args=None):
        await self.cur.execute(query, args)
        return await self.cur.fetchone()

    async def queryall(self, query: str, args=None):
        await self.cur.execute(query, args)
        return await self.cur.fetchall()

    async def querymany(self, query: str, size: int, args=None):
        await self.cur.execute(query, args)
        return await self.cur.fetchmany(size)

    async def execute(self, query: str, args=None):
        return await self.cur.execute(query, args)

    async def destroy(self) -> NoReturn:
        if self.is_rollback:
            await self.conn.rollback()
        else:
            await self.conn.commit()
        if self.cur:
            await self.cur.close()
        if self.conn:
            self.conn.close()
        self.launch = None


class MysqlService(MysqlConnService):
    """

    MysqlService是一个会话服务，你可以注册到scoped当中，
    且该服务依赖单例服务MysqlPoolService

    galaxy.py注册服务::

        stp.add_scoped(mysql.MysqlService).add_singleton(mysql.MysqlPoolService)

    控制器中获取服务::

        service = await self.obtain("MysqlService")(self.obtain("MysqlPoolService"))
        当服务被获取以后，之后再次调用obtain将返回相同对象，该对象被挂载到self当中

        如：self.MysqlService   self.MysqlPoolService 这些实例是非重复的
        通过catapult获取的服务会自动销毁和创建，如果服务未注册会返回空对象

    """

    def __init__(self, launch):
        super().__init__(launch)
        self.pool_service = None  # type: Optional[MysqlPoolService]

    async def __call__(self, service: MysqlPoolService):
        self.pool_service = service
        self.conn = await self.pool_service.pool.acquire()
        self.cur = await self.conn.cursor(aiomysql.cursors.DictCursor)
        await self.conn.begin()
        return self

    async def destroy(self):
        if self.is_rollback:
            await self.conn.rollback()
        else:
            await self.conn.commit()
        if self.cur:
            await self.cur.close()
        if self.conn and self.pool_service:
            self.pool_service.pool.release(self.conn)
        self.launch = None
        self.pool_service = None
