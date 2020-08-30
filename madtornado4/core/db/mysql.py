import aiomysql

from core.interface import IDispose

from typing import Optional


class MysqlPoolService(IDispose):

    def __init__(self, launch):
        self.launch = launch
        self.pool = None  # type: Optional[aiomysql.pool.Pool]

    def __await__(self):
        if self.pool is None:
            self.pool = yield from aiomysql.create_pool(**self.launch["galaxy"]["db-1"])
        return self

    async def destroy(self):
        if self.pool:
            self.pool.close()
            await self.pool.wait_closed()
        self.pool = None
        self.launch = None


class MysqlService(IDispose):

    def __init__(self, launch):
        self.launch = launch
        self.pool_service = None  # type: Optional[MysqlPoolService]
        self.conn = None  # type: Optional[aiomysql.Connection]
        self.cur = None  # type: Optional[aiomysql.Cursor]
        self.is_rollback = False

    async def __call__(self, service: MysqlPoolService):
        self.pool_service = service
        self.conn = await self.pool_service.pool.acquire()
        self.cur = await self.conn.cursor(aiomysql.cursors.DictCursor)
        await self.conn.begin()
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
