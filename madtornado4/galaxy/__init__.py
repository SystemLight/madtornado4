from core.interface import IStartup

"""
galaxy用于存放使用者的编码内容，为了不污染项目结构而特意开辟出的空间，
使用者编写的业务类代码可以放入到galaxy中使madtornado版本升级不会影响
到整个项目, 同时可以在launch.json中添加galaxy字段注入用户全局变量，
在Controller中通过self.setting["launch"]["galaxy"]获取详细值。

银河长存于世，万物取其中
"""


def injection(stp: IStartup) -> IStartup:
    """

    注入依赖服务，如数据库连接服务等等，这是很必要的内容，尽量不要自己管理这些类的实例与销毁，
    将这些工作交托出去，因此你需要注册不同生命周期的service。
    add_singleton 单例注册，全局共享一个实例对象，
    add_scoped 会话注册，会话开始创建，结束销毁

    :param stp: 启动器对象实例
    :return: 传入的启动器对象实例

    """
    return stp
