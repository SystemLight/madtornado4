import importlib
import os

"""

    .. note::

        madtornado4使用动态导入controllers下所有模块，这意味着你无需手动注册，
        但是通过pytinstaller导入时，可能会提示缺少某些内置模块，这时你需要在该
        文件下手动写上import [module_name]，让pyinstaller可以识别并打包进入程序

"""

# 加载controller路径下的模块，将其注册到路由表中
for module in os.listdir(os.path.join(os.path.dirname(__file__), "controllers")):
    if module.startswith("__"):
        continue
    (name, ext) = module.split(".")
    importlib.import_module("mvc.controllers.{}".format(name))
