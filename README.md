# Madtornado4

Madtornado4是一个构建MVC Tornado项目的工具。

[![Documentation Status](https://readthedocs.org/projects/madtornado4/badge/?version=latest)](https://madtornado4.readthedocs.io/?badge=latest)
[![Build Status](https://www.travis-ci.org/SystemLight/madtornado4.svg?branch=master)](https://www.travis-ci.org/SystemLight/madtornado4)

## 安装

```
pip install madtornado4
```

## 异步解决方案

| 领域 | 模块 |
| --- | --- |
| web | tornado |
| mysql | aiomysql |
| sqlite3 | aiosqlite |
| ORM | peewee-async |
| GraphQL | graphene-tornado |
| file | aiofiles |
| cpu | celery |


## 用法

madtornado4通过`mad`命令提供构建操作，在控制台中键入mad即可获得帮助

- mad install [version]: 指定madtornado的版本号在当前目录下初始化项目。
- mad list: 查看所有可用的madtornado版本。
- mad new [Template]: 在madtornado4项目下新建制定模板文件，如果不输入模板名称列出所有模板。

## 文档

- 你可以阅读 [madtornado4 Documentation](https://madtornado4.readthedocs.io/?badge=latest) 在线文档获取更多使用方法。
- 你也可以阅读 [tornado Documentation](https://www.osgeo.cn/tornado/index.html) 来了解tornado基础使用

## License

Madtornado4 uses the MIT license, see LICENSE file for the details.
