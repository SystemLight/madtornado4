import json
import time
import os
import zipfile
import shutil
from argparse import ArgumentParser
from urllib.request import urlopen, Request, urlretrieve
from http.client import HTTPResponse

releases_url = "https://api.github.com/repos/SystemLight/madtornado4/releases"
use_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 " \
            "Safari/537.36 "

model_template = """from core.form import PropertyType, Rule
from mvc.models import IModel

from typing import NoReturn, List


class NewModel(IModel):

    def __init__(self):
        self.__name = None

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str) -> NoReturn:
        self.__name = value

"""
controller_template = """from core.register import api_method
from mvc.controllers import ApiGhost


class NewController(ApiGhost):

    @api_method
    async def get(self):
        pass

    @api_method
    async def post(self):
        pass

"""


def download_progress(read_num, read_size, total_size):
    percent = float(read_num) * read_size * 100 / total_size
    percent = '\r当前进度:' + '%.2f%%' % (percent if percent < 100 else 100)
    print(percent)
    time.sleep(0.1)


def copy_zip(force: bool):
    for file_name in os.listdir("madtornado4"):
        source = "madtornado4/" + file_name
        target = "./" + file_name
        if os.path.isfile(source):
            shutil.copy(source, target)
        else:
            try:
                shutil.copytree(source, target)
            except FileExistsError as e:
                if force:
                    shutil.rmtree(target)
                    shutil.copytree(source, target)
                else:
                    raise e


def install_callback(**kwargs):
    tag_name = kwargs.get("version", None)
    force = kwargs.get("force")
    req = Request(url=releases_url, headers={"User-Agent": use_agent})
    with urlopen(req) as opener:  # type: HTTPResponse
        assets = json.loads(opener.read().decode("utf-8"))
    find_flag = False
    for i in assets:
        if tag_name in i["tag_name"]:
            download_url = i["assets"][0]["browser_download_url"]
            urlretrieve(download_url, "madtornado.zip", download_progress)
            find_flag = True
            break
    if not find_flag:
        return print("指定的版本号不存在，请使用 mad list 查看所有可用版本")
    zipfile.ZipFile("madtornado.zip").extractall("./")
    copy_zip(force)
    shutil.rmtree("madtornado4")
    os.remove("madtornado4.zip")


def list_callback(**kwargs):
    req = Request(url=releases_url, headers={"User-Agent": use_agent})
    with urlopen(req) as opener:  # type: HTTPResponse
        assets = json.loads(opener.read().decode("utf-8"))
    for i in assets:
        print("版本号：" + i["tag_name"])
        print("版本名称：" + i["assets"][0]["name"])
        print("下载地址：" + i["assets"][0]["browser_download_url"])
        print("内容简述：\r\n" + i["body"])
        print("=============================================\r\n\r\n\r\n")


def new_file(path, template):
    try:
        print(path)
        with open(path, "w") as fp:
            fp.write(template)
    except FileNotFoundError:
        print("请切换到madtornado项目根目录下执行 mad new 命令")
    else:
        print("成功创建模板文件...")


def new_file_wrap(path, template):
    if os.path.exists(path):
        return lambda: print(path + "\n文件已经存在...")
    return lambda: new_file(path, template)


def new_callback(**kwargs):
    template = kwargs.get("template")
    filename = kwargs.get("filename")[0]

    templates = {
        "controller": new_file_wrap(
            os.path.join("./mvc/controllers", filename + ".py"), controller_template
        ),
        "model": new_file_wrap(
            os.path.join("./mvc/models", filename + ".py"), model_template
        )
    }

    if template is None:
        print("""
Templates                                  Short Name                           Description

----------------------------------------------------------------------------------------------------------------
控制器模板文件                             controller                           新建一个控制器模板文件
模型模板文件                               model                                新建一个模型模板文件
""")
    else:
        if template in templates.keys():
            templates[template]()
        else:
            return print("指定的模板不存在")


def build_argparse() -> ArgumentParser:
    arg_parse = ArgumentParser(
        prog="mad",
        usage="mad",
        description="执行 mad 应用程序，构建项目",
        epilog="Please run the mad command in an empty folder path.",
        add_help=True
    )
    subparsers = arg_parse.add_subparsers(help="mad 命令集")

    install = subparsers.add_parser("install", help="安装指定版本的madtornado4到当前目录")
    install.set_defaults(callback=install_callback)
    install.add_argument("version", help="madtornado版本号")
    install.add_argument("-f", "--force", action="store_true", help="如果当前目录存在文件是否强制替换")

    list_version = subparsers.add_parser("list", help="列出所有可安装的madtornado版本")
    list_version.set_defaults(callback=list_callback)

    new = subparsers.add_parser("new", help="创建指定名称的模板代码")
    new.set_defaults(callback=new_callback)
    new.add_argument("template", nargs="?", default=None)
    new.add_argument("-fn, --filename", nargs=1, default=[str(int(time.time()))], dest="filename")

    return arg_parse


def main():
    arg_parse = build_argparse()
    kwargs = arg_parse.parse_args().__dict__
    if not kwargs:
        arg_parse.print_help()
    callback = kwargs.get("callback", None)
    if callback:
        callback(**kwargs)


if __name__ == '__main__':
    main()
