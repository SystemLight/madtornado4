import os
import random
import mimetypes
from abc import ABC, abstractmethod
from typing import NoReturn, Optional, List

__CHAR_POOL = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def generate_boundary(size: int = 15) -> str:
    """

    生成form-data报文字符串分割符号

    :return: Boundary分割符号

    """
    return "------SystemLightBoundary" + "".join(random.sample(__CHAR_POOL, size))


class Item(ABC):
    """

    form-data 子元素基类

    """

    def __init__(self):
        self.name = ""
        self.value = b''

    @abstractmethod
    def render(self) -> bytes:
        raise NotImplementedError()


class DataItem(Item):
    """

    form-data 文件格式子元素

    """

    def __init__(self):
        super().__init__()
        self.filename = ""
        self.mime = ""

    def render(self) -> bytes:
        disposition = 'Content-Disposition: form-data; name="{}"; filename="{}"'.format(self.name, self.filename)
        file_type = 'Content-Type: {}'.format(self.mime)
        file_header = "\r\n{}\r\n{}\r\n\r\n".format(disposition, file_type).encode("utf-8")
        return file_header + self.value + b"\r\n"


class FieldItem(Item):
    """

    form-data 字段格式子元素

    """

    def __init__(self):
        super().__init__()

    def render(self) -> bytes:
        disposition = 'Content-Disposition: form-data; name="{}";'.format(self.name)
        file_header = "\r\n{}\r\n\r\n".format(disposition).encode("utf-8")
        return file_header + self.value + b"\r\n"


class FormData:
    """

    form-data 请求体构造器

    """

    def __init__(self, boundary: str = generate_boundary()):
        self.boundary = boundary
        self.eof = "--{}--\r\n".format(self.boundary).encode("utf-8")
        self.items = []  # type: List[Item]

        self.__content_type = "multipart/form-data; boundary={}".format(boundary)

    def add_file(self, name: str, path: str, mime: str = None) -> NoReturn:
        """

        从文件中添加数据流

        :param name: 字段名称
        :param path: 文件路径
        :param mime: 文件Content-Type类型，可选
        :return: NoReturn

        """
        with open(path, "rb") as fp:
            data = fp.read()
        filename = os.path.basename(path)
        self.add_data(name, filename, data, mime)

    def add_data(self, name: str, filename: str, data: bytes, mime: Optional[str] = None) -> NoReturn:
        """

        添加数据流

        :param name: 字段名称
        :param filename: 文件名称
        :param data: 数据二进制对象
        :param mime: 文件Content-Type类型，可选
        :return: NoReturn

        """
        di = DataItem()
        di.name = name
        di.value = data
        di.mime = mime or mimetypes.guess_type(filename)[0]
        di.filename = filename
        self.items.append(di)

    def add_field(self, name: str, value: str) -> NoReturn:
        """

        添加字段

        :param name: 字段名称
        :param value: 字段值
        :return: NoReturn

        """
        di = FieldItem()
        di.name = name
        di.value = value.encode("utf-8")
        self.items.append(di)

    def get_body(self) -> bytes:
        """

        返回请求体，用于填充到body当中

        :return: body

        """
        body = b''
        boundary = b'--' + self.boundary.encode("utf-8")
        for item in self.items:
            body += boundary + item.render()
        return body + self.eof

    def get_content_type(self) -> str:
        """

        需要将请求头的Content-Type设置为该方法返回值

        :return: Content-Type

        """
        return self.__content_type

    def destroy(self) -> NoReturn:
        """

        销毁对象

        :return: NoReturn

        """
        del self.items
        del self.boundary
        del self.eof
        del self.__content_type
