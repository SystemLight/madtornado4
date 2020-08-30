import json

from typing import Dict, Any, NoReturn


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
