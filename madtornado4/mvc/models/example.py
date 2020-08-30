from core.form import PropertyType, Rule
from mvc.models import IModel

from typing import NoReturn, List

"""

定义复杂类模型实例，Elves是一个复杂的模型，在http方法中可以通过
verify进行捕获。

传递模型到verify中，返回验证通过的实例对象，否则直接自动返回对应数据
elves_obj = verify(elves.Elves, json.loads(self.request.body.decode("utf-8")).get)

"""


class Props(IModel):

    def __init__(self):
        self.__name = None
        self.__power = None

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str) -> NoReturn:
        self.__name = value

    @property
    def power(self) -> int:
        return self.__power

    @power.setter
    def power(self, value: int) -> NoReturn:
        self.__power = value


class Halo(IModel):

    def __init__(self):
        self.__light = None
        self.__p = None

    @property
    def light(self) -> int:
        return self.__light

    @light.setter
    @Rule.scope(0, 5)
    def light(self, value: int) -> NoReturn:
        self.__light = value

    @property
    def p(self) -> Props:
        return self.__p

    @p.setter
    @PropertyType.model(Props)
    def p(self, value: Props) -> NoReturn:
        self.__p = value


class Elves(IModel):

    def __init__(self):
        self.__name = None
        self.__age = None
        self.__props = None
        self.__halo = None

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str) -> NoReturn:
        self.__name = value

    @property
    def age(self) -> int:
        return self.__age

    @age.setter
    def age(self, value: int) -> NoReturn:
        self.__age = value

    @property
    def props(self) -> List[Props]:
        return self.__props

    @props.setter
    @PropertyType.array(Props)
    def props(self, value: List[Props]) -> NoReturn:
        self.__props = value

    @property
    def halo(self) -> Halo:
        return self.__halo

    @halo.setter
    @PropertyType.model(Halo)
    def halo(self, value: Halo) -> NoReturn:
        self.__halo = value
