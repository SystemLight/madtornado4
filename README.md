# Madtornado4

Madtornado4是一个构建MVC Tornado项目的工具。

[![Documentation Status](https://readthedocs.org/projects/madtornado4/badge/?version=latest)](https://madtornado4.readthedocs.io/?badge=latest)
[![Build Status](https://www.travis-ci.org/SystemLight/madtornado4.svg?branch=master)](https://www.travis-ci.org/SystemLight/madtornado4)

## 安装

```
pip install madtornado4
mad install <version>
```

## 用法

madtornado4通过`mad`命令提供构建操作，在控制台中键入mad即可获得帮助

- mad install [version]: 指定madtornado的版本号在当前目录下初始化项目。
- mad list: 查看所有可用的madtornado版本。
- mad new [Template]: 在madtornado4项目下新建制定模板文件，如果不输入模板名称列出所有模板。

## 数据库连接

1. 环境中需要安装aiomysql
2. 配置launch.json
3. 打开galaxy中的__init__.py，注册mysql服务`stp.add_scoped(mysql.MysqlService).add_singleton(mysql.MysqlPoolService)`
4. 基本使用举例

```python
class DatabaseInsertDemo(ApiGhost):
    __urls = api_router(["/database/insert"])

    @api_method
    async def get(self):
        """

        插入一条数据到表格
        访问地址：/api/database/insert

        """
        service: mysql.MysqlService = await self.obtain("MysqlService")(self.obtain("MysqlPoolService"))
        await service.execute("insert into user (name, age) values ('Lisys',20)")
        return "插入一条数据"


class DatabaseSelectDemo(ApiGhost):
    __urls = api_router(["/database/select"])

    @api_method
    async def get(self):
        """

        插入一条数据到表格
        访问地址：/api/database/select

        """
        service: mysql.MysqlService = await self.obtain("MysqlService")(self.obtain("MysqlPoolService"))
        data = await service.queryall("select * from user")
        return data
```

## 异步解决方案

| 领域 | 模块 |
| --- | --- |
| web | [tornado](https://github.com/tornadoweb/tornado) |
| mysql | [aiomysql](https://github.com/aio-libs/aiomysql) |
| sqlite3 | [aiosqlite](https://github.com/omnilib/aiosqlite) |
| ORM | [peewee-async](https://github.com/05bit/peewee-async) |
| GraphQL | [graphene-tornado](https://github.com/graphql-python/graphene-tornado) |
| file | [aiofiles](https://github.com/Tinche/aiofiles) |
| cpu | [celery](https://github.com/celery/celery) |

## 文档

- 你可以阅读 [madtornado4 Documentation](https://madtornado4.readthedocs.io/?badge=latest) 在线文档获取更多使用方法。
- 你也可以阅读 [tornado Documentation](https://www.osgeo.cn/tornado/index.html) 来了解tornado基础使用
- 自制正则路由辅助工具[regulex](https://jex.im/regulex)

## License

Madtornado4 uses the MIT license, see LICENSE file for the details.
