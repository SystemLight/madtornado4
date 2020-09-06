import os
import json
import platform
from typing import Dict, Any, NoReturn, Union


def require(path: str, encoding: str = "utf-8") -> Dict[str, Any]:
    """

    有时你可能只是需要从文件中读取到json数据，这是require函数将根据
    获取到的path，返回dict对象，相当方便，该函数同样类似于json.load

    :param path: json文件路径
    :param encoding: 编码方式
    :return: dict

    """
    fp = open(path, "r", encoding=encoding)
    data = fp.read()
    fp.close()
    try:
        return json.loads(data)
    except json.decoder.JSONDecodeError:
        return {}


def read(path: str, encoding: str = "utf-8") -> str:
    """

    读取文件返回字符串

    :param path: 文件路径
    :param encoding: 编码方式
    :return: 读取所有字符串

    """
    with open(path, "r", encoding=encoding) as fp:
        result = fp.read()
    return result


def write(path: str, data: str, encoding: str = "utf-8") -> NoReturn:
    """

    将字符串写入文件当中

    :param path: 文件路径
    :param data: 写入的字符串数据
    :param encoding: 编码方式
    :return:

    """
    with open(path, "w", encoding=encoding) as fp:
        fp.write(data)


def kill_form_port(port: Union[int, str]) -> NoReturn:
    """

    传入端口号，杀死进程

    :param port: 端口号，int类型
    :return: NoReturn

    """
    port = str(port)
    if platform.system() == 'Windows':
        command = """for /f "tokens=5" %i in ('netstat -ano ^| find \"""" + port + """\" ') do (taskkill /f /pid %i)"""
    else:
        command = """kill -9 $(netstat -nlp | grep :""" + port + """ | awk '{print $7}' | awk -F "/" '{print $1}')"""
    os.system(command)


class InvalidPath(Exception):
    pass


def check_join(root_path: str, *args) -> str:
    """

    检查合并后的路径是否在根路径当中，如果超出抛出异常

    :param root_path: 根路径
    :param args: 路径块集合
    :return: 合并后的绝对路径

    """
    result_path = os.path.abspath(os.path.join(root_path, *args))
    if root_path not in result_path:
        raise InvalidPath()
    return result_path


def safe_join(*args) -> str:
    """

    合并给定路径成为一个绝对路径，如果某个子路径块超出父路径会抛出异常

    :param args: 路径块集合
    :return: 合并后的绝对路径

    """
    safe_path = args[0]
    for i in range(1, len(args)):
        safe_path = check_join(safe_path, args[i])
    return safe_path
