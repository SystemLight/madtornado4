import importlib
import os

# 加载controller路径下的模块，将其注册到路由表中
for module in os.listdir(os.path.join(os.path.dirname(__file__), "controllers")):
    if module.startswith("__"):
        continue
    (name, ext) = module.split(".")
    importlib.import_module("mvc.controllers.{}".format(name))
